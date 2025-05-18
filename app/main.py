import logging.config

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError, ResponseValidationError

from app.config.logging import LOGGING
from app.config.settings import settings
from app.routers import exceptions
from app.routers.api import router as router_api

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

app = FastAPI(
    redoc_url="/documentation/redoc",
    docs_url="/documentation/docs",
    debug=settings.DEBUG,
)

app.include_router(router_api)

app.add_exception_handler(RequestValidationError, exceptions.handler_for_request_validation_error)
app.add_exception_handler(ResponseValidationError, exceptions.handler_for_response_validation_error)
app.add_exception_handler(HTTPException, exceptions.handler_for_http_exception)
