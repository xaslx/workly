from src.infrastructure.repositories.user.base import BaseUserRepository, T
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.user import User
from sqlalchemy import select, update, delete


@dataclass
class SQLAlchemyUserRepository(BaseUserRepository):
    
    _session: AsyncSession

    async def add_user(self, model: T) -> UserEntity:

        try:
            self._session.add(model)
            await self._session.commit()
            await self._session.refresh(model)
            return model.to_entity()
        except Exception as e:
            raise e
        
    async def save(self, model):
        return await super().save(model)
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserEntity | None:

        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            return user.to_entity()
        return None
    
    async def update_user(self, model):
        return await super().update_user(model)


    async def get_user_by_username(self, username: str) -> UserEntity | None:
        result = await self._session.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        if user:
            return user.to_entity()
        return None