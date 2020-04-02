from netrange._parser import separate_list
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ipadds
from netrange._parser import get_unranged_ipadds
from netrange._parser import parse_ipaddrs


def dumps_ips(*ips, max_len=None, verbose=False, range=False, delimiter='\n', unrange=False):
    ipaddrs = parse_ipaddrs(contents='\n'.join(ips))
    ipaddrs = sorted(ipaddrs, key=lambda ip: (
        int(ip[0]),
        int(ip[1]),
        int(ip[2]),
        int(ip[3].split('-')[0] if '-' in ip[3] else ip[3]),
        int(ip[3].split('-')[1]) if '-' in ip[3] else 0))

    if range:
        ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)
    elif unrange:
        ipaddrs = get_unranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)

    if max_len:
        separated_ipaddrs = separate_list(from_list=ipaddrs, max_len=max_len)
        return delimiter.join([','.join(ipaddrs) for ipaddrs in separated_ipaddrs])

    return delimiter.join(['.'.join(ipaddr) for ipaddr in ipaddrs])


def dump_ips(ipaddrs, max_len=None, verbose=False, range=False):
    ipaddrs = sorted(ipaddrs)

    if range:
        ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)

    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ipaddrs, max_len=max_len)
        return [','.join(ipaddrs) for ipaddrs in separated_ipaddrs]

    return [ipaddr for ipaddr in ipaddrs]


def dumps_ports(ports, max_len=None, verbose=False, range=False, delimiter='\n'):
    ports = sorted(ports)

    if range:
        ports = get_ranged_ports(ports=ports, verbose=verbose)

    # TODO: verify ports contains at least one port
    if max_len is not None:
        separated_ports = separate_list(from_list=ports, max_len=max_len)
        return delimiter.join([','.join(ports) for ports in separated_ports])

    return delimiter.join([port for port in ports])


def dump_ports(ports, max_len=None, verbose=False, range=False):
    ports = sorted(ports)

    # TODO: verify ports contains at least one port
    if range:
        ports = get_ranged_ports(ports=ports, verbose=verbose)

    if max_len is not None:
        separated_ports = separate_list(from_list=ports, max_len=max_len)
        return [','.join(port) for port in ports]
    return [port for port in ports]
