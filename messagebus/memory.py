from collections import defaultdict
from typing import Callable, Optional, Any, Type

from messagebus.model import Message, Event
from messagebus.bus import MessageBus, MessageType, EventType
from messagebus.util import get_class_path


class MemoryMessageBus(MessageBus):
    def __init__(self):
        self.message_handlers = defaultdict()
        self.event_handlers = defaultdict(set)

    def declare(
        self,
        message_type: Type[Message],
        handler: Callable[[MessageType], None],
    ):
        message_type_str = get_class_path(message_type)
        self.message_handlers[message_type_str] = handler

    def tell(
        self,
        message: Message,
    ):
        message_type_str = get_class_path(type(message))
        handler = self.message_handlers.get(message_type_str, None)
        if handler:
            handler(message)

    def ask(
        self,
        message: Message,
        *,
        timeout: Optional[int] = None,
    ) -> Optional[Any]:
        message_type_str = get_class_path(type(message))
        handler = self.message_handlers.get(message_type_str)
        if handler:
            return handler(message)

    def publish(
        self,
        event: Event,
    ):
        event_type_str = get_class_path(type(event))
        for event_handler in self.event_handlers[event_type_str]:
            event_handler(event)

    def subscribe(
        self,
        event_type: Type[Event],
        handler: Callable[[EventType], None],
    ):
        event_type_str = get_class_path(event_type)
        event_handlers = self.event_handlers[event_type_str]
        event_handlers.add(handler)
