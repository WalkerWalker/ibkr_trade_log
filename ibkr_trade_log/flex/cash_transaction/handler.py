from dataclasses import dataclass

from ibkr_trade_log.bootstrap.messagebus.handler import Handler
from ibkr_trade_log.flex.cash_transaction.repository import CashTransactionDataFrame
from ibkr_trade_log.bootstrap.messagebus.model import Command


@dataclass(frozen=True)
class StoreCashTransactions(Command):
    cash_transaction_data_frame: CashTransactionDataFrame


class CashTransactionHandler(Handler):
    def __init__(self, messagebus, cash_transaction_repository):
        super().__init__(messagebus)
        self.cash_transaction_repository = cash_transaction_repository

    def startup(self):
        self.messagebus.declare(StoreCashTransactions, self.handle_cash_transactions)

    def handle_cash_transactions(self, command: StoreCashTransactions):
        self.cash_transaction_repository.add(
            record_set=command.cash_transaction_data_frame,
        )
