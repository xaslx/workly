from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(kw_only=True)
class BaseEntity(ABC):

    id: int | None = None

    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    updated_at: datetime = field(
        default=None,
        kw_only=True,
    )
    
    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, __value: 'BaseEntity') -> bool:
        return self.id == __value.id