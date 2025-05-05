from punq import Container

from application.mediator.mediator import Mediator
from application.mediator.event_mediator import EventMediator
from domain.events.orders.paid import PaidOrderEvent
from domain.events.users.created import NewUserEvent
from domain.events.users.referred import ReferralAssignedEvent, ReferredUserEvent



def init_mediator(container: Container) -> Mediator:
    # container.register(PublisherEventHandler)


    mediator = Mediator()

    container.register(EventMediator, instance=mediator)


    return mediator