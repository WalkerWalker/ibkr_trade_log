from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Entity:
    id: UUID = field(init=True, default_factory=uuid4)


@dataclass(frozen=True)
class ValueObject:
    pass
