from cryptography.fernet import Fernet
from dishka import AsyncContainer, Provider, Scope, provide
from motor.motor_asyncio import AsyncIOMotorClient

from app.application.services.jwt_manager import JWTManager
from app.application.services.role_hierarchy import RoleAccessControl
from app.configs.app import app_settings
from app.domain.repositories.payment import BasePaymentRepository
from app.domain.repositories.servers import BaseServerRepository
from app.domain.repositories.subscriptions import BaseSubscriptionRepository
from app.domain.repositories.users import BaseUserRepository
from app.domain.services.servers import SecureService
from app.domain.services.subscription import SubscriptionPricingService
from app.domain.values.servers import ApiType, ProtocolType, Region
from app.infrastructure.api_client.factory import ApiClientFactory
from app.infrastructure.api_client.x_ui.aclient import A3xUiApiClient
from app.infrastructure.builders_params.factory import ProtocolBuilderFactory
from app.infrastructure.builders_params.vless.x_ui.builder import Vless3XUIProtocolBuilder
from app.infrastructure.mediator.base import BaseMediator
from app.infrastructure.mediator.commands import CommandRegisty
from app.infrastructure.mediator.event import BaseEventBus, EventRegisty, MediatorEventBus
from app.infrastructure.mediator.mediator import DishkaMediator
from app.infrastructure.mediator.queries import QueryRegistry
from app.application.services.payment import BasePaymentService
from app.infrastructure.payments.test import TestPaymentService
from app.setup.di.init_payment import inti_yookass
from app.setup.di.init_repositories import (
    init_mongo_payment_repository,
    init_mongo_server_repository,
    init_mongo_subscription_repository,
    init_mongo_user_repository
)


class ApplicationProvider(Provider):
    role_access_control = provide(RoleAccessControl, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def jwt_manager(self) -> JWTManager:
        return JWTManager(
            jwt_secret=app_settings.JWT_SECRET_KEY,
            jwt_algorithm=app_settings.JWT_ALGORITHM,
            access_token_expire_minutes=app_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token_expire_days=app_settings.REFRESH_TOKEN_EXPIRE_DAYS,
        )

    @provide(scope=Scope.APP)
    def mongo_client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            app_settings.mongo_url,
            serverSelectionTimeoutMS=3000,
            uuidRepresentation='standard'
        )

    @provide(scope=Scope.APP)
    def user_reposiotry(self, client: AsyncIOMotorClient) -> BaseUserRepository:
        return init_mongo_user_repository(client)

    @provide(scope=Scope.APP)
    def subscription_repository(self, client: AsyncIOMotorClient) -> BaseSubscriptionRepository:
        return init_mongo_subscription_repository(client)

    @provide(scope=Scope.APP)
    def payment_repository(self, client: AsyncIOMotorClient) -> BasePaymentRepository:
        return init_mongo_payment_repository(client)

    @provide(scope=Scope.APP)
    def server_repository(self, client: AsyncIOMotorClient) -> BaseServerRepository:
        return init_mongo_server_repository(client)

    @provide(scope=Scope.APP)
    def secure_service(self) -> SecureService:
        return SecureService(Fernet(app_settings.SECRET))

    @provide(scope=Scope.APP)
    def subscription_service(self) -> SubscriptionPricingService:
        return SubscriptionPricingService(
            daily_rate=2,
            device_rate_multiplier=0.5,
            region_multipliers={
                Region("🇳🇱", "Нидерланды", "NL"): 1.0,
            },
            protocol_multipliers={
                ProtocolType.VLESS: 0.15
            }
        )

    @provide(scope=Scope.APP)
    def protocol_factory(self) -> ProtocolBuilderFactory:
        factory_builder = ProtocolBuilderFactory()
        factory_builder.register(ApiType.x_ui, ProtocolType.VLESS, Vless3XUIProtocolBuilder)
        return factory_builder

    @provide(scope=Scope.APP)
    def client_factory(self, protocol_factory: ProtocolBuilderFactory, secure: SecureService) -> ApiClientFactory:
        factory_client = ApiClientFactory()
        factory_client.register(ApiType.x_ui, A3xUiApiClient(builder_factory=protocol_factory, secure_service=secure))
        return factory_client

    @provide(scope=Scope.APP)
    def payment_service(self) -> BasePaymentService:
        # return inti_yookass()
        return TestPaymentService()

    @provide(scope=Scope.APP)
    def event_mediator(self, container: AsyncContainer, event_maps: EventRegisty) -> BaseEventBus:
        return MediatorEventBus(
            container=container,
            event_registy=event_maps
        )

    @provide(scope=Scope.APP)
    def mediator(
        self,
        container: AsyncContainer,
        command_registry: CommandRegisty,
        query_registry: QueryRegistry,
    ) -> BaseMediator:
        mediator = DishkaMediator(
            container=container,
            command_registy=command_registry,
            query_registy=query_registry,
        )

        return mediator