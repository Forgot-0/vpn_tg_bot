from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from app.application.commands.servers.create import CreateServerCommand
from app.domain.values.servers import ApiType
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentUserJWTData
from app.presentation.routers.v1.servers.requests import CreateServerRequest



router = APIRouter(route_class=DishkaRoute)


@router.post("/{api_type}")
async def create_server(
    api_type: ApiType,
    server_request: CreateServerRequest,
    mediator: FromDishka[BaseMediator],
    user_jwt_data: CurrentUserJWTData
) -> None:

    await mediator.handle_command(
        CreateServerCommand(
            limit=server_request.limit,
            code=server_request.region_code,
            api_type=api_type.value,
            username=server_request.username,
            password=server_request.password,
            twoFactorCode=server_request.twoFactorCode,
            ip=server_request.ip,
            panel_path=server_request.panel_path,
            panel_port=server_request.panel_port,
            domain=server_request.domain,
            user_jwt_data=user_jwt_data
        )
    )

