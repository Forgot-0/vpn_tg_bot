from uuid import uuid4

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.kafka import KafkaMessageBroker
from settings.config import Config



def create_message_broker(config: Config) -> BaseMessageBroker:
    return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.broker.url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.broker.url,
                group_id=f"{uuid4()}",
                metadata_max_age_ms=30000,
            ),
        )
