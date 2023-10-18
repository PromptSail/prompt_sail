from typing import Any

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    project: Any
    request: Any
    response: Any
    buffer: list[Any] = Field(default_factory=list)
