from _datetime import datetime, timezone
from fastapi import Request

from .app import app


@app.get("/healthcheck")
async def healthcheck(request: Request):
    """
    API endpoint to information about the API's health status.

    :param request: The incoming request.
    """
    return {"status": "OK", "datetime": datetime.now(tz=timezone.utc)}


@app.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def home_page(request: Request):
    """
    API route for the all unsupported traffic.

    :param request: The incoming request.
    :return: A dictionary containing the status and current datetime.
    """
    return {"status": "OK", "datetime": datetime.now(tz=timezone.utc)}
