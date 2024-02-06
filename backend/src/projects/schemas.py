from pydantic import BaseModel


class ProjectAIProviderSchema(BaseModel):
    deployment_name: str
    api_base: str
    description: str
    provider_name: str


class GetAIProviderSchema(BaseModel):
    provider_name: str
    api_base_placeholder: str


class CreateProjectSchema(BaseModel):
    name: str
    slug: str
    description: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None


class UpdateProjectSchema(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    ai_providers: list[ProjectAIProviderSchema] | None = None
    tags: list[str] | None = None
    org_id: str | None = None


class GetProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None
    total_transactions: int = 0
