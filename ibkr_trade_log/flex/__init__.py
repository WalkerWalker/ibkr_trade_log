from ibkr_trade_log.flex.cash_transaction import CashTransactionRepository
from ibkr_trade_log.flex.order import OrderRepository
from ibkr_trade_log.flex.transfer import TransferRepository
from ibkr_trade_log.flex.handler import (
    FlexHandler,
    Topics,
    FlexConfig,
)


RepositoryMapping = {
    Topics.Order: OrderRepository,
    Topics.CashTransaction: CashTransactionRepository,
    Topics.Transfer: TransferRepository,
}


class FlexPlugin:
    def __init__(
        self,
        config: FlexConfig,
        app,
    ):
        self.config = config

        self.scheduler = app.scheduler
        self.messagebus = app.messagebus
        self.rdb_session_factory = app.rdb_session_factory

        self.order_repository = OrderRepository(
            rdb_session=self.rdb_session_factory.build(),
        )
        self.cash_transaction_repository = CashTransactionRepository(
            rdb_session=self.rdb_session_factory.build(),
        )
        self.transfer_repository = TransferRepository(
            rdb_session=self.rdb_session_factory.build(),
        )

        self.flex_handler = FlexHandler(
            messagebus=self.messagebus,
            config=self.config,
            scheduler=self.scheduler,
            order_repository=self.order_repository,
            transfer_repository=self.transfer_repository,
            cash_transaction_repository=self.cash_transaction_repository,
        )

    def startup(self):
        self.flex_handler.startup()
