from ibkr_trade_log.portfolio.handler import PortfolioHandler
from ibkr_trade_log.portfolio.portfolio import Portfolio


class PortfolioPlugin:
    def __init__(
        self,
        app,
    ):
        self.messagebus = app.messagebus

        self.portfolio_handler = PortfolioHandler(
            messagebus=self.messagebus,
            order_repository=app.flex_plugin.order_repository,
            transfer_repository=app.flex_plugin.transfer_repository,
            cash_transaction_repository=app.flex_plugin.cash_transaction_repository,
            portfolio=Portfolio(),
        )

    def startup(self):
        self.portfolio_handler.startup()
