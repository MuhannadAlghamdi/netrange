import json
import netrange

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']

ips_loaded_from_args = netrange.load_ipaddrs(from_args=ips_list)
print(ips_loaded_from_args)

ips_loaded_from_file = netrange.load_ipaddrs(from_file='/Users/muhannad/Dropbox/STC/ips')
print(ips_loaded_from_file)
