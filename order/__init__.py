from messagebus.bus import MessageBus
from rdb.session import RdbSessionFactory

from order.handler import OrderHandler
from order.repository import OrderRepository


def startup(rdb_session_factory: RdbSessionFactory, messagebus: MessageBus):
    order_repository = OrderRepository(
        rdb_session=rdb_session_factory.build(),
    )

    order_handler = OrderHandler(
        messagebus=messagebus,
        order_repository=order_repository,
    )
    order_handler.startup()
