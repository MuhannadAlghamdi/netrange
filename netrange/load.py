from netrange._parser import parse_ports
from netrange._parser import parse_ips


def load_ips_from_file(file, verbose=False):
    # TODO: check if file exists
    ips = parse_ips(contents=file.read())

    if verbose:
        print(f'loaded {len(ips)} ip addresses')

    return ['.'.join(ip) for ip in ips]


def load_ports_from_file(file, verbose=False):
    # TODO: check if file exists
    ports = parse_ports(file.read())
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ['.'.join(port) for port in ports]
