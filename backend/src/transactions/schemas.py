from typing import Any

from _datetime import datetime
from pydantic import BaseModel


class GetTransactionSchema(BaseModel):
    id: str
    project_id: str
    request: dict[str, Any]
    response: dict[str, Any]
    model: str
    model_type: str
    os: str | None
    token_usage: int
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
    model: str
    type: str
    os: str | None
    token_usage: int
    library: str
    status_code: int
    message: str | None
    prompt: str
    error_message: str | None
    request_time: datetime
    response_time: datetime
    tags: list[str]


class GetTransactionPageResponseSchema(BaseModel):
    items: list[GetTransactionWithProjectSlugSchema]
    page_index: int
    page_size: int
    total_pages: int
    total_elements: int
