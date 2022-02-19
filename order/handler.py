from dataclasses import dataclass
from typing import List

from messagebus.handler import Handler
from messagebus.model import Command
from order.repository import _Order, OrderDataFrame


@dataclass(frozen=True)
class StoreOrders(Command):
    order_data_frame: OrderDataFrame


class OrderHandler(Handler):
    def __init__(self, messagebus, order_repository):
        super().__init__(messagebus)
        self.order_repository = order_repository

    def startup(self):
        self.messagebus.declare(StoreOrders, self.handle_store_orders)

    def handle_store_orders(self, command: StoreOrders):
        self.order_repository.add(
            orders=command.order_data_frame,
        )
