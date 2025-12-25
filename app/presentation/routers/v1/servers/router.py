from typing import Annotated
from uuid import UUID
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status

from app.application.commands.servers.create import CreateServerCommand
from app.application.commands.servers.delete import DeleteServerCommand
from app.application.dtos.base import PaginatedResult
from app.application.dtos.servers.base import ServerDTO, ServerFilterParam, ServerListParams, ServerSortParam
from app.application.queries.servers.get_list import GetListServerQuery
from app.domain.values.servers import ApiType
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentAdminJWTData, CurrentUserJWTData
from app.presentation.routers.v1.servers.requests import CreateServerRequest
from app.presentation.schemas.filters import ListParamsBuilder



router = APIRouter(route_class=DishkaRoute)

server_list_params_builder = ListParamsBuilder(ServerSortParam, ServerFilterParam, ServerListParams)



@router.post("/{api_type}")
async def create_server(
    api_type: ApiType,
    server_request: CreateServerRequest,
    mediator: FromDishka[BaseMediator],
    user_jwt_data: CurrentAdminJWTData
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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_list_server(
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
    params: Annotated[ServerListParams, Depends(server_list_params_builder)]
) -> PaginatedResult[ServerDTO]:
    return await mediator.handle_query(
        GetListServerQuery(
            server_query=params,
            user_jwt_data=user_jwt_data
        )
    )


@router.delete(
    "/{server_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    server_id: UUID,
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
)  -> None:
    await mediator.handle_command(
        DeleteServerCommand(
            server_id=server_id,
            user_jwt_data=user_jwt_data
        )
    )
