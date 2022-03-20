from dataclasses import dataclass
from typing import TypeVar, Generic

from bootstrap.ddd import ValueObject


@dataclass(frozen=True)
class Message(ValueObject):
    pass


@dataclass(frozen=True)
class Command(Message):
    pass


QueryReturnType = TypeVar("QueryReturnType", bound=ValueObject)


@dataclass(frozen=True)
class Query(Message, Generic[QueryReturnType]):
    pass


@dataclass(frozen=True)
class Event(Message):
    pass
