from typing import Annotated
from uuid import UUID
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from app.application.commands.subscriptions.create import CreateSubscriptionCommand
from app.application.commands.subscriptions.renew import RenewSubscriptionCommand
from app.application.dtos.base import PaginatedResponseDTO
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.queries.subscription.get_by_id import GetSubscriptionByIdQuery
from app.application.queries.subscription.get_config import GetConfigQuery
from app.application.queries.subscription.get_list import GetListSubscriptionsQuery
from app.application.queries.subscription.get_price import GetPriceSubscriptionQuery
from app.domain.values.servers import VPNConfig
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentAdminJWTData, CurrentUserJWTData
from app.presentation.routers.v1.subscription.requests import (
    CreateSubscriptionRequests,
    GetSubscriptionsRequest,
    RenewSubscriptionRequests
)
from app.presentation.routers.v1.subscription.responses import PaymentUrlResponse, PriceSubscriptionResponse


router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/{subscription_id}",
    status_code=status.HTTP_200_OK
)
async def get_subscription(
    subscription_id: UUID,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> SubscriptionDTO:
    return await mediator.handle_query(
        GetSubscriptionByIdQuery(
            subscription_id=subscription_id,
            user_jwt_data=user_jwt_data
        )
    )

@router.get(
    "/{subscription_id}/config",
    status_code=status.HTTP_200_OK
)
async def get_subscription_config(
    subscription_id: UUID,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> list[VPNConfig]:
    return await mediator.handle_query(
        GetConfigQuery(
            subscription_id=subscription_id,
            user_jwt_data=user_jwt_data
        )
    )

@router.post(
    "/",
    status_code=status.HTTP_200_OK
)
async def create_subscription(
    subscription_request: CreateSubscriptionRequests,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> PaymentUrlResponse:
    result, *_ = await mediator.handle_command(
        CreateSubscriptionCommand(
            duration=subscription_request.duration_days,
            device_count=subscription_request.device_count,
            protocol_types=subscription_request.protocol_types,
            user_jwt_data=user_jwt_data
        )
    )
    return PaymentUrlResponse(url=result.url)


@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_subscriptions(
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
    subscription_request: Annotated[GetSubscriptionsRequest, Query()],
) -> PaginatedResponseDTO[SubscriptionDTO]:
    return await mediator.handle_query(
        GetListSubscriptionsQuery(
            subscription_query=subscription_request.to_subscription_filter(),
            user_jwt_data=user_jwt_data
        )
    )


@router.post(
    "/{subscription_id}/renew",
    status_code=status.HTTP_200_OK
)
async def renew(
    subscription_id: UUID,
    subscription_request: RenewSubscriptionRequests,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> PaymentUrlResponse:
    result, *_ = await mediator.handle_command(
        RenewSubscriptionCommand(
            subscription_id=subscription_id,
            duration=subscription_request.duration_days,
            user_jwt_data=user_jwt_data
        )
    )
    return PaymentUrlResponse(url=result.url)


@router.post(
    "/get_price",
    status_code=status.HTTP_200_OK
)
async def get_price_subs(
    mediator: FromDishka[BaseMediator],
    subscription_request: CreateSubscriptionRequests,
) -> PriceSubscriptionResponse:
    result = await mediator.handle_query(
        GetPriceSubscriptionQuery(
            duration=subscription_request.duration_days,
            device_count=subscription_request.device_count,
            protocol_types=subscription_request.protocol_types
        )
    )
    return PriceSubscriptionResponse(price=result)

