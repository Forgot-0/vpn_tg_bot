from uuid import UUID
from fastapi import APIRouter, Depends, Request, Response

from application.commands.payment.paid import PaidPaymentCommand
from infrastructure.mediator.base import BaseMediator


router = APIRouter(tags=['webhook'])


@router.post('/paid')
async def paid(requests: Request, mediator: BaseMediator):
    data = (await requests.json())

    await mediator.handle_command(
        PaidPaymentCommand(
            payment_id=UUID(hex=data['object']['id']),
        )
    )
    return Response()