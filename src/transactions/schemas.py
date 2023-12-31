from typing import Any

from _datetime import datetime
from pydantic import BaseModel


class GetTransactionSchema(BaseModel):
    id: str
    project_id: str
    request: dict[str, Any]
    response: dict[str, Any]
    timestamp: datetime

      
class GetTransactionWithProjectSlugSchema(BaseModel):
    id: str
    project_id: str
    project_name: str
    request: dict[str, Any]
    response: dict[str, Any]
    timestamp: datetime
 