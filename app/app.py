from api.plugin import ApiPlugin
from flex.handler import FlexConfig, FlexHandler
from messagebus.memory import MemoryMessageBus
from order import OrderPlugin
from rdb.config import RdbConfig
from rdb.session import RdbSessionFactory
from scheduler.scheduler import Scheduler


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

    async def startup(self):
        self.scheduler.startup()
        self.rdb_session_factory.startup()
        self.flex_handler.startup()
        self.order_plugin.startup()
