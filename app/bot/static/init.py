from json import JSONDecodeError, dump, load
from aiogram import Bot
from aiogram.types import FSInputFile

from configs.app import app_settings

images_fileId = {}

images_paths = {
    "about": "about.jpg",
    "buy": "buy.jpg",
    "device_count": "device_count.jpg",
    "duration": "duration.jpg",
    "help": "help.jpg",
    "menu": "menu.jpg",
    "type_vpn": "type_vpn.jpg",
}

async def init_photo(bot: Bot) -> None:
    try:
        with open("images_fileid.json", "rb") as f:
            data: dict[str, str] = load(f)
    except (JSONDecodeError, FileNotFoundError):
        data = {}

    if data and data.keys() == images_paths.keys(): return

    for key, path in images_paths.items():
        resp = await bot.send_photo(app_settings.BOT_OWNER_ID, FSInputFile(path))
        images_fileId[key] = resp.photo[-1].file_id

    with open('images_fileid.json', "w") as f:
        dump(images_fileId, f)

def get_image_id(key: str) -> str:
    return images_fileId.get(key, "")
