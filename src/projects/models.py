from pydantic import BaseModel, Field

from transactions.models import generate_uuid


class AIProvider(BaseModel):
    api_base: str
    provider_name: str
    ai_model_name: str


class Project(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    name: str
    slug: str  # regex for slug: ^[a-zA-Z][a-zA-Z0-9_-]*$
    description: str = Field(max_length=280)
    ai_providers: list[AIProvider]
    tags: list[str] = []
    org_id: str | None
