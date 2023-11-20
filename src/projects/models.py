from pydantic import BaseModel, Field

from transactions.models import generate_uuid


class AIProvider(BaseModel):
    api_base: str = Field(default_factory=str)
    provider_name: str = Field(default_factory=str)
    model_name: str = Field(default_factory=str)


class Project(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    name: str = Field(default_factory=str)
    slug: str = Field(default_factory=str)  # regex for slug: ^[a-zA-Z][a-zA-Z0-9_-]*$
    description: str = Field(default_factory=str, max_length=280)
    ai_providers: list[AIProvider] = Field(...)
    tags: list[str] = Field(...)
    org_id: str | None = Field(default_factory=str, null=True)
