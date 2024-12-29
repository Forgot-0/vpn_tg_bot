from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from application.commands.rewards.receive import ReceiveRewardCommand
from application.mediator.mediator import Mediator
from application.queries.rewards.get_users import GetRewardsByUserQuery
from application.queries.users.get import GetByUserIdQuery
from bot.messages.menu import MenuTextButtons
from bot.messages.reward import ReceiveRewardCallback, RewardMessage


router = Router()


@router.message(F.text==MenuTextButtons.REWARD)
async def reward_message(message: Message, mediator: Mediator):
    rewards = await mediator.handle_query(
        GetRewardsByUserQuery(
            user_id=message.from_user.id
        )
    )
    user = await mediator.handle_query(
        GetByUserIdQuery(
            user_id=message.from_user.id
        )
    )
    data = RewardMessage().build(user=user, rewards=rewards)
    await message.answer(**data)




@router.callback_query(ReceiveRewardCallback.filter())
async def receive_reward(callback_query: CallbackQuery, callback_data: ReceiveRewardCallback, mediator: Mediator):

    await mediator.handle_command(
        ReceiveRewardCommand(
            user_id=callback_query.from_user.id,
            reward_id=callback_data.reward_id
        )
    )