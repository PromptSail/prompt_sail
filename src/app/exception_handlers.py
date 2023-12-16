from fastapi import Request
from fastapi.responses import JSONResponse

from projects.repositories import ProjectNotFoundException, SlugAlreadyExistsException
from seedwork.exceptions import NotFoundException

from .app import app, templates


@app.exception_handler(ProjectNotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    message = exc.message
    if request.__dict__["scope"]["state"].get("is_web", False):
        return templates.TemplateResponse(
            "404.html", {"request": request, "message": message}
        )

    return JSONResponse(
        status_code=404,
        content={"message": message},
    )


@app.exception_handler(SlugAlreadyExistsException)
async def slug_already_exists_exception_handler(
    request: Request, exc: SlugAlreadyExistsException
):
    message = exc.message
    if request.__dict__["scope"]["state"].get("is_web", False):
        return templates.TemplateResponse(
            "400.html", {"request": request, "message": message}
        )

    return JSONResponse(
        status_code=400,
        content={"message": message},
    )
