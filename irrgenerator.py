#!/usr/bin/env python
"""
Author:
    James Di Trapani <james@ditrapani.com.au>
        - https://github.com/jamesditrapani

Description:
    Tool to assist Network Engineers with the auto creation of IRR objects

"""

from netaddr import IPNetwork
from netaddr.core import AddrFormatError
from datetime import date
import requests
import sys

__author__ = 'James Di Trapani <james@ditrapani.com.au>'

NOTIFY_EMAIL = 'noc@example.com'  # Your NOC Email
MAINT_OBJECT = 'MAINT-EXAMPLE-01'  # Your Maintainer Object
IRR_SOURCE = 'EXAMPLE-NTT'  # Your IRR Source


class IRRDataError(Exception):
    pass


class IRRGenerator(object):

    def __init__(self,
                 file_name: str = None,
                 prefixes: dict = None,
                 notify_email: str = NOTIFY_EMAIL,
                 maint_object: str = MAINT_OBJECT,
                 irr_source: str = IRR_SOURCE
                 ) -> None:
        """
            Initialise Class

            Arguments:
                file_name* (str): Relative or Full Path
                to the file containing the prefix data
                prefixes* (dict): Dictionary schema
                containing prefix & ASN combinations

            Note:
                * indicates optional field

        """
        # Set vars
        self._notify_email = notify_email
        self._maint_object = maint_object
        self._irr_source = irr_source

        # Ensure valid data has been passed
        if file_name is None and prefixes is None:
            raise IRRDataError('No data specified!')

        self.dnow = date.today().strftime("%Y%m%d")
        if prefixes is not None:
            self.data = [[key, item] for key, item in prefixes.items()]
        else:
            try:
                self.data = [x.split() for x in open(file_name, 'r')]
            except FileNotFoundError:
                raise IRRDataError(f'Cannot find {file_name}!') from None

    def create(self) -> dict:
        """
            Entry point to collect, parse & return parsed data

            Returns:
                dict: Nested dictionary containing parsed data for each
                supernet and the expanded subnet(s) OR error

        """
        response = {}
        for i in self.data:
            try:
                prefix, length = i[0].split('/')
                prefixes = self._find_prefixes(i[0], int(length))
                response.update({i[0]: self._format_data(prefixes, i[1])})
            except AddrFormatError as e:
                return {'error': 'Invalid IP Format, {e}'}
            except ValueError as e:
                return {'error': 'Passed data is in incorrect format!'}
        return response

    def _find_prefixes(self, prefix: str, prefix_len: int) -> list:
        """
            Expand prefix to all possible subnets up-to a /25.

            Arguments:
                prefix (str): Prefix to expand
                preifx_len (int): Current length of the prefix

            Returns:
                list: List of IPNetwork objects for each subnet

        """
        prefix = IPNetwork(prefix)
        data = [list(prefix.subnet(x)) for x in range(prefix_len, 25)]
        return [x for i in data for x in i]

    def _format_data(self, prefixes: list, asn: str) -> dict:
        """
            Parse the data for each supernet and the expanded
            subnets.

            Arguments:
                prefixes (list): List of IPNetwork objects
                asn (str): ASN in the format of `ASXXX`

            Returns:
                dict: Nested dictionary containing parsed data for each
                supernet and the expanded subnet(s)

        """
        asname = self._asn_desc(asn)
        response = {}
        for prefix in prefixes:
            response.update({(len(response) + 1): {
                'route': str(prefix.cidr),
                'descr': asname,
                'origin': asn,
                'notify': self._notify_email,
                'mnt-by': self._maint_object,
                'changed': f'{self._notify_email} {self.dnow}',
                'source': self._irr_source
            }})
        return response

    def _asn_desc(self, asn: str) -> str:
        """
            Turn ASN into Human identifiable name via bgptoolkit.net API

            Arguments:
                asn (str): ASN in the format of `ASXXX`

            Returns:
                str: Human readable name for corresponding ASN

        """
        session = requests.session()
        response = session.get(
            f'https://bgptoolkit.net/api/asn/{asn.strip("AS")}')
        data = response.json().get('data')
        return data.get('name') if data.get('name') is \
            not None else self.MAINT_OBJECT


def print_output(response: dict) -> None:
    """
        Print response output to stdout

        Arguments:
            response (dict): Nested dictionary returned from IRRCreation()

    """
    for prefix, prefix_data in response.items():
        for subnet, subnet_data in prefix_data.items():
            for key, item in subnet_data.items():
                print(f'{key}: {item}')
            print('')


if __name__ == '__main__':
    # Logic called when executed via CLI directly
    import argparse

    parser_help = """
irrgenerate [<args>]

When passing a file please ensure it is formatted like so:

Note: One prefix/asn combo per line

<prefix>/<cidr> <asn>

----------------------------------------

Prefix: Network Address of the following CIDR, (e.g, 1.1.1.0)
CIDR: Network CIDR to accompany the Prefix, (e.g. 23)
ASN: AS number that will be set in the Origin ASN field (e.g. AS13335)
    """
    # Allow file to be passed as an argument
    parser = argparse.ArgumentParser(
        description='Generate IRR Objects',
        usage=parser_help)

    parser.add_argument('-f', '--file_name',
                        required=False,
                        default='subnets.txt',
                        help='Full or Relative path to file')

    parser.add_argument('-e', '--notify_email',
                        required=False,
                        default=argparse.SUPPRESS,
                        help='Notify email address set in route object')

    parser.add_argument('-m', '--maint_object',
                        required=False,
                        default=argparse.SUPPRESS,
                        help='Maintainer set in route object')

    parser.add_argument('-s', '--irr_source',
                        required=False,
                        default=argparse.SUPPRESS,
                        help='IRR Source set in route object')

    args = parser.parse_args(sys.argv[1:])

    # Initate logic
    code = IRRGenerator(**vars(args))
    response = code.create()

    print_output(response)
