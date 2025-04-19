from dataclasses import dataclass
from src.application.dto.chat.message import SaveMessageDTO
from src.infrastructure.repositories.chat.base import BaseChatRepository
from src.domain.chat.entity import ChatMessagesEntity
from src.infrastructure.database.models.chat import ChatMessages


@dataclass
class SaveMessageUseCase:
    chat_repository: BaseChatRepository

    async def execute(self, message: SaveMessageDTO) -> bool:

        message: ChatMessagesEntity = ChatMessagesEntity.create_message(
            text=message.text,
            username=message.username,
            created_at=message.created_at,
        )

        model: ChatMessages = ChatMessages.from_entity(entity=message)
        res = await self.chat_repository.save_message(model=model)
        return res
