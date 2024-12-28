from punq import Container

from application.commands.orders.create import CreateOrderCommand, CreateOrderCommandHandler
from application.commands.orders.paid import PayOrderCommand, PayOrderCommandHandler
from application.commands.rewards.receive import ReceiveRewardCommand, ReceiveRewardCommandHandler
from application.commands.servers.create import CreateServerCommand, CreateServerCommandHandler
from application.commands.servers.delete_not_active_user import (
    DeletNotActiveUserCommand,
    DeletNotActiveUserCommandHandler
)
from application.commands.subscription.create import CreateSubscriptionCommnad, CreateSubscriptionCommnadHandler
from application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from application.events.base import PublisherEventHandler

from application.events.rewards.buying_referral import BuyingReferralEventHandler
from application.events.rewards.new_referral import CheckNewRewardEventHandler
from application.events.servers.decrement_free import UpdateCurrentServerEventHandler
from application.events.users.referred import ReferredUserEventHandler
from application.mediator.mediator import Mediator
from application.mediator.event_mediator import EventMediator
from application.queries.order.get_by_user import GetByUserOrdersQuery, GetByUserOrdersQueryHandler
from application.queries.rewards.get_users import GetRewardsByUserQuery, GetRewardsByUserQueryHandler
from application.queries.subscriptions.get import GetListSubscriptionQuery, GetListSubscriptionQueryHandler
from domain.events.orders.paid import PaidOrderEvent
from domain.events.users.referred import ReferralAssignedEvent, ReferredUserEvent



def init_mediator(container: Container) -> Mediator:
    container.register(PublisherEventHandler)


    mediator = Mediator()

    container.register(EventMediator, instance=mediator)

    #User
    container.register(CreateUserCommandHandler)
    mediator.register_command(CreateUserCommand, [container.resolve(CreateUserCommandHandler)])

    container.register(ReferredUserEventHandler)
    mediator.register_event(ReferredUserEvent, [container.resolve(ReferredUserEventHandler)])

    #Server
    container.register(CreateServerCommandHandler)
    mediator.register_command(CreateServerCommand, [container.resolve(CreateServerCommandHandler)])

    container.register(DeletNotActiveUserCommandHandler)
    mediator.register_command(DeletNotActiveUserCommand, [container.resolve(DeletNotActiveUserCommandHandler)])

    container.register(UpdateCurrentServerEventHandler)

    #Subscription
    container.register(CreateSubscriptionCommnadHandler)
    mediator.register_command(CreateSubscriptionCommnad, [container.resolve(CreateSubscriptionCommnadHandler)])

    container.register(GetListSubscriptionQueryHandler)
    mediator.register_query(GetListSubscriptionQuery, container.resolve(GetListSubscriptionQueryHandler))

    #Order
    container.register(CreateOrderCommandHandler)
    mediator.register_command(CreateOrderCommand, [container.resolve(CreateOrderCommandHandler)])

    container.register(PayOrderCommandHandler)
    mediator.register_command(PayOrderCommand, [container.resolve(PayOrderCommandHandler)])

    container.register(GetByUserOrdersQueryHandler)
    mediator.register_query(GetByUserOrdersQuery, container.resolve(GetByUserOrdersQueryHandler))

    #Reward
    container.register(ReceiveRewardCommandHandler)
    mediator.register_command(ReceiveRewardCommand, [container.resolve(ReceiveRewardCommandHandler)])

    container.register(GetRewardsByUserQueryHandler)
    mediator.register_query(GetRewardsByUserQuery, [container.resolve(GetRewardsByUserQueryHandler)])

    container.register(CheckNewRewardEventHandler)
    mediator.register_event(ReferralAssignedEvent, [container.resolve(CheckNewRewardEventHandler)])

    container.register(BuyingReferralEventHandler)
    

    #Events
    mediator.register_event(PaidOrderEvent, [
        container.resolve(UpdateCurrentServerEventHandler),
        container.resolve(BuyingReferralEventHandler)
    ])



    return mediator
