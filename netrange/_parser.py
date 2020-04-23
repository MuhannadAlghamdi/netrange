import re
from ipaddress import IPv4Address


def parse_ports(contents, unrange=False):
    PORT_REGEX = r'6553[1-5]?|655[1-2][0-9]|65[1-4][0-9]{2}|6[1-4][0-9]{3}|[1-5]?[0-9]{2,4}|[1-9]'
    regex = (
        r'('
        r'(?:(?:' + PORT_REGEX + r')(?![-]))'
        r'|'
        r'(?:(?:' + PORT_REGEX + r')\-(?:' + PORT_REGEX + r'))'
        r')'
    )

    ports = re.findall(pattern=r'\b(?<!\.)%s(?!\.)\b' % regex, string=contents)
    valid_ports = _validate_ports(ports)
    return valid_ports


def parse_ipaddrs(contents):
    IP_REGEX = r'25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?'
    CIDR_REGEX = r'3[0-2]|[12]?[0-9]'

    regex = (
        r'(' + IP_REGEX + r')\.'  # first octet
        r'(' + IP_REGEX + r')\.'  # second octet
        r'(' + IP_REGEX + r')\.'  # third octet
        r'('  # forth octet begin
        r'(?:(?:' + IP_REGEX + r')(?![-/]))'                    # if ends with with on - or /
        r'|'
        r'(?:(?:' + IP_REGEX + r')\-(?:' + IP_REGEX + r'))'     # if ends with - and octet
        r'|'
        r'(?:(?:' + IP_REGEX + r')\/(?:' + CIDR_REGEX + r'))'   # if ends with / and cidr
        r')'  # forth octet end
    )

    # return a list of tuples with string type
    ipaddrs = re.findall(pattern=r'\b(?<!\.)%s(?!\.)\b' % regex, string=contents)
    valid_ipaddrs = _validate_ipaddrs(ipaddrs)
    return valid_ipaddrs


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


def _unrange_ports(ports):
    for port in ports:
        if '-' in port:
            left, right = port.split('-')
            if int(left) < int(right):
                for i in range(int(left), int(right) + 1):
                    yield str(i)
        else:
            yield port


def _validate_ipaddrs(ipaddrs):
    for ipaddr in ipaddrs:
        if '-' in ipaddr[3]:
            left, right = ipaddr[3].split('-')
            if int(left) < int(right):
                yield ipaddr
        else:
            yield ipaddr


def _validate_ports(ports):
    for port in ports:
        if '-' in port:
            left, right = port.split('-')
            if int(left) < int(right):
                yield port
        else:
            yield port


def _unrange_ipaddrs(ipaddrs):
    for ipaddr in ipaddrs:
        if '-' in ipaddr[3]:
            left, right = ipaddr[3].split('-')
            if int(left) < int(right):
                for i in range(int(left), int(right) + 1):
                    yield ipaddr[:3] + (str(i),)
        else:
            yield ipaddr


def _range_ipaddrs(ipaddrs):
    ipaddrs = sorted(ipaddrs, key=lambda ip: (
        int(ip[0]),
        int(ip[1]),
        int(ip[2]),
        int(ip[3])))

    first = last = ipaddrs[0]
    for next in ipaddrs[1:]:
        if int(last[3]) + 1 == int(next[3]):
            last = next
        else:
            if first == last:
                yield first
            else:
                yield first[:3] + (first[3] + '-' + last[3],)
            first = last = next
    if first == last:
        yield first
    else:
        yield first[:3] + (first[3] + '-' + last[3],)


def separate_list(from_list, max_len):
    list = []
    for range in from_list:
        if (_len_list(list) + len(range) + len(list)) <= max_len:
            list.append('.'.join(range))
        else:
            yield list
            list = ['.'.join(range)]
    yield list


def _len_list(list):
    max = 0
    for i in list:
        max += len(i)

    return max


def get_unranged_ports(ports, verbose=False):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    return sorted_ports


def get_ranged_ports(ports, verbose=False):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    for ranged_ports in _range_ports(ports=sorted_ports):
        yield ranged_ports


def get_unranged_ipadds(ipaddrs, verbose=False):
    unranged_ipaddrs = _unrange_ipaddrs(ipaddrs)
    sorted_ipaddrs = sorted(set(unranged_ipaddrs), key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    return sorted_ipaddrs


def get_ranged_ipadds(ipaddrs, verbose=False):
    unranged_ipaddrs = _unrange_ipaddrs(ipaddrs)
    sorted_ipaddrs = sorted(set(unranged_ipaddrs), key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    for grouped_ipaddrs in _group_ipaddrs_by_octet(ipaddrs=sorted_ipaddrs, octet=3):
        for ranged_ipaddrs in _range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs


def get_cidr_block(ipaddrs):
    groups = _group_ipaddrs_by_octet_slow(ipaddrs).keys()
    sorted_groups = sorted(groups, key=lambda ip: (
        int(ip[0]),
        int(ip[1]),
        int(ip[2])))

    for group in sorted_groups:
        yield group + ('0/24',)


def _group_ipaddrs_by_octet_slow(ipaddrs, octet=3):
    groups = {}
    for ip in ipaddrs:
        if ip[:octet] not in groups:
            groups[ip[:octet]] = []
        groups[ip[:octet]].append(ip[3])

    return groups


def _group_ipaddrs_by_octet(ipaddrs, octet=3):
    group = [ipaddrs[0]]
    for ipaddr in ipaddrs[1:]:
        if ipaddr[:octet] == group[-1][:octet]:
            group.append(ipaddr)
        else:
            yield group
            group = [ipaddr]
    yield group
