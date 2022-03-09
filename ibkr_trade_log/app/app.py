from ibkr_trade_log.api.plugin import ApiPlugin
from ibkr_trade_log.flex.handler import FlexConfig, FlexHandler

from ibkr_trade_log.cli.cli import CliPlugin
from ibkr_trade_log.messagebus.memory import MemoryMessageBus
from ibkr_trade_log.order import OrderPlugin
from ibkr_trade_log.rdb.config import RdbConfig
from ibkr_trade_log.rdb.session import RdbSessionFactory
from ibkr_trade_log.scheduler.scheduler import Scheduler


class IbkrApp:
    def __init__(self, config: dict):
        self.messagebus = MemoryMessageBus()
        self.scheduler = Scheduler()

        rdb_config = RdbConfig(**config["rdb"])
        self.rdb_session_factory = RdbSessionFactory(config=rdb_config)

        flex_config = FlexConfig(**config["flex"])
        self.flex_handler = FlexHandler(
            messagebus=self.messagebus,
            scheduler=self.scheduler,
            config=flex_config,
        )

        self.order_plugin = OrderPlugin(
            rdb_session_factory=self.rdb_session_factory,
            messagebus=self.messagebus,
        )

        self.api_plugin = ApiPlugin(app=self)
        self.cli_plugin = CliPlugin(app=self)

    async def startup(self):
        self.scheduler.startup()
        self.rdb_session_factory.startup()
        self.flex_handler.startup()
        self.order_plugin.startup()
