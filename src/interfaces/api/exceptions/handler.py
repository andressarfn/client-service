from logging import getLogger

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = getLogger(__name__)


async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception occurred at %s", request.url, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error", "error": str(exc)},
    )


async def custom_validation_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error("Validation error occurred at %s", request.url, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation Error", "errors": str(exc)},
    )


async def custom_http_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.error("HTTP error occurred at %s", request.url, exc_info=exc)
    return JSONResponse(
        status_code=(
            exc.status_code
            if hasattr(exc, "status_code")
            else status.HTTP_502_BAD_GATEWAY
        ),
        content={"message": "HTTP Error", "errors": str(exc)},
    )
