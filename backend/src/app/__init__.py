import importlib

from fastapi.staticfiles import StaticFiles

from config import config

from .app import app

app.mount("/static", StaticFiles(directory=config.STATIC_DIRECTORY), name="static")
importlib.import_module("app.middleware")
importlib.import_module("app.exception_handlers")
importlib.import_module("app.web_ui")
importlib.import_module("app.web_api")
importlib.import_module("app.reverse_proxy")
