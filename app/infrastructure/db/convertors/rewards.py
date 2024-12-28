from typing import Any

from domain.entities.reward import Reward, RewardUser
from infrastructure.db.convertors.subscriptions import (
    convert_subscription_dict_to_entity,
    convert_subscription_entity_to_dict
)


def convert_reward_dict_to_entity(document: dict[str, Any]) -> Reward:
    return Reward(
        id=document['_id'],
        name=document['name'],
        description=document['description'],
        conditions=document['conditions'],
        present=convert_subscription_dict_to_entity(document['present']),
    )

def convert_reward_entity_to_dict(reward: Reward) -> dict[str, Any]:
    return {
        '_id': reward.id,
        'name': reward.name,
        'description': reward.description,
        'conditions': reward.conditions,
        'present': convert_subscription_entity_to_dict(reward.present),
    }

def convert_reward_user_entity_to_dict(reward_user: RewardUser) -> dict[str, Any]:
    return {
        'user_id': reward_user.user_id,
        'reward_id': reward_user.reward_id,
        'is_received': reward_user.is_received
    }

def convert_reward_user_dict_to_entity(document: dict[str, Any]) -> RewardUser:
    return RewardUser(
        user_id=document['user_id'],
        reward_id=document['reward_id'],
        is_received=document['is_received']
    )