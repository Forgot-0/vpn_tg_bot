from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import Request, Response


async def set_request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    request.state.request_id = uuid4()
    response = await call_next(request)
    return response
