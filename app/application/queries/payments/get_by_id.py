from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.payments.base import PaymentDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import NotFoundException
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.values.users import UserId, UserRole


@dataclass(frozen=True)
class GetByIDPaymentQuery(BaseQuery):
    id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetByIDPaymentQueryHandler(BaseQueryHandler[GetByIDPaymentQuery, PaymentDTO]):
    payment_repository: BasePaymentRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetByIDPaymentQuery) -> PaymentDTO:
        payment = await self.payment_repository.get_by_id(query.id)
        if payment is None:
            raise NotFoundException()

        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ) and UserId(UUID(query.user_jwt_data.id)) != payment.user_id: raise


        return PaymentDTO.from_entity(payment)
