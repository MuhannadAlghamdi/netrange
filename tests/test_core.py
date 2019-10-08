import json
from os import path
import netrange

this_directory = path.abspath(path.dirname(__file__))


ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']


def test_load_ipaddrs_from_list():
    ips = netrange.load_ipaddrs(from_args=ips_list)
    assert len(ips) > 0


def test_load_ipaddrs_from_file():
    ips = netrange.load_ipaddrs(from_file=f'{this_directory}/ips')
    assert len(ips) > 0
