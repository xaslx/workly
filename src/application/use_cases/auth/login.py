from dataclasses import dataclass
from src.application.services.jwt import JWTService
from src.application.services.code import CheckCode
from src.logger import logger


@dataclass
class LoginUserUseCase:
    jwt_service: JWTService
    check_code: CheckCode

    async def execute(self, telegram_id: int, code: int) -> str:

        res: bool = await self.check_code.execute(code=code, telegram_id=telegram_id)
        logger.info(f'Проверка кода при входе, для пользователя: {telegram_id}, код: {code}, результат: {res}')
        token: str | None = None

        if res:
            token, _ = self.jwt_service.create_access_token(data={'sub': telegram_id})
            logger.info(f'Токен получен: {token}')
            return token