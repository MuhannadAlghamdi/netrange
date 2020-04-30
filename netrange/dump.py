from netrange._parser import separate_list
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ipadds
from netrange._parser import get_unranged_ipadds
from netrange._parser import get_unranged_ports
from netrange._parser import get_cidr_block
from netrange._parser import parse_ipaddrs
from netrange._parser import parse_ports


def sort_ipaddrs(ip):
    first_part = ip[3].split(';')[0]
    if '-' in first_part:
        left, right = first_part.split('-')
        return (int(ip[0]), int(ip[1]), int(ip[2]), int(left), int(right))
    elif '/' in first_part:
        left, right = first_part.split('/')
        return (int(ip[0]), int(ip[1]), int(ip[2]), int(left), int(right))
    else:
        left = first_part
        return (int(ip[0]), int(ip[1]), int(ip[2]), int(left), 0)


def dumps_ips(*ips, max_len=None, verbose=False, range=False, delimiter='\n', unrange=False, cidr=False):
    ipaddrs = parse_ipaddrs(contents='\n'.join(ips))

    if range:
        ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)
    elif unrange:
        ipaddrs = get_unranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)
    elif cidr:
        ipaddrs = get_cidr_block(ipaddrs)
    else:
        ipaddrs = sorted(set(ipaddrs), key=sort_ipaddrs)

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


def dumps_ports(*ports, max_len=None, verbose=False, range=False, delimiter='\n', unrange=False):
    ports = parse_ports(contents='\n'.join(ports))

    if range:
        ports = get_ranged_ports(ports=ports, verbose=verbose)
    elif unrange:
        ports = get_unranged_ports(ports=ports, verbose=verbose)
    else:
        ports = sorted(ports, key=lambda port: (
            int(port.split('-')[0] if '-' in port else port),
            int(port.split('-')[1] if '-' in port else port)))

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
