from typing import Any

from _datetime import datetime
from pydantic import BaseModel

from transactions.models import QueryParams


class GetTransactionSchema(BaseModel):
    id: str
    project_id: str
    request: dict[str, Any]
    response: dict[str, Any]
    timestamp: datetime
    query_params: QueryParams


class GetTransactionWithProjectSlugSchema(BaseModel):
    id: str
    project_id: str
    project_name: str
    request: dict[str, Any]
    response: dict[str, Any]
    timestamp: datetime
    query_params: QueryParams


class GetTransactionPageResponseSchema(BaseModel):
    items: list[GetTransactionWithProjectSlugSchema]
    page_index: int
    page_size: int
    total_pages: int
    total_elements: int
