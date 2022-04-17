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

        self.repositories = {}
        for topic in self.config.topics:
            TopicRepository = RepositoryMapping[topic]
            self.repositories[topic] = TopicRepository(
                rdb_session=self.rdb_session_factory.build(),
            )

        self.flex_handler = FlexHandler(
            messagebus=self.messagebus,
            config=self.config,
            scheduler=self.scheduler,
            repositories=self.repositories,
        )

    def startup(self):
        self.flex_handler.startup()
