import iprange
import json

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199']

ips = iprange.load_ipaddrs(from_args=ips_list, verbose=True)
print(iprange.dumps_ipaddrs(ipaddrs=ips))
