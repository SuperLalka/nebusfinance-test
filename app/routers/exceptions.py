import datetime
import logging
from typing import Type

from fastapi import Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette import status

logger = logging.getLogger(__name__)


async def handler_for_request_validation_error(
    request: Request,
    exc: Type[ValidationError]
) -> JSONResponse:
    logger.info({"detail": exc.errors(), "body": exc.body})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "timestamp": str(datetime.datetime.now()),
                "detail": exc.errors(),
            }
        ),
    )


async def handler_for_response_validation_error(
    request: Request,
    exc: Type[ValidationError]
) -> JSONResponse:
    logger.error({"detail": exc.errors(), "body": exc.body})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "timestamp": str(datetime.datetime.now()),
                "detail": exc.errors(),
            }
        ),
    )


async def handler_for_http_exception(
    request: Request,
    exc: HTTPException
) -> JSONResponse:
    logger.debug({"detail": exc.detail})

    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "timestamp": str(datetime.datetime.now()),
                "detail": exc.detail,
            }
        ),
    )
