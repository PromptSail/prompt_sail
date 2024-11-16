from _datetime import datetime, timezone
from fastapi import Request

from .app import app


@app.get("/healthcheck")
async def healthcheck(request: Request):
    """
    Check the API's health status.

    This endpoint provides basic health check information about the API,
    including its current status and timestamp.

    Parameters:
    - **request**: The incoming request object

    Returns:
    - A dictionary containing:
      - status: Current API status ("OK")
      - datetime: Current timestamp in UTC
    """
    return {"status": "OK", "datetime": datetime.now(tz=timezone.utc)}


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def home_page(request: Request):
    """
    Handle unsupported traffic routes.

    This endpoint serves as a catch-all route for any requests that don't match
    other defined endpoints. It returns a basic response indicating the API is functioning.

    Parameters:
    - **request**: The incoming request object

    Returns:
    - A dictionary containing:
      - status: Current API status ("OK")
      - datetime: Current timestamp in UTC
    """
    return {"status": "OK", "datetime": datetime.now(tz=timezone.utc)}
