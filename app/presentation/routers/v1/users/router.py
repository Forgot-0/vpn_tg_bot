from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Depends, status

from app.application.dtos.base import PaginatedResult
from app.application.dtos.users.base import UserDTO, UserFilterParam, UserListParams, UserSortParam
from app.application.queries.users.get_list import GetListUserQuery
from app.application.queries.users.get_me import GetMeUserQuery
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentUserJWTData
from app.presentation.schemas.filters import ListParamsBuilder



router = APIRouter(route_class=DishkaRoute)

user_list_params_builder = ListParamsBuilder(UserSortParam, UserFilterParam, UserListParams)


@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_list_user(
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
    params: Annotated[UserListParams, Depends(user_list_params_builder)],
) -> PaginatedResult[UserDTO]:
    list_user: PaginatedResult[UserDTO]
    list_user = await mediator.handle_query(
        GetListUserQuery(
            user_jwt_data=user_jwt_data,
            user_query=params
        )
    )
    return list_user

@router.get(
    "/me",
    status_code=status.HTTP_200_OK
)
async def get_me(
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> UserDTO:
    return await mediator.handle_query(
        GetMeUserQuery(user_jwt_data=user_jwt_data)
    )


