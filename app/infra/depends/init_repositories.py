
from motor.motor_asyncio import AsyncIOMotorClient

from infra.repositories.subscriptions.mongo.repository import MongoSubscriptionRepository
from infra.repositories.users.mongo.repository import MongoUserRepository



def init_mongo_language_repository(client: AsyncIOMotorClient):
    return dict(
        mongo_db_client=client,
        mongo_db_db_name='test',
        mongo_db_collection_name='languages'
    )

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
