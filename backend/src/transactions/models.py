from typing import Any
from uuid import uuid4

from _datetime import datetime, timezone
from pydantic import BaseModel, Field


def generate_uuid() -> str:
    return str(uuid4())


class Transaction(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    project_id: str
    request: dict[str, Any]
    response: dict[str, Any]
    tags: list[str]
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
    generation_speed: int | float
    request_time: datetime
    response_time: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )
