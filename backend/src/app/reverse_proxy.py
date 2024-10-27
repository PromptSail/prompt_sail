from typing import Annotated

import httpx
from _datetime import datetime, timezone
from app.dependencies import get_logger, get_provider_pricelist, get_transaction_context
from fastapi import Depends, Request
from fastapi.responses import StreamingResponse
from lato import Application, TransactionContext
from projects.use_cases import get_project_by_slug
from raw_transactions.use_cases import store_raw_transactions
from starlette.background import BackgroundTask
from transactions.use_cases import store_transaction
from utils import ApiURLBuilder

from .app import app


async def iterate_stream(response, buffer):
    """
    Asynchronously iterate over the raw stream of a response and accumulate chunks in a buffer.

    This function asynchronously iterate over the raw stream of a response and accumulate chunks in a buffer
    for later processing.

    Parameters:
    - **response**: The response object containing the stream
    - **buffer**: List to store the accumulated response chunks

    Yields:
    - Chunks of the response data as they are received
    """
    async for chunk in response.aiter_raw():
        buffer.append(chunk)
        yield chunk


async def close_stream(
    app: Application,
    project_id,
    request,
    response,
    buffer,
    tags,
    ai_model_version,
    pricelist,
    request_time,
):
    """
    Process and store transaction data after stream completion.

    This function handles the post-streaming tasks, including storing transaction details
    and raw request/response data in the database.

    Parameters:
    - **app**: The Application instance
    - **project_id**: The unique identifier of the project
    - **request**: The original request object
    - **response**: The response object from the AI provider
    - **buffer**: Buffer containing the accumulated response data
    - **tags**: List of tags associated with the transaction
    - **ai_model_version**: Specific model version tag for cost calculation
    - **pricelist**: List of provider prices for cost calculation
    - **request_time**: Timestamp when the request was initiated
    """
    await response.aclose()
    with app.transaction_context() as ctx:
        data = ctx.call(
            store_transaction,
            project_id=project_id,
            request=request,
            response=response,
            buffer=buffer,
            tags=tags,
            ai_model_version=ai_model_version,
            pricelist=pricelist,
            request_time=request_time,
        )
        ctx.call(
            store_raw_transactions,
            request=request,
            request_content=data["request_content"],
            response=response,
            response_content=data["response_content"],
            transaction_id=data["transaction_id"],
        )


@app.api_route(
    "/{project_slug}/{provider_slug}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def reverse_proxy(
    project_slug: str,
    provider_slug: str,
    path: str,
    request: Request,
    ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
    tags: str | None = None,
    ai_model_version: str | None = None,
    target_path: str | None = None,
):
    """
    Forward requests to AI providers and handle responses.

    This endpoint acts as a reverse proxy, forwarding requests to various AI providers
    while monitoring and storing transaction details. It handles streaming responses,
    calculates costs, and maintains transaction history.

    Parameters:
    - **project_slug**: The unique slug identifier of the project
    - **provider_slug**: The slug identifier of the AI provider
    - **path**: The API endpoint path to forward to
    - **request**: The incoming request object
    - **ctx**: The transaction context dependency
    - **tags**: Optional comma-separated list of tags for the transaction
    - **ai_model_version**: Optional specific model version for accurate cost calculation
    - **target_path**: Optional override for the target API path

    Returns:
    - A StreamingResponse object containing the provider's response

    Notes:
    - Automatically handles request/response streaming
    - Stores transaction details and raw data in the background
    - Calculates costs based on the provider's pricing
    - Supports various HTTP methods (GET, POST, PUT, PATCH, DELETE)
    """
    logger = get_logger(request)

    # if not request.state.is_handled_by_proxy:
    #     return RedirectResponse("/ui")
    # project = ctx.call(get_project_by_slug, slug=request.state.slug)

    tags = tags.split(",") if tags is not None else []
    project = ctx.call(get_project_by_slug, slug=project_slug)
    url = ApiURLBuilder.build(project, provider_slug, path, target_path)

    pricelist = get_provider_pricelist(request)

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
        headers={
            k: v for k, v in request.headers.items() if k.lower() not in ("host",)
        },
        params=request.query_params,
        content=body,
        timeout=timeout,
    )
    logger.debug(f"Requesting on: {url}")
    rp_resp = await client.send(rp_req, stream=True, follow_redirects=True)

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
            ai_model_version,
            pricelist,
            request_time,
        ),
    )
