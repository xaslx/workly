from pydantic import BaseModel



class SendCodeSchema(BaseModel):
    telegram_id: str


class CheckCodeSchema(BaseModel):
    telegram_id: str
    confirmation_code: str
