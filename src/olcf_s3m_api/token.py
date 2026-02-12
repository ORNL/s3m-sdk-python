import json

from typing import Tuple

from .request import S3MRequest
from .error import S3MError
from .client import OLCFAPIClient

class TokenInfo:
    def set_values(self, info):
        self.username = info['username']
        self.project = info['project']
        self.permissions = info['permissions']
        self.plannedExpiration = info['plannedExpiration']
        self.securityEnclave = info['securityEnclave']
        self.description = info['description']
        self.oneTimeToken = info['oneTimeToken']
        self.delayedStart = info['delayedStart']
        self.delayDate = info['delayDate']
        self.ownerName = info['ownerName']
        self.grpcPermissions = info['grpcPermissions']

    def msg(self):
        msg = f'username: {self.username} \n'
        msg +=  f'project: {self.project} \n'
        msg +=  f'permissions: {self.permissions} \n'
        msg +=  f'projeplannedExpirationct: {self.plannedExpiration} \n'
        msg +=  f'securityEnclave: {self.securityEnclave} \n'
        msg +=  f'description: {self.description} \n'
        msg +=  f'oneTimeToken: {self.oneTimeToken} \n'
        msg +=  f'delayedStart: {self.delayedStart} \n'
        msg +=  f'delayDate: {self.delayDate} \n'
        msg +=  f'ownerName: {self.ownerName} \n'
        msg +=  f'grpcPermissions: {self.grpcPermissions}'

        return msg

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
            self._token_info = token_response["token"]

            token_info = TokenInfo()
            token_info.set_values(self._token_info)

            return True, token_info
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
