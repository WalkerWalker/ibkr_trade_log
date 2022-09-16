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
class CalculatePortfolio(Command):
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
        self.messagebus.declare(CalculatePortfolio, self.handle_calculate_portfolio)

    def handle_calculate_portfolio(self, command: CalculatePortfolio):
        transfers = self.transfer_repository.all_limit()
        orders = self.order_repository.all_limit()
        # change to events, superclass order, transfer, cash_transaction.
        # order by time
        for transfer in transfers:
            self.add_transfer_to_portfolio(transfer)

        for order in orders:
            self.add_order_to_portfolio(order)

        print(len(self.portfolio.campaigns))

    def handle_transfer(self, command: ProcessTransfer):
        self.logger.info(f"processing transfer {command.transfer}")
        self.add_transfer_to_portfolio(command.transfer)

    def handle_cash_transaction(self, command: ProcessCashTransaction):
        self.logger.info(f"processing cash transaction {command.cash_transaction}")
        self.add_cash_transaction_to_portfolio(command.cash_transaction)

    def handle_order_filled(self, command: ProcessOrderFilled):
        self.logger.info(f"processing filled order {command.order}")
        self.add_order_to_portfolio(command.order)

    def add_order_to_portfolio(self, order: Order):
        if order.underlyingSymbol is not None:
            symbol = order.underlyingSymbol
        else:
            symbol = order.symbol
        if symbol not in self.portfolio.campaigns:
            self.portfolio.campaigns[symbol] = []

        campaigns = self.portfolio.campaigns[symbol]
        for campaign in campaigns:
            if not campaign.is_closed:
                campaign.add_order(order)
                return

        new_campaign = Campaign()
        new_campaign.add_order(order)
        self.portfolio.campaigns[symbol].append(new_campaign)

    def add_transfer_to_portfolio(self, transfer: Transfer):
        # TODO move it to it's own helper
        if transfer.underlyingSymbol is not None:
            symbol = transfer.underlyingSymbol
        else:
            symbol = transfer.symbol

        if symbol == "--":
            return

        if symbol not in self.portfolio.campaigns:
            self.portfolio.campaigns[symbol] = []

        campaigns = self.portfolio.campaigns[symbol]
        for campaign in campaigns:
            if not campaign.is_closed:
                campaign.add_transfer(transfer)
                return

        new_campaign = Campaign()
        new_campaign.add_transfer(transfer)
        self.portfolio.campaigns[symbol].append(new_campaign)

    def add_cash_transaction_to_portfolio(self, cash_transaction: CashTransaction):
        raise NotImplementedError
