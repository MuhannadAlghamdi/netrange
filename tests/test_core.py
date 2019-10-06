import json
import netrange

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']

# load ipaddrs from args
ips_loaded_from_args = netrange.load_ipaddrs(from_args=ips_list)
print('\nload from args:\n', ips_loaded_from_args)

# load ipaddrs from file
ips_loaded_from_file = netrange.load_ipaddrs(from_file='/Users/muhannad/Dropbox/STC/ips')
print('\nload from file:\n', ips_loaded_from_file)

# dump

dump_ipaddrs = netrange.dump_ipaddrs(ipaddrs=ips_loaded_from_file)
print('\ndump:\n', dump_ipaddrs)
