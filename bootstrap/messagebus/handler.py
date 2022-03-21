from bootstrap.logger import LoggerMixin
from bootstrap.messagebus.bus import MessageBus


class Handler(LoggerMixin):
    def __init__(self, messagebus: MessageBus):
        self.messagebus = messagebus
