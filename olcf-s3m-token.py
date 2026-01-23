#!/usr/bin/env python3

import argparse

from os import getenv

from olcf_s3m_api.client import OLCFAPIClient
from olcf_s3m_api.token import TokenService


def info(service : TokenService):
    print('++++ OLCF S3M - Token Management ++++ Querying Token Details')
    success, msg = service.get_token_info()
    if success:
        print(msg)
    print('\n\n')

def revoke(service : TokenService):
    print('++++ OLCF S3M - Token Management ++++ Revoking Token')
    service.revoke_token()
    print('\n\n')

def show(service : TokenService):
    print('++++ OLCF S3M - Token Management ++++ Displaying Token')
    hash = service.get_token_hash()
    print(f'OLCF S3M API Token: {hash}')
    print('\n\n')


def main(args):
    my_api_client = OLCFAPIClient(api_token=getenv("olcf_s3m_api_TOKEN", "InvalidToken"))
    my_token_service = TokenService(api_client=my_api_client)
    if args.info:
        info(my_token_service)
    elif args.revoke:
        revoke(my_token_service)
    else:
        show(my_token_service)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('olcf-s3m-token')
    parser.add_argument('-i', '--info', help='get token details', action='store_true')
    parser.add_argument('-r', '--revoke', help='revoke current token', action='store_true')
    args = parser.parse_args()
    main(args)
