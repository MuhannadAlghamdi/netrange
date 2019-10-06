from unittest import TestCase

import json
import netrange

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']


class TestDumps_ipaddrs(TestCase):

    def test_is_string(self):
        s = netrange.dumps_ipaddrs(ipaddrs=ips_list)
        self.assertTrue(isinstance(s, basestring))
