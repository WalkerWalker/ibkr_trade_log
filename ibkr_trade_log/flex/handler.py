from dataclasses import dataclass
from datetime import timedelta, datetime
import random
from enum import Enum
from pathlib import Path
from typing import List, Optional

from ib_insync import FlexReport

from bootstrap.ddd import ValueObject
from bootstrap.messagebus.bus import MessageBus
from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Command, Query
from bootstrap.rdb.repository import RdbRepository
from bootstrap.scheduler.scheduler import Scheduler
from ibkr_trade_log.flex.order import Order


@dataclass(frozen=True)
class QueryAndStoreReport(Command):
    pass


@dataclass(frozen=True)
class LoadAndStoreReport(Command):
    filename: str


class Topics(str, Enum):
    Order = "Order"
    CashTransaction = "CashTransaction"
    Transfer = "Transfer"


@dataclass(frozen=True)
class FlexConfig(ValueObject):
    report_base: str
    token: str
    query_id: str
    query_interval_in_days: int = 1


@dataclass(frozen=True)
class OrdersInTimeRange(Query[List[Order]]):
    before: Optional[datetime] = None
    after: Optional[datetime] = None


class FlexHandler(Handler):
    def __init__(
        self,
        messagebus: MessageBus,
        scheduler: Scheduler,
        config: FlexConfig,
        order_repository: RdbRepository,
        cash_transaction_repository: RdbRepository,
        transfer_repository: RdbRepository,
    ):
        super().__init__(messagebus)
        self.scheduler = scheduler
        self.config = config
        self.order_repository = order_repository
        self.cash_transaction_repository = cash_transaction_repository
        self.transfer_repository = transfer_repository
        self._subscription = None

    def startup(self):
        self.messagebus.declare(OrdersInTimeRange, self.handler_orders_in_time_range)
        self.messagebus.declare(LoadAndStoreReport, self.handle_load_and_store_report)
        self.messagebus.declare(QueryAndStoreReport, self.handle_query_and_store_report)
        self._subscription = self.scheduler.schedule(
            duetime=timedelta(seconds=random.randint(0, 60)),
            period=timedelta(days=self.config.query_interval_in_days),
            callback=self.query_and_store_report,
        )

    def query_and_store_report(self):
        self.logger.info("Scheduler triggers query and store report")
        self.messagebus.tell(QueryAndStoreReport())

    def handle_load_and_store_report(self, command: LoadAndStoreReport):
        report = self.load_report(
            report_path=Path(self.config.report_base) / "reports" / command.filename
        )
        self.store_report(report)

    def handle_query_and_store_report(self, command: QueryAndStoreReport):
        report = FlexReport(
            token=self.config.token,
            queryId=self.config.query_id,
        )
        self.save_report_xml(report)
        self.store_report(report)

    def load_report(self, report_path: Path):
        return FlexReport(
            path=report_path,
        )

    def query_report(self, token: str, query_id: str):
        return FlexReport(
            token=token,
            queryId=query_id,
        )

    # we now assume the report is always configured to be YearToDate and therefore name it with year only, not date.
    def save_report_xml(self, report: FlexReport):
        report_info = report.extract("FlexStatement", parseNumbers=False)[0]
        account_id = report_info.accountId
        from_data = report_info.fromDate
        from_data_year = from_data[:4]
        filename = f"{account_id}_{from_data_year}.xml"
        report_path = Path(self.config.report_base) / "reports" / filename
        self.logger.info(f"Save or overwrite report {filename}")
        report.save(report_path)

    def store_report(self, report: FlexReport):
        report_info = report.extract("FlexStatement")[0]
        self.logger.info(
            f"Start storing report {report_info.fromDate} to {report_info.toDate}"
        )
        self.store_order_in_report(report)
        self.store_transfer_in_report(report)
        self.store_cash_transaction_in_report(report)

    def store_order_in_report(
        self,
        report: FlexReport,
    ):
        orders = report.extract(
            topic=Topics.Order,
            parseNumbers=False,
        )
        self.order_repository.add_domain_list(orders)

    def store_cash_transaction_in_report(
        self,
        report: FlexReport,
    ):
        cash_transactions = report.extract(
            topic=Topics.CashTransaction,
            parseNumbers=False,
        )
        self.cash_transaction_repository.add_domain_list(cash_transactions)

    def store_transfer_in_report(
        self,
        report: FlexReport,
    ):
        transfers = report.extract(
            topic=Topics.Transfer,
            parseNumbers=False,
        )
        self.transfer_repository.add_domain_list(transfers)

    def handler_orders_in_time_range(self, query: OrdersInTimeRange):
        return self.order_repository.filter_by_time(
            before=query.before,
            after=query.after,
        )
