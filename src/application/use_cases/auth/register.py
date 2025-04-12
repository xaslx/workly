from dataclasses import dataclass
from src.infrastructure.cache.redis import RedisCache
from src.domain.user.exception import UserAlreadyExistsException, UsernameLengthException
from src.application.dto.user.register import UserRegisterDTO
from src.infrastructure.repositories.user.base import BaseUserRepository
from src.domain.user.entity import UserEntity
from src.infrastructure.database.models.user import User
from src.logger import logger
from src.infrastructure.broker.rabbitmq.publisher import publish


@dataclass
class RegisterUserUseCase:
    user_repository: BaseUserRepository
    redis_cache: RedisCache

    async def execute(self, new_user: UserRegisterDTO) -> UserEntity:
        
        user = await self.user_repository.get_user_by_username(username=new_user.username)
        logger.info(f'Поиск пользователя в базе по username: {new_user.username}')

        if user:
            logger.info(f'Пользователь: {new_user.username} найден в базе данных')
            raise UserAlreadyExistsException()
        
        if not (4 <= len(new_user.username) <= 15):
            raise UsernameLengthException('Username должен быть от 4 до 15 символов')
        
        new_user: UserEntity = UserEntity.create_user(
            telegram_id=new_user.telegram_id,
            name=new_user.name,
            username=new_user.username,
        )
        
        model: User = User.from_entity(entity=new_user)
        user: UserEntity = await self.user_repository.add_user(model=model)
        logger.info(f'Новый пользователь: {new_user.username} добавлен в базу данных')

        await publish(chat_id=new_user.telegram_id, text=f'Вы успешно зарегистрировались на сервисе Workly и привязали свой Телеграм.')
        logger.info(f'Пользователю: {new_user.telegram_id} направлено уведомление в Телеграм о успешной регистрации')

        return user
