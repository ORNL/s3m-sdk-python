import json
import requests

from typing import List, Tuple

from .client import OLCFAPIClient

class StreamingService:

    def __init__(self, service_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._service_name = service_name
        self._service_url = f'{api_client.base_url}/v1alpha/streaming/{service_name}'
        self._cluster_name = "unknown"
        self._cluster_provisioned = False

    def list_services(self) -> Tuple[bool, str]:
        list_url = f'{self._client.base_url}/v1alpha/streaming/list_backends'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            service_list = response.json()
            services = json.dumps(service_list["backends"], indent=4)
            services_info = f'INFO: Available Streaming Services\n{services}'
            return True, services_info
        else:
            error = f'GET from {list_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error

    def start_cluster(self,
                      cluster_name : str,
                      node_count : int = 1,
                      cpu_count : int = 4,
                      ram_gib : int = 4) -> Tuple[bool, str]:
        
        cluster_kind = "general"
        if self._service_name == "redis":
            cluster_kind = "dragonfly-general"

        provision_url = f'{self._service_url}/provision_cluster'
        
        provision_template = \
'''{{
    "kind": "{kind}",
    "name": "{cluster}",
    "resourceSettings": [
        {{
            "nodes": {nodes},
            "cpus": {cpus},
            "ram_gbs": {ram}
        }}
    ]
}}'''
        provision_request_str = provision_template.format(kind=cluster_kind,
                                                          cluster=cluster_name,
                                                          nodes=node_count,
                                                          cpus=cpu_count,
                                                          ram=ram_gib)
        #print(f'DEBUG: POST\n{provision_request_str}\n')
        provision_request = provision_request_str.encode()
        
        response = requests.post(url=provision_url, data=provision_request,
                                 headers={"Authorization": f'{self._client.api_token}'})
        if response:
            provision_details = json.dumps(response.json(), indent=4)
            #print(f'DEBUG: provision response\n{provision_details}')
            self._cluster_name = cluster_name
            self._cluster_provisioned = True
            return True, provision_details
        else:
            error = f'POST to {provision_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error

    def get_cluster_info(self, cluster_name : str) -> bool:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'
        
        response = requests.get(url=cluster_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_response = response.json()
            self._cluster_info = json.dumps(cluster_response["cluster"], indent=4)
            self._cluster_name = cluster_name
            cluster_info = f'INFO: {self._service_name} Cluster Deployment\n{self._cluster_info}'
            return True, cluster_info
        else:
            error = f'GET from {cluster_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error

    def stop_cluster(self, cluster_name : str) -> Tuple[bool, str]:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'

        response = requests.delete(url=cluster_url,
                                   headers={"Authorization": f'{self._client.api_token}'})
        if response:
            shutdown_details = json.dumps(response.json(), indent=4)
            shutdown_info = f'INFO: {self._service_name} Cluster Shutdown\n{shutdown_details}'
            return True, shutdown_info
        else:
            error = f'DELETE {cluster_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error

    def list_clusters(self) -> Tuple[bool, str]:
        list_url = f'{self._service_url}/list_clusters'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_list = response.json()
            clusters = json.dumps(cluster_list["clusters"], indent=4)
            clusters_info = f'INFO: Existing {self._service_name} Clusters\n{clusters}'
            return True, clusters_info
        else:
            error = f'GET from {list_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error
