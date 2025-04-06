from pydantic import BaseModel, Field





class RegisterUserSchema(BaseModel):
    telegram_id: int
    name: str
    username: str