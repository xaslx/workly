from dataclasses import dataclass
from src.domain.common.entity import BaseEntity


@dataclass(kw_only=True)
class ChatMessagesEntity(BaseEntity):
    text: str
    username: str

    @classmethod
    def create_message(
        cls,
        text: str,
        username: str,
    ) -> 'ChatMessagesEntity':
        
        return cls(
            text=text,
            username=username,
        )
