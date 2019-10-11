from netrange._parser import parse_ipaddrs


def load(from_file, verbose=False):
    contents = from_file.read()
    ipaddrs = parse_ipaddrs(contents=contents)

    if verbose:
        print(f'loaded {len(ipaddrs)} ip addresses')

    return ipaddrs


def loads(from_args, verbose=False):
    contents = '\n'.join(from_args)
    ipaddrs = parse_ipaddrs(contents=contents)

    if verbose:
        print(f'loaded {len(ipaddrs)} ip addresses')

    return ipaddrs
