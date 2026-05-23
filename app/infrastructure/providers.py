from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide, provide_all
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession, async_sessionmaker

from app.configs.app import app_config
from app.infrastructure.db.repositories.servers import SQLAlchemyVPNServerRepository
from app.infrastructure.db.repositories.subscriptions import (
    SQLAlchemySubscriptionPlanRepository,
    SQLAlchemySubscriptionRepository
)
from app.infrastructure.db.repositories.users import SQLAlchemyUserRepository
from app.infrastructure.db.session import create_async_marker, create_engine



class InfrastructureProvider(Provider):
    scope = Scope.APP


    @provide(scope=Scope.APP)
    async def get_engine(self) -> AsyncIterable[AsyncEngine]:
        engine = create_engine()
        yield engine
        await engine.dispose(close=True)

    @provide(scope=Scope.APP)
    async def get_marker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
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

    repositories = provide_all(
        SQLAlchemyVPNServerRepository,
        SQLAlchemySubscriptionRepository,
        SQLAlchemySubscriptionPlanRepository,
        SQLAlchemyUserRepository
    )
