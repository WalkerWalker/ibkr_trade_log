from dataclasses import dataclass
from datetime import timedelta
import random
from pathlib import Path
from typing import Optional, List

import pandas as pd
from ib_insync import FlexReport
from rx.disposable import Disposable

from ibkr_trade_log.ddd import ValueObject
from ibkr_trade_log.flex.order.repository import OrderDataFrame
from ibkr_trade_log.messagebus.handler import Handler
from ibkr_trade_log.messagebus.model import Command
from ibkr_trade_log.flex.order.handler import StoreOrders
from ibkr_trade_log.scheduler.scheduler import Scheduler


@dataclass(frozen=True)
class QueryAndStoreReport(Command):
    pass


@dataclass(frozen=True)
class LoadAndStoreReport(Command):
    filename: str


@dataclass(frozen=True)
class FlexConfig(ValueObject):
    report_base: str
    token: str
    query_id: str
    topics: List[str]
    query_interval_in_days: int = 1


class FlexHandler(Handler):
    def __init__(self, messagebus, scheduler: Scheduler, config: FlexConfig):
        super().__init__(messagebus)
        self.scheduler = scheduler
        self.config = config
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
        data_frame_in_topics = []
        for topic in self.config.topics:
            data_frame = report.df(
                topic=topic,
                parseNumbers=False,
            )
            data_frame_in_topics.append(data_frame)
        data_frame = pd.concat(data_frame_in_topics)
        self.messagebus.tell(
            StoreOrders(
                order_data_frame=OrderDataFrame(
                    data_frame=data_frame,
                )
            )
        )
