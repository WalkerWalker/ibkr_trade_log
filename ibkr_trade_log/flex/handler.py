from dataclasses import dataclass
from datetime import timedelta
import random
from enum import Enum
from pathlib import Path

from ib_insync import FlexReport

from bootstrap.ddd import ValueObject
from bootstrap.messagebus.bus import MessageBus
from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Command
from bootstrap.rdb.repository import RdbRepository
from bootstrap.scheduler.scheduler import Scheduler
from ibkr_trade_log.event_log.handler import (
    OrdersExecuted,
    TransfersExecuted,
    CashTransactionsExecuted,
)


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
        self.messagebus.publish(
            OrdersExecuted(
                orders=orders,
            )
        )

    def store_cash_transaction_in_report(
        self,
        report: FlexReport,
    ):
        cash_transactions = report.extract(
            topic=Topics.CashTransaction,
            parseNumbers=False,
        )
        self.cash_transaction_repository.add_domain_list(cash_transactions)
        self.messagebus.publish(
            CashTransactionsExecuted(cash_transactions=cash_transactions)
        )

    def store_transfer_in_report(
        self,
        report: FlexReport,
    ):
        transfers = report.extract(
            topic=Topics.Transfer,
            parseNumbers=False,
        )
        self.transfer_repository.add_domain_list(transfers)
        self.messagebus.publish(TransfersExecuted(transfers=transfers))
