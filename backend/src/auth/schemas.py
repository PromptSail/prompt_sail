from pydantic import BaseModel


class GetUserSchema(BaseModel):
    id: str
    external_id: str | None
    email: str
    organization: str | None
    given_name: str
    family_name: str
    picture: str | None
    issuer: str
    is_active: bool


class GetPartialUserSchema(BaseModel):
    id: str
    email: str
    full_name: str
    picture: str | None


class CreateUserSchema(BaseModel):
    email: str
    given_name: str
    family_name: str
    password: str
    repeated_password: str


class LoginSchema(BaseModel):
    email: str
    password: str
