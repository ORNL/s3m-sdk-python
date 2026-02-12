# Overview

This repository contains the `olcf_s3m_api` library of python modules wrapping the
OLCF's Secure Scientific Service Mesh (S3M) REST APIs, and a collection of python command-line tools that make it easy to test the library and interact with S3M.

For more information on the available S3M APIs, please visit https://docs.olcf.ornl.gov/services_and_applications/s3m/api/

# General Usage
One command-line tool can be run within the SDK without an access token. It can be used to provide status information about a specific cluster or about all available clusters. The following shows how to do either function:

## olcf-s3m-status.py

``` bash
> python3 olcf-s3m-status.py -c defiant
++++ OLCF S3M - Compute Job Orchestration ++++ Getting Compute System Status for Defiant
name: defiant 
description: Defiant 
systemType: resource 
securityEnclave: open 
organization: olcf 
status: OPERATIONAL 
annotations: {} 
downtimeScheduleAvailable: False 
upcomingDowntimes: [] 
retrievedAt: 2026-02-12T14:30:03Z

> python3 olcf-s3m-status.py
++++ OLCF S3M - Compute Job Orchestration ++++ Getting Compute System Status
name: defiant 
description: Defiant 
systemType: resource 
securityEnclave: open 
organization: olcf 
status: OPERATIONAL 
annotations: {} 
downtimeScheduleAvailable: False 
upcomingDowntimes: [] 
retrievedAt: 2026-02-12T14:30:03Z

name: wombat 
description: ARM86 Computational Resource 
systemType: resource 
securityEnclave: open 
organization: olcf 
status: OPERATIONAL 
annotations: {} 
downtimeScheduleAvailable: False 
upcomingDowntimes: [] 
retrievedAt: 2026-02-12T14:30:03Z

name: quokka 
description: ACE Intel-based CPU-only system 
systemType: resource 
securityEnclave: open 
organization: olcf 
status: OPERATIONAL 
annotations: {} 
downtimeScheduleAvailable: False 
upcomingDowntimes: [] 
retrievedAt: 2026-02-12T14:30:03Z

name: andes 
description: general purpose data analysis cluster 
systemType: resource 
securityEnclave: moderate 
organization: olcf 
status: OPERATIONAL 
annotations: {} 
downtimeScheduleAvailable: True 
upcomingDowntimes: [] 
retrievedAt: 2026-02-12T14:30:03Z

name: frontier 
description: Frontier HPE Cray EX325a 
systemType: resource 
securityEnclave: moderate 
organization: olcf 
status: OPERATIONAL 
annotations: {} 
downtimeScheduleAvailable: True 
upcomingDowntimes: [] 
retrievedAt: 2026-02-12T14:30:03Z
```

All other command-line tools within the SDK assume you have already acquired an OLCF API access token as described in the 'Getting Started' section of the S3M docs.

You should set the value of the `olcf_s3m_api_TOKEN` environment variable to your token string.

``` bash
export olcf_s3m_api_TOKEN="abcDEFxyZ123..."
```

If you intend to use the `olcf-s3m-compute.py` tool, you will additionally need to set the `olcf_s3m_api_PROJECT` and `olcf_s3m_api_WORKDIR` environment variables to the appropriate values for submitting jobs to the OLCF ACE Defiant machine (see [here](https://docs.olcf.ornl.gov/ace_testbed/defiant_quick_start_guide.html)). For example, assuming an OLCF Open project id of 'CSC123' and a job working directory within the project-shared area on the Lustre filesystem, you could use the following settings:

``` bash
export olcf_s3m_api_PROJECT="csc123"
export olcf_s3m_api_WORKDIR="/lustre/polis/csc123/proj-shared"
```

## olcf-s3m-token.py

1. Display current token (as set in `olcf_s3m_api_TOKEN`)

    ``` bash
    > python3 olcf-s3m-token.py
    ++++ OLCF S3M - Token Management ++++ Displaying Token
    OLCF S3M API Token: abcDEFxyZ123...
    ```

2. Get token details

    ``` bash
    > python3 olcf-s3m-token.py --info
    ++++ OLCF S3M - Token Management ++++ Querying Token Details
    username: stf053_auser 
    project: stf053 
    permissions: ['data-streaming', 'compute-ace'] 
    projeplannedExpirationct: 2026-02-13T12:24:51.227709Z 
    securityEnclave: open 
    description: kbc-s3m-token 
    oneTimeToken: False 
    delayedStart: False 
    delayDate: None 
    ownerName: campbellkb 
    grpcPermissions: []
    ```

3. Revoke current token

    ``` bash
    > python3 olcf-s3m-token.py --revoke
    ++++ OLCF S3M - Token Management ++++ Revoking Token
    ```

## olcf-s3m-compute.py

1. Get compute system status for Defiant

    ``` bash
    > python3 olcf-s3m-compute.py defiant
    ++++ OLCF S3M - Compute Job Orchestration ++++ Getting Compute System Status
    name: defiant 
    description: Defiant 
    systemType: resource 
    securityEnclave: open 
    organization: olcf 
    status: OPERATIONAL 
    annotations: {} 
    downtimeScheduleAvailable: False 
    upcomingDowntimes: [] 
    retrievedAt: 2026-02-12T14:30:03Z
    ```

2. Get a list of compute queues for Defiant

    ``` bash
    > python3 olcf-s3m-compute.py --queuelist defiant
    ++++ OLCF S3M - Compute Job Orchestration ++++ Listing Queues
    ['batch-cpu', 'batch-gpu', 'cron']
    ```

3. Submit a job to the `batch-cpu` queue on Defiant using 2 nodes with walltime of 4 minutes

    ``` bash
    > python3 olcf-s3m-compute.py --submit defiant batch-cpu ./tests/defiant-job.slurm 2 4
    ++++ OLCF S3M - Compute Job Orchestration ++++ Submitting a 2-node Job
    8149
    ```

4. Get job details for the submitted job on Defiant

    ``` bash
    > python3 olcf-s3m-compute.py defiant batch-cpu 8149
    ++++ OLCF S3M - Compute Job Orchestration ++++ Getting Job Information
    {
        "account": "csc123",
        "comment": {
            "administrator": "",
            "job": "",
            "system": ""
        },
        "allocation_nodes": 2,
        "array": {
            "job_id": 0,
            "task_id": {
                "set": false,
                "infinite": false,
                "number": 0
            },
            "task": "",
            "limits": {
                "max": {
                    "running": {
                        "tasks": 0
                    }
                }
            }
        },
        ...
    }
    ```
# Development

Prerequisites:
  - [uv][uv-docs] is suggested to use for package management

To setup development environment using `uv`
```
uv pip install -e .
```

To run tests:
```
uv run pytest tests/
```

[uv-docs]: https://astral.sh/blog/uv-unified-python-packaging
[olcf-s3m-api-docs]: https://s3m.apps.olivine.ccs.ornl.gov/docs/
