from contextlib import asynccontextmanager

from config import config
from config.containers import TopLevelContainer
from fastapi import FastAPI

container = TopLevelContainer()
container.config.override(config)


@asynccontextmanager
async def fastapi_lifespan(app: FastAPI):
    import os

    from dotenv import find_dotenv, load_dotenv
    from projects.models import AIProvider, Project
    from projects.use_cases import add_project
    from settings.models import OrganizationSettings
    from settings.use_cases import add_settings

    load_dotenv(find_dotenv())

    application = container.application()
    with application.transaction_context() as ctx:
        project_repository = ctx["project_repository"]
        settings_repository = ctx["settings_repository"]

        if project_repository.count() == 0:
            data1 = Project(
                name="Models Playground",
                slug="models-playground",
                description="Default description for models playground project.",
                ai_providers=[
                    AIProvider(
                        deployment_name="openai",
                        slug="openai",
                        api_base="https://api.openai.com/v1",
                        description="",
                        provider_name="OpenAI",
                    ),
                ],
                tags=["research", "internal", "experiment", "east-us"],
                org_id=os.getenv("ORGANIZATION_NAME", "PromptSail"),
                owner="anonymous@unknown.com",
            )
            data2 = Project(
                name="Client campaign",
                slug="client-campaign",
                description="Default description for client campaign project.",
                ai_providers=[
                    AIProvider(
                        deployment_name="openai",
                        slug="openai",
                        api_base="https://api.openai.com/v1",
                        description="",
                        provider_name="OpenAI",
                    ),
                ],
                tags=["client-zebra", "team-tigers", "central-eu", "production-system"],
                org_id=os.getenv("ORGANIZATION_NAME", "PromptSail"),
                owner="anonymous@unknown.com",
            )
            ctx.call(add_project, data1)
            ctx.call(add_project, data2)

        if settings_repository.count() == 0:
            organization_name = os.getenv("ORGANIZATION_NAME", "PromptSail")

            if organization_name is not None:
                data = OrganizationSettings(
                    id="settings",
                    organization_name=organization_name,
                )
                ctx.call(add_settings, data)
            else:
                raise ValueError(
                    "Theres no ORGANIZATION_NAME in environment variables!"
                )
    yield
    ...


app = FastAPI(lifespan=fastapi_lifespan, 
              title="PromptSail API",
              description="API for PromptSail - prompt management and monitoring tool",
              version="0.5.4",
              openapi_version="3.1.0",
              )
app.container = container
