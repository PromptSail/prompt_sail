from pydantic import BaseModel


class ProjectAIProviderSchema(BaseModel):
    api_base: str
    provider_name: str
    model_name: str


class CreateProjectSchema(BaseModel):
    name: str
    slug: str
    description: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None


class UpdateProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None


class GetProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None
