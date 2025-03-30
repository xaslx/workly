from src.infrastructure.database.models.base import Base
from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database.models.review import Review


class User(Base):
    __tablename__ = 'users'

    balance: Mapped[Numeric] = mapped_column(Numeric(10, 2), default=0.00)
    is_premium: Mapped[bool] = mapped_column(default=False)
    is_available: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    hold_balance: Mapped[Numeric | None] = mapped_column(Numeric(10, 2), default=None, nullable=True)
    telegram_id: Mapped[int]
    rating_avg: Mapped[float] = mapped_column(default=0.0)
    rating_count: Mapped[int] = mapped_column(default=0)
    completed_orders_as_freelancer: Mapped[int] = mapped_column(default=0)
    completed_orders_as_customer: Mapped[int] = mapped_column(default=0)


    reviews: Mapped[list['Review']] = relationship(back_populates='user')