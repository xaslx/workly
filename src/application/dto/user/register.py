from dataclasses import dataclass, field


@dataclass
class UserRegisterDTO:
    telegram_id: int
    name: str
    username: str


