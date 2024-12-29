from uuid import UUID
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from application.dto.rewards import RewardDTO
from application.dto.user import UserDTO
from bot.messages.base import BaseMessageBuilder


class ReceiveRewardCallback(CallbackData, prefix="receive_reward"):
    reward_id: UUID



class RewardMessage(BaseMessageBuilder):
    _text = ""
    _reply_markup = ...

    def build(self, user: UserDTO, rewards: list[RewardDTO] | None):
        url = f"https://t.me/forgot_vpn_bot?start={user.id}"
        self._text = (
            "╔═ 👑 БОНУСНАЯ СИСТЕМА 👑 ═╗\n"
            "\n"
            "📊 ВАША СТАТИСТИКА:\n"
            f"└─ 👥 Приглашено друзей: {user.referrals_count}\n"
            "\n"
            "🌟 БОНУСНАЯ ПРОГРАММА:\n"
            "├─ 🎯 За каждые 10 друзей = подписка на 7*кол-во десятков приглашенных)\n"
            "└─ 📦 Так же за покупку своего реферала вы получите подписку с длительностью 10% от его\n"
            "\n"
            "🔗 ВАША РЕФЕРАЛЬНАЯ ССЫЛКА:\n"
            f"└─ {url}\n"
        )

        inline_keyboard=InlineKeyboardBuilder()
        inline_keyboard.add(
            InlineKeyboardButton(
                text='Пригласи друга и получи бонус',
                switch_inline_query="🔒 Безопасный и быстрый VPN! Присоединяйся по моей ссылке: " + url
            )
        )

        if rewards is None:
            rewards = list()

        for reward in rewards:
            # self._text += (

            # )
            inline_keyboard.add(
                InlineKeyboardButton(
                    text=f"{reward.name}",
                    callback_data=ReceiveRewardCallback(reward_id=reward.id).pack()
                )
            )

        self._reply_markup = inline_keyboard.as_markup()

        content = {
            "text": self._text,
            "reply_markup": self._reply_markup
        }

        return content
