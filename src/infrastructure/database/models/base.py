from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import func
from abc import ABC, abstractmethod
from typing import TypeVar
from datetime import datetime
from sqlalchemy import DateTime


T = TypeVar('T')


class Base(DeclarativeBase, ABC):

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now)

    @abstractmethod
    def to_entity() -> T:
        ...
