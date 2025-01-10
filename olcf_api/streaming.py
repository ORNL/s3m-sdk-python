import json
import requests

from .client import OLCFAPIClient

class StreamingService:

    def __init__(self, service_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._service_name = service_name
        self._service_url = f'{api_client.base_url}/v1alpha/streaming/{service_name}'
        self._cluster_name = "unknown"
        self._cluster_provisioned = False

    def list_services(self):
        list_url = f'{self._client.base_url}/v1alpha/streaming/list_backends'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            service_list = response.json()
            services = json.dumps(service_list["backends"], indent=4)
            print(f'INFO: Available Streaming Services\n{services}')
            return True
        else:
            print(f'GET from {list_url} failed - {response.status_code}')
            return False

    def start_cluster(self,
                      cluster_name : str,
                      node_count : int = 1,
                      cpu_count : int = 4,
                      ram_gib : int = 4) -> bool:
        
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
            return True
        else:
            print(f'POST to {provision_url} failed - {response.status_code}')
            return False

    def get_cluster_info(self, cluster_name : str) -> bool:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'
        
        response = requests.get(url=cluster_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_info = response.json()
            self._cluster_info = json.dumps(cluster_info["cluster"], indent=4)
            print(f'INFO: {self._service_name} Cluster Deployment\n{self._cluster_info}')
            self._cluster_name = cluster_name
            return True
        else:
            print(f'GET from {cluster_url} failed - {response.status_code}')
            return False

    def stop_cluster(self, cluster_name : str) -> bool:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'

        response = requests.delete(url=cluster_url,
                                   headers={"Authorization": f'{self._client.api_token}'})
        if response:
            shutdown_details = json.dumps(response.json(), indent=4)
            print(f'INFO: {self._service_name} Cluster Shutdown\n{shutdown_details}')
            return True
        else:
            print(f'DELETE {cluster_url} failed - {response.status_code}')
            return False

    def list_clusters(self) -> bool:
        list_url = f'{self._service_url}/list_clusters'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_list = response.json()
            clusters = json.dumps(cluster_list["clusters"], indent=4)
            print(f'INFO: Existing {self._service_name} Clusters\n{clusters}')
            return True
        else:
            print(f'GET from {list_url} failed - {response.status_code}')
            return False
