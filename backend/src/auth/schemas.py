from pydantic import BaseModel


class GetUserSchema(BaseModel):
    external_id: str
    email: str
    organization: str | None
    given_name: str
    family_name: str
    picture: str | None
    issuer: str
