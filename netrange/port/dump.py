from netrange._parser import get_ranged_ports
from netrange._parser import separate_list


def dumps(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = _parser.get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = _parser.separate_list(from_list=ranged_ports, max_len=max_len)
        return '\n'.join([','.join(ports) for ports in separated_ports])
    return ','.join([ports for ports in ranged_ports])


def dump(ports, max_len=None, verbose=False):
    # TODO: verify ports contains at least one port
    ranged_ports = _parser.get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = _parser.separate_list(from_list=ranged_ports, max_len=max_len)
        return [','.join(ports) for ports in separated_ports]
    return [ports for ports in ranged_ports]
