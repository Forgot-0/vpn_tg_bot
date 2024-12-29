from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from application.dto.subscription import SubscriptionDTO



class BuyBotton:
    text: str = "Купить VPN"
    callback_data: str = 'buy_vpn'



class TarifsMessage:
    _text = (
        "Приобретая подписку на VPN vless \\- Вы получаете 👇 \n"
        "└ 🚀 Высокую скорость и стабильность \n"
        "└ 👥 Поддержку в чате 24/7 \n"
        "└✅ Безлимитный трафик \n"
        "└ 🔕 Без рекламы \n"
        "└ ⛔️ Без автосписаний с карты \n"
        "\n"
        "Регионы 🌐 \n"
        "└ 🇳🇱 Нидерланды \n"
        "\n"
        "Одновременно использовать vpn может одно устройство \n"
    )

    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BuyBotton.text, callback_data=BuyBotton.callback_data)]
        ]
    )

    def build(self, subscriptions: list[SubscriptionDTO]):
        self._text += "\nТарифы👇 \n"
        for subscription in subscriptions:
            price_with_discount = subscription.price_with_discount
            self._text += (
                f"└ {subscription.name} \\- "
            )
            if price_with_discount:
                self._text += (
                    f"за ~{subscription.price}~ {price_with_discount} руб \n"
                )
            else:
                self._text += (
                    f"за {subscription.price} руб \n"
                )

        content = {"text": self._text}
        content["reply_markup"] = self._reply_markup
        content['parse_mode'] = "MarkdownV2"
        return content