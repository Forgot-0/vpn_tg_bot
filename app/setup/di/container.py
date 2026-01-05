from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import AiogramProvider
from dishka.integrations.fastapi import FastapiProvider

from app.setup.di.providers import ApplicationProvider
from app.setup.di.registry import MediatorProvider


def create_container(*providers) -> AsyncContainer:
    return make_async_container(
        *providers,
        MediatorProvider(), ApplicationProvider(), AiogramProvider(), FastapiProvider(),
    )
