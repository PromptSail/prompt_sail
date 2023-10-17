import httpx
from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTask

from config import config
from repository import project_repository

app = FastAPI()


@app.middleware("detect_project")
async def __call__(request: Request, call_next):
    host = config["DOMAIN"] or request.headers.get("host", "")
    subdomain = host.split(".")[0]

    project = project_repository.get(subdomain)
    request.state.project = project

    print("middleware", host, request.state.project)

    response = await call_next(request)
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


async def iterate_stream(response):
    async for chunk in response.aiter_raw():
        print("chunk", chunk)
        yield chunk


async def close_stream(response):
    print("close_stream")
    return response.aclose()


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def reverse_proxy(path: str, request: Request, background_tasks: BackgroundTasks):
    print("reverse_proxy", path, request.state.project)
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
    buffer = []
    return StreamingResponse(
        iterate_stream(rp_resp, buffer),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(close_stream, rp_resp),
    )
