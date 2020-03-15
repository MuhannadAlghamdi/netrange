from netrange._parser import parse_ports
from netrange._parser import parse_ipaddrs


def load_ips_from_file(file, verbose=False):
    # TODO: check if file exists
    ips = parse_ipaddrs(contents=file.read())

    if verbose:
        print(f'loaded {len(ips)} ip addresses')

    return ['.'.join(ip) for ip in ips]


def loads_ips(*ips, verbose=False):
    ips = parse_ipaddrs(contents='\n'.join(ips))

    if verbose:
        print(f'loaded {len(ips)} ip addresses')

    return ['.'.join(ip) for ip in ips]


def loads_ports(*ports, verbose=False):
    ports = parse_ports('\n'.join(ports))

    if verbose:
        print(f'loaded {len(ports)} ports')

    return ['.'.join(port) for port in ports]


def load_ports_from_file(file, verbose=False):
    # TODO: check if file exists
    ports = parse_ports(file.read())
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ['.'.join(port) for port in ports]
