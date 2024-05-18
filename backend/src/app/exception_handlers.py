from auth.repositories import UserAlreadyExistsException, UserNotFoundException
from fastapi import Request
from fastapi.responses import JSONResponse
from projects.repositories import ProjectNotFoundException, SlugAlreadyExistsException
from seedwork.exceptions import NotFoundException

from .app import app


@app.exception_handler(ProjectNotFoundException)
async def project_not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Exception handler for ProjectNotFoundException.

    :param request: The incoming request.
    :param exc: The ProjectNotFoundException instance.
    :return: A JSONResponse with a 404 status code and the exception message.
    """
    message = exc.message
    return JSONResponse(
        status_code=404,
        content={"message": message},
    )


@app.exception_handler(SlugAlreadyExistsException)
async def slug_already_exists_exception_handler(
    request: Request, exc: SlugAlreadyExistsException
):
    """
    Exception handler for SlugAlreadyExistsException.

    :param request: The incoming request.
    :param exc: The SlugAlreadyExistsException instance.
    :return: A JSONResponse with a 400 status code and the exception message.
    """
    message = exc.message
    return JSONResponse(
        status_code=400,
        content={"message": message},
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request: Request, exc: NotFoundException):
    """
    Exception handler for UserNotFoundException.

    :param request: The incoming request.
    :param exc: The UserNotFoundException instance.
    :return: A JSONResponse with a 404 status code and the exception message.
    """
    message = exc.message
    return JSONResponse(
        status_code=404,
        content={"message": message},
    )


@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_exception_handler(
    request: Request, exc: SlugAlreadyExistsException
):
    """
    Exception handler for UserAlreadyExistsException.

    :param request: The incoming request.
    :param exc: The UserAlreadyExistsException instance.
    :return: A JSONResponse with a 400 status code and the exception message.
    """
    message = exc.message
    return JSONResponse(
        status_code=400,
        content={"message": message},
    )
