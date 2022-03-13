from ibkr_trade_log.flex.handler import FlexConfig, FlexHandler, QueryAndStoreReport


from ibkr_trade_log.flex.order.handler import OrderHandler
from ibkr_trade_log.flex.order.repository import OrderRepository, OrderDataFrame, Order


class FlexPlugin:
    def __init__(
        self,
        config: FlexConfig,
        app,
    ):
        self.config = config

        self.scheduler = app.scheduler
        self.messagebus = app.messagebus
        self.rdb_session_factory = app.rdb_session_factory

        self.flex_handler = FlexHandler(
            messagebus=self.messagebus, config=self.config, scheduler=self.scheduler
        )

        self.order_repository = OrderRepository(
            rdb_session=self.rdb_session_factory.build(),
        )

        self.order_handler = OrderHandler(
            messagebus=self.messagebus,
            order_repository=self.order_repository,
        )

    def startup(self):
        self.flex_handler.startup()
        self.order_handler.startup()
