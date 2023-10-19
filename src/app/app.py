from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from config import config
from config.containers import TopLevelContainer

templates = Jinja2Templates(directory="web/templates")

container = TopLevelContainer()
# container.config.from_pydantic(config)
container.config.override(config)


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    from projects.models import Project

    application = container.application()
    with (application.transaction_context() as ctx):
        project_repository = ctx["project_repository"]
        if project_repository.count() == 0:
            project_repository.add(
                Project(
                    id="project1",
                    name="Project 1",
                    api_base="https://api.openai.com/v1",
                )
            )
            project_repository.add(
                Project(
                    id="project2",
                    name="Project 2",
                    api_base="https://api.openai.com/v1",
                )
            )
    yield
    ...


app = FastAPI(lifespan=fastapi_lifespan)
app.container = container
