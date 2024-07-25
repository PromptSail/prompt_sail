from pydantic import BaseModel, Field
from transactions.models import generate_uuid


class UserCredential(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    user_id: str
    password: str
