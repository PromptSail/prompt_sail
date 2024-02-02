from typing import Annotated

import httpx
from _datetime import datetime, timezone
from app.dependencies import get_logger, get_transaction_context
from fastapi import Depends, Request
from fastapi.responses import StreamingResponse
from lato import Application, TransactionContext
from projects.use_cases import get_project_by_slug
from starlette.background import BackgroundTask
from transactions.use_cases import store_transaction
from utils import ApiURLBuilder

from .app import app


async def iterate_stream(response, buffer):
    async for chunk in response.aiter_raw():
        buffer.append(chunk)
        yield chunk


async def close_stream(
    app: Application, project_id, request, response, buffer, tags, request_time
):
    await response.aclose()
    with app.transaction_context() as ctx:
        ctx.call(
            store_transaction,
            project_id=project_id,
            request=request,
            response=response,
            buffer=buffer,
            tags=tags,
            request_time=request_time,
        )


@app.api_route(
    "/{project_slug}/{deployment_name}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def reverse_proxy(
    project_slug: str,
    deployment_name: str,
    path: str,
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    tags: str | None = None,
    target_path: str | None = None,
):
    logger = get_logger(request)

    # if not request.state.is_handled_by_proxy:
    #     return RedirectResponse("/ui")
    # project = ctx.call(get_project_by_slug, slug=request.state.slug)

    tags = tags.split(",") if tags is not None else []
    project = ctx.call(get_project_by_slug, slug=project_slug)
    url = ApiURLBuilder.build(project, deployment_name, path, target_path)

    logger.debug(f"got projects for {project}")

    # Get the body as bytes for non-GET requests
    body = await request.body() if request.method != "GET" else None

    # Make the request to the upstream server
    client = httpx.AsyncClient()
    # todo: copy timeout from request, temporary set to 100s
    timeout = httpx.Timeout(100.0, connect=50.0)

    request_time = datetime.now(tz=timezone.utc)
    rp_req = client.build_request(
        method=request.method,
        url=url,
        # headers=request.headers.raw,
        headers={
            k: v for k, v in request.headers.items() if k.lower() not in ("host",)
        },
        params=request.query_params,
        content=body,
        timeout=timeout,
    )
    logger.debug(f"Requesting on: {url}")
    rp_resp = await client.send(rp_req, stream=True)

    buffer = []
    return StreamingResponse(
        iterate_stream(rp_resp, buffer),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(
            close_stream,
            ctx["app"],
            project.id,
            rp_req,
            rp_resp,
            buffer,
            tags,
            request_time,
        ),
    )
