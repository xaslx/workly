from src.infrastructure.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.chat.entity import ChatMessagesEntity


class ChatMessages(Base):
    __tablename__ = 'chat_messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    username: Mapped[str]


    @classmethod
    def from_entity(cls, entity: ChatMessagesEntity) -> 'ChatMessages':

        return cls(
            text=entity.text,
            username=entity.username,
        )