import netrange

ips_list = ['172.25.12.195', '172.25.12.196', '172.25.12.197', '172.25.12.199', 'dfdfd']

print(netrange.dumps_ips(*ips_list, delimiter=','))