from uuid import UUID

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response

from app.application.commands.payment.paid import PaidPaymentCommand
from app.infrastructure.mediator.base import BaseMediator


router = APIRouter(tags=['webhook'], route_class=DishkaRoute)


@router.post('/paid')
async def paid(requests: Request, mediator: BaseMediator):
    data = (await requests.json())

    await mediator.handle_command(
        PaidPaymentCommand(
            payment_id=UUID(hex=data['object']['id']),
        )
    )
    return Response()

