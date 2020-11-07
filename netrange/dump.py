from netrange._parser import shorten
from netrange._parser import parse_ips
from netrange._parser import parse_ports
from netrange._parser import get_subnet_ips
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ips
from netrange._parser import get_unranged_ports
from netrange._parser import get_unranged_ips
from netrange._utilities import sort_ips
from netrange._utilities import separate_list


def dumps_ips(*ips, max_len=None, _range=False, line_sep='\n', unrange=False, subnet=False, cidr=False, short=False):
    ips = parse_ips(ips)

    if _range:
        ips = get_ranged_ips(ips=ips, cidr=cidr)
        if short:
            ips = shorten(ips)
    elif unrange:
        ips = get_unranged_ips(ips=ips, cidr=cidr)
    elif subnet:
        ips = get_unranged_ips(ips=ips, cidr=True)
        ips = get_subnet_ips(ips=ips)

    ips = sorted(set(ips), key=sort_ips)

    if max_len:
        line_sep = line_sep if line_sep not in ['\n', r'\n'] else ','
        separated_ips = separate_list(_list=ips, max_len=max_len, line_sep=line_sep)
        return '\n'.join(separated_ips)

    line_sep = line_sep if line_sep != r'\n' else '\n'
    return line_sep.join(ips)


def dump_ips(*ips, _range=False, unrange=False, cidr=False, short=False, subnet=False):
    ips = parse_ips(ips)

    if _range:
        ips = get_ranged_ips(ips=ips, cidr=cidr)
        if short:
            ips = shorten(ips)
    elif unrange:
        ips = get_unranged_ips(ips=ips, cidr=cidr)
    elif subnet:
        ips = get_unranged_ips(ips=ips, cidr=True)
        ips = get_subnet_ips(ips=ips)

    ips = sorted(set(ips), key=sort_ips)
    return ips


def dumps_ports(*ports, max_len=None, _range=False, line_sep='\n', unrange=False, step=1):
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
        line_sep = line_sep if line_sep not in ['\n', r'\n'] else ','
        separated_ports = separate_list(_list=ports, max_len=max_len, line_sep=line_sep)
        return '\n'.join(separated_ports)

    line_sep = line_sep if line_sep != r'\n' else '\n'
    return line_sep.join([port for port in ports])


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
