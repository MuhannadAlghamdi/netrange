import json

import netrange

from os import path

this_directory = path.abspath(path.dirname(__file__))

ips_list = ['172.25.12.',
            '172.25.12.19622',  # sould not accept this
            '172.25.12.197-',
            '172.25.12.199-200',
            '172.25.12.200-119',
            'dfdfd',
            '172.25.12.110/23',
            '172.25.12.110/']

ports_list = ['0',
              '20-',
              '21-22',
              '22-1',
              '2322222',
              '25,33-']


def test_loads_ips():
    ips = netrange.loads_ips(*ips_list)
    print(ips)
    assert len(ips) == 2


def test_load_ips_from_file():
    file_name = f'{this_directory}/ips'
    file = open(file=file_name, mode='r')
    ips = netrange.load_ips_from_file(file=file)
    assert len(ips) == 256


def test_loads_ports():
    ports = netrange.loads_ports(*ports_list)
    print(ports)
    assert len(ports) == 2


def test_load_ports_from_file():
    file_name = f'{this_directory}/ports'
    file = open(file=file_name, mode='r')
    ports = netrange.load_ports_from_file(file=file)
    assert len(ports) == 14
