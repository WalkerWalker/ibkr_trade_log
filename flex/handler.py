from dataclasses import dataclass
from ib_insync import FlexReport
import yaml

from ddd import ValueObject
from messagebus.handler import Handler
from messagebus.model import Command


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
        data_frame = command.report.df(topic=command.topic)
        print(data_frame)


def flex():
    with open("../config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    flex_config = FlexConfig(**config["flex"])
    topic = "Trade"
    report = FlexReport(
        token=flex_config.token,
        queryId=flex_config.query_id,
    )
    order_list = report.df(topic="Order")
    order_list.set_index(
        keys=["tradeDate"],
        inplace=True,
    )
    order_list.sort_index(
        axis="index",
        inplace=True,
    )
    return order_list.to_dict()
