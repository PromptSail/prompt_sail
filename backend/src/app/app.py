from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import logging
import json
import sys
from starlette.concurrency import iterate_in_threadpool
import traceback

from config import config
from config.containers import TopLevelContainer

container = TopLevelContainer()
container.config.override(config)

# Create a custom handler and formatter for our middleware logs
request_handler = logging.StreamHandler(sys.stdout)
request_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Create a separate logger for request logging
request_logger = logging.getLogger("request_logger")
request_logger.addHandler(request_handler)
request_logger.setLevel(logging.INFO)
# Prevent logs from being passed to parent handlers
request_logger.propagate = False

@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    import os

    from dotenv import find_dotenv, load_dotenv
    from projects.models import AIProvider, Project
    from projects.use_cases import add_project
    from settings.models import OrganizationSettings
    from settings.use_cases import add_settings

    load_dotenv(find_dotenv())

    application = container.application()
    with application.transaction_context() as ctx:
        project_repository = ctx["project_repository"]
        settings_repository = ctx["settings_repository"]

        if project_repository.count() == 0:
            data1 = Project(
                name="Models Playground",
                slug="models-playground",
                description="Default description for models playground project.",
                ai_providers=[
                    AIProvider(
                        deployment_name="openai",
                        slug="openai",
                        api_base="https://api.openai.com/v1",
                        description="",
                        provider_name="OpenAI",
                    ),
                ],
                tags=["research", "internal", "experiment", "east-us"],
                org_id=os.getenv("ORGANIZATION_NAME", "PromptSail"),
                owner="anonymous@unknown.com",
            )
            data2 = Project(
                name="Client campaign",
                slug="client-campaign",
                description="Default description for client campaign project.",
                ai_providers=[
                    AIProvider(
                        deployment_name="openai",
                        slug="openai",
                        api_base="https://api.openai.com/v1",
                        description="",
                        provider_name="OpenAI",
                    ),
                ],
                tags=["client-zebra", "team-tigers", "central-eu", "production-system"],
                org_id=os.getenv("ORGANIZATION_NAME", "PromptSail"),
                owner="anonymous@unknown.com",
            )
            ctx.call(add_project, data1)
            ctx.call(add_project, data2)

        if settings_repository.count() == 0:
            organization_name = os.getenv("ORGANIZATION_NAME", "PromptSail")

            if organization_name is not None:
                data = OrganizationSettings(
                    id="settings",
                    organization_name=organization_name,
                )
                ctx.call(add_settings, data)
            else:
                raise ValueError(
                    "Theres no ORGANIZATION_NAME in environment variables!"
                )
    yield
    ...

# Add this middleware function before creating the FastAPI app
async def log_request_middleware(request: Request, call_next):
    request_logger.info(f"\n{'='*50}\nIncoming Request: {request.method} {request.url.path}\n{'='*50}")
    request_logger.info(f"Request Headers:\n{json.dumps(dict(request.headers), indent=2)}")
    
    # Only try to log body for POST/PUT/PATCH requests
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        if body:
            try:
                body_json = json.loads(body)
                
                # Specifically log if this is an OpenAI request
                if "chat/completions" in request.url.path:
                    request_logger.info("\n=== OpenAI Request Details ===")
                    request_logger.info(f"Model: {body_json.get('model', 'not specified')}")
                    request_logger.info(f"Temperature: {body_json.get('temperature', 'not specified')}")
                    request_logger.info(f"Stream: {body_json.get('stream', 'not specified')}")
                    if "messages" in body_json:
                        request_logger.info(f"Number of messages: {len(body_json['messages'])}")
                        request_logger.info("\nSystem Message:")
                        system_msg = next((m for m in body_json['messages'] if m['role'] == 'system'), None)
                        if system_msg:
                            request_logger.info(f"{system_msg['content'][:200]}...")
                        request_logger.info("\nLast User Message:")
                        last_user_msg = next((m for m in reversed(body_json['messages']) if m['role'] == 'user'), None)
                        if last_user_msg:
                            request_logger.info(last_user_msg['content'])
                    request_logger.info("\nFull Request Payload:")
                    request_logger.info(json.dumps(body_json, indent=2))
            except json.JSONDecodeError:
                request_logger.info(f"Request Body (raw): {body.decode()}")
            
            # Restore the request body
            async def get_body():
                return body
            request._body = body
            request.body = get_body

    response = await call_next(request)
    
    request_logger.info(f"\n{'='*50}\nResponse Status: {response.status_code}\n{'='*50}")
    
    # For error responses (4xx and 5xx), try to log the response body
    if response.status_code >= 400:
        try:
            # Create a new response with the same content
            response_body = [chunk async for chunk in response.body_iterator]
            # Log the body content
            body = b''.join(response_body).decode()
            
            request_logger.error("\n=== Error Details ===")
            try:
                json_body = json.loads(body)
                request_logger.error(f"Response Body (JSON):\n{json.dumps(json_body, indent=2)}")
            except json.JSONDecodeError:
                request_logger.error(f"Response Body (raw):\n{body}")
                
            # If it's an OpenAI error, try to parse it differently
            if "openai" in str(request.url).lower():
                request_logger.error("\nOpenAI Error Response:")
                request_logger.error(f"URL: {request.url}")
                request_logger.error(f"Method: {request.method}")
                request_logger.error(f"Headers sent: {dict(request.headers)}")
                request_logger.error(f"Status code: {response.status_code}")
                request_logger.error(f"Response body: {body}")
            
            # Create a new iterator with the same content
            response.body_iterator = iterate_in_threadpool(iter(response_body))
        except Exception as e:
            request_logger.error(f"Error reading response body: {str(e)}")
            request_logger.error(f"Error traceback: {traceback.format_exc()}")
    
    return response

# Modify the FastAPI app creation to include the middleware
app = FastAPI(
    lifespan=fastapi_lifespan, 
    title="PromptSail API",
    description="API for PromptSail - prompt management and monitoring tool",
    version="0.5.4",
    openapi_version="3.1.0",
)

# Add the middleware to the app
app.middleware("http")(log_request_middleware)

app.container = container
