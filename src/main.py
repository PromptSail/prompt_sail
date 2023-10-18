from typing import Annotated

import httpx
from fastapi import BackgroundTasks, Depends, FastAPI, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from config import config
from config.containers import TopLevelContainer
from models import Transaction
from project.use_cases import get_project
from seedwork.application import Application, TransactionContext
from tasks import persist_transaction

container = TopLevelContainer()

app = FastAPI()
app.container = container


async def get_application(request: Request) -> Application:
    application = request.app.container.application()
    return application


async def xxx_get_transaction_context(
    application: Annotated[Application, Depends(get_application)],
) -> TransactionContext:
    """Creates a new transaction context for each request"""

    with application.transaction_context() as ctx:
        yield ctx


def get_transaction_context(request: Request) -> TransactionContext:
    return request.state.transaction_context


def get_logger(request: Request):
    return request.app.container.application().dependency_provider["logger"]


@app.middleware("detect_project")
async def __call__(request: Request, call_next):
    host = config["DOMAIN"] or request.headers.get("host", "")
    subdomain = host.split(".")[0]

    ctx = get_transaction_context(request)
    project = ctx.call(get_project, project_id=subdomain)
    request.state.project = project

    logger = get_logger(request)
    logger.debug(f"got project for {host}: {project}")

    response = await call_next(request)
    return response


@app.middleware("transaction_context")
async def __call__(request: Request, call_next):
    application = request.app.container.application()
    ctx = application.transaction_context()
    request.state.transaction_context = ctx
    ctx.__enter__()
    response = await call_next(request)
    ctx.__exit__(None, None, None)
    return response


@app.middleware("proxy_tunnel")
async def __call__(request: Request, call_next):
    if request.method == "CONNECT":
        # Parse the host and port from the request's path
        host, port = request.scope.get("path").split(":")
        port = int(port)

        print("proxy_tunnel", host, port)

        raise NotImplementedError(
            "Using PromptSail as a true proxy is not supported yet"
        )

        # Create a socket connection to the target server
        # client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # await request.send({"type": "http.response.start", "status": 200})

        # try:
        #     await request.app.proxy_tunnel(client_socket, host, port)
        # except Exception as e:
        #     print(f"Error during proxy tunnel: {e}")
        # finally:
        #     client_socket.close()
        #
        # return Response(content=b"", status_code=200)

    response = await call_next(request)
    return response


async def iterate_stream(response, transaction):
    async for chunk in response.aiter_raw():
        print("chunk", chunk)
        transaction.buffer.append(chunk)
        yield chunk


async def close_stream(response, transaction, background_tasks: BackgroundTasks):
    print("close_stream")
    persist_transaction(transaction)
    await response.aclose()


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def reverse_proxy(path: str, request: Request, background_tasks: BackgroundTasks):
    logger = get_logger(request)
    logger.debug("reverse_proxy {path} {request.state.project}")
    project = request.state.project
    # Get the body as bytes for non-GET requests
    body = await request.body() if request.method != "GET" else None

    client = httpx.AsyncClient()
    rp_req = client.build_request(
        method=request.method,
        url=f"{project.api_base}/{path}",
        # headers=request.headers.raw,
        headers={
            k: v for k, v in request.headers.items() if k.lower() not in ("host",)
        },
        params=request.query_params,
        content=body,
    )

    rp_resp = await client.send(rp_req, stream=True)
    transaction = Transaction(project=project, request=rp_req, response=rp_resp)

    buffer = []
    return StreamingResponse(
        iterate_stream(rp_resp, transaction),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(close_stream, rp_resp, transaction, background_tasks),
    )
