from enum import Enum
from typing import Any
from pydantic import BaseModel, Field
from transactions.models import generate_uuid


class TransactionTypeEnum(str, Enum):
    request = "request"
    response = "response"


class RawTransaction(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    transaction_id: str
    type: TransactionTypeEnum
    data: dict[str, Any]
    