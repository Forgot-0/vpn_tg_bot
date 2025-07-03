from punq import Container

from application.commands.servers.create import CreateServerCommand, CreateServerCommandHandler
from application.commands.subscriptions.renew import RenewSubscriptionCommand, RenewSubscriptionCommandHandler
from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from application.commands.payment.paid import PaidPaymentCommand, PaidPaymentCommandHandler
from application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from application.queries.subscription.get_by_id import GetByIdQuery, GetByIdQueryHandler
from application.queries.subscription.get_by_tgid import GetByTgIdQuery, GetByTgIdQueryHandler
from application.queries.subscription.get_config import GetConfigQuery, GetConfigQueryHandler
from domain.events.base import BaseEvent
from domain.events.paymens.paid import PaidPaymentEvent
from application.events.server.decrement_free import DecrementFreeServerEventHandler
from infrastructure.log.event_handler import LogHandlerEvent
from infrastructure.mediator.event_mediator import EventMediator
from infrastructure.mediator.mediator import Mediator


def init_mediator(container: Container) -> Mediator:
    mediator = Mediator()

    container.register(EventMediator, instance=mediator)

    container.register(LogHandlerEvent)
    mediator.register_event(BaseEvent, [container.resolve(LogHandlerEvent)])

    container.register(CreateUserCommandHandler)
    mediator.register_command(
        CreateUserCommand,
        [container.resolve(CreateUserCommandHandler)]
    )

    container.register(PaidPaymentCommandHandler)
    mediator.register_command(
        PaidPaymentCommand,
        [container.resolve(PaidPaymentCommandHandler)]
    )

    container.register(CreateSubscriptionCommandHandler)
    mediator.register_command(
        CreateSubscriptionCommand,
        [container.resolve(CreateSubscriptionCommandHandler)]
    )

    container.register(RenewSubscriptionCommandHandler)
    mediator.register_command(
        RenewSubscriptionCommand,
        [container.resolve(RenewSubscriptionCommandHandler)]
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
        PaidPaymentEvent,
        [container.resolve(DecrementFreeServerEventHandler)]
    )

    container.register(CreateServerCommandHandler)
    mediator.register_command(
        CreateServerCommand,
        [container.resolve(CreateServerCommandHandler)]
    )

    return mediator