
from motor.motor_asyncio import AsyncIOMotorClient

from infrastructure.db.repositories.discounts import MongoDiscountRepository, MongoDiscountUserRepository
from infrastructure.db.repositories.orders import MongoOrderRepository
from infrastructure.db.repositories.servers import MongoServerRepository
from infrastructure.db.repositories.subscription import MongoSubscriptionRepository
from infrastructure.db.repositories.users import MongoUserRepository



def init_mongo_user_repository(client: AsyncIOMotorClient):
    return MongoUserRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='users',
    )

def init_mongo_subscription_repository(client: AsyncIOMotorClient):
    return MongoSubscriptionRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='subscriptions',
    )

def init_mongo_order_repository(client: AsyncIOMotorClient):
    return MongoOrderRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='orders',
    )


def init_mongo_server_repository(client: AsyncIOMotorClient):
    return MongoServerRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='servers',
    )

def init_mong_discount_repository(client: AsyncIOMotorClient):
    return MongoDiscountRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='discounts',
    )

def init_mong_discount_user_repository(client: AsyncIOMotorClient):
    return MongoDiscountUserRepository(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='discount_users',
    )