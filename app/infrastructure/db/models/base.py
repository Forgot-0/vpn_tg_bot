from sqlalchemy.orm import DeclarativeBase, registry

mapper_registry = registry()


class BaseModelORM(DeclarativeBase):
    registry = mapper_registry
