from typing import Any

from _datetime import datetime, timedelta
from pydantic import BaseModel


class GetTransactionSchema(BaseModel):
    id: str
    project_id: str
    request: dict[str, Any]
    response: dict[str, Any]
    provider: str
    model: str | None
    type: str
    os: str | None
    input_tokens: int | None
    output_tokens: int | None
    library: str
    status_code: int
    message: str | None
    prompt: str
    error_message: str | None
    request_time: datetime
    response_time: datetime
    generation_speed: int | float
    tags: list[str]


class GetTransactionWithProjectSlugSchema(BaseModel):
    id: str
    project_id: str
    project_name: str
    request: dict[str, Any]
    response: dict[str, Any]
    provider: str
    model: str | None
    type: str
    os: str | None
    input_tokens: int | None
    output_tokens: int | None
    library: str
    status_code: int
    message: str | None
    prompt: str
    error_message: str | None
    request_time: datetime
    response_time: datetime
    generation_speed: int | float
    input_cost: int | float
    output_cost: int | float
    total_cost: int | float
    tags: list[str]


class StatisticTransactionSchema(BaseModel):
    project_id: str
    provider: str
    model: str
    total_input_tokens: int
    total_output_tokens: int
    status_code: int
    latency: timedelta
    date: datetime
    total_transactions: int
    generation_speed: int | float


class GetTransactionUsageStatisticsSchema(BaseModel):
    provider: str
    model: str
    date: datetime
    total_input_tokens: int
    total_output_tokens: int
    input_cumulative_total: int
    output_cumulative_total: int
    total_transactions: int
    total_cost: float


class GetTransactionStatusStatisticsSchema(BaseModel):
    date: datetime
    status_200: int
    status_300: int
    status_400: int
    status_500: int
    total_transactions: int


class GetTransactionLatencyStatisticsSchema(BaseModel):
    provider: str
    model: str
    date: datetime
    mean_latency: timedelta | int | float
    tokens_per_second: int | float
    total_transactions: int


class GetTransactionPageResponseSchema(BaseModel):
    items: list[GetTransactionWithProjectSlugSchema]
    page_index: int
    page_size: int
    total_pages: int
    total_elements: int
