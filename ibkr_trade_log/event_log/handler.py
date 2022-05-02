from dataclasses import dataclass

from bootstrap.messagebus.bus import MessageBus
from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Event
from ibkr_trade_log.event_log.repository import EventRepository


@dataclass(frozen=True)
class OrdersExecuted(Event):
    orders: list


@dataclass(frozen=True)
class TransfersExecuted(Event):
    transfers: list


@dataclass(frozen=True)
class CashTransactionsExecuted(Event):
    cash_transactions: list


class EventHandler(Handler):
    def __init__(
        self,
        messagebus: MessageBus,
        event_repository: EventRepository,
    ):
        super().__init__(messagebus)
        self.event_repository = event_repository

    def startup(self):
        self.messagebus.subscribe(OrdersExecuted, self.handle_orders_executed)
        self.messagebus.subscribe(TransfersExecuted, self.handle_transfers_executed)
        self.messagebus.subscribe(
            CashTransactionsExecuted, self.handle_cash_transactions_executed
        )

    def handle_orders_executed(self, event: OrdersExecuted):
        self.logger.info("handler orders executed")

    def handle_transfers_executed(self, event: TransfersExecuted):
        self.logger.info("handler transfers executed")

    def handle_cash_transactions_executed(self, event: CashTransactionsExecuted):
        self.logger.info("handler cash transactions executed")
