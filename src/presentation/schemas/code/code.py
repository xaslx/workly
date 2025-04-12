from pydantic import BaseModel, Field
from enum import StrEnum


class AuthTypeSchema(StrEnum):
    REGISTER = 'REGISTER'
    LOGIN = 'LOGIN'


class SendCodeSchema(BaseModel):
    telegram_id: int
    auth_type: AuthTypeSchema


class CheckCodeSchema(BaseModel):
    telegram_id: int
    confirmation_code: int


class LoginUserWithCode(CheckCodeSchema):
    ...