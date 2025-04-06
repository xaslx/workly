from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from src.config import Config
from jose import ExpiredSignatureError, JWTError, jwt
from dataclasses import dataclass


@dataclass
class JWTService(ABC):
    
    @abstractmethod
    def create_access_token(self, data: dict, **kwargs) -> tuple[str, int]:
        ...

    @abstractmethod
    def valid_token(self, token: str) -> dict | None:
        ...
        

@dataclass   
class JWTServiceImpl(JWTService):

    config: Config

    def create_access_token(self, data: dict, exp: int | None = 10) -> tuple[str, int]:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=exp)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, self.config.jwt.secret_key, self.config.jwt.algorithm), expire

    def valid_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token,self.config.jwt.secret_key, self.config.jwt.algorithm)
        except ExpiredSignatureError:
            return None
        except JWTError:
            return None
        return payload