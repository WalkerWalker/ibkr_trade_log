from ibkr_trade_log.messagebus.bus import MessageBus
from ibkr_trade_log.rdb.session import RdbSessionFactory

from ibkr_trade_log.order.handler import OrderHandler
from ibkr_trade_log.order.repository import OrderRepository


class OrderPlugin:
    def __init__(
        self,
        rdb_session_factory: RdbSessionFactory,
        messagebus: MessageBus,
    ):
        self.order_repository = OrderRepository(
            rdb_session=rdb_session_factory.build(),
        )

        self.order_handler = OrderHandler(
            messagebus=messagebus,
            order_repository=self.order_repository,
        )

    def startup(self):
        self.order_handler.startup()
