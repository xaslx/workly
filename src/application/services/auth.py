from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.application.services.jwt import JWTService
from src.domain.user.exception import UserIsNotPresentException, UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity


@dataclass
class BaseAuthService(ABC):
    
    user_repository: BaseUserRepository
    jwt_service: JWTService
    
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

        payload = self.jwt_service.valid_token(token=token)
    
        if not payload:
            return None
        
        user_tg_id: str | None = payload.get('sub')
        user: UserEntity | None = await self.user_repository.get_user_by_telegram_id(telegram_id=int(user_tg_id))

        if user is None:
            raise UserIsNotPresentException()

        return user