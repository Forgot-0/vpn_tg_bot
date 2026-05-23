from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.base import BaseModelORM



ModelT = TypeVar("ModelT", bound=BaseModelORM)


class SQLAlchemyRepository(Generic[ModelT]):
    model_class: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
