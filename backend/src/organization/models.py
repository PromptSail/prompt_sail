from enum import Enum

from _datetime import datetime, timezone
from pydantic import BaseModel, Field
from transactions.models import generate_uuid


class OrganizationTypeEnum(str, Enum):
    personal = "Personal"
    group = "Group"


class Organization(BaseModel):
    id: str = Field(default_factory=generate_uuid)
    type: OrganizationTypeEnum = OrganizationTypeEnum.personal
    name: str
    owner: str
    members: list[str] = []
    created_at: datetime = datetime.now(tz=timezone.utc)
