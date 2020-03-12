from netrange._parser import separate_list
from netrange._parser import get_ranged_ports
from netrange._parser import get_ranged_ipadds


def dumps_ips(ipaddrs, max_len=None, verbose=False, range=False):
    ipaddrs = sorted(ipaddrs)

    if range:
        ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)

    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ipaddrs, max_len=max_len)
        return '\n'.join([','.join(ipaddrs) for ipaddrs in separated_ipaddrs])

    return '\n'.join([ipaddr for ipaddr in ipaddrs])


def dump_ips(ipaddrs, max_len=None, verbose=False, range=False):
    ipaddrs = sorted(ipaddrs)

    if range:
        ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)

    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ipaddrs, max_len=max_len)
        return [','.join(ipaddrs) for ipaddrs in separated_ipaddrs]

    return [ipaddrs for ipaddrs in ranged_ipaddrs]


def dumps_ports(ports, max_len=None, verbose=False):
    ports = sorted(ports)

    # TODO: verify ports contains at least one port
    ranged_ports = get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = separate_list(from_list=ranged_ports, max_len=max_len)
        return '\n'.join([','.join(ports) for ports in separated_ports])
    return ','.join([ports for ports in ranged_ports])


def dump_ports(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = separate_list(from_list=ranged_ports, max_len=max_len)
        return [','.join(ports) for ports in separated_ports]
    return [ports for ports in ranged_ports]
