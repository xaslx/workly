from dishka import Provider, Scope, provide, from_context
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable
from src.domain.user.entity import UserEntity
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.repositories.user.sqlalchemy import SQLAlchemyUserRepository
from src.config import Config
from src.infrastructure.database.postgresql import new_session_maker
from fastapi.templating import Jinja2Templates
from src.infrastructure.cache.redis import RedisCache
from src.application.use_cases.user.register import RegisterUserUseCase
from src.application.use_cases.code.code import CheckCode, SendCode
from src.application.services.auth import BaseAuthService, AuthServiceImpl
from src.application.services.jwt import JWTService, JWTServiceImpl


class AppProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)
    request: Request = from_context(provides=Request, scope=Scope.REQUEST)


    @provide(scope=Scope.APP)
    def get_jinja_template(self) -> Jinja2Templates:
        template: Jinja2Templates = Jinja2Templates(directory='src/presentation/static/html')
        return template

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def get_redis(self, config: Config) -> RedisCache:

        return RedisCache(
            host=config.redis.host,
            port=config.redis.port,
            decode_responses=True,
        )
    

    #репозитории
    @provide(scope=Scope.REQUEST)
    async def get_user_repository(
        self,
        session: AsyncSession,

    ) -> BaseUserRepository:
        
        return SQLAlchemyUserRepository(
            _session=session,
        )

    #сервисы
    @provide(scope=Scope.REQUEST)
    async def get_register_user_use_case(
        self,
        user_repository: BaseUserRepository,
    ) -> RegisterUserUseCase:
        
        return RegisterUserUseCase(
            user_repository=user_repository,
        )
    
    @provide(scope=Scope.REQUEST)
    async def get_send_code_use_case(
        self,
        redis_cache: RedisCache,
        user_repository: BaseUserRepository,
    ) -> SendCode:
        
        return SendCode(
            redis_cache=redis_cache,
            user_repository=user_repository,
        )
    
    @provide(scope=Scope.REQUEST)
    async def get_check_code_use_case(
        self,
        redis_cache: RedisCache,
    ) -> CheckCode:
        
        return CheckCode(
            redis_cache=redis_cache,
        )
    
    @provide(scope=Scope.REQUEST)
    async def get_jwt_use_case(
        self,
        config: Config,
    ) -> JWTService:
        
        return JWTServiceImpl(
            config=config,
        )
    
    @provide(scope=Scope.REQUEST)
    async def get_auth_use_case(
        self,
        user_repository: BaseUserRepository,
        jwt_service: JWTService,
    ) -> BaseAuthService:
        
        return AuthServiceImpl(
            user_repository=user_repository,
            jwt_service=jwt_service,

        )
    

    #current user
    @provide(scope=Scope.REQUEST)
    def get_token(self, request: Request) -> str:
        
        token: str = request.cookies.get('user_access_token')
    
        if not token:
            return None
        return token


    @provide(scope=Scope.REQUEST)
    async def get_current_user_dependency(
        self,
        auth_service: BaseAuthService,
        token: str,
    ) -> UserEntity:
        
        if not token:
            return None
        
        return await auth_service.get_current_user(token=token)