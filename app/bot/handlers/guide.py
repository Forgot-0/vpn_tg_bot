from aiogram import F, Router
from aiogram.types import Message

from bot.messages.guide import GuideMessage, GuideText, TypeSystemButtons
from bot.messages.menu import MenuTextButtons

router = Router()


@router.message(F.text==MenuTextButtons.GUIDE)
async def guide(message: Message):
    await message.delete()
    data = GuideMessage().build()
    await message.answer(**data)


@router.message(F.text==TypeSystemButtons.IOS)
async def get_guide_ios(message: Message):
    await message.delete()
    await message.answer(
        text=GuideText.DOWNLOAD_IOS,
        parse_mode='MarkdownV2',
        disable_web_page_preview=True
    )
    await message.answer_video(
        video=GuideText.VIDEO_IOS,
    )


@router.message(F.text==TypeSystemButtons.WINDOWS)
async def get_guide_windows(message: Message):
    await message.delete()
    await message.answer(
        text=GuideText.DOWNLOAD_WINDOWS,
        parse_mode='MarkdownV2',
        disable_web_page_preview=True
    )
    await message.answer(
        text=GuideText.ROUTE_NEKORAY_SETTING,
        parse_mode='MarkdownV2'
    )

    await message.answer_video(
        video=GuideText.VIDEO_WINDOWS,
    )

@router.message(F.text==TypeSystemButtons.LINUX)
async def get_guide_linux(message: Message):
    await message.delete()
    await message.answer(
        text=GuideText.DOWNLOAD_LINUX,
        parse_mode='MarkdownV2',
        disable_web_page_preview=True
    )
    await message.answer(
        text=GuideText.ROUTE_NEKORAY_SETTING,
        parse_mode='MarkdownV2'
    )


@router.message(F.text==TypeSystemButtons.ANDROID)
async def get_guide_android(message: Message):
    await message.delete()
    await message.answer(
        text=GuideText.DOWNLOAD_ANDROID,
        parse_mode='MarkdownV2',
        disable_web_page_preview=True
    )
    await message.answer_video(
        video=GuideText.VIDEO_ANDROID,
    )