from ibkr_trade_log.event_log.handler import EventHandler
from ibkr_trade_log.event_log.repository import EventRepository


class EventPlugin:
    def __init__(
        self,
        app,
    ):
        self.messagebus = app.messagebus
        self.rdb_session_factory = app.rdb_session_factory

        self.event_repository = EventRepository(
            rdb_session=self.rdb_session_factory.build(),
        )
        self.event_handler = EventHandler(
            messagebus=self.messagebus,
            event_repository=self.event_repository,
        )

    def startup(self):
        self.event_handler.startup()
