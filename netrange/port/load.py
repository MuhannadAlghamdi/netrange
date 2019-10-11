from netrange._parser import parse_ports


def loads(from_args, verbose=False):
    contents = '\n'.join(from_args)
    ports = parse_ports(contents)
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ports


def load(from_file, verbose=False):
    contents = from_file.read()
    ports = parse_ports(contents)
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ports
