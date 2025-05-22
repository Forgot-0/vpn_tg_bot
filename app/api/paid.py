from uuid import UUID
from aiohttp import web

from application.commands.payment.paid import PaidOrderCommand
from infrastructure.depends.init import get_mediator
from infrastructure.mediator.mediator import Mediator


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