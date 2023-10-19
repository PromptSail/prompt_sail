from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from config.containers import TopLevelContainer

templates = Jinja2Templates(directory="src/web/templates")

container = TopLevelContainer()

app = FastAPI()
app.container = container
