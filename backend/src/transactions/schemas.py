from typing import Any

from _datetime import datetime
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
    tags: list[str]
    

class StatisticTransactionSchema(BaseModel):
    project_id: str
    provider: str
    model: str
    total_input_tokens: int
    total_output_tokens: int
    status_code: int
    date: datetime
    total_transactions: int
    
    
class GetTransactionUsageStatisticsSchema(BaseModel):
    project_id: str
    provider: str
    model: str
    date: datetime
    total_input_tokens: int
    total_output_tokens: int
    total_transactions: int
    total_cost: float
    

class GetTransactionStatusStatisticsSchema(BaseModel):
    project_id: str
    provider: str
    model: str
    date: datetime
    status_code: int
    total_transactions: int
    

class GetTransactionPageResponseSchema(BaseModel):
    items: list[GetTransactionWithProjectSlugSchema]
    page_index: int
    page_size: int
    total_pages: int
    total_elements: int
