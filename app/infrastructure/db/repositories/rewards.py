from dataclasses import dataclass
from typing import Any
from uuid import UUID

from domain.entities.reward import Reward, RewardUser
from domain.repositories.rewards import BaseRewardRepository, BaseRewardUserRepository
from infrastructure.db.convertors.rewards import (
    convert_reward_dict_to_entity,
    convert_reward_entity_to_dict,
    convert_reward_user_dict_to_entity,
    convert_reward_user_entity_to_dict
)
from infrastructure.db.repositories.base import BaseMongoDBRepository


@dataclass
class MongoRewardRepository(BaseRewardRepository, BaseMongoDBRepository):
    async def create(self, reward: Reward) -> None:
        document = convert_reward_entity_to_dict(reward)
        await self._collection.insert_one(document=document)

    async def get(self) -> list[Reward]:
        documents = await self._collection.find().to_list(length=None)
        if documents: return [convert_reward_dict_to_entity(document) for document in documents]

    async def get_by_id(self, id: UUID) -> Reward:
        document = await self._collection.find_one({'_id': id})
        if document: return convert_reward_dict_to_entity(document)

    async def get_by_conditions(self, filters: dict[str, Any]) -> Reward:
        document = await self._collection.find_one(
            filter=filters
        )
        if document: return convert_reward_dict_to_entity(document)


@dataclass
class MongoRewardUserRepository(BaseRewardUserRepository, BaseMongoDBRepository):
    async def create(self, reward_user: RewardUser):
        document = convert_reward_user_entity_to_dict(reward_user)
        await self._collection.insert_one(document=document)

    async def get_by_reward_user(self, reward_id: UUID, user_id: int) -> RewardUser:
        document = await self._collection.find_one(
            {
                'user_id': user_id,
                'reward_id': reward_id
            }
        )
        if document: return convert_reward_user_dict_to_entity(document)

    async def get_not_received_by_user(self, user_id: int) -> list[RewardUser]:
        documents = await self._collection.find(
            {'user_id': user_id, 'is_received': False}
        ).to_list(length=None)

        if documents: return [convert_reward_user_dict_to_entity(document) for document in documents]

    async def receive(self, reward_id: UUID, user_id: int) -> None:
        await self._collection.update_one(
            filter={
                'user_id': user_id,
                'reward_id': reward_id
            },
            update={"$set": {"is_received": True}}
        )