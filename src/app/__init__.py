import importlib

from fastapi.staticfiles import StaticFiles

from .app import app

app.mount("/static", StaticFiles(directory="static"), name="static")
importlib.import_module("app.middleware")
importlib.import_module("app.ui")
importlib.import_module("app.reverse_proxy")
