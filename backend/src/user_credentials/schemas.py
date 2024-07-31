from pydantic import BaseModel
from user_credentials.models import UserCredential


class CreateUserCredentialSchema(BaseModel):
    user_id: str
    password: str


class GetUserCredentialSchema(UserCredential):
    ...


class PasswordChangeSchema(BaseModel):
    password: str
    repeated_password: str
