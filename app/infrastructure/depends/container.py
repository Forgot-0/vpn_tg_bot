from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient

from application.mediator.mediator import Mediator
from domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository
from domain.repositories.orders import BaseOrderRepository
from domain.repositories.rewards import BaseRewardRepository, BaseRewardUserRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.services.discounts import DiscountService
from domain.services.rewards import RewardService
# from infrastructure.depends.init_broker import create_message_broker
from domain.values.servers import ApiType, ProtocolType
from infrastructure.api_client.factory import ApiClientFactory
from infrastructure.api_client.x_ui.aclient import A3xUiApiClient
from infrastructure.builders_params.factory import ProtocolBuilderFactory
from infrastructure.builders_params.vless.x_ui.builder import Vless3XUIProtocolBuilder
from infrastructure.depends.init_mediator import init_mediator
from infrastructure.depends.init_payment import inti_yookass
from infrastructure.depends.init_repositories import (
    init_mongo_order_repository,
    init_mongo_server_repository,
    init_mongo_subscription_repository,
    init_mongo_user_repository
)
# from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.payments.base import BasePaymentService
from settings.config import Config




def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    # Broker
    # container.register(
    #     BaseMessageBroker,
    #     factory=lambda: create_message_broker(config=config),
    #     scope=Scope.singleton
    # )

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
    client: AsyncIOMotorClient = container.resolve(AsyncIOMotorClient)

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

    # container.register(
    #     BaseDiscountRepository, 
    #     factory=lambda: init_mongo_discount_repository(client),
    #     scope=Scope.singleton
    # )

    # container.register(
    #     BaseDiscountUserRepository, 
    #     factory=lambda: init_mongo_discount_user_repository(client),
    #     scope=Scope.singleton
    # )

    # container.register(
    #     BaseRewardRepository, 
    #     factory=lambda: init_mongo_reward_repository(client),
    #     scope=Scope.singleton
    # )

    # container.register(
    #     BaseRewardUserRepository, 
    #     factory=lambda: init_mongo_reward_user_repository(client),
    #     scope=Scope.singleton
    # )

    # SERVICES
    container.register(DiscountService, scope=Scope.singleton)
    container.register(RewardService, scope=Scope.singleton)

    # BUILDER PROTOCOL
    factory_builder = ProtocolBuilderFactory()
    factory_builder.register(ApiType("3X-UI"), ProtocolType("VLESS"), Vless3XUIProtocolBuilder)

    #API CLIENT
    factory_client = ApiClientFactory()
    factory_client.register(ApiType("3X-UI"), A3xUiApiClient(builder_factory=factory_builder))

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
        factory=lambda: inti_yookass(config=config),
        scope=Scope.singleton
    )

    # Mediator
    container.register(
        Mediator,
        factory=lambda: init_mediator(container=container)
    )

    return container