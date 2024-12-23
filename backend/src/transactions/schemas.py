from typing import Any

from _datetime import datetime, timedelta
from pydantic import BaseModel


class GetTransactionSchema(BaseModel):
    id: str
    project_id: str
    provider: str
    model: str | None
    type: str
    os: str | None
    input_tokens: int | None
    output_tokens: int | None
    input_tokens: int | None
    library: str
    status_code: int
    messages: list[dict[str, Any]] | str | None
    last_message: str | None
    prompt: str
    error_message: str | None
    request_time: datetime
    response_time: datetime
    generation_speed: int | float | None
    input_cost: int | float | None
    output_cost: int | float | None
    total_cost: int | float | None
    tags: list[str]


class GetTransactionWithProjectSlugSchema(GetTransactionSchema):
    project_name: str


class GetTransactionWithRawDataSchema(GetTransactionWithProjectSlugSchema):
    request: dict[str, Any]
    response: dict[str, Any]



class CreateTransactionWithRawDataSchema(BaseModel):
    project_id: str
    request_json: dict[str, Any]
    response_json: dict[str, Any]
    tags: list[str]
    provider: str
    model: str | None
    type: str
    os: str | None
    input_tokens: int | None
    output_tokens: int | None
    library: str
    status_code: int
    messages: list[dict[str, Any]] | str | None
    last_message: str | None
    prompt: str
    error_message: str | None
    generation_speed: int | float | None
    request_time: datetime
    input_cost: int | float | None
    output_cost: int | float | None
    total_cost: int | float | None
    response_time: datetime | None


class CreateTransactionSchema(BaseModel):
    project_id: str
    tags: list[str]
    provider: str
    model: str | None
    type: str
    os: str | None
    input_tokens: int | None
    output_tokens: int | None
    library: str
    status_code: int
    messages: list[dict[str, Any]] | str | None
    last_message: str | None
    prompt: str
    error_message: str | None
    generation_speed: int | float | None
    request_time: datetime
    input_cost: int | float | None
    output_cost: int | float | None
    total_cost: int | float | None
    response_time: datetime | None





class StatisticTransactionSchema(BaseModel):
    project_id: str
    provider: str
    model: str
    total_input_tokens: int
    total_output_tokens: int
    total_input_cost: int | float | None
    total_output_cost: int | float | None
    total_cost: int | float | None
    status_code: int
    latency: timedelta
    date: datetime
    total_transactions: int
    generation_speed: int | float | None


class TagStatisticTransactionSchema(BaseModel):
    tag: str
    total_input_tokens: int
    total_output_tokens: int
    total_input_cost: int | float | None
    total_output_cost: int | float | None
    total_cost: int | float | None
    date: datetime
    total_transactions: int


class GetTagStatisticTransactionSchema(BaseModel):
    tag: str
    total_input_tokens: int
    total_output_tokens: int
    input_cumulative_total: int | float | None
    output_cumulative_total: int | float | None
    total_cost: int | float | None
    date: datetime
    total_transactions: int


class GetTagStatisticsSchema(BaseModel):
    tag: str
    total_input_tokens: int
    total_output_tokens: int
    input_cumulative_total: int | float | None
    output_cumulative_total: int | float | None
    total_cost: int | float | None
    total_transactions: int


class GetTagStatisticsInTime(BaseModel):
    date: datetime
    records: list[GetTagStatisticsSchema]


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


class GetTransactionUsageStatisticsWithoutDateSchema(BaseModel):
    provider: str
    model: str
    total_input_tokens: int
    total_output_tokens: int
    input_cumulative_total: int
    output_cumulative_total: int
    total_transactions: int
    total_cost: float


class GetTransactionsUsageStatisticsSchema(BaseModel):
    date: datetime
    records: list[GetTransactionUsageStatisticsWithoutDateSchema]


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


class GetTransactionLatencyStatisticsWithoutDateSchema(BaseModel):
    provider: str
    model: str
    mean_latency: timedelta | int | float
    tokens_per_second: int | float
    total_transactions: int


class GetTransactionsLatencyStatisticsSchema(BaseModel):
    date: datetime
    records: list[GetTransactionLatencyStatisticsWithoutDateSchema]


class GetTransactionPageResponseSchema(BaseModel):
    items: list[GetTransactionWithProjectSlugSchema]
    page_index: int
    page_size: int
    total_pages: int
    total_elements: int

