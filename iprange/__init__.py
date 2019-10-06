import re


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

    regex = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    ipaddrs = re.findall(pattern=regex, string=contents)
    if verbose:
        print(f'loaded {len(ipaddrs)} ip addresses')

    return ipaddrs


def group_ipaddrs(ipaddrs, octet):
    """
    Group list of ip addresses by octet number expecting the input ipaddrs is a tuple of 4 indexes
    :param ipaddrs:
    :param octet:
    """
    group = [ipaddrs[0]]
    for ip in ipaddrs[1:]:
        if ip[:octet] == group[-1][:octet]:
            group.append(ip)
        else:
            yield group
            group = [ip]
    yield group


def range_ports(ports):
    """
    Range list of ports and return list of ranged ports.
    :param ports:
    """
    first = last = ports[0]
    for next in ports[1:]:
        if int(next) - 1 == int(last):
            last = next
        else:
            if first == last:
                yield first
            else:
                yield first + '-' + last
            first = last = next
    if first == last:
        yield first
    else:
        yield first + '-' + last


def range_ipaddrs(ipaddrs):
    """
    Range a list of of addresses and return list of ranged ip addresses.
    :param ipaddrs:
    """
    first = last = ipaddrs[0]
    for next in ipaddrs[1:]:
        if int(next[3]) - 1 == int(last[3]):
            last = next
        else:
            if first == last:
                yield '.'.join(first)
            else:
                yield '.'.join(first) + '-' + last[3]
            first = last = next
    if first == last:
        yield '.'.join(first)
    else:
        yield '.'.join(first) + '-' + last[3]


def separate_list(from_list, max_len):
    """
    Separate list of it contains an element that longer than max_len.
    :param from_list:
    :param max_len:
    """
    list = []
    for range in from_list:
        if (len_list(list) + len(range) + len(list)) <= max_len:
            list.append(range)
        else:
            yield list
            list = [range]
    yield list


def len_list(list):
    """
    Return the sum of all elements length in list.
    :param list:
    :return:
    """
    max = 0
    for i in list:
        max += len(i)

    return max


def get_ranged_ports(ports, verbose=False):
    unduplicated_ports = list(set(ports))
    duplicated_ports = len(ports) - len(unduplicated_ports)
    if verbose and duplicated_ports > 0:
        print(f'found {duplicated_ports} duplicated ports')

    sorted_ports = sorted(unduplicated_ports, key=int)
    for ranged_ports in range_ports(ports=sorted_ports):
        yield ranged_ports


def get_ranged_ipadds(ipaddrs, verbose=False):
    unduplicated_ipaddrs = list(set(ipaddrs))
    duplicated_ipaddrs = len(ipaddrs) - len(unduplicated_ipaddrs)
    if verbose and duplicated_ipaddrs > 0:
        print(f'found {duplicated_ipaddrs} duplicated ip addresses')

    sorted_ipaddrs = sorted(unduplicated_ipaddrs)
    for grouped_ipaddrs in group_ipaddrs(ipaddrs=sorted_ipaddrs, octet=3):
        for ranged_ipaddrs in range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs


def dumps_ipaddrs(ipaddrs, max_len=None, verbose=False):
    ranged_ipaddrs = get_ranged_ipadds(ipaddrs=ipaddrs, verbose=verbose)
    if max_len is not None:
        separated_ipaddrs = separate_list(from_list=ranged_ipaddrs, max_len=max_len)
        return '\n'.join([','.join(ipaddrs) for ipaddrs in separated_ipaddrs])
    return '\n'.join([ipaddrs for ipaddrs in ranged_ipaddrs])


def dumps_ports(ports, max_len=None, verbose=False):
    ranged_ports = get_ranged_ports(ports=ports, verbose=verbose)
    if max_len is not None:
        separated_ports = separate_list(from_list=ranged_ports, max_len=max_len)
        return '\n'.join([','.join(ports) for ports in separated_ports])
    return '\n'.join([ports for ports in ranged_ports])
