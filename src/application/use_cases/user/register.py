from dataclasses import dataclass
from src.infrastructure.cache.redis import RedisCache


@dataclass
class RegisterUserUseCase:
    user_repository: ...
    redis_cache: RedisCache

    async def execute(self):
        ...