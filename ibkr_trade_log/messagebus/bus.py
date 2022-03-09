from typing import Callable, Optional, Any, Type, TypeVar

from ibkr_trade_log.messagebus.model import Message, Event

MessageType = TypeVar("MessageType", bound=Message)
EventType = TypeVar("EventType", bound=Event)


class MessageBus:
    def declare(
        self,
        message_type: Type[Message],
        handler: Callable[[MessageType], None],
    ):
        raise NotImplementedError()

    def tell(
        self,
        message: Message,
    ):
        raise NotImplementedError()

    def ask(
        self,
        message: Message,
        *,
        timeout: Optional[int] = None,
    ) -> Optional[Any]:
        raise NotImplementedError()

    def publish(
        self,
        event: Event,
    ):
        raise NotImplementedError()

    def subscribe(
        self,
        event_type: Type[Event],
        handler: Callable[[EventType], None],
    ):
        raise NotImplementedError()
