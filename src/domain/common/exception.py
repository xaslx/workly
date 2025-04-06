from dataclasses import dataclass
from fastapi import HTTPException, status


@dataclass(eq=False)
class AppErrorException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Ошибка приложения'

    


@dataclass(eq=False)
class DomainErrorException(HTTPException):
    ...