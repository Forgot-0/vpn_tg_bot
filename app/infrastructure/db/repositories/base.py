from abc import ABC
from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorClient



@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AsyncIOMotorClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

