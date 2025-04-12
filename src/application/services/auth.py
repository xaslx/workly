from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from src.infrastructure.cache.redis import RedisCache
from src.application.services.jwt import JWTService
from src.domain.user.exception import UserIsNotPresentException, UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity
import orjson
from src.logger import logger


def decimal_default(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError()


def serialize_user(user: UserEntity) -> bytes:
    return orjson.dumps(
        user,
        default=decimal_default,
        option=orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS
    )


@dataclass
class BaseAuthService(ABC):
    
    user_repository: BaseUserRepository
    jwt_service: JWTService
    redis_cache: RedisCache
    
    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> UserEntity | None:
        ...

    @abstractmethod
    async def get_current_user(self, token: str) -> UserEntity | None:
        ...
    

@dataclass
class AuthServiceImpl(BaseAuthService):

    async def authenticate_user(self, telegram_id: int) -> UserEntity | None:

        user: UserEntity | None = await self.user_repository.get_user_by_telegram_id(telegram_id=telegram_id)

        if not user:
            raise UserNotFoundException()

        return user


    async def get_current_user(self, token: str) -> UserEntity | None:

        payload: dict | None = self.jwt_service.valid_token(token=token)
        if not payload:
            return None
        
        user_tg_id: str | None = payload.get('sub')
        if not user_tg_id:
            return None

        cache_key: str = f'user:{user_tg_id}'
        cached_user: str | None = await self.redis_cache.get(cache_key)
        
        if cached_user:
            try:
                return UserEntity(**orjson.loads(cached_user))
            except orjson.JSONDecodeError:
                logger.error(f'ORJSON error')

        user: UserEntity | None = await self.user_repository.get_user_by_telegram_id(int(user_tg_id))
        if not user:
            raise UserIsNotPresentException()


        await self.redis_cache.set_with_ttl(
            key=cache_key,
            value=serialize_user(user).decode('utf-8'),
            ttl_seconds=600
        )

        return user