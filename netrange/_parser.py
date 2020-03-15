import re
from ipaddress import IPv4Address


def parse_ports(contents):
    regex = r'\b([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5]?)\b'
    return re.findall(pattern=regex, string=contents)


def parse_ipaddrs(contents):
    regex = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'((?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(?:(?:\-(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))|(?:\/(?:3[0-2]|[1-2][0-9]|[0-9])))?)'

    ipaddrs = re.findall(pattern=regex, string=contents)
    unranged_ipaddrs = _unrange_ipaddrs(ipaddrs=ipaddrs)
    return [ipaddr for ipaddr in unranged_ipaddrs]


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
        if '-' in ipaddr[3]:
            left, right = ipaddr[3].split('-')
            if left < right:
                for i in range(int(left), int(right) + 1):
                    yield ipaddr[:3] + (str(i),)
        elif '/' in ipaddr[3]:
            pass
            # try:
            #     cidr = IPv4Address(address=ipaddr)
            #     yield str(cidr)
            # except Exception as e:
            #     print(f'unable to parse {ipaddr}. {e}')
        else:
            yield ipaddr


def _range_ipaddrs(ipaddrs):
    ipaddrs = sorted(ipaddrs)
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
        print(f'found { duplicated_ports } duplicated ports')

    sorted_ports = sorted(unduplicated_ports, key=int)
    for ranged_ports in _range_ports(ports=sorted_ports):
        yield ranged_ports


def get_ranged_ipadds(ipaddrs, verbose=False):
    ipaddrs_tuples = parse_ipaddrs(contents='\n'.join(ipaddrs))
    unduplicated_ipaddrs = list(set(ipaddrs_tuples))
    duplicated_ipaddrs = len(ipaddrs_tuples) - len(unduplicated_ipaddrs)
    if verbose:
        print(f'found { duplicated_ipaddrs } duplicated ip addresses')

    int_ipaddrs_tuples = [tuple(int(octet) for octet in list(ipaddr)) for ipaddr in unduplicated_ipaddrs]
    for grouped_ipaddrs in _group_ipaddrs_by_octet(ipaddrs=int_ipaddrs_tuples, octet=3):
        for ranged_ipaddrs in _range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs


def _group_ipaddrs_by_octet_slow(ipaddrs, octet=3):
    groups = {}
    for ip in ipaddrs:
        if ip[:octet] not in groups:
            groups[ip[:octet]] = []
        groups[ip[:octet]].append(ip[3])

    return groups


def _group_ipaddrs_by_octet(ipaddrs, octet=3):
    ipaddrs = sorted(ipaddrs)
    group = [ipaddrs[0]]
    for ipaddr in ipaddrs[1:]:
        if ipaddr[:octet] == group[-1][:octet]:
            group.append(ipaddr)
        else:
            yield group
            group = [ipaddr]
    yield group
