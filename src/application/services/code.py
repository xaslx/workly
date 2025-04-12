from dataclasses import dataclass
from src.domain.user.exception import UserAlreadyExistsException, UserNotFoundException
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.infrastructure.cache.redis import RedisCache
import random
from src.infrastructure.broker.rabbitmq.publisher import publish
from src.logger import logger
from abc import ABC



async def send_and_cache(telegram_id: int, redis_cache: RedisCache) -> bool:

    code: str = str(random.randint(100000, 999999))
    logger.info(f'Сгенерирован код: {code} для пользователя: {telegram_id}')

    await publish(chat_id=telegram_id, text=f'Ваш код: {code}')
    logger.info(f'Код: {code} отправлен пользователю в телеграм: {telegram_id}')

    await redis_cache.set_with_ttl(key=f'{telegram_id}:code', value=code, ttl_seconds=600)
    logger.info(f'Код записан в редис')

    return True


@dataclass
class SendCode(ABC):
    user_repository: BaseUserRepository
    redis_cache: RedisCache

    async def _check_user(self, telegram_id: int) -> bool:
        return await self.user_repository.get_user_by_telegram_id(telegram_id=telegram_id)
    
    async def execute(self, telegram_id: int, auth_type: str) -> bool:
        
        user: bool = await self._check_user(telegram_id=telegram_id)

        if auth_type == 'REGISTER':

            if user:
                raise UserAlreadyExistsException()
        
        if auth_type == 'LOGIN':

            if not user:
                raise UserNotFoundException()

        return await send_and_cache(telegram_id=telegram_id, redis_cache=self.redis_cache)


@dataclass
class CheckCode:
    redis_cache: RedisCache

    async def execute(self, code: int, telegram_id: int) -> bool:

        cache_code = await self.redis_cache.get(key=f'{telegram_id}:code')
        logger.info(f'Получение кода из кэша, для пользователя: {telegram_id}: код: {cache_code}')

        if not cache_code:
            logger.info(f'Не удалось найти код в редисе, для пользователя: {telegram_id}')
            return False
        
        if int(cache_code) != code:
            logger.warning(f'Пользователь: {telegram_id} ввел неверный код: {code}')
            return False
        
        logger.info(f'Успешная проверка кода: {code} для пользователя: {telegram_id}')

        await self.redis_cache.delete(key=f'{telegram_id}:code')
        logger.info(f'Код из кэша для пользователя: {telegram_id} удален')

        return True
        
