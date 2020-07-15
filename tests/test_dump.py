from os import path

import netrange

this_directory = path.abspath(path.dirname(__file__))


ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']
ports_list = ['0', '20', '21', '22', '23', '25', '53', '80']


def test_dump_ips():
    ips = netrange.dump_ips(*ips_list, range=True)
    assert ips == ['172.25.12.195-197', '172.25.12.199']


def test_dumps_ips():
    ips = netrange.dumps_ips(*ips_list, range=True, delimiter=',')
    assert ips == '172.25.12.195-197,172.25.12.199'
