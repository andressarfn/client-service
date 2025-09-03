import uuid
from logging import getLogger

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError

from interfaces.api.exceptions.handler import (
    custom_exception_handler, custom_http_exception_handler,
    custom_validation_exception_handler)
from src.infrastructure.config.settings import settings
from utils.trace_id import configure_trace_id

logger = getLogger(__name__)


async def lifespan(app: FastAPI):
    # Startup code can be added here
    yield
    # Shutdown code can be added here


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    root_path=settings.ROOT_PATH,
    docs_url="docs",
    openapi_url="/documentation",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_middleware(request: Request, call_next: callable):
    request_id = request.headers.get("X-Request-ID")
    trace_id = configure_trace_id(request)

    if not request_id:
        logger.debug("The x-request-id is missing. Creating generic one.")
        request_id = str(uuid.uuid4())

    with logger.contextualize(
        request_id=request_id, trace_id=trace_id, context="APP", route=request.url.path
    ):
        logger.info("Request start")

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id

        logger.info("Request end", status_code=response.status_code)

        return response


app.add_exception_handler(Exception, custom_exception_handler)
app.add_exception_handler(RequestValidationError, custom_validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
