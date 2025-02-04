import json
import requests
import time

from dataclasses import dataclass
from typing import Dict, List, Tuple, Union

from .client import OLCFAPIClient

@dataclass
class StreamingServiceDeployment:
    service_name      : str
    service_ports     : Dict[str, int]
    cluster_name      : str
    cluster_hosts     : List[str]
    cluster_resources : Dict[str, str]
    auth_user         : str
    auth_pass         : str

class StreamingService:

    def __init__(self, service_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._service_name = service_name
        self._service_url = f'{api_client.base_url}/olcf/v1alpha/streaming/{service_name}'
        self._cluster_name = "unknown"
        self._cluster_provisioned = False

    def list_services(self) -> Tuple[bool, str]:
        list_url = f'{self._client.base_url}/olcf/v1alpha/streaming/list_backends'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            service_list = response.json()
            services = json.dumps(service_list["backends"], indent=4)
            return True, services
        else:
            error = f'GET from {list_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def start_cluster(self,
                      cluster_name : str,
                      wait_for_healthy : bool = False,
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
    "resourceSettings": {{
        "cpus": {cpus},
        "ram-gbs": {ram},
        "nodes": {nodes}
    }}
}}'''
        provision_request_str = provision_template.format(kind=cluster_kind,
                                                          cluster=cluster_name,
                                                          nodes=node_count,
                                                          cpus=cpu_count,
                                                          ram=ram_gib)
        #print(f'DEBUG: POST\n{provision_request_str}\n')
        provision_request = provision_request_str.encode()

        response = requests.post(url=provision_url, data=provision_request,
                                 headers={"Authorization": f'{self._client.api_token}', "Content-Type": "application/json"})
        #print(f'DEBUG: response\n{response.json()}\n')
        if response:
            provision_details = json.dumps(response.json(), indent=4)
            print(f'DEBUG: provision response\n{provision_details}')
            self._cluster_name = cluster_name
            self._cluster_provisioned = True

            if wait_for_healthy:
                self._cluster_healthy = False
                timeout = 60
                waited = 0
                while not self._cluster_healthy:
                    rc, info = self.get_cluster_info(cluster_name)
                    if rc:
                        cluster_info = json.loads(info)
                        if cluster_info["healthStatus"] == "healthy":
                            self._cluster_healthy = True
                        else:
                            time.sleep(5)
                            waited += 5
                            if waited >= timeout:
                                break
                    else:
                        break

            return True, provision_details
        else:
            error = f'POST to {provision_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def get_cluster_info(self, cluster_name : str) -> Tuple[bool, str]:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'

        response = requests.get(url=cluster_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_response = response.json()
            self._cluster_info = json.dumps(cluster_response["cluster"], indent=4)
            self._cluster_name = cluster_name
            return True, self._cluster_info
        else:
            error = f'GET from {cluster_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def get_cluster_deployment(self, cluster_name : str) -> Union[StreamingServiceDeployment, None]:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'

        response = requests.get(url=cluster_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_response = response.json()
            if "cluster" not in cluster_response:
                error = f'Failed to extract cluster information using key "cluster" from response: {cluster_response}'
                print(f'ERROR: {error}')
                return None

            self._cluster_info = json.dumps(cluster_response["cluster"], indent=4)

            hosts = None
            ports = None
            endpoints_key = "brokerEndpoints" if self._service_name == "rabbitmq" else "endpoints"
            if endpoints_key in cluster_response["cluster"]:
                endpoints = cluster_response["cluster"][endpoints_key]
                hosts = endpoints["addresses"]
                ports = endpoints["ports"]
            elif self._service_name == "rabbitmq":
                if "amqpsUrl" in cluster_response["cluster"]:
                    url : str = cluster_response["cluster"]["amqpsUrl"]
                    url_parts = url.split('@')
                    if len(url_parts) == 2:
                        hostport = url_parts[1].split(':')
                        hosts = [ hostport[0] ]
                        ports = dict()
                        ports["amqps"] = int(hostport[1])


            user = None
            if "username" in cluster_response["cluster"]:
                user = cluster_response["cluster"]["username"]

            passwd = None
            if "password" in cluster_response["cluster"]:
                passwd = cluster_response["cluster"]["password"]

            resources = None
            if "resourceSettings" in cluster_response["cluster"]:
                resources = cluster_response["cluster"]["resourceSettings"]

            self._deployment = StreamingServiceDeployment(service_name=self._service_name,
                                                          service_ports=ports,
                                                          cluster_name=cluster_name,
                                                          cluster_hosts=hosts,
                                                          cluster_resources=resources,
                                                          auth_user=user, auth_pass=passwd)

            return self._deployment
        else:
            error = f'GET from {cluster_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return None

    def stop_cluster(self, cluster_name : str) -> Tuple[bool, str]:
        cluster_url = f'{self._service_url}/cluster/{cluster_name}'

        response = requests.delete(url=cluster_url,
                                   headers={"Authorization": f'{self._client.api_token}'})
        if response:
            shutdown_details = json.dumps(response.json(), indent=4)
            shutdown_info = f'INFO: {self._service_name} Cluster Shutdown\n{shutdown_details}'
            return True, shutdown_info
        else:
            error = f'DELETE {cluster_url} failed - {response.reason} ({response.status_code})'
            print(f'ERROR: {error}')
            return False, error

    def list_clusters(self) -> Tuple[bool, str]:
        list_url = f'{self._service_url}/list_clusters'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            cluster_list = response.json()
            clusters = json.dumps(cluster_list["clusters"], indent=4)
            return True, clusters
        else:
            error = f'GET from {list_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error
