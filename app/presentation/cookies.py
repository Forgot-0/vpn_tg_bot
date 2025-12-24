from dataclasses import dataclass
from typing import Literal

from fastapi import Response


@dataclass
class RefreshTokenCookieManager:
    COOKIE_NAME: str = "refresh_token"
    PATH: str = "/"
    SAMESITE: Literal["lax", "strict", "none"] = "none"
    HTTPONLY: bool = True
    SECURE: bool = True

    def set_refresh_token(self, response: Response, refresh_token: str) -> None:
        response.set_cookie(
            self.COOKIE_NAME,
            refresh_token,
            samesite=self.SAMESITE,
            httponly=self.HTTPONLY,
            secure=self.SECURE,
            path=self.PATH,
        )

    def delete_refresh_token(self, response: Response) -> None:
        response.delete_cookie(self.COOKIE_NAME, samesite=self.SAMESITE, path=self.PATH)

