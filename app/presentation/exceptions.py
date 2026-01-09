import logging

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from app.domain.exception.base import DomainException
from app.domain.services.utils import now_utc
from app.presentation.schemas.errors import ErrorDetail, ErrorResponse, ORJSONResponse


logger = logging.getLogger(__name__)

def handle_domain_exeption(request: Request, exc: DomainException) -> ORJSONResponse:
    logger.error(
        "Domain exception",
        exc_info=exc,
        extra={"status": exc.status, "title": exc.message, "detail": exc.detail, "code": exc.code}
    )
    return ORJSONResponse(
        status_code=exc.status,
        content=ErrorResponse(
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
                detail=exc.detail
            ),
            status=exc.status,
            request_id=request.state.request_id.hex,
            timestamp=now_utc().timestamp()
        ),
    )

def handle_validation_exeption(request: Request, exc: RequestValidationError) -> ORJSONResponse:
    logger.error(
        "Validation exception",
        exc_info=exc,
        extra={"error": exc.errors()}
    )
    return ORJSONResponse(
        status_code=422,
        content=ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION",
                message="Validation exception",
                detail=jsonable_encoder(exc.errors()),
            ),
            status=422,
            request_id=request.state.request_id.hex,
            timestamp=now_utc().timestamp()
        ),
    )

def handle_uncown_exception(request: Request, exc: Exception) -> ORJSONResponse:
    logger.error(
        "Uncown exception",
        exc_info=exc,
        extra={"error": exc}
    )
    return ORJSONResponse(
        status_code=500,
        content=ErrorResponse(
            error=ErrorDetail(
                code="UNCOWN_EXCEPTION",
                message="Uncown exception",
            ),
            status=500,
            request_id=request.state.request_id.hex,
            timestamp=now_utc().timestamp()
        ),
    )
