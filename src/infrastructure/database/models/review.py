from src.infrastructure.database.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.infrastructure.database.models.user import User


class Review(Base):
    __tablename__ = 'reviews'

    reviewer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    rating: Mapped[int]
    comment: Mapped[str] = mapped_column(String(500))

    user: Mapped['User'] = relationship(back_populates='reviews', foreign_keys=[user_id])
    reviewer: Mapped['User'] = relationship(foreign_keys=[reviewer_id])