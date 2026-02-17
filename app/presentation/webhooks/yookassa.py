from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response

from app.application.commands.payment.paid import PaidPaymentCommand
from app.infrastructure.mediator.base import BaseMediator


router = APIRouter(tags=['webhook'], route_class=DishkaRoute)


@router.post('/paid')
async def paid(request: Request, mediator: FromDishka[BaseMediator]) -> Response:
    await mediator.handle_command(
        PaidPaymentCommand(
            playload=await request.json(),
            headers=request.headers
        )
    )
    return Response()

