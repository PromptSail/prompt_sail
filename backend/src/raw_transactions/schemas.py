from typing import Any

from pydantic import BaseModel

from .models import RawTransaction, TransactionTypeEnum


class RawTransactionSchema(RawTransaction):
    ...


class CreateRawTransactionSchema(BaseModel):
    transaction_id: str
    type: TransactionTypeEnum
    data: dict[str, Any]
