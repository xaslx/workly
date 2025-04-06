from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.base import Base


T = TypeVar('T', bound=Base)


@dataclass
class BaseUserRepository(ABC, Generic[T]):

    @abstractmethod
    async def add_user(self, model: T) -> UserEntity:
        ...

    @abstractmethod
    async def save(self, model: T) -> UserEntity:
        ...

    @abstractmethod
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def update_user(self, model: T) -> UserEntity:
        ...