from messagebus.bus import MessageBus
from rdb.session import RdbSessionFactory

from order.handler import OrderHandler
from order.repository import OrderRepository


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
