import json
import requests

from typing import List, Tuple

from .client import OLCFAPIClient

class ComputeService:

    def __init__(self, cluster_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._cluster_name = cluster_name
        self._service_url = f'{api_client.base_url}/slurm/v0.0.42/{cluster_name}'

    def get_status(self) -> Tuple[bool, str]:
        status_url = f'{self._client.base_url}/v1alpha/status/{self._cluster_name}'

        response = requests.get(url=status_url)
        if response:
            status = json.dumps(response.json(), indent=4)
            return True, status
        else:
            error = f'GET from {status_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error

    def list_jobs(self) -> Tuple[bool, str]:
        list_url = f'{self._service_url}/jobs'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            job_list = response.json()
            jobs = json.dumps(job_list["jobs"], indent=4)
            print(f'INFO: Slurm Jobs on {self._cluster_name}\n{jobs}')
            return True, jobs
        else:
            error = f'GET from {list_url} failed - {response.status_code}'
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

        time_seconds = time_minutes * 60

        job_template = \
'''{{
   "job": {{
        "script": "{contents}",
        "name": "{job_name}",
        "account": "{account}",
        "partition": "{queue}",
        "current_working_directory": {cwd},
        "environment": {env},
        "nodes": "{nodes}",
        "time_limit": {{
            "number": {walltime},
            "set": true
        }}
    }}
}}'''
        submit_request_str = job_template.format(contents=script_contents,
                                                 job_name=job_name,
                                                 account=project,
                                                 queue=job_queue,
                                                 cwd=workdir,
                                                 env=ev_json_list,
                                                 nodes=node_count,
                                                 walltime=time_seconds)
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
            error = f'POST to {submit_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error

    def get_job_info(self, jobid : str) -> Tuple[bool, str]:
        cluster_url = f'{self._service_url}/job/{jobid}'
        
        response = requests.get(url=cluster_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            job_info = response.json()
            info = json.dumps(job_info["jobs"], indent=4)
            return True, info
        else:
            error = f'GET from {cluster_url} failed - {response.status_code}'
            print(f'ERROR: {error}')
            return False, error
