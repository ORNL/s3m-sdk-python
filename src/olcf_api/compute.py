import json
import requests

from typing import List, Tuple

from .client import OLCFAPIClient

class ComputeService:

    def __init__(self, cluster_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._cluster_name = cluster_name
        self._service_url = f'{api_client.base_url}/slurm/v0.0.42/{cluster_name}'

    def get_system_status(self) -> Tuple[bool, str]:
        status_url = f'{self._client.base_url}/olcf/v1alpha/status/{self._cluster_name}'

        response = requests.get(url=status_url)
        if response:
            status_response = response.json()
            #print(f'DEBUG: {self._cluster_name} status - {json.dumps(status_response, indent=4)}')
            status = json.dumps(status_response, indent=4)
            return True, status
        else:
            error = f'GET from {status_url} failed - {response.reason} ({response.status_code})'
            print(f'ERROR: {error}')
            return False, error
        
    def get_queue_status(self, queue_name : str) -> Tuple[bool, str]:
        status_url = f'{self._service_url}/partitions'

        response = requests.get(url=status_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            qstatus = "UNKNOWN"
            list_response = response.json()
            if "partitions" in list_response:
                partitions = list_response["partitions"]
                for part in partitions:
                    #print(f'DEBUG: partition info - {json.dumps(part, indent=4)}')
                    if part["name"] == queue_name:
                        #print(f'DEBUG: found {queue_name} partition')
                        qstatus = json.dumps(part["partition"]["state"][0])
                        break
            
            return True, qstatus
        else:
            error = f'GET from {status_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def list_jobs(self) -> Tuple[bool, str]:
        list_url = f'{self._service_url}/jobs'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            list_response = response.json()
            job_list = list_response["jobs"]
            jobs = json.dumps(job_list, indent=4)
            print(f'DEBUG: Slurm Jobs on {self._cluster_name} - {jobs}')
            return True, jobs
        else:
            error = f'GET from {list_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def list_queues(self) -> Tuple[bool, str]:
        list_url = f'{self._service_url}/partitions'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            list_response = response.json()
            partitions = list_response["partitions"]
            names : str = ""
            for part in partitions:
                part_name = json.dumps(part["name"])
                names += f'{part_name} '
            print(f'DEBUG: Slurm Queues on {self._cluster_name} - {names}')
            return True, names
        else:
            error = f'GET from {list_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error
    
    def submit_job(self,
                   project : str,
                   workdir : str,
                   job_name : str,
                   job_queue : str,
                   script_contents : str = None,
                   time_minutes : int = 1,
                   node_count : int = 1,
                   env_vars : List[str] = None) -> Tuple[bool, str]:

        submit_url = f'{self._service_url}/job/submit'
        
        ev_json_list = "[]"
        if env_vars:
            ev_json_list = json.dumps(env_vars)

        time_seconds = 60 * time_minutes

        job_template = \
'''{{
   "job": {{
        "script": "{contents}",
        "name": "{job_name}",
        "account": "{account}",
        "partition": "{queue}",
        "current_working_directory": "{cwd}",
        "environment": {env},
        "nodes": "{nodes}",
        "time_limit": {{
            "number": {walltime},
            "set": true
        }}
    }}
}}'''
        escaped_contents = script_contents.replace('"', '\\"')
        escaped_contents = escaped_contents.replace('\n', '\\n')
        submit_request_str = job_template.format(contents=escaped_contents,
                                                 job_name=job_name,
                                                 account=project,
                                                 queue=job_queue,
                                                 cwd=workdir,
                                                 env=ev_json_list,
                                                 nodes=str(node_count),
                                                 walltime=str(time_seconds))
        #print(f'DEBUG: POST\n{submit_request_str}\n')
        submit_request = submit_request_str.encode()
        
        response = requests.post(url=submit_url, data=submit_request,
                                 headers={"Authorization": f'{self._client.api_token}', "Content-Type": "application/json"})
        if response:
            submit_response = response.json()
            submit_details = json.dumps(submit_response)
            #print(f'DEBUG: submit response\n{submit_details}')
            jobid = json.dumps(submit_response["job_id"])
            return True, jobid
        else:
            error = f'POST to {submit_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def cancel_job(self, jobid : str) -> Tuple[bool, str]:
        job_url = f'{self._service_url}/job/{jobid}'
        
        response = requests.delete(url=job_url,
                                   headers={"Authorization": f'{self._client.api_token}'})
        if response:
            return True, ""
        else:
            error = f'DELETE {job_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error

    def get_job_info(self, jobid : str) -> Tuple[bool, str]:
        job_url = f'{self._service_url}/job/{jobid}'
        
        response = requests.get(url=job_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            job_response = response.json()
            job_info = job_response["jobs"][0]
            info = json.dumps(job_info, indent=4)
            return True, info
        else:
            error = f'GET from {job_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error
        
    def get_job_status(self, jobid : str) -> Tuple[bool, str]:
        job_url = f'{self._service_url}/job/{jobid}'
        
        response = requests.get(url=job_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            job_response = response.json()
            job_info = job_response["jobs"][0]
            status = json.dumps(job_info["state"]["current"])
            return True, status
        else:
            error = f'GET from {job_url} failed - {response.reason} ({response.status_code}) - {response.json()}'
            print(f'ERROR: {error}')
            return False, error
