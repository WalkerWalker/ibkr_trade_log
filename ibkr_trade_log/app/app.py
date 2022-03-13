from ibkr_trade_log.api.plugin import ApiPlugin
from ibkr_trade_log.flex import FlexPlugin
from ibkr_trade_log.flex.handler import FlexConfig

from ibkr_trade_log.cli.cli import CliPlugin
from ibkr_trade_log.messagebus.memory import MemoryMessageBus
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
        self.flex_plugin = FlexPlugin(config=flex_config, app=self)

        self.api_plugin = ApiPlugin(app=self)
        self.cli_plugin = CliPlugin(app=self)

    async def startup(self):
        self.scheduler.startup()
        self.rdb_session_factory.startup()
        self.flex_plugin.startup()
