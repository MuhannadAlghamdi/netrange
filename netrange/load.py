from netrange._parser import parse_ports
from netrange._parser import parse_ipaddrs


def load_ips_from_file(file, verbose=False):
    # TODO: check if file exists
    ips = parse_ipaddrs(contents=file.read())

    if verbose:
        print(f'loaded {len(ips)} ip addresses')

    return ['.'.join(ip) for ip in ips]


def load_ips_from_string(*ips, verbose=False):
    ips = parse_ipaddrs(contents='\n'.join(ips))

    if verbose:
        print(f'loaded {len(ips)} ip addresses')

    return ['.'.join(ip) for ip in ips]


def load_ports_from_string(*ports, verbose=False):
    contents = '\n'.join(ports)
    ports = parse_ports(contents)
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ports


def load_ports_from_file(file, verbose=False):
    contents = file.read()
    ports = parse_ports(contents)
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ports
