from aiohttp import web

from application.commands.subscriptions.paid import PaidSubscriptionCommand
from application.mediator.mediator import Mediator
from infra.depends.init import get_mediator


router = web.RouteTableDef()


@router.post('/paid')
async def paid(requests: web.Request):
    data = (await requests.json())
    mediator: Mediator = get_mediator()

    await mediator.handle_command(
        PaidSubscriptionCommand(
            tg_id=int(data['object']['metadata']['tg_id']),
            payment_id=data['object']['id'],
            subscription_id=data['object']['metadata']['subscription_id']
        )
    )
