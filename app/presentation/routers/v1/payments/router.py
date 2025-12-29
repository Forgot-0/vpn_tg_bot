from typing import Annotated
from dishka import FromDishka
from fastapi import APIRouter, Query, status
from dishka.integrations.fastapi import DishkaRoute

from app.application.dtos.base import PaginatedResponseDTO
from app.application.dtos.payments.base import PaymentDTO
from app.application.queries.payments.get_list import GetListPaymentQuery
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentAdminJWTData
from app.presentation.routers.v1.payments.requests import GetPaymentsRequest


router = APIRouter(route_class=DishkaRoute)



@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_list_payments(
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
    payment_request: Annotated[GetPaymentsRequest, Query()],
) -> PaginatedResponseDTO[PaymentDTO]:
    return await mediator.handle_query(
        GetListPaymentQuery(
            payment_query=payment_request.to_payment_filter(),
            user_jwt_data=user_jwt_data
        )
    )

