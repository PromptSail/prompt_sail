from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class OrganizationSettings(BaseModel):
    id: str
    organization_name: str
    users: list[User]
