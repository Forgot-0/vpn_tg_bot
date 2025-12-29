from dataclasses import dataclass

from app.application.dtos.base import PaginatedResponseDTO
from app.application.dtos.payments.base import PaymentDTO
from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.base import BaseQuery, BaseQueryHandler
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.filters.payment import PaymentFilter
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.values.users import UserRole


@dataclass(frozen=True)
class GetListPaymentQuery(BaseQuery):
    payment_query: PaymentFilter
    user_jwt_data: UserJWTData


@dataclass(frozen=True)
class GetListPaymentQueryHandler(BaseQueryHandler[GetListPaymentQuery, PaginatedResponseDTO[PaymentDTO]]):
    payment_repository: BasePaymentRepository
    role_access_control: RoleAccessControl

    async def handle(self, query: GetListPaymentQuery) -> PaginatedResponseDTO[PaymentDTO]:
        if not self.role_access_control.can_action(
            UserRole(query.user_jwt_data.role), target_role=UserRole.ADMIN
        ): raise

        result = await self.payment_repository.find_by_filter(query.payment_query)

        return PaginatedResponseDTO(
            items=[PaymentDTO.from_entity(user) for user in result.items],
            total=result.total,
            page=result.page,
            page_size=result.page_size,
            total_pages=result.total_pages,
            has_next=result.has_next,
            has_previous=result.has_previous,
            next_page=result.next_page,
            previous_page=result.previous_page
        )
