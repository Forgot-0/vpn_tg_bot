from dataclasses import dataclass

from app.domain.entities.subscription import Subscription
from app.domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository


@dataclass
class DiscountService:
    discount_repository: BaseDiscountRepository
    discount_user_repository: BaseDiscountUserRepository
