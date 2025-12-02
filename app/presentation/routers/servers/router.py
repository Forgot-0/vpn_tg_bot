from aiogram.utils.web_app import safe_parse_webapp_init_data
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends

from application.commands.servers.create import CreateServerCommand
from domain.values.servers import ApiType
from infrastructure.mediator.base import BaseMediator
from presentation.routers.servers.requests.servers import Create3XUISerrverRequest


router = APIRouter(route_class=DishkaRoute)




@router.post("/3X-UI")
async def create_server(
    server_request: Create3XUISerrverRequest,
    mediator: FromDishka[BaseMediator]
) -> None:

    await mediator.handle_command(
        CreateServerCommand(
            limit=server_request.limit,
            code=server_request.region_code,
            api_type=ApiType.x_ui.value,
            username=server_request.username,
            password=server_request.password,
            twoFactorCode=server_request.twoFactorCode,
            ip=server_request.ip,
            panel_path=server_request.panel_path,
            panel_port=server_request.panel_port,
            domain=server_request.domain
        )
    )


