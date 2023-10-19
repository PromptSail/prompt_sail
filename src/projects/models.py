from pydantic import BaseModel, Field


class Project(BaseModel):
    id: str = Field(default_factory=str)
    name: str = Field(default_factory=str)
    api_base: str = Field(default_factory=str)
