from fastapi import Request
from lato import Application, TransactionContext


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application


def get_transaction_context(request: Request) -> TransactionContext:
    return request.state.transaction_context


def get_logger(request: Request):
    return request.app.container.application().dependency_provider["logger"]
