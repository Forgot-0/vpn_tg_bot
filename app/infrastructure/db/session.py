from sqlalchemy import AsyncAdaptedQueuePool, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.configs.app import app_config



def create_engine() -> AsyncEngine:
    if app_config.ENVIRONMENT == "testing":
        pool_class = NullPool
        pool_size = 0
        max_overflow = 0
    else:
        pool_class = AsyncAdaptedQueuePool
        pool_size = 10
        max_overflow = 15

    return create_async_engine(
        str(app_config.postgres_url),
        pool_pre_ping=False,
        pool_size=pool_size,
        poolclass=pool_class,
        max_overflow=max_overflow,
        echo=app_config.SQL_ECHO,
        pool_recycle=3600,
        pool_timeout=30,
        future=True,
    )

def create_async_marker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )


