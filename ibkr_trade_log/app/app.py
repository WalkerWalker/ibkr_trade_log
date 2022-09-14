from bootstrap.logger import LoggerMixin, configure_logger
from bootstrap.rdb.config import RdbConfig
from bootstrap.scheduler.scheduler import Scheduler
from ibkr_trade_log.api.plugin import ApiPlugin
from ibkr_trade_log.flex import FlexPlugin
from ibkr_trade_log.flex.handler import FlexConfig

from ibkr_trade_log.cli.cli import CliPlugin
from bootstrap.messagebus.memory import MemoryMessageBus
from bootstrap.rdb.session import RdbSessionFactory
from ibkr_trade_log.portfolio import PortfolioPlugin


class IbkrApp(LoggerMixin):
    def __init__(self, config: dict):
        configure_logger()
        self.logger.info("Ibkr App init")

        self.messagebus = MemoryMessageBus()
        self.scheduler = Scheduler()

        rdb_config = RdbConfig(**config["rdb"])
        self.rdb_session_factory = RdbSessionFactory(config=rdb_config)

        flex_config = FlexConfig(**config["flex"])
        self.flex_plugin = FlexPlugin(config=flex_config, app=self)
        self.api_plugin = ApiPlugin(app=self)
        self.cli_plugin = CliPlugin(app=self)
        self.portfolio_plugin = PortfolioPlugin(app=self)

    async def startup(self):
        self.logger.info("Ibkr App startup")
        self.scheduler.startup()
        self.rdb_session_factory.startup()
        self.flex_plugin.startup()
        self.portfolio_plugin.startup()
