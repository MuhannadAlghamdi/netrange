from netrange._parser import shorten
from netrange._parser import parse_ips
from netrange._parser import parse_ports
from netrange._parser import get_cidr_block
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ips
from netrange._parser import get_unranged_ports
from netrange._parser import get_unranged_ips
from netrange._utilities import sort_ips
from netrange._utilities import separate_list


def dumps_ips(*ips, max_len=None, _range=False, delimiter='\n', unrange=False, cidr=False, shorter=False):
    ips = parse_ips(ips)

    if _range:
        ips = get_ranged_ips(ips=ips)
        if shorter:
            ips = shorten(ips)
    elif unrange:
        ips = get_unranged_ips(ips=ips)
        if shorter:
            ips = shorten(ips)
    elif cidr:
        ips = get_cidr_block(ips)
    else:
        ips = sorted(set(ips), key=sort_ips)

    ips = ['.'.join(ip) for ip in ips]

    if max_len:
        separated_ips = separate_list(_list=ips, max_len=max_len, delimiter=delimiter)
        return '\n'.join(separated_ips)

    return delimiter.join(ips)


def dump_ips(*ips, _range=False, unrange=False, cidr=False, shorter=False):
    ips = parse_ips(ips)

    if _range:
        ips = get_ranged_ips(ips=ips)
        if shorter:
            ips = shorten(ips)
    elif unrange:
        ips = get_unranged_ips(ips=ips)
        if shorter:
            ips = shorten(ips)
    elif cidr:
        ips = get_cidr_block(ips)
    else:
        ips = sorted(set(ips), key=sort_ips)

    ips = ['.'.join(ip) for ip in ips]
    return ips


def dumps_ports(*ports, max_len=None, _range=False, delimiter='\n', unrange=False, step=1):
    ports = parse_ports(ports)

    if _range:
        ports = get_ranged_ports(ports=ports, step=step)
    elif unrange:
        ports = get_unranged_ports(ports=ports)
    else:
        ports = sorted(ports, key=lambda port: (
            int(port.split('-')[0] if '-' in port else port),
            int(port.split('-')[1] if '-' in port else port)))

    if max_len is not None:
        separated_ports = separate_list(_list=ports, max_len=max_len, delimiter=delimiter)
        return '\n'.join(separated_ports)

    return delimiter.join([port for port in ports])


def dump_ports(*ports, max_len=None, _range=False, unrange=False, step=1):
    ports = parse_ports(ports)

    if _range:
        ports = get_ranged_ports(ports=ports, step=step)
    elif unrange:
        ports = get_unranged_ports(ports=ports)
    else:
        ports = sorted(ports, key=lambda port: (
            int(port.split('-')[0] if '-' in port else port),
            int(port.split('-')[1] if '-' in port else port)))

    if max_len is not None:
        separated_ports = separate_list(from_list=ports, max_len=max_len)
        return [','.join(ports) for ports in separated_ports]

    return [port for port in ports]
