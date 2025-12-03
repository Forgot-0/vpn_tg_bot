from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.tokens.verify import VerifyTokenQuery
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.cookies import RefreshTokenCookieManager



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)



class UserJWTDataGetter:
    @inject
    async def __call__(
        self,
        mediator: FromDishka[BaseMediator],
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserJWTData:
        if token is None:
            raise

        user_jwt_data: UserJWTData
        user_jwt_data = await mediator.handle_query(
            VerifyTokenQuery(token=token)
        )
        return user_jwt_data


CurrentUserJWTData = Annotated[UserJWTData, Depends(UserJWTDataGetter())]

def get_refresh_token_manager() -> RefreshTokenCookieManager:
    return RefreshTokenCookieManager()

CookieManager = Annotated[RefreshTokenCookieManager, Depends(get_refresh_token_manager)]
