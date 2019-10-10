import re
from netrange import _parser


def load_ports(from_file=None, from_args=None, verbose=False):
    if from_args:
        contents = '\n'.join(from_args)
    elif from_file:
        contents = from_file.read()

    regex = r'\b([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5]?)\b'
    ports = re.findall(pattern=regex, string=contents)
    if verbose:
        print(f'loaded {len(ports)} ports')

    return ports


def load_ipaddrs(from_file=None, from_args=None, verbose=False):
    if from_args:
        contents = '\n'.join(from_args)
    elif from_file:
        contents = from_file.read()

    regex = r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    ipaddrs = re.findall(pattern=regex, string=contents)
    if verbose:
        print(f'loaded {len(ipaddrs)} ip addresses')

    return ipaddrs
