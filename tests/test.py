import netrange
import json

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199']

ips = netrange.load_ipaddrs(from_args=ips_list, verbose=True)
print(ips)
print(netrange.dumps_ipaddrs(ipaddrs=ips))
