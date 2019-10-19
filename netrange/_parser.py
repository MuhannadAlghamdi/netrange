import re


def parse_ports(contents):
    regex = r'\b([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5]?)\b'
    return re.findall(pattern=regex, string=contents)



def parse_ipaddrs(contents):
    regex = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:\-(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))?)'

    ipaddrs = re.findall(pattern=regex, string=contents)
    unranged_ipaddrs = _unrange_ipaddrs(ipaddrs=ipaddrs)
    return [ipaddr for ipaddr in unranged_ipaddrs]


def _group_ipaddrs(ipaddrs, octet):
    group = [ipaddrs[0]]
    for ip in ipaddrs[1:]:
        if ip[:octet] == group[-1][:octet]:
            group.append(ip)
        else:
            yield group
            group = [ip]
    yield group


def _range_ports(ports):
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


def _unrange_ipaddrs(ipaddrs):
    for ipaddr in ipaddrs:
        if '-' not in ipaddr[3]:
            yield ipaddr
        else:
            left, right = ipaddr[3].split('-')
            if left < right:
                for i in range(int(left), int(right) + 1):
                    yield ipaddr[:3] + (str(i),)


def _range_ipaddrs(ipaddrs):
    first = last = ipaddrs[0]
    for next in ipaddrs[1:]:
        if next[3] - 1 == last[3]:
            last = next
        else:
            if first == last:
                yield '.'.join(map(str, first))
            else:
                yield '.'.join(map(str, first)) + '-' + str(last[3])
            first = last = next
    if first == last:
        yield '.'.join(map(str, first))
    else:
        yield '.'.join(map(str, first)) + '-' + str(last[3])


def separate_list(from_list, max_len):
    list = []
    for range in from_list:
        if (_len_list(list) + len(range) + len(list)) <= max_len:
            list.append(range)
        else:
            yield list
            list = [range]
    yield list


def _len_list(list):
    max = 0
    for i in list:
        max += len(i)

    return max


def get_ranged_ports(ports, verbose=False):
    unduplicated_ports = list(set(ports))
    duplicated_ports = len(ports) - len(unduplicated_ports)
    if verbose:
        print(f'found {duplicated_ports} duplicated ports')

    sorted_ports = sorted(unduplicated_ports, key=int)
    for ranged_ports in _range_ports(ports=sorted_ports):
        yield ranged_ports


def get_ranged_ipadds(ipaddrs, verbose=False):
    unduplicated_ipaddrs = list(set(ipaddrs))
    duplicated_ipaddrs = len(ipaddrs) - len(unduplicated_ipaddrs)
    if verbose:
        print(f'found {duplicated_ipaddrs} duplicated ip addresses')

    # groups = group_ipaddrs_by_octet(unduplicated_ipaddrs, 3)
    # sorted_groups = [{key: sorted(map(int, values))} for key, values in groups.items()]

    integer_ipaddrs = [tuple(int(octet) for octet in list(ipaddr)) for ipaddr in unduplicated_ipaddrs]
    sorted_ipaddrs = sorted(integer_ipaddrs)
    for grouped_ipaddrs in _group_ipaddrs(ipaddrs=sorted_ipaddrs, octet=3):
        for ranged_ipaddrs in _range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs


def group_ipaddrs_by_octet(ipaddrs, octet=3):
    groups = {}
    for ip in ipaddrs:
        if ip[:octet] not in groups:
            groups[ip[:octet]] = []
        groups[ip[:octet]].append(ip[3])

    return groups
