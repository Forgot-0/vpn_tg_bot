from dataclasses import dataclass

from application.dto.rewards import RewardDTO
from application.queries.base import BaseQuery, BaseQueryHandler

from domain.services.rewards import RewardService



@dataclass(frozen=True)
class GetRewardsByUserQuery(BaseQuery):
    user_id: int


@dataclass(frozen=True)
class GetRewardsByUserQueryHandler(BaseQueryHandler[GetRewardsByUserQuery, list[RewardDTO]]):
    reward_service: RewardService

    async def handle(self, query: GetRewardsByUserQuery) -> list[RewardDTO]:
        rewards = await self.reward_service.get_rewerds_user(
            user_id=query.user_id
        )
        
        return [RewardDTO.from_entity(reward) for reward in rewards]