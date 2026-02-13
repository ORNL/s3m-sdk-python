import requests

class MachineStatus:
    def __init__(self):
        self.status = 'UNSPECIFIED' # Initial valid state
    @property
    def status(self):
        """Get the current machine status."""
        return self._status
    @status.setter
    def status(self, value):
        """Set the machine status with validation"""
        allowed_status_values = ['UNSPECIFIED', 'OPERATIONAL', 'UNAVAILABLE']
        if value not in allowed_status_values:
            raise ValueError(f'Invalid machine status: {value}. Must be one of {allowed_status_values}')
        self._status = value

class Status:
    def set_values(self, info):
        self.name = info['name']
        self.description = info['description']
        self.systemType = info['systemType']
        self.securityEnclave = info['securityEnclave']
        self.organization = info['organization']
        
        ms = MachineStatus()
        ms.status = info['status']
        self.status = ms.status

        self.annotations = info['annotations']
        self.downtimeScheduleAvailable = info['downtimeScheduleAvailable']
        self.upcomingDowntimes = info['upcomingDowntimes']
        self.retrievedAt = info['retrievedAt']

    def msg(self):
        msg = f'name: {self.name} \n'
        msg += f'description: {self.description} \n'
        msg += f'systemType: {self.systemType} \n'
        msg += f'securityEnclave: {self.securityEnclave} \n'
        msg += f'organization: {self.organization} \n'
        msg += f'status: {self.status} \n'
        msg += f'annotations: {self.annotations} \n'
        msg += f'downtimeScheduleAvailable: {self.downtimeScheduleAvailable} \n'
        msg += f'upcomingDowntimes: {self.upcomingDowntimes} \n'
        msg += f'retrievedAt: {self.retrievedAt}'

        return msg

class StatusService:
    def __init__(self):
        self.base_url = 'https://s3m.olcf.ornl.gov'

    def get_system_status(self, cluster_name: str) -> dict:
        """Fetch system status for a given cluster. Raises on failure."""
        status_url = f'{self.base_url}/olcf/v1alpha/status/{cluster_name}'

        try:
            response = requests.get(status_url)
            response.raise_for_status()

            status = Status()
            status.set_values(response.json())

            return status
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to fetch status for {cluster_name}: {e}')
    
    def get_all_systems_status(self) -> dict:
        """Fetch status of all systems. Raises on failure."""
        status_url = f'{self.base_url}/olcf/v1alpha/status'

        try:
            response = requests.get(status_url)
            response.raise_for_status()

            systems = []
            for system in response.json()['resources']:
                status = Status()
                status.set_values(system)

                systems.append(status)

            return systems
        except requests.RequestException as e:
            raise RuntimeError(f'Failed to fetch status for all systems.')