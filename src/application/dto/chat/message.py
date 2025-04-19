from dataclasses import dataclass
from datetime import datetime


@dataclass
class SaveMessageDTO:
    text: str
    username: str
    created_at: datetime