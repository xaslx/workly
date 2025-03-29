from dishka import Provider, Scope, provide, AnyOf, from_context
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncIterable
from src.config import Config
from src.infrastructure.database.postgresql import new_session_maker
from fastapi.templating import Jinja2Templates


class AppProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)

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

