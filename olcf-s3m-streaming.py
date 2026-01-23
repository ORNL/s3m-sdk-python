#!/usr/bin/env python3

import argparse

from os import getenv

from olcf_s3m_api.client import OLCFAPIClient
from olcf_s3m_api.streaming import StreamingService

def list_services(service : StreamingService):
    print('++++ OLCF S3M - Streaming Service Orchestration ++++ Listing Available Services')
    success, msg = service.list_services()
    if success:
        print(msg)
    print('\n\n')

def show(service : StreamingService):
    print('++++ OLCF S3M - Streaming Service Orchestration ++++ Showing Existing Deployments')
    success, msg = service.list_clusters()
    if success:
        print(msg)
    print('\n\n')

def deploy(service : StreamingService, cluster : str, nodes : int = 1):
    print(f'++++ OLCF S3M - Streaming Service Orchestration ++++ Deploying a {nodes}-node Service')
    success, msg = service.start_cluster(cluster_name=cluster, wait_for_healthy=True, node_count=nodes)
    if success:
        print(f'{msg}\n\n')

        print('++++ OLCF S3M - Streaming Service Orchestration ++++ Getting Cluster Deployment')
        deployment = service.get_cluster_deployment(cluster_name=cluster)
        if deployment:
            print(deployment)
    print('\n\n')

def info(service : StreamingService, cluster : str):
    print('++++ OLCF S3M - Streaming Service Orchestration ++++ Getting Cluster Information')
    success, msg = service.get_cluster_info(cluster_name=cluster)
    if success:
        print(msg)
    print('\n\n')

def shutdown(service : StreamingService, cluster : str):
    print('++++ OLCF S3M - Streaming Service Orchestration ++++ Shutting Down Service')
    success, msg = service.stop_cluster(cluster_name=cluster)
    if success:
        print(msg)
    print('\n\n')


def main(args):
    my_strm_service_name = args.service
    my_cluster_name = args.cluster
    my_api_client = OLCFAPIClient(api_token=getenv("olcf_s3m_api_TOKEN", "InvalidToken"))
    my_strm_service = StreamingService(service_name=my_strm_service_name,
                                       api_client=my_api_client)
    if args.avail:
        list_services(my_strm_service)
    elif args.deploy:
        deploy(my_strm_service, my_cluster_name, args.hostcount)
    elif args.info:
        info(my_strm_service, my_cluster_name)
    elif args.shutdown:
        shutdown(my_strm_service, my_cluster_name)
    else:
        show(my_strm_service)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('olcf-s3m-streaming')
    parser.add_argument('-a', '--avail', help='list available streaming services', action='store_true')
    parser.add_argument('-d', '--deploy', help='deploy a service cluster', action='store_true')
    parser.add_argument('-i', '--info', help='get information about a service cluster', action='store_true')
    parser.add_argument('-s', '--shutdown', help='shutdown a service cluster', action='store_true')
    parser.add_argument('service', nargs='?', help='name of a supported streaming service', default='rabbitmq')
    parser.add_argument('cluster', nargs='?', help='name for your streaming service cluster', default='ds2hpc_demo')
    parser.add_argument('hostcount', nargs='?', help='number of hosts for streaming service cluster', default=1)
    args = parser.parse_args()
    main(args)
