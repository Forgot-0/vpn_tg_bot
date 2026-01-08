from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, status

from app.application.commands.subscriptions.add_protocol_price import AddProtocolPriceCommand
from app.application.commands.subscriptions.add_region_price import AddRegionPriceCommand
from app.application.commands.subscriptions.update_price import UpdatePriceConfigCommand
from app.application.queries.subscription.get_price_config import GetPriceConfigQuery
from app.domain.entities.price import PriceConfig
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentAdminJWTData
from app.presentation.routers.v1.price.requests import AddProtocolPriceRequest, AddRegionPriceRequest, UpdatePriceRequest



router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_price_config(
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
) -> PriceConfig:
    return await mediator.handle_query(
        GetPriceConfigQuery(user_jwt_data=user_jwt_data)
    )

@router.post(
    "/add_protocol",
    status_code=status.HTTP_200_OK
)
async def add_protocol_price(
    create_request: AddProtocolPriceRequest,
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
) -> None:
    await mediator.handle_command(
        AddProtocolPriceCommand(
            protocol=create_request.protocol,
            coef=create_request.coef,
            user_jwt_data=user_jwt_data
        )
    )

@router.post(
    "/add_redion",
    status_code=status.HTTP_200_OK
)
async def add_region_price(
    create_request: AddRegionPriceRequest,
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
) -> None:
    await mediator.handle_command(
        AddRegionPriceCommand(
            region_code=create_request.region,
            coef=create_request.coef,
            user_jwt_data=user_jwt_data
        )
    )


@router.patch(
    "/",
    status_code=status.HTTP_200_OK
)
async def update_price(
    update_request: UpdatePriceRequest,
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
) -> None:
    await mediator.handle_command(
        UpdatePriceConfigCommand(
            daily_rate=update_request.daily_rate,
            device_rate_multiplier=update_request.device_rate_multiplier,
            region_base_multiplier=update_request.region_base_multiplier,
            region_multipliers=update_request.region_multipliers,
            protocol_base_multiplier=update_request.protocol_base_multiplier,
            protocol_multipliers=update_request.protocol_multipliers,
            user_jwt_data=user_jwt_data
        )
    )
