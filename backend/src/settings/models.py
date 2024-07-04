from pydantic import BaseModel


class OrganizationSettings(BaseModel):
    id: str
    organization_name: str
