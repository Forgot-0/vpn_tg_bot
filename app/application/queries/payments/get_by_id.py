from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.payments.base import PaymentDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.exception import NotFoundException
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetByIDPaymentQuery(BaseQuery):
    id: UUID
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetByIDPaymentQueryHandler(BaseQueryHandler[GetByIDPaymentQuery, PaymentDTO]):
    payment_repository: BasePaymentRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetByIDPaymentQuery) -> PaymentDTO:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        payment = await self.payment_repository.get_by_id(query.id)
        if payment is None:
            raise NotFoundException()

        return PaymentDTO.from_entity(payment)
