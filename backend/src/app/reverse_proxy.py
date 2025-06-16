from typing import Annotated

import httpx
from datetime import datetime, timezone
from app.dependencies import get_logger, get_provider_pricelist, get_transaction_context
from fastapi import Depends, Request, HTTPException
from fastapi.responses import StreamingResponse, Response
from lato import Application, TransactionContext
from projects.use_cases import get_project_by_slug
from raw_transactions.use_cases import store_raw_transactions
from starlette.background import BackgroundTask
from transactions.use_cases import store_transaction
from utils import ApiURLBuilder
import logging
import json
import sys
import os
from app.logging import logger
from .db_logging import MongoDBLogger, Direction
from starlette.requests import ClientDisconnect

from .app import app

# Create a custom handler and formatter for proxy logs
proxy_handler = logging.StreamHandler(sys.stdout)
proxy_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Check if we should log to stdout
log_to_stdout = os.getenv("LOG_TO_STDOUT", "True").lower() == "true"

# Create a separate logger for proxy logging
proxy_logger = logging.getLogger("proxy_logger")
if log_to_stdout:
    proxy_logger.addHandler(proxy_handler)
proxy_logger.setLevel(logging.INFO)
proxy_logger.propagate = False

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
    logger.debug("Starting to iterate over response stream")
    async for chunk in response.aiter_raw():
        try:
            buffer.append(chunk)
            yield chunk
        except ClientDisconnect:
            logger.warning("Client disconnected during stream")
            await response.aclose()
            return
        except Exception as e:
            logger.error(f"Error during stream iteration: {str(e)}")
            raise
    logger.debug(f"Finished stream iteration, buffer size: {len(buffer)}")


