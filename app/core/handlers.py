from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    NotFoundError,
    ConflictError,
    DatabaseError,
    InternalServerError,
)


async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


async def database_handler(request: Request, exc: DatabaseError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error"},
    )


async def internal_handler(request: Request, exc: InternalServerError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )