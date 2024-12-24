from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient

from application.mediator.mediator import Mediator
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from infrastructure.depends.init_broker import create_message_broker
from infrastructure.depends.init_mediator import init_mediator
from infrastructure.depends.init_repositories import (
    init_mongo_order_repository,
    init_mongo_server_repository,
    init_mongo_subscription_repository,
    init_mongo_user_repository
)
from infrastructure.depends.init_vpn import init_vpn_service
from infrastructure.depends.init_youkass_payment import inti_youkass
from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.payments.base import BasePaymentService
from infrastructure.vpn_service.base import BaseVpnService
from settings.config import Config




def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    # Broker
    container.register(
        BaseMessageBroker,
        factory=lambda: create_message_broker(config=config),
        scope=Scope.singleton
    )

    # MongoDB
    def create_mongodb_client():
        return AsyncIOMotorClient(
            config.db.url,
            serverSelectionTimeoutMS=3000,
            uuidRepresentation='standard'
        )

    container.register(
        AsyncIOMotorClient,
        factory=create_mongodb_client,
        scope=Scope.singleton
    )
    client = container.resolve(AsyncIOMotorClient)

    # Repositories
    container.register(
        BaseUserRepository, 
        factory=lambda: init_mongo_user_repository(client),
        scope=Scope.singleton
    )

    container.register(
        BaseSubscriptionRepository, 
        factory=lambda: init_mongo_subscription_repository(client),
        scope=Scope.singleton
    )

    container.register(
        BaseOrderRepository, 
        factory=lambda: init_mongo_order_repository(client),
        scope=Scope.singleton
    )

    container.register(
        BaseServerRepository, 
        factory=lambda: init_mongo_server_repository(client),
        scope=Scope.singleton
    )
    

    #VPN SERVICE
    container.register(
        BaseVpnService,
        factory=lambda: init_vpn_service(config),
        scope=Scope.singleton
    )


    # Bot aiogram
    container.register(
        Bot,
        factory=lambda: Bot(
            token=config.bot.token,
            default=DefaultBotProperties(parse_mode='HTML')
        ),
        scope=Scope.singleton
    )

    container.register(
        Dispatcher,
        factory=lambda: Dispatcher(storage=MemoryStorage()),
        scope=Scope.singleton
    )

    # PAYMENT

    container.register(
        BasePaymentService,
        factory=lambda: inti_youkass(config=config),
        scope=Scope.singleton
    )

    # Mediator
    container.register(
        Mediator,
        factory=lambda: init_mediator(container=container)
    )

    return container
