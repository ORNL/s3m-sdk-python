import json
import requests

from typing import Tuple

from .error import S3MError, AuthenticationError
from .client import OLCFAPIClient

class TokenService:

    def __init__(self, api_client : OLCFAPIClient):
        self._client = api_client
        self._service_url = f'{api_client.base_url}/olcf/v1/token'

    def get_token_hash(self) -> str:
        return self._client.api_token

    def get_token_info(self) -> Tuple[bool, str]:
        token_url = f'{self._service_url}/ctls/introspect'
        
        response = requests.get(url=token_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            token_response = response.json()
            self._token_info = json.dumps(token_response["token"], indent=4)
            #print(f'DEBUG: Token {self._client.api_token}\n{self._token_info}')
            return True, self._token_info
        else:
            raise AuthenticationError(f'GET from {token_url} failed - {response.status_code}')

    def revoke_token(self) -> Tuple[bool, str]:
        revoke_url = f'{self._service_url}/ctls/revoke'

        response = requests.delete(url=revoke_url,
                                   headers={"Authorization": f'{self._client.api_token}'})
        if response:
            return True, None
        else:
            raise AuthenticationError(f'DELETE {revoke_url} failed - {response.status_code}')
