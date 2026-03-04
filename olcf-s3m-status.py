#!/usr/bin/env python3

import argparse

from olcf_s3m_api.status import StatusService

def status(service : StatusService, cluster : str=None):
    if cluster:
        print(f'++++ OLCF S3M - Compute Job Orchestration ++++ Getting Compute System Status for {cluster.capitalize()}')

        system_status = service.get_system_status(cluster)
        msg = system_status.msg()
    else:
        print('++++ OLCF S3M - Compute Job Orchestration ++++ Getting Compute System Status')

        systems_status = service.get_all_systems_status()
        msg = ''
        for system in systems_status:
            msg += system.msg()
            msg += '\n\n'
        
        msg = msg.rstrip('\n\n')

    print(msg)
    print('\n\n')

def main(args):   
    my_status_service = StatusService()
    
    if args.cluster is not None:
        status(my_status_service, args.cluster)
    else:
        status(my_status_service)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('olcf-s3m-status')
    parser.add_argument('-c', '--cluster', help='get status for a specific cluster', type=str, default=None)
    args = parser.parse_args()
    main(args)
