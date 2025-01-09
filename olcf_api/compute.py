import json
import requests

from .client import OLCFAPIClient

class ComputeService:

    def __init__(self, cluster_name : str, api_client : OLCFAPIClient):
        self._client = api_client
        self._cluster_name = cluster_name
        self._service_url = f'{api_client.base_url}/slurm/v0.0.42/{cluster_name}'


    def list_jobs(self):
        list_url = f'{self._service_url}/jobs'

        response = requests.get(url=list_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            job_list = response.json()
            jobs = json.dumps(job_list["jobs"], indent=4)
            print(f'INFO: Slurm Jobs on {self._cluster_name}\n{jobs}')
            return True
        else:
            print(f'GET from {list_url} failed - {response.status_code}')
            return False

    def submit_job(self,
                   project : str,
                   job_name : str,
                   job_queue : str,
                   job_minutes : int = 5,
                   node_count : int = 1,
                   task_count : int = 1,
                   ) -> bool:

        submit_url = f'{self._service_url}/job/submit'
        
        job_template = \
'''{{
 "job": {{
    "script": "{job_script_contents}",
    "name": "{job_name}",
    "account": "{account}",
    "partition": "{queue}",
    "current_working_directory": "/lustre/polis/{account}/proj-shared",
    "environment": ["HELLO=world"],
    "nodes": "{nodes}",
    "tasks": {tasks},
    "time_limit": {{
        "number": {walltime},
        "set":    true
    }}
  }}
}}
'''
        submit_request_str = job_template.format(job_script_contents=???,
                                                 job_name=job_name,
                                                 account=project,
                                                 queue=job_queue,
                                                 nodes=node_count,
                                                 tasks=task_count,
                                                 walltime=job_minutes)
        #print(f'DEBUG: POST\n{submit_request_str}\n')
        submit_request = submit_request_str.encode()
        
        response = requests.post(url=submit_url, data=submit_request,
                                 headers={"Authorization": f'{self._client.api_token}', "Content-Type": "application/json"})
        if response:
            submit_details = json.dumps(response.json(), indent=4)
            #print(f'DEBUG: submit response\n{submit_details}')
            TODO("extract jobid from response")
            return True
        else:
            print(f'POST to {submit_url} failed - {response.status_code}')
            return False

    def get_job_info(self, jobid : str) -> bool:
        cluster_url = f'{self._service_url}/job/{jobid}'
        
        response = requests.get(url=cluster_url,
                                headers={"Authorization": f'{self._client.api_token}'})
        if response:
            job_info = response.json()
            info = json.dumps(job_info["jobs"], indent=4)
            print(f'INFO: {self._cluster_name} Job Details\n{info}')
            return True
        else:
            print(f'GET from {cluster_url} failed - {response.status_code}')
            return False
