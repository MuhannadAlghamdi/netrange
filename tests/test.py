import netrange
import json


print(netrange.__version__)

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']

ips = netrange.load_ipaddrs(from_args=ips_list)
# print(ips)

ranges = netrange.dumps_ipaddrs(ips, 200)
print(ranges)

dump = netrange.dump_ipaddrs(ips, 200)
print(dump)
