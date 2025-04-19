from src.domain.common.entity import BaseEntity
from dataclasses import dataclass
from decimal import Decimal


@dataclass(kw_only=True)
class UserEntity(BaseEntity):
    """Пользователь - агрегат в доменной модели"""
    
    telegram_id: int
    name: str
    username: str
    balance: Decimal = Decimal('0.00')
    hold_balance: Decimal | None = None
    is_premium: bool = False
    is_available: bool = True
    is_active: bool = True
    rating_avg: float = 0.0
    is_deleted: bool = False
    role: str = 'user'
    completed_orders_as_freelancer: int = 0
    completed_orders_as_customer: int = 0

    @classmethod
    def create_user(
        cls,
        telegram_id: int,
        name: str,
        username: str,

    ) -> 'UserEntity':

        return cls(
            telegram_id=telegram_id,
            name=name,
            username=username,
            balance=cls.balance,
            hold_balance=cls.hold_balance,
            is_premium=cls.is_premium,
            is_available=cls.is_available,
            is_active=cls.is_active,
            rating_avg=cls.rating_avg,
            role=cls.role,
            is_deleted=cls.is_deleted,
            completed_orders_as_freelancer=cls.completed_orders_as_freelancer,
            completed_orders_as_customer=cls.completed_orders_as_customer,
        )

    def add_completed_order_as_freelancer(self) -> None:
        """Увеличить счетчик успешно выполненных заказов как фрилансер"""
        self.completed_orders_as_freelancer += 1

    def add_completed_order_as_customer(self) -> None:
        """Увеличить счетчик успешно выполненных заказов как заказчик"""
        self.completed_orders_as_customer += 1

    def get_total_completed_orders(self) -> int:
        """Общее количество успешных заказов (в обеих ролях)"""
        return self.completed_orders_as_freelancer + self.completed_orders_as_customer
    
    def delete_user(self) -> None:

        if not self.is_deleted:
            self.is_deleted = True

    def add_to_balance(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount

    def hold_funds(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if self.balance < amount:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.hold_balance = (self.hold_balance or Decimal('0.00')) + amount