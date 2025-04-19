from pydantic import BaseModel, Field
from datetime import datetime


class Message(BaseModel):
    text: str
    username: str
    created_at: datetime = Field(default_factory=datetime.now)