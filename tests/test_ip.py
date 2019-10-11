import json
from os import path
import netrange

this_directory = path.abspath(path.dirname(__file__))


ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']


def test_load_ips_from_string():
    ips = netrange.load_ips_from_string(*ips_list)
    assert len(ips) > 0


def test_load_ips_from_file():
    file = open(file=f'{this_directory}/ips', mode='r')
    ips = netrange.load_ips_from_file(file=file)
    assert len(ips) > 0
