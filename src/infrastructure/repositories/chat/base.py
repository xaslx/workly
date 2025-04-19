from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from src.domain.chat.entity import ChatMessagesEntity
from src.infrastructure.database.models.base import Base


T = TypeVar('T', bound=Base)


@dataclass
class BaseChatRepository(ABC, Generic[T]):

    @abstractmethod
    async def save_message(self, model: T) -> T:
        ...

    @abstractmethod
    async def delete_message(self, model: T) -> None:
        ...

    @abstractmethod
    async def clear_chat(self) -> bool:
        ...

    @abstractmethod
    async def get_all_messages(self) -> list[T] | None:
        ...