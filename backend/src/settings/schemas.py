from pydantic import BaseModel


class GetUserSchema(BaseModel):
    username: str
    password: str


class AuthorizeUserSchema(GetUserSchema):
    ...
