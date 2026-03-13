import multiprocessing

from taskiq import AsyncBroker, InMemoryBroker
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend

from configs.app import app_settings

broker: AsyncBroker

is_worker_process = "worker" in multiprocessing.current_process().name.lower()


if app_settings.ENVIRONMENT == "testing" and not is_worker_process:
    broker = InMemoryBroker()
else:
    broker = ListQueueBroker(url=app_settings.redis_url)
    broker.with_result_backend(RedisAsyncResultBackend(app_settings.redis_url))

