from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from punq import Container, Scope

from motor.motor_asyncio import AsyncIOMotorClient

from domain.repositories.discounts import BaseDiscountRepository, BaseDiscountUserRepository
from domain.repositories.payment import BasePaymentRepository
from domain.repositories.rewards import BaseRewardRepository, BaseRewardUserRepository
from domain.repositories.servers import BaseServerRepository
from domain.repositories.subscriptions import BaseSubscriptionRepository
from domain.repositories.users import BaseUserRepository
from domain.services.discounts import DiscountService
from domain.services.rewards import RewardService
# from infrastructure.depends.init_broker import create_message_broker
from domain.services.subscription import SubscriptionPricingService
from domain.values.servers import ApiType, ProtocolType, Region
from infrastructure.api_client.factory import ApiClientFactory
from infrastructure.api_client.x_ui.aclient import A3xUiApiClient
from infrastructure.builders_params.factory import ProtocolBuilderFactory
from infrastructure.builders_params.vless.x_ui.builder import Vless3XUIProtocolBuilder
from infrastructure.depends.init_mediator import init_mediator
from infrastructure.depends.init_payment import inti_yookass
from infrastructure.depends.init_repositories import (
    init_mongo_payment_repository,
    init_mongo_server_repository,
    init_mongo_subscription_repository,
    init_mongo_user_repository
)
# from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.mediator.mediator import Mediator
from infrastructure.payments.base import BasePaymentService
from configs.app import app_settings




def _init_container() -> Container:
    container = Container()


    # Broker
    # container.register(
    #     BaseMessageBroker,
    #     factory=lambda: create_message_broker(config=config),
    #     scope=Scope.singleton
    # )

    # MongoDB

    client: AsyncIOMotorClient = AsyncIOMotorClient(
            app_settings.mongo_url,
            serverSelectionTimeoutMS=3000,
            uuidRepresentation='standard'
        )

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
        BasePaymentRepository, 
        factory=lambda: init_mongo_payment_repository(client),
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
    container.register(
        SubscriptionPricingService,
        instance=SubscriptionPricingService(
            daily_rate=2,
            device_rate_multiplier=0.5,
            region_multipliers={
                Region("🇳🇱", "Нидерланды", "NL"): 1.0,
            },
            protocol_multipliers={
                ProtocolType.VLESS: 0.15
            }
        )
    )

    # BUILDER PROTOCOL
    factory_builder = ProtocolBuilderFactory()
    factory_builder.register(ApiType.x_ui, ProtocolType.VLESS, Vless3XUIProtocolBuilder)

    container.register(ProtocolBuilderFactory, instance=factory_builder)

    #API CLIENT
    factory_client = ApiClientFactory()
    factory_client.register(ApiType.x_ui, A3xUiApiClient(builder_factory=factory_builder))

    container.register(ApiClientFactory, instance=factory_client)

    # PAYMENT

    container.register(
        BasePaymentService,
        factory=lambda: inti_yookass(),
        scope=Scope.singleton
    )

    # Mediator
    container.register(
        Mediator,
        factory=lambda: init_mediator(container=container)
    )

    return container