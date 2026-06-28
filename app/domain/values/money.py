from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "RU"

    def __post_init__(self) -> None:
        if self.amount < Decimal("0"):
            raise

    def _assert_same_currency(self, other: Money) -> None:
        if self.currency != other.currency:
            raise 

    def __add__(self, other: Money) -> Money:
        self._assert_same_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: Money) -> Money:
        self._assert_same_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: int | float | Decimal) -> Money:
        return Money(self.amount * Decimal(str(factor)), self.currency)

    def __lt__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount < other.amount

    def __le__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount <= other.amount

    def __gt__(self, other: Money) -> bool:
        self._assert_same_currency(other)
        return self.amount > other.amount

    def is_zero(self) -> bool:
        return self.amount == Decimal("0")

    def __str__(self) -> str:
        return f"{self.amount} {self.currency}"

    @classmethod
    def zero(cls, currency: str = "RU") -> Money:
        return cls(Decimal("0"), currency)