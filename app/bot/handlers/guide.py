from aiogram import F, Router
from aiogram.types import Message

from bot.keyboards.guide import TypeSystemButtons, type_system
from bot.keyboards.menu import MenuTextButtons
from bot.texts.guides import GuideText


router = Router()


@router.message(F.text==MenuTextButtons.GUIDE)
async def get_guide(message: Message):
    await message.answer(text="Выберите систему под которую нужно настроить `vpn`", reply_markup=type_system())


@router.message(F.text==TypeSystemButtons.IOS)
async def get_guide(message: Message):
    await message.answer(text=GuideText.DOWNLOAD_IOS, parse_mode='MarkdownV2', disable_web_page_preview=True)
    await message.answer_video(
        video=GuideText.VIDEO_IOS,
    )


@router.message(F.text==TypeSystemButtons.WINDOWS)
async def get_guide(message: Message):
    await message.answer(text=GuideText.DOWNLOAD_WINDOWS, parse_mode='MarkdownV2', disable_web_page_preview=True)
    await message.answer(text=GuideText.ROUTE_NEKORAY_SETTING, parse_mode='MarkdownV2')

    await message.answer_video(
        video=GuideText.VIDEO_WINDOWS,
    )

@router.message(F.text==TypeSystemButtons.LINUX)
async def get_guide(message: Message):
    await message.answer(text=GuideText.DOWNLOAD_LINUX, parse_mode='MarkdownV2', disable_web_page_preview=True)
    await message.answer(text=GuideText.ROUTE_NEKORAY_SETTING, parse_mode='MarkdownV2')


@router.message(F.text==TypeSystemButtons.ANDROID)
async def get_guide(message: Message):
    await message.answer(text=GuideText.DOWNLOAD_ANDROID, parse_mode='MarkdownV2', disable_web_page_preview=True)
    await message.answer_video(
        video=GuideText.VIDEO_ANDROID,
    )