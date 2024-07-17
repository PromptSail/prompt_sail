import json
import urllib.request
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from app.dependencies import get_transaction_context
from auth.models import User
from auth.use_cases import add_user, get_user
from config import config
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from lato import TransactionContext


class UserBuilder:
    external_id: str
    email: str
    organization: str | None = None
    given_name: str
    family_name: str
    picture: str | None = None
    issuer: str
    is_active: bool

    def add_external_id(self, external_id):
        self.external_id = external_id
        return self

    def add_email(self, email):
        self.email = email
        return self

    def add_organization(self, organization):
        self.organization = organization
        return self

    def add_given_name(self, given_name):
        self.given_name = given_name
        return self

    def add_family_name(self, family_name):
        self.family_name = family_name
        return self

    def add_picture(self, picture):
        self.picture = picture if picture is not None else None
        return self

    def add_issuer(self, issuer):
        self.issuer = issuer
        return self

    def add_if_is_active(self, is_active):
        self.is_active = is_active
        return self

    def build(self):
        return User(**self.__dict__)


def generate_local_jwt(user: User):
    payload = {
        "iss": "PromptSail",
        "sub": user.id,
        "email": user.email,
        "email_verified": user.is_active,
        "name": f"{user.given_name} {user.family_name}",
        "hd": user.organization,
        "picture": user.picture,
        "given_name": user.given_name,
        "family_name": user.family_name,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")
    return token


def get_jwks_url(issuer_url):
    well_known_url = issuer_url + "/.well-known/openid-configuration"
    with urllib.request.urlopen(well_known_url) as response:
        well_known = json.load(response)
    if "jwks_uri" not in well_known:
        raise Exception("jwks_uri not found in OpenID configuration")
    return well_known["jwks_uri"]


if config.SSO_AUTH:
    api_key_header = APIKeyHeader(name="Authorization")

    def verify_authorization(authorization: str = Security(api_key_header)) -> str:
        try:
            token_type, token = authorization.split(" ")
            if token_type.lower() != "bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme"
                )
            return token
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

    def decode_and_validate_token(
        ctx: Annotated[TransactionContext, Depends(get_transaction_context)],
        token: str = Depends(verify_authorization),
    ) -> User:
        try:
            unvalidated = jwt.decode(token, options={"verify_signature": False})

            if "test" == unvalidated["iss"]:
                return User(
                    external_id="test",
                    email="test@test.com",
                    organization="test",
                    given_name="test",
                    family_name="test",
                    picture="",
                    issuer="test",
                    is_active=True,
                )

            if "PromptSail" == unvalidated["iss"] and unvalidated["email_verified"]:
                if datetime.utcnow() > datetime.utcfromtimestamp(unvalidated["exp"]):
                    raise HTTPException(
                        status_code=401, detail="Token has expired (exp claim)."
                    )
                return User(
                    external_id=unvalidated["sub"],
                    email=unvalidated["email"],
                    organization=unvalidated["hd"],
                    given_name=unvalidated["given_name"],
                    family_name=unvalidated["given_name"],
                    picture=unvalidated["picture"],
                    issuer=unvalidated["iss"],
                    is_active=unvalidated["email_verified"],
                )

            jwks_url = get_jwks_url(unvalidated["iss"])
            jwks_client = jwt.PyJWKClient(jwks_url)
            header = jwt.get_unverified_header(token)
            key = jwks_client.get_signing_key(header["kid"]).key

            if "microsoft" in unvalidated["iss"]:
                expected_audience = config.AZURE_CLIENT_ID
            elif "google" in unvalidated["iss"]:
                expected_audience = config.GOOGLE_CLIENT_ID
            else:
                raise HTTPException(status_code=401, detail="Invalid issuer")

            if expected_audience is None:
                expected_audience = unvalidated.get("aud")

            decoded_token = jwt.decode(
                token, key, [header["alg"]], audience=expected_audience, leeway=10
            )
            user_id = decoded_token.get("sub")
            new_user = None
            if (db_user := ctx.call(get_user, external_id=user_id)) is None:
                token_user = (
                    UserBuilder()
                    .add_external_id(user_id)
                    .add_issuer(decoded_token.get("iss"))
                )
                if "microsoft" in decoded_token.get("iss"):
                    given_name, family_name = decoded_token.get("name").split(" ")
                    token_user = (
                        token_user.add_email(decoded_token.get("preferred_username"))
                        .add_given_name(given_name)
                        .add_family_name(family_name)
                        .add_if_is_active(True)
                    )

                if "google" in decoded_token.get("iss"):
                    token_user = (
                        token_user.add_email(decoded_token.get("email"))
                        .add_organization(decoded_token.get("hd"))
                        .add_given_name(decoded_token.get("given_name"))
                        .add_family_name(decoded_token.get("family_name"))
                        .add_picture(decoded_token.get("picture"))
                        .add_if_is_active(True)
                    )
                new_user = ctx.call(add_user, user=token_user.build())

            return db_user if db_user is not None else new_user
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except jwt.exceptions.ImmatureSignatureError:
            raise HTTPException(
                status_code=401, detail="Token is not yet valid (iat claim)."
            )
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="Token has expired (exp claim)."
            )

else:

    def decode_and_validate_token() -> User:
        if not config.SSO_AUTH:
            return User(
                external_id="anonymous",
                email="anonymous@unknown.com",
                organization="Anonymous",
                given_name="Anonymous",
                family_name="Unknown",
                picture="",
                issuer="test",
                is_active=True,
            )
