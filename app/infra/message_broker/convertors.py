from dataclasses import asdict
from typing import Any
import orjson

from domain.events.base import BaseEvent


def convert_event_to_broker_message(event: BaseEvent) -> bytes:
    return orjson.dumps(event)


def convert_event_to_json(event: BaseEvent) -> dict[str, Any]:
    return asdict(event)