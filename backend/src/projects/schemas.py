from _datetime import datetime
from pydantic import BaseModel


class ProjectAIProviderSchema(BaseModel):
    deployment_name: str
    slug: str
    api_base: str
    description: str
    provider_name: str


class GetAIProviderSchema(BaseModel):
    provider_name: str
    api_base_placeholder: str


class GetAIProviderPriceSchema(BaseModel):
    provider: str
    model_name: str
    start_date: datetime | str | None
    match_pattern: str
    input_price: int | float
    output_price: int | float
    total_price: int | float


class CreateProjectSchema(BaseModel):
    name: str
    slug: str
    description: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None
    owner: str = ""


class UpdateProjectSchema(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    ai_providers: list[ProjectAIProviderSchema] | None = None
    tags: list[str] | None = None
    org_id: str | None = None
    owner: str | None = None


class GetProjectSchema(BaseModel):
    id: str
    name: str
    slug: str
    description: str
    ai_providers: list[ProjectAIProviderSchema]
    tags: list[str] = []
    org_id: str | None = None
    created_at: datetime
    owner: str
    total_cost: int | float = 0
    total_transactions: int = 0


class GetProjectPortfolioSchema(BaseModel):
    id: str
    name: str
    slug: str
    tags: list[str] = 0
    created_at: datetime
    owner: str


class GetCostPerTagSchema(BaseModel):
    tag: str
    cost: int | float


class GetProjectUsageSchema(BaseModel):
    project_name: str
    project_id: str
    total_input_tokens: int
    total_output_tokens: int
    input_cumulative_total: int
    output_cumulative_total: int
    total_transactions: int
    total_cost: int | float


class GetProjectsUsageInTimeSchema(BaseModel):
    date: datetime
    records: list[GetProjectUsageSchema]


class GetProjectPortfolioCostPerTagSchema(BaseModel):
    date: datetime
    records: list[GetCostPerTagSchema]


class GetPortfolioDetailsSchema(BaseModel):
    total_cost: int | float
    total_transactions: int
    projects: list[GetProjectPortfolioSchema]
    projects: list[GetProjectPortfolioSchema]
