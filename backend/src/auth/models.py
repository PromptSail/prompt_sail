from pydantic import BaseModel, Field
from transactions.models import generate_uuid


class User(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    external_id: str
    email: str
    organization: str | None = None
    given_name: str
    family_name: str
    picture: str | None = None
    issuer: str
