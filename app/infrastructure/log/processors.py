import logging
from collections.abc import Callable
from typing import Any
from uuid import UUID

import orjson
import structlog

from app.domain.values.base import BaseValueObject

logger = logging.getLogger(__name__)

ProcessorType = Callable[
    [
        structlog.types.WrappedLogger,
        str,
        structlog.types.EventDict,
    ],
    str | bytes,
]


def additionally_serialize(obj: object) -> Any:
    if isinstance(obj, UUID):
        return str(obj)
    if isinstance(obj, BaseValueObject):
        return obj.as_generic_type()

    logger.warning("Not serializable: %s", type(obj), extra={"obj": repr(obj)})
    return repr(obj)


def serialize_to_json(data: Any, default: Any) -> str:
    return orjson.dumps(data, default=additionally_serialize).decode()


def get_render_processor(
    render_json_logs: bool = False,
    serializer: Callable[..., str | bytes] = serialize_to_json,
    colors: bool = True,
) -> ProcessorType:
    if render_json_logs:
        return structlog.processors.JSONRenderer(serializer=serializer)
    return structlog.dev.ConsoleRenderer(colors=colors)