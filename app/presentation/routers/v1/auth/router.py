from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Cookie, Response, status

from application.commands.auth.login import LoginTelegramUserCommand
from application.commands.auth.refresh import RefreshTokenCommand
from infrastructure.mediator.base import BaseMediator
from presentation.deps import CookieManager, CurrentUserJWTData
from presentation.routers.v1.auth.requests import LoginTelegram
from presentation.routers.v1.auth.response import AccessTokenResponse


router = APIRouter(route_class=DishkaRoute)




@router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login_by_tg(
    login_request: LoginTelegram,
    mediator: FromDishka[BaseMediator],
    cookie_manager: CookieManager,
    response: Response
) -> AccessTokenResponse:
    token_group, *_ = await mediator.handle_command(
        LoginTelegramUserCommand(
            init_data=login_request.init_data
        )
    )
    cookie_manager.set_refresh_token(response, token_group.refresh_token)

    return AccessTokenResponse(access_token=token_group.access_token)



@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
)
async def refresh(
    mediator: FromDishka[BaseMediator],
    cookie_manager: CookieManager,
    response: Response,
    user_jwt_data: CurrentUserJWTData,
    refresh_token: Annotated[str | None, Cookie()] = None ,
) -> AccessTokenResponse:
    token_group, *_ = await mediator.handle_command(
        RefreshTokenCommand(
            refresh_token=refresh_token,
            user_jwt_data=user_jwt_data
        )
    )
    cookie_manager.set_refresh_token(response, token_group.refresh_token)

    return AccessTokenResponse(access_token=token_group.access_token)

