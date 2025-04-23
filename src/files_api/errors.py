

import pydantic
from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse


# fast api docs on middleware: https://fastapi.tiangolo.com/tutorial/middleware/
async def handle_broad_exceptions(request: Request, call_next) -> JSONResponse:
    """Handle any exception that goes unhandled by a more specific exception handler."""
    try:
        print("entered the middleware")
        return await call_next(request)
    except Exception as err:
        print("IN the middleware except statement")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal Server Error"},
        )
    

# fast api docs on error handlers: https://fastapi.tiangolo.com/tutorial/handling-errors/
async def handle_pydantic_validation_errors(request: Request, exc: pydantic.ValidationError) -> JSONResponse:
    errors = exc.errors()
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": [
                {
                    "msg": error["msg"],
                    "input": error["input"],
                    }
                for error in errors
            ]
        },
    )