from typing import Annotated
from uuid import UUID
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse

from app.application.commands.subscriptions.create import CreateSubscriptionCommand
from app.application.commands.subscriptions.renew import RenewSubscriptionCommand
from app.application.dtos.base import PaginatedResult
from app.application.dtos.subscriptions.subscription import (
    SubscriptionDTO,
    SubscriptionFilterParam,
    SubscriptionListParams,
    SubscriptionSortParam
)
from app.application.queries.subscription.get_by_id import GetByIdQuery
from app.application.queries.subscription.get_config import GetConfigQuery
from app.application.queries.subscription.get_list import GetListSubscriptionsQuery
from app.application.queries.subscription.get_price import GetPriceSubscriptionQuery
from app.domain.values.servers import VPNConfig
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentAdminJWTData, CurrentUserJWTData
from app.presentation.routers.v1.subscription.requests import CreateSubscriptionRequests, RenewSubscriptionRequests
from app.presentation.routers.v1.subscription.responses import PriceSubscriptionResponse
from app.presentation.schemas.filters import ListParamsBuilder


router = APIRouter(route_class=DishkaRoute)

subscription_list_params_builder = ListParamsBuilder(
    SubscriptionSortParam, SubscriptionFilterParam, SubscriptionListParams
)


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
        GetByIdQuery(
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
) -> VPNConfig:
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
) -> RedirectResponse:
    result, *_ = await mediator.handle_command(
        CreateSubscriptionCommand(
            duration=subscription_request.duration_days,
            device_count=subscription_request.device_count,
            protocol_types=subscription_request.protocol_types,
            user_jwt_data=user_jwt_data
        )
    )
    return RedirectResponse(url=result.url)

@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_subscriptions(
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
    params: Annotated[SubscriptionListParams, Depends(subscription_list_params_builder)],
) -> PaginatedResult[SubscriptionDTO]:
    return await mediator.handle_query(
        GetListSubscriptionsQuery(
            subscription_query=params,
            user_jwt_data=user_jwt_data
        )
    )


@router.post(
    "/{subscription_id}/renew",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def renew(
    subscription_id: UUID,
    subscription_request: RenewSubscriptionRequests,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> RedirectResponse:
    result, *_ = await mediator.handle_command(
        RenewSubscriptionCommand(
            subscription_id=subscription_id,
            duration=subscription_request.duration_days,
            user_jwt_data=user_jwt_data
        )
    )
    return RedirectResponse(url=result.url)


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

