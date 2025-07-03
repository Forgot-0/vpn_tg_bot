from uuid import UUID
from fastapi import APIRouter, Depends, Request, Response

from application.commands.payment.paid import PaidPaymentCommand
from infrastructure.depends.init import get_mediator
from infrastructure.mediator.mediator import Mediator


router = APIRouter(tags=['webhook'])


@router.post('/paid')
async def paid(requests: Request, mediator: Mediator=Depends(get_mediator)):
    data = (await requests.json())

    await mediator.handle_command(
        PaidPaymentCommand(
            payment_id=UUID(hex=data['object']['id']),
        )
    )
    return Response()