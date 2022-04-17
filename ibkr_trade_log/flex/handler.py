from dataclasses import dataclass
from datetime import timedelta
import random
from enum import Enum
from pathlib import Path
from typing import Dict, List

from ib_insync import FlexReport

from bootstrap.ddd import ValueObject
from bootstrap.messagebus.bus import MessageBus
from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Command
from bootstrap.rdb.repository import RdbRepository
from bootstrap.scheduler.scheduler import Scheduler


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
    topics: List[Topics]
    query_interval_in_days: int = 1


class FlexHandler(Handler):
    def __init__(
        self,
        messagebus: MessageBus,
        scheduler: Scheduler,
        config: FlexConfig,
        repositories: Dict[Topics, RdbRepository],
    ):
        super().__init__(messagebus)
        self.scheduler = scheduler
        self.config = config
        self.repositories = repositories
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
        for topic in self.config.topics:
            self.store_topic_in_report(
                report=report,
                topic=topic,
            )

    def store_topic_in_report(
        self,
        report: FlexReport,
        topic: Topics,
    ):
        data_frame = report.df(
            topic=topic,
            parseNumbers=False,
        )
        if data_frame is not None:
            self.repositories[topic].add(data_frame)
