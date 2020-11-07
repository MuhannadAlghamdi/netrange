import netrange
import ipaddress

ips_list = [
    '10.21.51.232',
    '10.21.51.233',
    '10.21.51.234',
    '10.21.51.235',
    '10.21.51.236',
    '10.21.51.237',
    '10.21.51.238',
    '10.21.51.239',
    '10.21.51.240',
    '10.21.51.241',
    '10.21.51.242',
    '10.21.51.243',
    '10.21.51.244',
    '10.21.51.245',
    '10.21.51.246',
    '10.21.51.247',
    '10.21.51.248',
    '10.21.51.249',
    '10.21.51.250',
    '10.21.51.251',
]

# print(netrange.dumps_ips(*ips_list, delimiter=','))
# print(netrange.dump_ports('22,443,8080-8090', unrange=True))

nets = [ipaddress.ip_network(_ip) for _ip in ips_list]
cidrs = ipaddress.collapse_addresses(nets)
print([str(ip) for ip in cidrs])
