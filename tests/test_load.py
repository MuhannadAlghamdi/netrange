import json
from os import path
import netrange

this_directory = path.abspath(path.dirname(__file__))

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd', '172.25.12.110-114']
ports_list = ['0', '20', '21', '22', '23', '25', '53', '80']


def test_load_ips_from_string():
    ips = netrange.load_ips_from_string(*ips_list)
    assert len(ips) == 8


def test_load_ips_from_file():
    file_name = f'{this_directory}/ips'
    file = open(file=file_name, mode='r')
    ips = netrange.load_ips_from_file(file=file)
    assert len(ips) == 4


def test_load_ports_from_string():
    ports = netrange.load_ports_from_string(*ports_list)
    assert len(ports) == 7


def test_load_ports_from_file():
    file_name = f'{this_directory}/ports'
    file = open(file=file_name, mode='r')
    ports = netrange.load_ports_from_file(file=file)
    assert len(ports) == 14
