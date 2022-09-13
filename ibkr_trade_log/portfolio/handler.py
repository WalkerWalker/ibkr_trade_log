from dataclasses import dataclass

from bootstrap.messagebus.bus import MessageBus
from bootstrap.messagebus.handler import Handler
from bootstrap.messagebus.model import Command
from ibkr_trade_log.flex import TransferRepository
from ibkr_trade_log.flex.cash_transaction import (
    CashTransaction,
    CashTransactionRepository,
)
from ibkr_trade_log.flex.order import Order, OrderRepository
from ibkr_trade_log.flex.transfer import Transfer
from ibkr_trade_log.portfolio.campaign import Campaign
from ibkr_trade_log.portfolio.portfolio import Portfolio


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
        portfolio: Portfolio,
    ):
        super().__init__(messagebus)
        self.cash_transaction_repository = cash_transaction_repository
        self.order_repository = order_repository
        self.transfer_repository = transfer_repository
        self.portfolio = portfolio

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
        self.add_order_to_portfolio(command.order)

    def add_order_to_portfolio(self, order: Order):
        symbol = order.symbol
        campaigns = self.portfolio.campaigns[symbol]
        if len(campaigns) == 0:
            self.portfolio.campaigns[symbol] = []

        for campaign in campaigns:
            if not campaign.is_closed:
                campaign.add(order)
                return

        new_campaign = Campaign()
        new_campaign.add_order(order)
        self.portfolio.campaigns[symbol].append(new_campaign)
