from punq import Container

from application.commands.subscriptions.paid import PaidSubscriptionCommand, PaidSubscriptionCommandHandler
from application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from application.events.base import PublisherEventHandler

from application.events.subscription.paid import PaidSubscriptionEventHandler
from application.mediator.mediator import Mediator
from application.mediator.event_mediator import EventMediator
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

    container.register(PaidSubscriptionEventHandler)
    mediator.register_event(
        PaidSubscriptionEvent,
        [
            container.resolve(PaidSubscriptionEventHandler),
            PublisherEventHandler(
                message_broker=container.resolve(BaseMessageBroker),
                broker_topic='subscription'
            )
            
        ]
    )
    return mediator
