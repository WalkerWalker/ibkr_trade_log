from dataclasses import dataclass
from datetime import timedelta
import random
from typing import Optional

from ib_insync import FlexReport
from rx.disposable import Disposable

from ddd import ValueObject
from messagebus.handler import Handler
from messagebus.model import Command
from order.handler import StoreOrders
from order.repository import OrderDataFrame
from scheduler.scheduler import Scheduler


@dataclass(frozen=True)
class StoreReport(Command):
    report: FlexReport
    topic: str


@dataclass(frozen=True)
class QueryAndStoreReport(Command):
    topic: str


@dataclass(frozen=True)
class FlexConfig(ValueObject):
    token: str
    query_id: str
    query_interval_in_days: int = 1


class FlexHandler(Handler):
    def __init__(self, messagebus, scheduler, config: FlexConfig):
        super().__init__(messagebus)
        self.scheduler: Scheduler = scheduler
        self.config = config
        self._subscription: Optional[Disposable] = None

    def startup(self):
        self.messagebus.declare(StoreReport, self.handle_store_report)
        self.messagebus.declare(QueryAndStoreReport, self.handle_query_and_store_report)

        self._subscription = self.scheduler.schedule(
            duetime=timedelta(seconds=random.randint(0, 60)),
            period=timedelta(days=self.config.query_interval_in_days),
            callback=self.query_and_store_report,
        )

    def query_and_store_report(self):
        self.messagebus.tell(
            QueryAndStoreReport(topic="Order")  # TODO put topic(s) in config
        )

    def handle_query_and_store_report(self, command: QueryAndStoreReport):
        report = FlexReport(
            token=self.config.token,
            queryId=self.config.query_id,
        )
        data_frame = report.df(
            topic=command.topic,
            parseNumbers=False,
        )
        self.messagebus.tell(
            StoreOrders(
                order_data_frame=OrderDataFrame(
                    data_frame=data_frame,
                )
            )
        )

    def handle_store_report(self, command: StoreReport):
        data_frame = command.report.df(
            topic=command.topic,
            parseNumbers=False,
        )
        self.messagebus.tell(
            StoreOrders(
                order_data_frame=OrderDataFrame(
                    data_frame=data_frame,
                )
            )
        )
