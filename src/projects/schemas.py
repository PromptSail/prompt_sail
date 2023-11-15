from pydantic import BaseModel


class CreateProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    api_base: str = "https://api.openai.com/v1"
    org_id: str | None = None


class UpdateProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    api_base: str
    org_id: str | None = None


class GetProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    api_base: str
    org_id: str | None = None
