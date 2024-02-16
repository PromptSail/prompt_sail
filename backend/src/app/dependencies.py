from fastapi import Request
from lato import Application, TransactionContext


async def get_application(request: Request) -> Application:
    """
    Retrieve the application instance from the request.

    :param request: The incoming request.
    :return: The Application instance.
    """
    application = request.app.container.application()
    return application


def get_transaction_context(request: Request) -> TransactionContext:
    """
    Retrieve the transaction context from the request state.

    :param request: The incoming request.
    :return: The TransactionContext instance.
    """
    return request.state.transaction_context


def get_logger(request: Request):
    """
    Retrieve the logger from the request.

    :param request: The incoming request.
    :return: The logger instance.
    """
    return request.app.container.application().dependency_provider["logger"]
