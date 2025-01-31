<<<<<<< HEAD
# Overview

This repository contains the `olcf_api` library of python modules wrapping the
[OLCF's Secure Scientific Service Mesh (S3M) REST APIs][olcf-s3m-api-docs],
and a collection of python command-line 
tools that make it easy to test the library and interact with S3M.

For more information on the available S3M APIs, please visit https://s3m.apps.olivine.ccs.ornl.gov/docs/

# General Usage

All the command-line tools assume you have already acquired an OLCF API access token as described in the 'Getting Started' section of the S3M docs.

You should set the value of the `OLCF_API_TOKEN` environment variable to your token string.

``` bash
export OLCF_API_TOKEN="abcDEFxyZ123..."
```

If you intend to use the `olcf-s3m-compute.py` tool, you will additionally need to set the `OLCF_API_PROJECT` and `OLCF_API_WORKDIR` environment variables to the appropriate values for submitting jobs to the OLCF ACE Defiant machine (see [here](https://docs.olcf.ornl.gov/ace_testbed/defiant_quick_start_guide.html)). For example, assuming an OLCF Open project id of 'CSC123' and a job working directory within the project-shared area on the Lustre filesystem, you could use the following settings:

``` bash
export OLCF_API_PROJECT="csc123"
export OLCF_API_WORKDIR="/lustre/polis/csc123/proj-shared"
```

## olcf-s3m-token.py

1. Display current token (as set in `OLCF_API_TOKEN`)

    ``` bash
    > python3 olcf-s3m-token.py
    ++++ OLCF S3M - Token Management ++++ Displaying Token
    OLCF S3M API Token: abcDEFxyZ123...
    ```

2. Get token details

    ``` bash
    > python3 olcf-s3m-token.py --info
    ++++ OLCF S3M - Token Management ++++ Querying Token Details
    {
        "username": "csc123_auser",
        "project": "CSC123",
        "scopes": [
            "compute-ace",
            "data-streaming"
        ],
        "plannedExpiration": "2025-02-01T01:04:36.653935Z",
        "securityEnclave": "open",
        "description": "my-token-name",
        "oneTimeToken": false,
        "delayedStart": false,
        "delayDate": null,
        "ownerName": "somebody"
    }
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
    {
        "name": "defiant",
        "description": "Defiant",
        "systemType": "resource",
        "securityEnclave": "open",
        "organization": "olcf",
        "status": "OPERATIONAL",
        "annotations": {},
        "downtimeScheduleAvailable": false,
        "upcomingDowntimes": [],
        "retrievedAt": "2025-01-31T18:45:01Z"
    }
    ```

2. Get a list of compute queues for Defiant

    ``` bash
    > python3 olcf-s3m-compute.py --queuelist defiant
    ++++ OLCF S3M - Compute Job Orchestration ++++ Listing Queues
    "batch-gpu" "batch-cpu" "cron"
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
