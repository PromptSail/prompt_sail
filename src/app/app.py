from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from config import config
from config.containers import TopLevelContainer

templates = Jinja2Templates(directory=config.TEMPLATES_DIRECTORY)

container = TopLevelContainer()
container.config.override(config)


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    from projects.schemas import CreateProjectSchema, ProjectAIProviderSchema
    from projects.use_cases import add_project

    application = container.application()
    with application.transaction_context() as ctx:
        project_repository = ctx["project_repository"]
        if project_repository.count() == 0:
            data1 = CreateProjectSchema(
                    name="Project 1",
                    slug="project1",
                    description="Project 1 description",
                    ai_providers=[
                        ProjectAIProviderSchema(
                            api_base="https://api.openai.com/v1",
                            provider_name="OpenAI",
                            ai_model_name="gpt-3.5-turbo",
                        ),
                    ],
                    tags=["tag1", "tag2"],
                    org_id="organization",
                )
            data2 = CreateProjectSchema(
                    name="Project 2",
                    slug="project2",
                    description="Project 2 description",
                    ai_providers=[
                        ProjectAIProviderSchema(
                            api_base="https://api.openai.com/v1",
                            provider_name="OpenAI",
                            ai_model_name="gpt-3.5-turbo",
                        ),
                    ],
                    tags=["tag1", "tag2", "tag3"],
                    org_id="organization",
                )
            ctx.call(add_project, data1)
            ctx.call(add_project, data2)
    yield
    ...


app = FastAPI(lifespan=fastapi_lifespan)
app.container = container
