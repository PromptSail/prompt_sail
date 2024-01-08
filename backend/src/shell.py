from lato import Application

from app import app as fastapi_app

app: Application = fastapi_app.container.application()


def print_handlers_for_module(m):
    print()
    print("Module: ", m.name)
    print("Handlers:")
    for k, v in m._handlers.items():
        print(k, v)
    else:
        print("-")

    for submodule in m._submodules:
        print_handlers_for_module(submodule)


print_handlers_for_module(app)
