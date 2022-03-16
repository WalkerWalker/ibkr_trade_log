from ibkr_trade_log.flex.cash_transaction.handler import CashTransactionHandler
from ibkr_trade_log.flex.cash_transaction.repository import CashTransactionRepository
from ibkr_trade_log.flex.handler import FlexConfig, FlexHandler, QueryAndStoreReport


from ibkr_trade_log.flex.order.handler import OrderHandler
from ibkr_trade_log.flex.order.repository import OrderRepository, OrderDataFrame, Order
from ibkr_trade_log.flex.transfer.handler import TransferHandler
from ibkr_trade_log.flex.transfer.repository import TransferRepository


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

        self.flex_handler = FlexHandler(
            messagebus=self.messagebus, config=self.config, scheduler=self.scheduler
        )

        self.order_repository = OrderRepository(
            rdb_session=self.rdb_session_factory.build(),
        )

        self.order_handler = OrderHandler(
            messagebus=self.messagebus,
            order_repository=self.order_repository,
        )

        self.cash_transaction_repository = CashTransactionRepository(
            rdb_session=self.rdb_session_factory.build(),
        )

        self.cash_transaction_handler = CashTransactionHandler(
            messagebus=self.messagebus,
            cash_transaction_repository=self.cash_transaction_repository,
        )

        self.transfer_repository = TransferRepository(
            rdb_session=self.rdb_session_factory.build(),
        )

        self.transfer_handler = TransferHandler(
            messagebus=self.messagebus,
            transfer_repository=self.transfer_repository,
        )

    def startup(self):
        self.flex_handler.startup()
        self.order_handler.startup()
        self.cash_transaction_handler.startup()
        self.transfer_handler.startup()
