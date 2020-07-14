from netrange._parser import shorten
from netrange._parser import parse_ips
from netrange._parser import parse_ports
from netrange._parser import separate_list
from netrange._parser import separate_ports
from netrange._parser import get_cidr_block
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ips
from netrange._parser import get_unranged_ports
from netrange._parser import get_unranged_ipadds


def sort_ips(ip):
    first_part = ip[3].split(';')[0]
    if '-' in first_part:
        left, right = first_part.split('-')
        return int(ip[0]), int(ip[1]), int(ip[2]), int(left), int(right)
    elif '/' in first_part:
        left, right = first_part.split('/')
        return int(ip[0]), int(ip[1]), int(ip[2]), int(left), int(right)
    else:
        left = first_part
        return int(ip[0]), int(ip[1]), int(ip[2]), int(left), 0


def dumps_ips(*ips, max_len=None, verbose=False, range=False, delimiter='\n', unrange=False, cidr=False, shorter=False):
    ips = parse_ips(contents='\n'.join(ips))

    if range:
        ips = get_ranged_ips(ips=ips, verbose=verbose)
        if shorter:
            ips = shorten(ips)
    elif unrange:
        ips = get_unranged_ipadds(ipaddrs=ips, verbose=verbose)
        if shorter:
            ips = shorten(ips)
    elif cidr:
        ips = get_cidr_block(ips)
    else:
        ips = sorted(set(ips), key=sort_ips)

    if max_len:
        separated_ips = separate_list(from_list=ips, max_len=max_len)
        return delimiter.join([','.join(ipaddrs) for ipaddrs in separated_ips])

    return delimiter.join(['.'.join(ip) for ip in ips])


def dump_ips(*ips, verbose=False, range=False, unrange=False, cidr=False, shorter=False):
    ips = parse_ips(contents='\n'.join(ips))

    if range:
        ips = get_ranged_ips(ips=ips, verbose=verbose)
        if shorter:
            ips = shorten(ips)
    elif unrange:
        ips = get_unranged_ipadds(ipaddrs=ips, verbose=verbose)
        if shorter:
            ips = shorten(ips)
    elif cidr:
        ips = get_cidr_block(ips)
    else:
        ips = sorted(set(ips), key=sort_ips)

    return ['.'.join(ip) for ip in ips]


def dumps_ports(*ports, max_len=None, verbose=False, range=False, delimiter='\n', unrange=False, step=1):
    ports = parse_ports(contents='\n'.join(ports))

    if range:
        ports = get_ranged_ports(ports=ports, verbose=verbose, step=step)
    elif unrange:
        ports = get_unranged_ports(ports=ports, verbose=verbose)
    else:
        ports = sorted(ports, key=lambda port: (
            int(port.split('-')[0] if '-' in port else port),
            int(port.split('-')[1] if '-' in port else port)))

    if max_len is not None:
        separated_ports = separate_ports(from_list=ports, max_len=max_len)
        return '\n'.join([delimiter.join(ports) for ports in separated_ports])

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
