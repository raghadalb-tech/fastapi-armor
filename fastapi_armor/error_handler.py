import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

JSON_MEDIA_TYPE = "application/json; charset=utf-8"


def add_exception_handlers(app: FastAPI, logger: logging.Logger) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            media_type=JSON_MEDIA_TYPE,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={"error": "Validation failed", "detail": exc.errors()},
            media_type=JSON_MEDIA_TYPE,
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception occurred", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"},
            media_type=JSON_MEDIA_TYPE,
        )
