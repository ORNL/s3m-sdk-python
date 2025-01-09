import json
import requests

from .client import OLCFAPIClient

class TokenService:

    def __init__(self, service_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._service_url = f'{api_client.base_url}/v1/token'

    def get_token_info(self) -> bool:
        token_url = f'{self._service_url}/ctls/introspect'
        
        response = requests.get(url=token_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            token_info = response.json()
            self._token_info = json.dumps(token_info["token"], indent=4)
            print(f'INFO: Token {self._client.api_token}\n{self._token_info}')
            return True
        else:
            print(f'GET from {token_url} failed - {response.status_code}')
            return False

    def revoke_token(self, cluster_name : str) -> bool:
        revoke_url = f'{self._service_url}/ctls/revoke'

        response = requests.delete(url=revoke_url,
                                   headers={"Authorization": f'{self._client.api_token}'})
        if response:
            return True
        else:
            print(f'DEL {cluster_url} failed - {response.status_code}')
            return False