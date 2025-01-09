#!/usr/bin/env python3

import argparse

from os import getenv

from olcf_api.client import OLCFAPIClient
from olcf_api.token import TokenService
from olcf_api.streaming import StreamingService

def list_services(service : StreamingService):
    print('++++ OLCF DS2HPC DEMO ++++ Listing Available Services')
    service.list_services()
    print('\n\n')

def show(service : StreamingService):
    print(f'++++ OLCF DS2HPC DEMO ++++ Showing Existing Deployments')
    service.list_clusters()
    print('\n\n')

def deploy(service : StreamingService, cluster : str):
    print('++++ OLCF DS2HPC DEMO ++++ Deploying a 1-node Service')
    success = service.start_cluster(cluster_name=cluster)
    if success:
        print('\n\n')

        print('++++ OLCF DS2HPC DEMO ++++ Getting Cluster Information')
        service.get_cluster_info(cluster_name=cluster)
        print('\n\n')

def info(service : StreamingService, cluster : str):
    print('++++ OLCF DS2HPC DEMO ++++ Getting Cluster Information')
    service.get_cluster_info(cluster_name=cluster)
    print('\n\n')

def shutdown(service : StreamingService, cluster : str):
    print('++++ OLCF DS2HPC DEMO ++++ Shutting Down Service')
    service.stop_cluster(cluster_name=cluster)
    print('\n\n')


def main(args):
    #print("DEBUG: Arguments\n", args)

    my_strm_service_name = args.service
    my_cluster_name = args.cluster
    my_api_client = OLCFAPIClient(api_token=getenv("OLCF_API_TOKEN", "InvalidToken"))
    my_strm_service = StreamingService(service_name=my_strm_service_name,
                                       api_client=my_api_client)
    if args.avail:
        list_services(my_strm_service)
    elif args.deploy:
        deploy(my_strm_service, my_cluster_name)
    elif args.info:
        info(my_strm_service, my_cluster_name)
    elif args.shutdown:
        shutdown(my_strm_service, my_cluster_name)
    else:
        show(my_strm_service)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('smc24-streaming-demo')
    parser.add_argument('-a', '--avail', help='list available streaming services', action='store_true')
    parser.add_argument('-d', '--deploy', help='deploy a service cluster', action='store_true')
    parser.add_argument('-i', '--info', help='get information about a service cluster', action='store_true')
    parser.add_argument('-s', '--shutdown', help='shutdown a service cluster', action='store_true')
    parser.add_argument('service', nargs='?', help='name of a supported streaming service', default='rabbitmq')
    parser.add_argument('cluster', nargs='?', help='name for your streaming service cluster', default='ds2hpc_demo')
    args = parser.parse_args()
    main(args)
