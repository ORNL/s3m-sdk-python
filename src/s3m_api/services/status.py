import json
import requests

from typing import List, Tuple

#from .client import OLCFAPIClient

class StatusService:

    def __init__(self):
        self.base_url = 'https://s3m.apps.olivine.ccs.ornl.gov'
        # self._client = api_client
        # self._cluster_name = cluster_name
        # self._service_url = f'{api_client.base_url}/slurm/v0.0.42/{cluster_name}'


    def get_system_status(self, cluster_name: str) -> dict:
        """Fetch system status for a given cluster. Raises on failure."""
        status_url = f'{self.base_url}/olcf/v1alpha/status/{cluster_name}'

        try:
            response = requests.get(status_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to fetch status for {cluster_name}: {e}')
