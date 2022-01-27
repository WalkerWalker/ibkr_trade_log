from dataclasses import dataclass
from ib_insync import FlexReport
import yaml


@dataclass
class FlexConfig:
    token: str
    query_id: str


def flex():
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    flex_config = FlexConfig(**config["flex"])
    topic = "Order"
    report = FlexReport(
        token=flex_config.token,
        queryId=flex_config.query_id,
    )
    order_list = report.df(topic=topic)
    order_list.set_index(
        keys=["tradeDate"],
        inplace=True,
    )
    order_list.sort_index(
        axis="index",
        inplace=True,
    )
    return order_list.to_dict()
