from dataclasses import dataclass
from ib_insync import FlexReport
import yaml

from ddd import ValueObject
from messagebus.handler import Handler
from messagebus.model import Command
from order.handler import StoreOrders
from order.repository import OrderDataFrame


@dataclass(frozen=True)
class StoreReport(Command):
    report: FlexReport
    topic: str


@dataclass(frozen=True)
class FlexConfig(ValueObject):
    token: str
    query_id: str


class FlexHandler(Handler):
    def __init__(self, messagebus):
        super().__init__(messagebus)

    def startup(self):
        self.messagebus.declare(StoreReport, self.handle_store_report)

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
