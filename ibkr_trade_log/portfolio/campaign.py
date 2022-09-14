from typing import List, Dict

from bootstrap.ddd import Entity
from ibkr_trade_log.flex.order import Order
from ibkr_trade_log.flex.transfer import Transfer


class Campaign(Entity):
    symbols: str
    orders: List[Order] = []
    positions: Dict[int, int] = {}

    def add_order(self, order: Order):
        self.orders.append(order)
        if order.conid not in self.positions:
            self.positions[order.conid] = 0
        self.positions[order.conid] += order.quantity

    def add_transfer(self, transfer: Transfer):
        if transfer.conid not in self.positions:
            self.positions[transfer.conid] = 0
        self.positions[transfer.conid] += transfer.quantity

    @property
    def is_closed(self) -> bool:
        return not self.has_open_positions and self.realized_pnl > 0

    @property
    def realized_pnl(self):
        return sum([order.fifoPnlRealized for order in self.orders])

    @property
    def has_open_positions(self):
        return self.positions.values() != [0]
