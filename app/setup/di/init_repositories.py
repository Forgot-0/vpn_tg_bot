from motor.motor_asyncio import AsyncIOMotorClient

from app.configs.app import app_settings
from app.domain.entities.price import PriceConfig
from app.infrastructure.db.repositories.payment import PaymentRepository
from app.infrastructure.db.repositories.price import PriceRepository
from app.infrastructure.db.repositories.server import ServerRepository
from app.infrastructure.db.repositories.subscription import SubscriptionRepository
from app.infrastructure.db.repositories.user import UserRepository


def init_mongo_user_repository(client: AsyncIOMotorClient):
    return UserRepository(
        mongo_db_client=client,
        mongo_db_db_name=app_settings.DATABASE_DB,
        mongo_db_collection_name='users',
    )

def init_mongo_subscription_repository(client: AsyncIOMotorClient):
    return SubscriptionRepository(
        mongo_db_client=client,
        mongo_db_db_name=app_settings.DATABASE_DB,
        mongo_db_collection_name='subscriptions',
    )

def init_mongo_payment_repository(client: AsyncIOMotorClient):
    return PaymentRepository(
        mongo_db_client=client,
        mongo_db_db_name=app_settings.DATABASE_DB,
        mongo_db_collection_name='payments',
    )


def init_mongo_server_repository(client: AsyncIOMotorClient):
    return ServerRepository(
        mongo_db_client=client,
        mongo_db_db_name=app_settings.DATABASE_DB,
        mongo_db_collection_name='servers',
    )

async def init_mongo_price_repository(
        client: AsyncIOMotorClient,
        cfg: PriceConfig
    ):
    return await PriceRepository.create(
        cfg=cfg,
        mongo_db_client=client,
        mongo_db_db_name=app_settings.DATABASE_DB,
        mongo_db_collection_name='price',
    )

# def init_mongo_discount_repository(client: AsyncIOMotorClient):
#     return MongoDiscountRepository(
#         mongo_db_client=client,
#         mongo_db_db_name=app_settings.DATABASE_DB,
#         mongo_db_collection_name='discounts',
#     )

# def init_mongo_discount_user_repository(client: AsyncIOMotorClient):
#     return MongoDiscountUserRepository(
#         mongo_db_client=client,
#         mongo_db_db_name=app_settings.DATABASE_DB,
#         mongo_db_collection_name='discount_users',
#     )

# def init_mongo_reward_repository(client: AsyncIOMotorClient):
#     return MongoRewardRepository(
#         mongo_db_client=client,
#         mongo_db_db_name=app_settings.DATABASE_DB,
#         mongo_db_collection_name='rewards',
#     )

# def init_mongo_reward_user_repository(client: AsyncIOMotorClient):
#     return MongoRewardUserRepository(
#         mongo_db_client=client,
#         mongo_db_db_name=app_settings.DATABASE_DB,
#         mongo_db_collection_name='reward_user',
#     )