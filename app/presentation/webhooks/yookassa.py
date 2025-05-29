from uuid import UUID
from fastapi import APIRouter, Request, Response

from application.commands.payment.paid import PaidPaymentCommand
from infrastructure.depends.init import get_mediator
from infrastructure.mediator.mediator import Mediator


router = APIRouter()


@router.post('/paid')
async def paid(requests: Request):
    data = (await requests.json())
    mediator: Mediator = get_mediator()

    await mediator.handle_command(
        PaidPaymentCommand(
            payment_id=UUID(hex=data['object']['id']),
        )
    )

    return Response()