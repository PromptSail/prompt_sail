from typing import Annotated

import httpx
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from starlette.background import BackgroundTask

from app.dependencies import get_logger, get_transaction_context
from config import config
from projects.use_cases import get_project
from seedwork.application import Application, TransactionContext
from transactions.models import Transaction
from transactions.use_cases import store_transaction

from .app import app


async def iterate_stream(response, transaction):
    async for chunk in response.aiter_raw():
        transaction.buffer.append(chunk)
        yield chunk


async def close_stream(response, app: Application, transaction):
    await response.aclose()
    with app.transaction_context() as ctx:
        ctx.call(store_transaction, transaction=transaction)


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def reverse_proxy(
    path: str,
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
):
    host = config.get("DOMAIN") or request.headers.get("host", "")

    logger = get_logger(request)
    subdomain = host.split(".")[0]

    if subdomain in ["ui", "www", "promptsail"]:
        return RedirectResponse("/ui")

    project = ctx.call(get_project, project_id=subdomain)

    logger.debug(f"got projects for {host}: {project}")

    # Get the body as bytes for non-GET requests
    body = await request.body() if request.method != "GET" else None

    # Make the request to the upstream server
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

    return StreamingResponse(
        iterate_stream(rp_resp, transaction),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(close_stream, rp_resp, ctx.app, transaction),
    )
