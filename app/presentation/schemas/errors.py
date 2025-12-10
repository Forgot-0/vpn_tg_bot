from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from uuid import UUID

import orjson
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse as _ORJSONResponse

from app.application.exception import ApplicationException



class ErrorDetail(BaseModel):
    code: str
    message: str
    detail: dict | list | None = None



ER = TypeVar("ER", bound=ErrorDetail) 


class ErrorResponse(BaseModel, Generic[ER]):
    error: ER
    status: int
    request_id: str
    timestamp: float


def additionally_serialize(obj: Any) -> Any:
    match obj:
        case Exception():
            text = obj.args[0] if len(obj.args) > 0 else "Unknown error"
            return f"{obj.__class__.__name__}: {text}"
        case UUID():
            return str(obj)
        case BaseModel():
            return obj.model_dump()
    return repr(obj)


class ORJSONResponse(_ORJSONResponse):
    def render(self, content: Any) -> bytes:
        return orjson.dumps(
            content,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
            default=additionally_serialize,
        )


    
