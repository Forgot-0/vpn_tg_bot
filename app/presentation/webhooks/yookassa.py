from ipaddress import IPv4Address, IPv6Address, ip_address, ip_network

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Request, Response

from app.application.commands.payment.paid import PaidPaymentCommand
from app.application.exception import BadRequestException, ForbiddenException
from app.infrastructure.mediator.base import BaseMediator


router = APIRouter(tags=['webhook'], route_class=DishkaRoute)


ip_ranges_yookass = [
    ip_network("185.71.76.0/27"),
    ip_network("185.71.77.0/27"),
    ip_network("77.75.153.0/25"),
    ip_address("77.75.156.11"),
    ip_address("77.75.156.35"),
    ip_network("77.75.154.128/25"),
    ip_network("2a02:5180::/32")
]


def check_ip_in_ranges(client_ip: str) -> bool:
    ip = ip_address(client_ip)
    for network in ip_ranges_yookass:
        if isinstance(network, IPv4Address | IPv6Address):
            if ip == network:
                return True

        elif ip in network:
            return True

    return False


@router.post('/paid')
async def paid(request: Request, mediator: FromDishka[BaseMediator]) -> Response:
    x_forwarded_for = request.headers.get("X-Forwarded-For")

    if x_forwarded_for is None:
        raise BadRequestException()

    if not check_ip_in_ranges(x_forwarded_for.split(",")[0]):
        raise ForbiddenException()

    data = (await request.json())

    await mediator.handle_command(
        PaidPaymentCommand(
            payment_id=data['object']['id'],
        )
    )
    return Response()

