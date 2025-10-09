
from motor.motor_asyncio import AsyncIOMotorClient

from infrastructure.db.repositories.payment import PaymentRepository
from infrastructure.db.repositories.server import ServerRepository
from infrastructure.db.repositories.subscription import SubscriptionRepository
from infrastructure.db.repositories.user import UserRepository



def init_mongo_user_repository(client: AsyncIOMotorClient):
    return UserRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='users',
    )

def init_mongo_subscription_repository(client: AsyncIOMotorClient):
    return SubscriptionRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='subscriptions',
    )

def init_mongo_payment_repository(client: AsyncIOMotorClient):
    return PaymentRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='payments',
    )


def init_mongo_server_repository(client: AsyncIOMotorClient):
    return ServerRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='servers',
    )

# def init_mongo_discount_repository(client: AsyncIOMotorClient):
#     return MongoDiscountRepository(
#         mongo_db_client=client,
#         mongo_db_db_name='test',
#         mongo_db_collection_name='discounts',
#     )

# def init_mongo_discount_user_repository(client: AsyncIOMotorClient):
#     return MongoDiscountUserRepository(
#         mongo_db_client=client,
#         mongo_db_db_name='test',
#         mongo_db_collection_name='discount_users',
#     )

# def init_mongo_reward_repository(client: AsyncIOMotorClient):
#     return MongoRewardRepository(
#         mongo_db_client=client,
#         mongo_db_db_name='test',
#         mongo_db_collection_name='rewards',
#     )

# def init_mongo_reward_user_repository(client: AsyncIOMotorClient):
#     return MongoRewardUserRepository(
#         mongo_db_client=client,
#         mongo_db_db_name='test',
#         mongo_db_collection_name='reward_user',
#     )