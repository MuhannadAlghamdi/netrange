from netrange._parser import get_ranged_ipadds
from netrange._parser import get_ranged_ports
from netrange._parser import parse_ipaddrs_tuples


def dumps(ipaddrs, max_len=None, verbose=False):
    ipaddrs_tuple = parse_ipaddrs_tuples('\n'.join(ipaddrs))
    if not ipaddrs_tuple:
        return

    ranged_ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return '\n'.join([','.join(ipaddrs) for ipaddrs in separated_ipaddrs])
    return ','.join([ipaddrs for ipaddrs in ranged_ipaddrs])


def dump(ipaddrs, max_len=None, verbose=False):
    ipaddrs_tuple = parse_ipaddrs_tuples('\n'.join(ipaddrs))
    if not ipaddrs_tuple:
        return

    ranged_ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return [','.join(ipaddrs) for ipaddrs in separated_ipaddrs]
    return [ipaddrs for ipaddrs in ranged_ipaddrs]
