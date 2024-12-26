from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.messages.base import BaseMessageBuilder


class ReferralMessage(BaseMessageBuilder):
    _text = (
        "╔═ 👑 РЕФЕРАЛЬНАЯ СИСТЕМА 👑 ═╗\n"
        "\n"
        "📊 ВАША СТАТИСТИКА:\n"
        "└─ 👥 Приглашено друзей: 0\n"
        "\n"
        "🌟 БОНУСНАЯ ПРОГРАММА:\n"
        "├─ 💰 +3% скидки за каждого друга\n"
        "├─ ⭐️ Максимальная скидка: 20%\n"
        "├─ 🎯 Каждые 5 друзей = 1 конфиг\n"
        "└─ 📦 Бонусный конфиг: 5 ГБ\n"
        "\n"
        "🔗 ВАША РЕФЕРАЛЬНАЯ ССЫЛКА:\n"
        "└─ "

    )
    _reply_markup = ()

    def build(self, user_id):
        url = f"https://t.me/forgot_vpn_bot?start={user_id}"
        self._text += url
        self._reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text='Пригласи друга и получи бонус',
                    switch_inline_query="🔒 Безопасный и быстрый VPN! Присоединяйся по моей ссылке: " + url
                )]
            ]
        )

        content = {
            "text": self.text,
            "reply_markup": self.reply_markup
        }

        return content
