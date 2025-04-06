from src.infrastructure.database.models.base import Base
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from src.domain.user.entity import UserEntity
from decimal import Decimal
from src.infrastructure.database.models.review import Review


class User(Base):
    __tablename__ = 'users'

    balance: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0.00)
    is_premium: Mapped[bool] = mapped_column(default=False)
    is_available: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    hold_balance: Mapped[Numeric | None] = mapped_column(Numeric(10, 2), default=None, nullable=True)
    telegram_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    rating_avg: Mapped[float] = mapped_column(default=0.0)
    rating_count: Mapped[int] = mapped_column(default=0)
    completed_orders_as_freelancer: Mapped[int] = mapped_column(default=0)
    completed_orders_as_customer: Mapped[int] = mapped_column(default=0)

    reviews: Mapped[list['Review']] = relationship(
        back_populates='user',
        foreign_keys='Review.user_id'
    )

    
    def to_entity(self) -> UserEntity:

        return UserEntity(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            telegram_id=self.telegram_id,
            name=self.name,
            username=self.username,
            balance=self.balance if isinstance(self.balance, Decimal) else Decimal(str(self.balance)),
            hold_balance=self.hold_balance if isinstance(self.hold_balance, Decimal) or self.hold_balance is None else Decimal(str(self.hold_balance)),
            is_premium=self.is_premium,
            is_available=self.is_available,
            is_active=self.is_active,
            rating_avg=self.rating_avg,
            is_deleted=self.is_deleted,
            completed_orders_as_freelancer=self.completed_orders_as_freelancer,
            completed_orders_as_customer=self.completed_orders_as_customer,
        )

    @classmethod
    def from_entity(cls, entity: UserEntity) -> 'User':

        return cls(
            id=entity.id,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            telegram_id=entity.telegram_id,
            name=entity.name,
            username=entity.username,
            balance=entity.balance,
            hold_balance=entity.hold_balance,
            is_premium=entity.is_premium,
            is_available=entity.is_available,
            is_active=entity.is_active,
            rating_avg=entity.rating_avg,
            is_deleted=entity.is_deleted,
            completed_orders_as_freelancer=entity.completed_orders_as_freelancer,
            completed_orders_as_customer=entity.completed_orders_as_customer,
        )