import re
from netrange import helpers


def load_ports(from_file=None, from_args=None, verbose=False):
    if from_args:
        contents = '\n'.join(from_args)
    elif from_file:
        with open(from_file, 'r') as f:
            contents = f.read()

    regex = r'\b([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5]?)\b'
    ports = re.findall(pattern=regex, string=contents)
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ports


def load_ipaddrs(from_file=None, from_args=None, verbose=False):
    if from_args:
        contents = '\n'.join(from_args)
    elif from_file:
        with open(from_file, 'r') as f:
            contents = f.read()

    regex = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    ipaddrs = re.findall(pattern=regex, string=contents)
    if verbose:
        print(f'loaded {len(ipaddrs)} ip addresses')

    return ipaddrs


def dumps_ipaddrs(ipaddrs, max_len=None, verbose=False):
    regex = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    ipaddrs_tuple = re.findall(pattern=regex, string='\n'.join(ipaddrs))
    if not ipaddrs_tuple:
        return

    ranged_ipaddrs = helpers.get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = helpers.separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return '\n'.join([','.join(ipaddrs) for ipaddrs in separated_ipaddrs])
    return ','.join([ipaddrs for ipaddrs in ranged_ipaddrs])


def dumps_ports(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = helpers.get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = helpers.separate_list(from_list=ranged_ports, max_len=max_len)
        return '\n'.join([','.join(ports) for ports in separated_ports])
    return ','.join([ports for ports in ranged_ports])


def dump_ipaddrs(ipaddrs, max_len=None, verbose=False):
    regex = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    ipaddrs_tuple = re.findall(pattern=regex, string='\n'.join(ipaddrs))
    if not ipaddrs_tuple:
        return

    ranged_ipaddrs = helpers.get_ranged_ipadds(ipaddrs=ipaddrs_tuple, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = helpers.separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return [','.join(ipaddrs) for ipaddrs in separated_ipaddrs]
    return [ipaddrs for ipaddrs in ranged_ipaddrs]


def dump_ports(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = helpers.get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = helpers.separate_list(from_list=ranged_ports, max_len=max_len)
        return [','.join(ports) for ports in separated_ports]
    return [ports for ports in ranged_ports]
