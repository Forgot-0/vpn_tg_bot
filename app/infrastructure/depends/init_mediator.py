from punq import Container

from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from application.commands.order.paid import PaidOrderCommand, PaidOrderCommandHandler
from application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from application.queries.subscription.get_by_id import GetByIdQuery, GetByIdQueryHandler
from application.queries.subscription.get_by_tgid import GetByTgIdQuery, GetByTgIdQueryHandler
from application.queries.subscription.get_config import GetConfigQuery, GetConfigQueryHandler
from domain.events.orders.paid import PaidOrderEvent
from application.events.server.deecrement_free import DecrementFreeServerEventHandler
from infrastructure.mediator.event_mediator import EventMediator
from infrastructure.mediator.mediator import Mediator


def init_mediator(container: Container) -> Mediator:
    mediator = Mediator()

    container.register(EventMediator, instance=mediator)

    container.register(CreateUserCommandHandler)
    mediator.register_command(
        CreateUserCommand,
        [container.resolve(CreateUserCommandHandler)]
    )

    container.register(PaidOrderCommandHandler)
    mediator.register_command(
        PaidOrderCommand,
        [container.resolve(PaidOrderCommandHandler)]
    )

    container.register(CreateSubscriptionCommandHandler)
    mediator.register_command(
        CreateSubscriptionCommand,
        [container.resolve(CreateSubscriptionCommandHandler)]
    )

    container.register(GetByTgIdQueryHandler)
    mediator.register_query(
        GetByTgIdQuery,
        container.resolve(GetByTgIdQueryHandler)
    )

    container.register(GetByIdQueryHandler)
    mediator.register_query(
        GetByIdQuery,
        container.resolve(GetByIdQueryHandler)
    )

    container.register(GetConfigQueryHandler)
    mediator.register_query(
        GetConfigQuery,
        container.resolve(GetConfigQueryHandler)
    )

    container.register(DecrementFreeServerEventHandler)
    mediator.register_event(
        PaidOrderEvent,
        [container.resolve(DecrementFreeServerEventHandler)]
    )

    return mediator