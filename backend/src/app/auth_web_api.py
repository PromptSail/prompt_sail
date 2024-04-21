from fastapi import Request, Header, HTTPException, Depends, Security
import urllib.request
import json
import jwt
from starlette.responses import JSONResponse

from .app import app


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
    

def decode_and_validate_token(token: str = Depends(verify_authorization), expected_audience=None):
    try:
        unvalidated = jwt.decode(token, options={"verify_signature": False})
        jwks_url = get_jwks_url(unvalidated['iss'])
        jwks_client = jwt.PyJWKClient(jwks_url)
        header = jwt.get_unverified_header(token)
        key = jwks_client.get_signing_key(header["kid"]).key
        if expected_audience is None:
            expected_audience = unvalidated.get('aud')
        return jwt.decode(token, key, [header["alg"]], audience=expected_audience)
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid token")
        

@app.get('/api/auth/whoami', dependencies=[Security(decode_and_validate_token)])
def whoami(request: Request, user_info: dict = Depends(decode_and_validate_token)):
    return JSONResponse(content=user_info)
