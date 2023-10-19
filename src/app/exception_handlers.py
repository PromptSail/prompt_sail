from fastapi import Request
from fastapi.responses import JSONResponse

from projects.repositories import ProjectNotFoundException
from seedwork.exceptions import NotFoundException

from .app import app, templates


@app.exception_handler(ProjectNotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    message = exc.message
    if request.state.is_web:
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": message}
        )

    return JSONResponse(
        status_code=404,
        content={"message": message},
    )
