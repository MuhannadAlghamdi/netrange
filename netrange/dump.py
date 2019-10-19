from netrange._parser import separate_list
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ipadds
from netrange._parser import parse_ipaddrs


def dump_ips_string(ipaddrs, max_len=None, verbose=False):
    ipaddrs_tuple = parse_ipaddrs(contents='\n'.join(ipaddrs))
    if not ipaddrs_tuple:
        return

    ranged_ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return '\n'.join([','.join(ipaddrs) for ipaddrs in separated_ipaddrs])
    return ','.join([ipaddrs for ipaddrs in ranged_ipaddrs])


def dump_ips_list(ipaddrs, max_len=None, verbose=False):
    ipaddrs_tuple = parse_ipaddrs('\n'.join(ipaddrs))
    if not ipaddrs_tuple:
        return

    ranged_ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return [','.join(ipaddrs) for ipaddrs in separated_ipaddrs]
    return [ipaddrs for ipaddrs in ranged_ipaddrs]


def dump_ports_string(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = separate_list(from_list=ranged_ports, max_len=max_len)
        return '\n'.join([','.join(ports) for ports in separated_ports])
    return ','.join([ports for ports in ranged_ports])


def dump_ports_list(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = separate_list(from_list=ranged_ports, max_len=max_len)
        return [','.join(ports) for ports in separated_ports]
    return [ports for ports in ranged_ports]
