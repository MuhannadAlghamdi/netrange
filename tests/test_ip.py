import json
from os import path
from netrange import ip

this_directory = path.abspath(path.dirname(__file__))


ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']


def test_load_ipaddrs_from_list():
    ips = ip.loads(from_args=ips_list)
    assert len(ips) > 0


def test_load_ipaddrs_from_file():
    file = open(file=f'{this_directory}/ips', mode='r')
    ips = ip.load(from_file=file)
    assert len(ips) > 0
