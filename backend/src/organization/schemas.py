from _datetime import datetime
from organization.models import OrganizationTypeEnum
from pydantic import BaseModel


class CreateOrganizationSchema(BaseModel):
    name: str
    type: OrganizationTypeEnum
    owner: str | None = None


class GetOrganizationSchema(BaseModel):
    type: OrganizationTypeEnum
    name: str
    owner: str
    members: list[str]
    created_at: datetime


class GetOrganizationForUserSchema(BaseModel):
    id: str
    name: str
    type: str


class UpdateOrganizationSchema(BaseModel):
    type: OrganizationTypeEnum
    name: str


class GetOrganizationsForUserSchema(BaseModel):
    user_id: str
    owned: list[GetOrganizationForUserSchema]
    as_member: list[GetOrganizationForUserSchema]
