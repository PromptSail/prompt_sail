import importlib

from config import config
from fastapi.staticfiles import StaticFiles

from .app import app

app.mount("/static", StaticFiles(directory=config.STATIC_DIRECTORY), name="static")
importlib.import_module("app.middleware")
importlib.import_module("app.exception_handlers")
importlib.import_module("app.web_api")
importlib.import_module("app.reverse_proxy")
importlib.import_module("app.web_home")
