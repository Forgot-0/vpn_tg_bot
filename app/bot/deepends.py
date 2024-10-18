from punq import Container

from infra.depends.init import init_container
from infra.repositories.users.base import BaseUserRepository


async def create_indexes() -> None:
    container: Container = init_container()
    user_repo: BaseUserRepository = container.resolve(BaseUserRepository)
    await user_repo.create_indexes()