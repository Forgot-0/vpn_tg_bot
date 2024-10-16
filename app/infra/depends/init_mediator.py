from punq import Container

from application.commands.servers.create import CreateServerCommand, CreateServerCommandHandler
from application.commands.servers.delete_not_active_user import (
    DeletNotActiveUserCommand, 
    DeletNotActiveUserCommandHandler
)
from application.commands.subscriptions.paid import PaidSubscriptionCommand, PaidSubscriptionCommandHandler
from application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from application.events.base import PublisherEventHandler

from application.events.servers.decrement_free import UpdateCurrentServerEventHandler
from application.events.subscriptions.paid import PaidSubscriptionEventHandler
from application.mediator.mediator import Mediator
from application.mediator.event_mediator import EventMediator
from application.queries.subscriptions.get_active_subs import GetAllActiveSubsQuery, GetAllActiveSubsQueryHandler
from domain.events.subscriptions.paid import PaidSubscriptionEvent
from infra.message_broker.base import BaseMessageBroker



def init_mediator(container: Container) -> Mediator:
    container.register(PublisherEventHandler)


    mediator = Mediator()

    container.register(EventMediator, instance=mediator)


    container.register(CreateUserCommandHandler)
    mediator.register_command(CreateUserCommand, [container.resolve(CreateUserCommandHandler)])

    container.register(CreateSubscriptionCommandHandler)
    mediator.register_command(CreateSubscriptionCommand, [container.resolve(CreateSubscriptionCommandHandler)])

    container.register(PaidSubscriptionCommandHandler)
    mediator.register_command(PaidSubscriptionCommand, [container.resolve(PaidSubscriptionCommandHandler)])

    container.register(GetAllActiveSubsQueryHandler)
    mediator.register_query(GetAllActiveSubsQuery, container.resolve(GetAllActiveSubsQueryHandler))

    container.register(PaidSubscriptionEventHandler)
    container.register(UpdateCurrentServerEventHandler)
    mediator.register_event(
        PaidSubscriptionEvent,
        [
            container.resolve(PaidSubscriptionEventHandler),
            container.resolve(UpdateCurrentServerEventHandler),
            PublisherEventHandler(
                message_broker=container.resolve(BaseMessageBroker),
                broker_topic='subscription'
            ),
        ]
    )


    container.register(CreateServerCommandHandler)
    mediator.register_command(CreateServerCommand, [container.resolve(CreateServerCommandHandler)])

    container.register(DeletNotActiveUserCommandHandler)
    mediator.register_command(DeletNotActiveUserCommand, [container.resolve(DeletNotActiveUserCommandHandler)])
    return mediator
