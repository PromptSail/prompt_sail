from pydantic import BaseModel


class GetUserSchema(BaseModel):
    external_id: str
    email: str
    given_name: str
    family_name: str
    picture: str
    issuer: str
    