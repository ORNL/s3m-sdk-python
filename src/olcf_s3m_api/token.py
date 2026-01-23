import json

from typing import Tuple

from .request import S3MRequest
from .error import S3MError
from .client import OLCFAPIClient

class TokenService:

    def __init__(self, api_client : OLCFAPIClient):
        self._client = api_client
        self._service_url = f'{api_client.base_url}/olcf/v1/token'

    def get_token_hash(self) -> str:
        return self._client.api_token

    def get_token_info(self) -> Tuple[bool, str]:
        token_url = f'{self._service_url}/ctls/introspect'
        
        client = S3MRequest()
        response = client.get(url=token_url,
                              headers={"Authorization": f'{self._client.api_token}'})
        if response:
            token_response = response.json()
            self._token_info = json.dumps(token_response["token"], indent=4)
            return True, self._token_info
        else:
            raise S3MError(f'GET from {token_url} failed - {response.status_code}')

    def revoke_token(self) -> Tuple[bool, str]:
        revoke_url = f'{self._service_url}/ctls/revoke'

        client = S3MRequest()
        response = client.delete(url=revoke_url,
                                 headers={"Authorization": f'{self._client.api_token}'})
        if response:
            return True, None
        else:
            raise S3MError(f'DELETE {revoke_url} failed - {response.status_code}')
