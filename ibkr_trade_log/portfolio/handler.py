from dataclasses import dataclass

from bootstrap.messagebus.bus import MessageBus
from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Command
from ibkr.flex.cash_transaction import (
    CashTransaction,
    CashTransactionRepository,
)
from ibkr.flex.order import Order, OrderRepository
from ibkr.flex.transfer import Transfer, TransferRepository


@dataclass(frozen=True)
class ProcessTransfer(Command):
    transfer: Transfer


@dataclass(frozen=True)
class ProcessCashTransaction(Command):
    cash_transaction: CashTransaction


@dataclass(frozen=True)
class ProcessOrderFilled(Command):
    order: Order


@dataclass(frozen=True)
class CalculatePortfolioNow(Command):
    pass


class PortfolioHandler(Handler):
    def __init__(
        self,
        messagebus: MessageBus,
        cash_transaction_repository: CashTransactionRepository,
        order_repository: OrderRepository,
        transfer_repository: TransferRepository,
    ):
        super().__init__(messagebus)
        self.cash_transaction_repository = cash_transaction_repository
        self.order_repository = order_repository
        self.transfer_repository = transfer_repository

    def startup(self):
        self.messagebus.declare(ProcessTransfer, self.handle_transfer)
        self.messagebus.declare(ProcessCashTransaction, self.handle_cash_transaction)
        self.messagebus.declare(ProcessOrderFilled, self.handle_order_filled)

    def handle_transfer(self, command: ProcessTransfer):
        self.logger.info(f"processing transfer {command.transfer}")

    def handle_cash_transaction(self, command: ProcessCashTransaction):
        self.logger.info(f"processing cash transaction {command.cash_transaction}")

    def handle_order_filled(self, command: ProcessOrderFilled):
        self.logger.info(f"processing filled order {command.order}")
