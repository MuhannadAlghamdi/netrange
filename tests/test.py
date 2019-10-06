import netrange
import json

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']

ips = netrange.load_ipaddrs(from_args=ips_list)
print(ips)

ranges = netrange.dumps_ipaddrs(ipaddrs=ips)

print(ranges)
