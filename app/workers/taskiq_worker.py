from dishka.integrations.taskiq import TaskiqProvider, setup_dishka
from taskiq import TaskiqEvents, TaskiqScheduler, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisScheduleSource

from app.configs.app import app_settings
from app.infrastructure.message_brokers.base import BaseMessageBroker
from app.infrastructure.tasks.taskiq.init import broker
from app.setup.di.container import create_container

container = create_container(TaskiqProvider())

setup_dishka(container=container, broker=broker)

@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    message_broker = await container.get(BaseMessageBroker)
    await message_broker.start()


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    message_broker = await container.get(BaseMessageBroker)
    await message_broker.close()


if app_settings.ENVIRONMENT == "testing":
    sources = [LabelScheduleSource(broker=broker)]

else:
    redis_schedule_source = RedisScheduleSource(
        url=app_settings.queue_redis_url,
    )
    sources = [redis_schedule_source, LabelScheduleSource(broker=broker)]



scheduler = TaskiqScheduler(
    broker=broker,
    sources=sources, # type: ignore
)

