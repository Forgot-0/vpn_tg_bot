

from dishka import AsyncContainer, make_async_container
from dishka.integrations.aiogram import AiogramProvider
from dishka.integrations.fastapi import FastapiProvider

from app.infrastructure.di.providers import ApplicationProvider
from app.infrastructure.di.registry import MediatorProvider


def create_container(*providers) -> AsyncContainer:
    return make_async_container(
        MediatorProvider(), ApplicationProvider(), AiogramProvider(), FastapiProvider()
    )