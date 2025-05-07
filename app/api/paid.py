from uuid import UUID
from aiohttp import web

from application.commands.order.paid import PaidOrderCommand
from application.mediator.mediator import Mediator
from infrastructure.depends.init import get_mediator


router = web.RouteTableDef()


@router.post('/paid')
async def paid(requests: web.Request):
    data = (await requests.json())
    mediator: Mediator = get_mediator()

    await mediator.handle_command(
        PaidOrderCommand(
            payment_id=UUID(hex=data['object']['id']),
        )
    )

    return web.Response()