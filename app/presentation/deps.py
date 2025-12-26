from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.application.dtos.users.jwt import UserJWTData
from app.application.queries.tokens.verify import VerifyTokenQuery
from app.application.services.role_hierarchy import RoleAccessControl
from app.domain.values.users import UserRole
from app.infrastructure.mediator.base import BaseMediator
from app.presentation.cookies import RefreshTokenCookieManager
from app.application.exception import ForbiddenException, UnauthorizedException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)



class UserJWTDataGetter:
    def __init__(self, role: UserRole | None=None) -> None:
        self.reqrequired_role = role

    @inject
    async def __call__(
        self,
        mediator: FromDishka[BaseMediator],
        role_access_control: FromDishka[RoleAccessControl],
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> UserJWTData:
        if token is None:
            raise UnauthorizedException()

        user_jwt_data: UserJWTData
        user_jwt_data = await mediator.handle_query(
            VerifyTokenQuery(token=token)
        )
        if self.reqrequired_role:
            if not role_access_control.can_action(
            UserRole(user_jwt_data.role), target_role=self.reqrequired_role
        ): raise ForbiddenException()

        return user_jwt_data


CurrentUserJWTData = Annotated[UserJWTData, Depends(UserJWTDataGetter())]
CurrentAdminJWTData = Annotated[UserJWTData, Depends(UserJWTDataGetter(UserRole.ADMIN))]


def get_refresh_token_manager() -> RefreshTokenCookieManager:
    return RefreshTokenCookieManager()

CookieManager = Annotated[RefreshTokenCookieManager, Depends(get_refresh_token_manager)]

