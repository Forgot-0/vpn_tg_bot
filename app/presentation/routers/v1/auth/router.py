from typing import Annotated
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Cookie, Response, status

from app.application.commands.auth.login import LoginTelegramUserCommand
from app.application.commands.auth.refresh import RefreshTokenCommand
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.deps import CookieManager
from app.presentation.routers.v1.auth.requests import LoginTelegram
from app.presentation.routers.v1.auth.response import AccessTokenResponse


router = APIRouter(route_class=DishkaRoute)




@router.post(
    "/login_by_tg",
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
    refresh_token: Annotated[str | None, Cookie()] = None ,
) -> AccessTokenResponse:
    token_group, *_ = await mediator.handle_command(
        RefreshTokenCommand(
            refresh_token=refresh_token,
        )
    )
    cookie_manager.set_refresh_token(response, token_group.refresh_token)

    return AccessTokenResponse(access_token=token_group.access_token)

