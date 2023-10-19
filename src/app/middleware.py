from fastapi import Request

from config import config

from .app import app


@app.middleware("detect_subdomain")
async def __call__(request: Request, call_next):
    host = config.get("DOMAIN") or request.headers.get("host", "")
    subdomain = host.split(".")[0]

    if subdomain in ["ui", "www", "promptsail"]:
        request.state.is_web = True
    else:
        request.state.is_web = False

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
