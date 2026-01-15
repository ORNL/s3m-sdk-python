import requests

class StatusService:
    def __init__(self):
        self.base_url = 'https://s3m.olcf.ornl.gov'

    def get_system_status(self, cluster_name: str) -> dict:
        """Fetch system status for a given cluster. Raises on failure."""
        status_url = f'{self.base_url}/olcf/v1alpha/status/{cluster_name}'

        try:
            response = requests.get(status_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to fetch status for {cluster_name}: {e}')
    
    def get_all_systems_status(self) -> dict:
        """Fetch status of all systems. Raises on failure."""
        status_url = f'{self.base_url}/olcf/v1alpha/status'

        try:
            response = requests.get(status_url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to fetch status for all systems.')