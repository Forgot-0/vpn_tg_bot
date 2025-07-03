from json import JSONDecodeError, dumps, loads
from aiogram import Bot
from aiogram.types import FSInputFile

from configs.app import app_settings

class ImageManager:
    def __init__(self):
        self.images_fileId = {}
        self.images_paths = {
            "about": "about.jpg",
            "buy": "buy.jpg",
            "device_count": "device_count.jpg",
            "duration": "duration.jpg",
            "help": "help.jpg",
            "menu": "menu.jpg",
            "type_vpn": "type_vpn.jpg",
        }

    async def load_image_ids(self) -> dict[str, str]:
        try:
            with open("./bot/static/images_fileid.json", "r") as f:
                data = f.read()
                return loads(data) if data else {}
        except (JSONDecodeError, FileNotFoundError):
            return {}

    async def save_image_ids(self) -> None:
        with open('./bot/static/images_fileid.json', 'w') as f:
            f.write(dumps(self.images_fileId))

    async def init_photo(self, bot: Bot) -> None:
        self.images_fileId = await self.load_image_ids()

        if self.images_fileId and set(self.images_fileId.keys()) == set(self.images_paths.keys()):
            return

        for key, path in self.images_paths.items():
            file_path = f"./bot/static/{path}"
            print(file_path)
            resp = await bot.send_photo(app_settings.BOT_OWNER_ID, FSInputFile(file_path))
            self.images_fileId[key] = resp.photo[-1].file_id

        await self.save_image_ids()

    def get_image_id(self, key: str) -> str:
        return self.images_fileId.get(key, "")

photo_manager = ImageManager()
