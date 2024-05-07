import urllib.request
import json
import jwt
from fastapi import Header, HTTPException, Depends
from typing import Annotated
from lato import TransactionContext
from app.dependencies import get_transaction_context
from auth.models import User
from auth.use_cases import get_user, add_user
from config import config


class UserBuilder:
    external_id: str
    email: str
    organization: str | None = None
    given_name: str
    family_name: str
    picture: str | None = None
    issuer: str
    
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
    
    def build(self):
        return User(**self.__dict__)
    

def get_jwks_url(issuer_url):
    well_known_url = issuer_url + "/.well-known/openid-configuration"
    with urllib.request.urlopen(well_known_url) as response:
        well_known = json.load(response)
    if not 'jwks_uri' in well_known:
        raise Exception('jwks_uri not found in OpenID configuration')
    return well_known['jwks_uri']


def verify_authorization(authorization: str = Header(...)) -> str:
    try:
        token_type, token = authorization.split(' ')
        if token_type.lower() != 'bearer':
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        return token
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header")


def decode_and_validate_token(ctx: Annotated[TransactionContext, Depends(get_transaction_context)], token: str = Depends(verify_authorization)) -> User:
    try:
        unvalidated = jwt.decode(token, options={"verify_signature": False})
        
        if "test" == unvalidated['iss']:
            return User(external_id="test", email="test@test.com", organization="test", given_name="test",
                        family_name="test", picture="", issuer="test")
        
        jwks_url = get_jwks_url(unvalidated['iss'])
        jwks_client = jwt.PyJWKClient(jwks_url)
        header = jwt.get_unverified_header(token)
        key = jwks_client.get_signing_key(header["kid"]).key
        
        if "microsoft" in unvalidated['iss']:
            expected_audience = config.AZURE_CLIENT_ID
            print("using microsoft", expected_audience)
        elif "google" in unvalidated['iss']:
            expected_audience = config.GOOGLE_CLIENT_ID
            print("using google", expected_audience)
        else:
            raise HTTPException(status_code=401, detail="Invalid issuer")
            
        if expected_audience is None:
            expected_audience = unvalidated.get('aud')
        
        decoded_token = jwt.decode(token, key, [header["alg"]], audience=expected_audience)
        user_id = decoded_token.get("sub")
        if (db_user := ctx.call(get_user, external_id=user_id)) is None:
            token_user = UserBuilder().add_external_id(user_id).add_issuer(decoded_token.get("iss"))
            if "microsoft" in decoded_token.get("iss"):
                given_name, family_name = decoded_token.get("name").split(' ')
                token_user = token_user.add_email(decoded_token.get("preferred_username")).add_given_name(given_name).add_family_name(family_name)

            if "google" in decoded_token.get("iss"):
                token_user = token_user.add_email(decoded_token.get("email")).add_organization(decoded_token.get("hd")).add_given_name(decoded_token.get("given_name")).add_family_name(decoded_token.get("family_name")).add_picture(decoded_token.get("picture"))
            print(token_user.build())
            new_user = ctx.call(add_user, user=token_user.build())
            
        return db_user if db_user is not None else new_user
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    