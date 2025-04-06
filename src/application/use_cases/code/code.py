from dataclasses import dataclass
from src.domain.user.exception import UserAlreadyExistsException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.cache.redis import RedisCache
import random
from src.infrastructure.broker.rabbitmq.publisher import publish
from src.logger import logger





@dataclass
class SendCode:
    user_repository: BaseUserRepository
    redis_cache: RedisCache

    async def execute(self, telegram_id: str) -> bool:

        user = await self.user_repository.get_user_by_telegram_id(telegram_id=int(telegram_id))

        if user:
            raise UserAlreadyExistsException()

        code: str = str(random.randint(100000, 999999))
        logger.info(f'Сгенерирован код: {code} для пользователя: {telegram_id}')

        await publish(chat_id=telegram_id, text=f'Ваш код: {code}')
        logger.info(f'Код: {code} отправлен пользователю в телеграм: {telegram_id}')

        await self.redis_cache.set_with_ttl(key=telegram_id, value=code, ttl_seconds=600)
        logger.info(f'Код записан в редис')

        return True
    

@dataclass
class CheckCode:
    redis_cache: RedisCache

    async def execute(self, code: str, telegram_id: str) -> bool:

        cache_code = await self.redis_cache.get(key=int(telegram_id))
        logger.info(f'Получение кода из кэша, для пользователя: {telegram_id}: код: {cache_code}')

        if not cache_code:
            logger.info(f'Не удалось найти код в редисе, для пользователя: {telegram_id}')
            return False
        
        if cache_code != code:
            logger.warning(f'Пользователь: {telegram_id} ввел неверный код: {code}')
            return False
        
        logger.info(f'Успешная проверка кода: {code} для пользователя: {telegram_id}')
        return True
        
