from _datetime import datetime
from pydantic import BaseModel
from organization.models import OrganizationTypeEnum


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
    
    
class UpdateOrganizationSchema(BaseModel):
    type: OrganizationTypeEnum
    name: str
    