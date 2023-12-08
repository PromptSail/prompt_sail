from pydantic import BaseModel

from transactions.schemas import GetTransactionSchema


class ProjectAIProviderSchema(BaseModel):
    api_base: str
    provider_name: str
    ai_model_name: str


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


class GetProjectWithTransactionsSchema(GetProjectSchema):
    transactions: list[GetTransactionSchema] = []
    