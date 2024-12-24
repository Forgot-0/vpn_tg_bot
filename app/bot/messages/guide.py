from aiogram.types import ReplyKeyboardMarkup,  KeyboardButton

from bot.messages.base import BaseMessageBuilder
from bot.messages.menu import BackMainMenu




class TypeSystemButtons:
    IOS = "🍏 Mac OS/IOS"
    WINDOWS = "🖥 Windows"
    LINUX = "💻 Linux"
    ANDROID = "🤖 Android"


class GuideMessage(BaseMessageBuilder):
    _text= "Выберите систему под которую нужно настроить `vpn`"
    _reply_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=TypeSystemButtons.IOS), KeyboardButton(text=TypeSystemButtons.WINDOWS)],
            [KeyboardButton(text=TypeSystemButtons.ANDROID), KeyboardButton(text=TypeSystemButtons.LINUX)],
            [KeyboardButton(text=BackMainMenu.BACK)]
        ]
    )


class GuideText:
    DOWNLOAD_IOS: str = (
        "Установка vpn на IOS и Mac проходит одинаково для этого скачиваем из App Store приложение" 
        "[FoXray](https://apps.apple.com/app/id6448898396)"
    )
    VIDEO_IOS: str = 'BAACAgIAAxkBAAICr2cP480AAaNa9exfr4F4CudJtAzsJQACJVoAAj8rgUhroyC-o9ySDDYE'

    DOWNLOAD_WINDOWS: str = (
        "Установка nekoray на Windows скачиваем zip"
    "[nekoray](https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-windows64.zip)"
    )
    VIDEO_WINDOWS: str = 'BAACAgIAAxkBAAIC9GcP7tG9hvT6PTWCOjdbrZlpRAOfAAK8YAACXX6BSLw113YYrOJnNgQ'

    DOWNLOAD_LINUX: str = (
        "Установка nekoray на Linux заходим на github"
        "[nekoray](https://github.com/MatsuriDayo/nekoray/releases) и скачивайте файл под свою систему"
    )

    DOWNLOAD_ANDROID = (
        "Установите v2rayNG на свой телефон"
        "[v2rayNG](https://play.google.com/store/apps/details?id=com.v2ray.ang)"
    )
    VIDEO_ANDROID: str = 'BAACAgIAAxkBAAICbWcP4yJqSPs00s1yRKIltoDTzxqIAAIoYAACXX6BSITrtGMXiIQbNgQ'

    ROUTE_NEKORAY_SETTING: str = '`{"rules": [{"domain_suffix": [".ru"], "outbound": "direct"}]}`'