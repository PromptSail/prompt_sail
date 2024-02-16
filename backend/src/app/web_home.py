from _datetime import datetime, timezone
from fastapi import Request

from .app import app


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
