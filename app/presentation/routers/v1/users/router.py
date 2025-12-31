from typing import Annotated
from uuid import UUID
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Query, status

from app.application.dtos.base import PaginatedResponseDTO
from app.application.dtos.subscriptions.subscription import SubscriptionDTO
from app.application.dtos.users.base import UserDTO
from app.application.queries.subscription.get_by_user import GetSubscriptionsUserQuery
from app.application.queries.users.get_by_id import GetByIdUserQuery
from app.application.queries.users.get_list import GetListUserQuery
from app.application.queries.users.get_me import GetMeUserQuery
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CurrentAdminJWTData, CurrentUserJWTData
from app.presentation.routers.v1.users.requests import GetUsersRequest



router = APIRouter(route_class=DishkaRoute)



@router.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_list_user(
    user_jwt_data: CurrentAdminJWTData,
    mediator: FromDishka[BaseMediator],
    users_request: Annotated[GetUsersRequest, Query()],
) -> PaginatedResponseDTO[UserDTO]:

    list_user: PaginatedResponseDTO[UserDTO]

    list_user = await mediator.handle_query(
        GetListUserQuery(
            user_jwt_data=user_jwt_data,
            user_query=users_request.to_user_filter()
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


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK
)
async def get_user(
    user_id: UUID,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> UserDTO:
    return await mediator.handle_query(
        GetByIdUserQuery(
            user_id=user_id,
            user_jwt_data=user_jwt_data
        )
    )


@router.get(
    "/{user_id}/subscriptions",
    description="Пользователь может посмотреть свои подписки или любые если админ.",
    status_code=status.HTTP_200_OK
)
async def get_user_subscriptions(
    user_id: UUID,
    user_jwt_data: CurrentUserJWTData,
    mediator: FromDishka[BaseMediator],
) -> list[SubscriptionDTO]:
    return await mediator.handle_query(
        GetSubscriptionsUserQuery(
            user_id=user_id,
            user_jwt_data=user_jwt_data
        )
    )


