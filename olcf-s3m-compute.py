#!/usr/bin/env python3

import argparse

from pathlib import Path
from os import getenv

from olcf_api.client import OLCFAPIClient
from olcf_api.compute import ComputeService

def list_jobs(service : ComputeService):
    print('++++ OLCF S3M - Compute Job Orchestration ++++ Listing Jobs')
    success, msg = service.list_jobs()
    if success:
        print(msg)
    print('\n\n')

def show(service : ComputeService):
    print(f'++++ OLCF S3M - Compute Job Orchestration ++++ Showing Compute System Status')
    success, msg = service.get_status()
    if success:
        print(msg)
    print('\n\n')

def submit(service : ComputeService,
           job_script : str,
           queue : str,
           project : str,
           workdir : str,
           nodes : int = 1,
           walltime : int = 5):
    print(f'++++ OLCF S3M - Compute Job Orchestration ++++ Submitting a {nodes}-node Job')
    
    jobfile = Path(job_script)
    if jobfile.exists() and jobfile.is_file():
        jobname = jobfile.stem
        jobscript = jobfile.read_text()
    jobenv = ["EXAMPLE_VARIABLE_1=test1", "EXAMPLE_VARIABLE_2=/some/interesting/path"]
    success, msg = service.submit_job(project=project,
                                      workdir=workdir,
                                      job_name=jobname,
                                      job_queue=queue,
                                      script_contents=jobscript,
                                      time_minutes=walltime,
                                      node_count=nodes,
                                      env_vars=jobenv)
    if success:
        print(f'{msg}\n\n')
    print('\n\n')

def info(service : ComputeService, job_id : str):
    print('++++ OLCF S3M - Compute Job Orchestration ++++ Getting Job Information')
    success, msg = service.get_job_info(jobid=job_id)
    if success:
        print(msg)
    print('\n\n')


def main(args):
    #print("DEBUG: Arguments\n", args)

    my_system_name = args.system
    my_queue = args.queue
    my_job = args.job
    
    my_api_client = OLCFAPIClient(api_token=getenv("OLCF_API_TOKEN", "InvalidToken"))
    my_project = getenv("OLCF_API_PROJECT", "InvalidProject")
    my_workdir = getenv("OLCF_API_WORKDIR", str(Path.cwd()))
    
    my_comp_service = ComputeService(cluster_name=my_system_name,
                                     api_client=my_api_client)
    if args.jobinfo:
        info(my_comp_service, my_job)
    elif args.joblist:
        list_jobs(my_comp_service)
    elif args.submit:
        submit(service=my_comp_service,
               job_script=my_job,
               queue=my_queue,
               project=my_project,
               workdir=my_workdir)
    else:
        show(my_comp_service)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('olcf-s3m-compute')
    parser.add_argument('-i', '--jobinfo', help='get information about a specific job', action='store_true')
    parser.add_argument('-l', '--joblist', help='list compute jobs for system', action='store_true')
    parser.add_argument('-s', '--submit', help='submit a job to the system', action='store_true')
    parser.add_argument('system', nargs='?', help='name of the target HPC system', default='defiant')
    parser.add_argument('queue', nargs='?', help='job queue to use on the target system', default='batch')
    parser.add_argument('job', nargs='?', help='job script file to submit or existing job id', default='invalid')
    args = parser.parse_args()
    main(args)
