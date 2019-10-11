from netrange._parser import parse_ipaddrs


def load(from_file, verbose=False):
    """
    Load the CoNLL-U source in a string into a Conll object.
    Args:
        source: The CoNLL-U formatted string.
    Returns:
        A Conll object equivalent to the provided source.
    Raises:
        ParseError: If there is an error parsing the input into a Conll object.
    """
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
