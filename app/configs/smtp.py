from typing import TypedDict


class SMTPConfig(TypedDict, total=False):
    hostname: str | None
    port: int
    username: str | None
    password: str | None
    use_tls: bool

