from fastapi import Request

from .app import app

# @app.middleware("detect_subdomain")
# async def __call__(request: Request, call_next):
#     """
#     Middleware for detecting subdomain in the request and setting corresponding state.
# 
#     :param request: The incoming request.
#     :param call_next: The callable representing the next middleware or endpoint in the chain.
#     :return: The response from the middleware or endpoint.
#     """
#     host = request.headers.get("host", "")
#     subdomain = detect_subdomain(host, config.BASE_URL)
# 
#     if subdomain in [None, "ui", "www"]:
#         request.state.is_handled_by_proxy = False
#     else:
#         request.state.is_handled_by_proxy = True
#         request.state.slug = subdomain
# 
#     response = await call_next(request)
#     return response


@app.middleware("transaction_context")
async def __call__(request: Request, call_next):
    """
    Middleware for managing transaction context.

    :param request: The incoming request.
    :param call_next: The callable representing the next middleware or endpoint in the chain.
    :return: The response from the middleware or endpoint.
    """
    application = request.app.container.application()
    ctx = application.transaction_context()
    request.state.transaction_context = ctx
    ctx.__enter__()
    response = await call_next(request)
    ctx.__exit__(None, None, None)
    return response


@app.middleware("proxy_tunnel")
async def __call__(request: Request, call_next):
    """
    Middleware for handling proxy tunnel requests.

    :param request: The incoming request.
    :param call_next: The callable representing the next middleware or endpoint in the chain.
    :return: The response from the middleware or endpoint.
    """
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
