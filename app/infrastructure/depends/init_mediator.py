from punq import Container

from application.mediator.mediator import Mediator
from application.mediator.event_mediator import EventMediator

from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from application.commands.order.paid import PaidOrderCommand, PaidOrderCommandHandler
from application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from application.queries.subscription.get_by_tgid import GetByTgIdQuery, GetByTgIdQueryHandler
from domain.events.orders.paid import PaidOrderEvent
from application.events.server.deecrement_free import DecrementFreeServerEventHandler


def init_mediator(container: Container) -> Mediator:
    mediator = Mediator()

    container.register(EventMediator, instance=mediator)

    mediator.register_command(
        CreateUserCommand,
        [container.resolve(CreateUserCommandHandler)]
    )
    mediator.register_command(
        PaidOrderCommand,
        [container.resolve(PaidOrderCommandHandler)]
    )
    mediator.register_command(
        CreateSubscriptionCommand,
        [container.resolve(CreateSubscriptionCommandHandler)]
    )

    mediator.register_query(
        GetByTgIdQuery,
        container.resolve(GetByTgIdQueryHandler)
    )

    mediator.register_event(
        PaidOrderEvent,
        [container.resolve(DecrementFreeServerEventHandler)]
    )

    return mediator