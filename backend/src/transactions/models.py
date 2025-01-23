from typing import Any
from uuid import uuid4

from _datetime import datetime, timezone
from pydantic import BaseModel, Field


def generate_uuid() -> str:
    return str(uuid4())


class Transaction(BaseModel):
    id: str = Field(default_factory=generate_uuid)
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
    input_cost: int | float | None
    output_cost: int | float | None
    total_cost: int | float | None
    request_time: datetime
    response_time: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc)
    )

    # old fields
    # hate: Any = None
    # self_harm: Any = None
    # violence: Any = None
    # sexual: Any = None

    def __init__(self, **data):
        super().__init__(**data)
        self.prompt = data.get('prompt', '')
        self.last_message = data.get('last_message', '')
