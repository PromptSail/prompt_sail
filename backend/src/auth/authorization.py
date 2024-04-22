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
        jwks_url = get_jwks_url(unvalidated['iss'])
        jwks_client = jwt.PyJWKClient(jwks_url)
        header = jwt.get_unverified_header(token)
        key = jwks_client.get_signing_key(header["kid"]).key
        if (expected_audience := config.CLIENT_ID) is None:
            expected_audience = unvalidated.get('aud')
        decoded_token = jwt.decode(token, key, [header["alg"]], audience=expected_audience)
        user_id = decoded_token.get("sub")
        if (db_user := ctx.call(get_user, external_id=user_id)) is None:
            token_user = User(
                external_id=decoded_token.get("sub"),
                email=decoded_token.get("email"),
                given_name=decoded_token.get("given_name"),
                family_name=decoded_token.get("family_name"),
                picture=decoded_token.get("picture"),
                issuer=decoded_token.get("iss")
            )
            new_user = ctx.call(add_user, user=token_user)
            
        return db_user if db_user is not None else new_user
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
    