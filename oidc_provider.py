from requests import auth, get, post
from requests.models import HTTPError
from jwt import get_unverified_header, decode, PyJWKClient
from typing import List, Union
import json
class OIDCProvider:

    def __init__(self, client_id: str, client_secret: str, auth_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        resp = get(f'{auth_uri}/.well-known/openid-configuration')
        oidc_config = resp.json()
        self.token_endpoint = oidc_config['token_endpoint']
        self.jwks_client = PyJWKClient(oidc_config['jwks_uri'])
        self.userinfo_endpoint = oidc_config['userinfo_endpoint']

    def get_token(self, code: str, redirect_uri: str) -> str:
        resp = post(
            self.token_endpoint, 
            auth = (self.client_id, self.client_secret),
            data = {
               'grant_type': 'authorization_code',
               'code': code,
               'redirect_uri': redirect_uri            }
        )
        print(resp.status_code)
        return ''
    
    def decode_token(self, token: str, algos: List[str] = ['RS256']) -> Union[dict, bool]:
        try:
            claims = decode(token, self.jwks_client.get_signing_key_from_jwt(token).key, algorithms=algos)
            return claims
        except Exception:
            return False