from uuid import UUID
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status
from fastapi.responses import RedirectResponse

from app.application.commands.subscriptions.create import CreateSubscriptionCommand
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.queries.subscription.get_by_id import GetByIdQuery
from app.application.queries.subscription.get_config import GetConfigQuery
from app.domain.values.servers import VPNConfig
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentUserJWTData
from app.presentation.routers.v1.subscription.requests import CreateSubscriptionRequests


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
            duration=subscription_request.duration,
            device_count=subscription_request.device_count,
            protocol_types=subscription_request.protocol_types,
            user_jwt_data=user_jwt_data
        )
    )
    return RedirectResponse(url=result.url)