from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from httpx import AsyncClient
from passlib.context import CryptContext
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.application.interfaces.auth import JWTManager
from app.application.interfaces.password import PasswordService
from app.application.interfaces.payments import PaymentGateway
from app.application.interfaces.servers import PanelClientFactory
from app.configs.app import app_config
from app.domain.repositories.payments import PaymentOrderRepository
from app.domain.repositories.servers import VPNServerRepository
from app.domain.repositories.subscription_drafts import SubscriptionDraftRepository
from app.domain.repositories.subscriptions import SubscriptionPlanRepository, SubscriptionRepository
from app.domain.repositories.uow import UnitOfWork
from app.domain.repositories.users import UserRepository
from app.infrastructure.db.repositories.payments import SQLAlchemyPaymentOrderRepository
from app.infrastructure.db.repositories.servers import SQLAlchemyVPNServerRepository
from app.infrastructure.db.repositories.subscription_drafts import SQLAlchemySubscriptionDraftRepository
from app.infrastructure.db.repositories.subscription_plans import SQLAlchemySubscriptionPlanRepository
from app.infrastructure.db.repositories.subscriptions import SQLAlchemySubscriptionRepository
from app.infrastructure.db.repositories.users import SQLAlchemyUserRepository
from app.infrastructure.db.session import create_async_marker, create_engine
from app.infrastructure.db.uow import SQLAlchemyUoW
from app.infrastructure.panels.xui.client import ThreeXUIClient
from app.infrastructure.payments.yookassa.gateway import YooKassaPaymentGateway
from app.infrastructure.services.jwt import IJWTService
from app.infrastructure.services.password import IPasswordService


class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_engine()
        yield engine
        await engine.dispose(close=True)

    @provide(scope=Scope.APP)
    def get_marker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_async_marker(engine=engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, marker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        async with marker() as session:
            yield session

    @provide(scope=Scope.APP)
    async def get_redis(self) -> Redis:
        return Redis.from_url(app_config.redis_url, max_connections=50, decode_responses=True)

    @provide(scope=Scope.REQUEST)
    def get_uow(self, session: AsyncSession) -> UnitOfWork:
        return SQLAlchemyUoW(session)

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> UserRepository:
        return SQLAlchemyUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_payment_repository(self, session: AsyncSession) -> PaymentOrderRepository:
        return SQLAlchemyPaymentOrderRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_server_repository(self, session: AsyncSession) -> VPNServerRepository:
        return SQLAlchemyVPNServerRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_subscription_draft_repository(
        self, session: AsyncSession,
    ) -> SubscriptionDraftRepository:
        return SQLAlchemySubscriptionDraftRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_subscription_repository(self, session: AsyncSession) -> SubscriptionRepository:
        return SQLAlchemySubscriptionRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_subscription_plan_repository(
        self, session: AsyncSession
    ) -> SubscriptionPlanRepository:
        return SQLAlchemySubscriptionPlanRepository(session)

    @provide(scope=Scope.APP)
    def get_payment_gateway(self) -> PaymentGateway:
        return YooKassaPaymentGateway()

    @provide(scope=Scope.APP)
    def get_password_service(self) -> PasswordService:
        return IPasswordService(
            pwd_context=CryptContext(schemes=["argon2"], deprecated="auto"),
        )

    @provide(scope=Scope.APP)
    def get_jwt_service(self) -> JWTManager:
        return IJWTService()

    @provide(scope=Scope.APP)
    async def get_http_client(self) -> AsyncIterable[AsyncClient]:
        async with AsyncClient(timeout=30.0) as client:
            yield client

    @provide(scope=Scope.APP)
    def get_panel_client_factory(self, http_client: AsyncClient) -> PanelClientFactory:
        factory = PanelClientFactory()
        factory.register(ThreeXUIClient(client=http_client))
        return factory
