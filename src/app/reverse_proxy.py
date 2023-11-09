from typing import Annotated

import httpx
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from lato import Application, TransactionContext
from starlette.background import BackgroundTask

from app.dependencies import get_logger, get_transaction_context
from projects.use_cases import get_project
from transactions.use_cases import store_transaction

from .app import app


async def iterate_stream(response, buffer):
    async for chunk in response.aiter_raw():
        buffer.append(chunk)
        yield chunk


async def close_stream(app: Application, project_id, request, response, buffer):
    await response.aclose()
    with app.transaction_context() as ctx:
        ctx.call(
            store_transaction,
            project_id=project_id,
            request=request,
            response=response,
            buffer=buffer,
        )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def reverse_proxy(
    path: str,
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
):
    logger = get_logger(request)

    if not request.state.is_handled_by_proxy:
        return RedirectResponse("/ui")

    project = ctx.call(get_project, project_id=request.state.project_id)

    logger.debug(f"got projects for {project}")

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

    buffer = []
    return StreamingResponse(
        iterate_stream(rp_resp, buffer),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(
            close_stream, ctx.app, project.id, rp_req, rp_resp, buffer
        ),
    )