async def close_stream(
    app: Application,
    project_id,
    ai_provider_request,
    ai_provider_response,
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
    - **ai_provider_request**: The original request object
    - **ai_provider_response**: The response object from the AI provider
    - **buffer**: Buffer containing the accumulated response data
    - **tags**: List of tags associated with the transaction
    - **ai_model_version**: Specific model version tag for cost calculation
    - **pricelist**: List of provider prices for cost calculation
    - **request_time**: Timestamp when the request was initiated
    """
    logger = app.dependency_provider["logger"]  # Get logger first
    logger.debug("Starting close_stream")
    await ai_provider_response.aclose()
    
    logger.debug(f"Storing transaction for project {project_id}")
    logger.debug(f"Request URL: {ai_provider_request.url}")
    logger.debug(f"Response status: {ai_provider_response.status_code}")
    logger.debug(f"Buffer length: {len(buffer) if buffer else 0}")
    
    with app.transaction_context() as ctx:
        try:
            logger.debug("Calling store_transaction")
            data = ctx.call(
                store_transaction,
                project_id=project_id,
                ai_provider_request=ai_provider_request,
                ai_provider_response=ai_provider_response,
                buffer=buffer,
                tags=tags,
                ai_model_version=ai_model_version,
                pricelist=pricelist,
                request_time=request_time,
            )
            logger.debug(f"Transaction stored successfully with ID: {data.get('transaction_id')}")
            
            # Also store raw transaction data
            try:
                logger.debug("Storing raw transaction data")
                ctx.call(
                    store_raw_transactions,
                    request=ai_provider_request,
                    request_content=data["request_content"],
                    response=ai_provider_response,
                    response_content=data["response_content"],
                    transaction_id=data["transaction_id"],
                )
                logger.debug("Raw transaction data stored successfully")
            except Exception as raw_e:
                logger.error(f"Failed to store raw transaction data: {str(raw_e)}")
                logger.error(f"Error type: {type(raw_e)}")
                logger.error(f"Error args: {raw_e.args}")
                
        except Exception as e:
            logger.error(f"Failed to store transaction: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            logger.error(f"Error args: {e.args}")
            raise


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
    tags = tags.split(",") if tags is not None else []
    try:
        project = ctx.call(get_project_by_slug, slug=project_slug)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Project not found: {project_slug}")

    url = ApiURLBuilder.build(project, provider_slug, path, target_path)
    pricelist = get_provider_pricelist(request)

    logger.debug(f"got projects for {project}")

    # Get the body once and store it
    try:
        body = await request.body() if request.method != "GET" else None
    except ClientDisconnect:
        return Response(
            content=json.dumps({
                "error": "Client disconnected during request"
            }),
            status_code=499
        )

    # Create headers without transfer-encoding
    headers = {k: v for k, v in request.headers.items() 
              if k.lower() not in ("host", "transfer-encoding")}
    
    # Add Content-Length if we have a body
    if body:
        headers["Content-Length"] = str(len(body))
    
    # Preserve WebSocket headers if present
    if request.headers.get("upgrade", "").lower() == "websocket":
        headers["Connection"] = request.headers.get("Connection")
        headers["Upgrade"] = request.headers.get("Upgrade")
        headers["Sec-WebSocket-Version"] = request.headers.get("Sec-WebSocket-Version")

    # Log the outgoing request details
    if log_to_stdout:
        proxy_logger.info(f"\n{'='*50}\nOutgoing Request to OpenAI\n{'='*50}")
        proxy_logger.info(f"URL: {url}")
        proxy_logger.info(f"Method: {request.method}")
        proxy_logger.info("Headers being sent to OpenAI:")
        proxy_logger.info(json.dumps(headers, indent=2))
    
    # If it's a POST/PUT request, log the body
    if body:
        try:
            body_json = json.loads(body)
            proxy_logger.info("Request Body to OpenAI:")
            proxy_logger.info(json.dumps(body_json, indent=2))
        except json.JSONDecodeError:
            proxy_logger.info(f"Raw body: {body.decode()}")

    # Make the request to the upstream server
    client = httpx.AsyncClient()
    timeout = httpx.Timeout(100.0, connect=50.0)

    request_time = datetime.now(tz=timezone.utc)
    ai_provider_request = client.build_request(
        method=request.method,
        url=url,
        headers=headers,
        params=request.query_params,
        content=body,
        timeout=timeout,
    )
    
    # Log the final request that will be sent
    proxy_logger.info("\n=== Final Request to OpenAI ===")
    proxy_logger.info(f"Full URL: {ai_provider_request.url}")
    proxy_logger.info("Final Headers:")
    proxy_logger.info(json.dumps(dict(ai_provider_request.headers), indent=2))
    
    # Log the actual request body being sent
    if ai_provider_request.content:
        try:
            # Try to decode and parse as JSON
            content = ai_provider_request.content.decode('utf-8')
            content_json = json.loads(content)
            proxy_logger.info("Request Body being sent to OpenAI:")
            proxy_logger.info(json.dumps(content_json, indent=2))
        except Exception as e:
            proxy_logger.info(f"Raw request body: {ai_provider_request.content}")

    logger.debug(f"Requesting on: {url}")
    ai_provider_response = await client.send(ai_provider_request, stream=True, follow_redirects=True)

    # Log the response headers immediately
    proxy_logger.info("\n=== Response from OpenAI ===")
    proxy_logger.info(f"Status: {ai_provider_response.status_code}")
    proxy_logger.info("Response Headers:")
    proxy_logger.info(json.dumps(dict(ai_provider_response.headers), indent=2))

    # If it's a streaming response, collect all chunks and return as one response
    buffer = []
    if ai_provider_response.headers.get("transfer-encoding") == "chunked":
        logger.debug("Handling chunked response")
        async for chunk in ai_provider_response.aiter_bytes():
            try:
                buffer.append(chunk)
            except ClientDisconnect:
                logger.warning("Client disconnected during chunked response")
                await ai_provider_response.aclose()
                return Response(status_code=499)
            except Exception as e:
                logger.error(f"Error processing chunk: {str(e)}")
                raise
        content = b''.join(buffer)
        
        # Set up background task for chunked responses too
        logger.debug("Setting up background task for chunked response")
        background = BackgroundTask(
            close_stream,
            app=ctx["app"],
            project_id=project.id,
            ai_provider_request=ai_provider_request,
            ai_provider_response=ai_provider_response,
            buffer=buffer,
            tags=tags,
            ai_model_version=ai_model_version,
            pricelist=pricelist,
            request_time=request_time,
        )
        
        return Response(
            content=content,
            status_code=ai_provider_response.status_code,
            headers={
                "Content-Type": "application/json",
                **{k: v for k, v in ai_provider_response.headers.items() 
                   if k.lower() not in ("transfer-encoding", "content-encoding")}
            },
            background=background  # Add background task here too
        )
    else:
        # In the reverse_proxy function, before returning StreamingResponse
        logger.debug("Setting up background task for transaction storage")
        background = BackgroundTask(
            close_stream,
            app=ctx["app"],
            project_id=project.id,
            ai_provider_request=ai_provider_request,
            ai_provider_response=ai_provider_response,
            buffer=buffer,
            tags=tags,
            ai_model_version=ai_model_version,
            pricelist=pricelist,
            request_time=request_time,
        )
        logger.debug("Returning streaming response with background task")
        return StreamingResponse(
            iterate_stream(ai_provider_response, buffer),
            status_code=ai_provider_response.status_code,
            headers=ai_provider_response.headers,
            background=background,
        )
