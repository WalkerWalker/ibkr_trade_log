from messagebus.bus import MessageBus


class Handler:
    def __init__(self, messagebus: MessageBus):
        self.messagebus = messagebus
