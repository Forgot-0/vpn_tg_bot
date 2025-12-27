from dishka import AsyncContainer

from app.configs.app import app_settings
from app.domain.entities.user import User
from app.domain.repositories.users import BaseUserRepository
from app.domain.values.users import UserRole



async def init_data(container: AsyncContainer):
    user_repository = await container.get(
        BaseUserRepository
    )

    user = await user_repository.get_by_telegram_id(app_settings.BOT_OWNER_ID)
    if user is None:
        user = User.create(
            telegram_id=app_settings.BOT_OWNER_ID,
            username="SUPER_ADMIN",
            fullname="SUPER_ADMIN",
        )

        user.role = UserRole.SUPER_ADMIN
        await user_repository.create(user)

