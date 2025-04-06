from redis.asyncio import Redis
from typing import Any


class RedisCache:
    def __init__(
        self,
        host: str = 'redis',
        port: int = 6379,
        db: int = 0,
        decode_responses: bool = False,
        **kwargs
    ):

        self._client = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
            **kwargs
        )

    def get(self, key: str) -> Any | None:

        return self._client.get(key)

    def set(self, key: str, value: Any, **kwargs) -> bool:

        return self._client.set(key, value, **kwargs)

    def set_with_ttl(self, key: str, value: Any, ttl_seconds: int) -> bool:

        return self._client.setex(key, ttl_seconds, value)

    @property
    def client(self) -> Redis:

        return self._client