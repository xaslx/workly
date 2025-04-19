from src.infrastructure.repositories.chat.base import BaseChatRepository, T
from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.models.chat import ChatMessages
from src.domain.chat.entity import ChatMessagesEntity
from sqlalchemy import select


@dataclass
class SQLAlchemyChatRepository(BaseChatRepository):
    
    _session: AsyncSession

    async def save_message(self, model: T) -> T:
        return await super().save_message()
    
    async def delete_message(self, model: T) -> None:
        return await super().delete_message()
    
    async def clear_chat(self) -> bool:
        return await super().clear_chat()
    
    async def get_all_messages(self) -> list[ChatMessagesEntity] | None:
        result = await self._session.execute(select(ChatMessages))
        messages = result.scalars().all()

        if not messages:
            return None

        return [
            ChatMessagesEntity(
                id=msg.id,
                username=msg.username,
                text=msg.text,
                created_at=msg.created_at,
            )
            for msg in messages
        ]


