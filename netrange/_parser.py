import re
from ipaddress import IPv4Address
from netrange.exceptions import NetrangeParserError


def parse_ports(contents, unrange=False):
    port_regex = r'6553[1-5]?|655[1-2][0-9]|65[1-4][0-9]{2}|6[1-4][0-9]{3}|[1-5]?[0-9]{2,4}|[1-9]'
    regex = (
        r'('
        r'(?:(?:' + port_regex + r')(?![-]))'
        r'|'
        r'(?:(?:' + port_regex + r')\-(?:' + port_regex + r'))'
        r')'
    )

    ports = re.findall(pattern=r'\b(?<!\.)%s(?!\.)\b' % regex, string=contents)
    valid_ports = _validate_ports(ports)
    return valid_ports


def parse_ips(contents):
    ip_regex = r'25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?'
    cidr_regex = r'3[0-2]|[12]?[0-9]'

    full_ips_regex = (
        r'(' + ip_regex + r')\.'                                # first octet
        r'(' + ip_regex + r')\.'                                # second octet
        r'(' + ip_regex + r')\.'                                # third octet
        r'('                                                    # forth octet begin
        r'(?:'
        r'(?:'
        r'(?:(?:' + ip_regex + r')\/(?:' + cidr_regex + r'))'   # if ends with / and cidr
        r'|'
        r'(?:(?:' + ip_regex + r')\-(?:' + ip_regex + r'))'     # if ends with - and octet
        r'|'
        r'(?:(?:' + ip_regex + r')(?![-\/]))'                    # if ends with with on - or /
        r')'
        r'\;'
        r')*'
        r'(?:'
        r'(?:(?:' + ip_regex + r')\/(?:' + cidr_regex + r'))'   # if ends with / and cidr
        r'|'
        r'(?:(?:' + ip_regex + r')\-(?:' + ip_regex + r'))'     # if ends with - and octet
        r'|'
        r'(?:(?:' + ip_regex + r')(?![-\/]))'                    # if ends with with on - or /
        r')'
        r')'                                                    # forth octet end
    )

    # return a list of tuples with string type
    ips = re.findall(pattern=full_ips_regex, string=contents)
    valid_ips = _validate_ips(ips)
    return valid_ips


def _range_ports(ports, step=1):
    first_port = last_port = ports[0]
    for next_port in ports[1:]:
        found = False
        for index in range(1, step + 1):
            if int(next_port) - index == int(last_port):
                found = True
                last_port = next_port
                break
        if not found:
            if first_port == last_port:
                yield first_port
            else:
                yield first_port + '-' + last_port
            first_port = last_port = next_port
    if first_port == last_port:
        yield first_port
    else:
        yield first_port + '-' + last_port


def _unrange_ports(ports):
    for port in ports:
        if '-' in port:
            left, right = port.split('-')
            if int(left) < int(right):
                for i in range(int(left), int(right) + 1):
                    yield str(i)
        else:
            yield port


def _validate_ips(ips):
    if not ips:
        raise NetrangeParserError('No IP found.')

    for ip in ips:
        for part in ip[3].split(';'):
            if '-' in part:
                left, right = part.split('-')
                if int(left) < int(right):
                    yield ip
            elif '/' in part:
                yield ip
            else:
                yield ip


def _validate_ports(ports):
    if not ports:
        raise NetrangeParserError('No port found.')

    for port in ports:
        if '-' in port:
            left, right = port.split('-')
            if int(left) < int(right):
                yield port
        else:
            yield port


def _unrange_ips(ips):
    for ip in ips:
        for part in ip[3].split(';'):
            if '-' in part:
                left, right = part.split('-')
                if int(left) < int(right):
                    for i in range(int(left), int(right) + 1):
                        yield ip[:3] + (str(i),)
            elif '/' in part:
                pass
            else:
                yield ip[:3] + (part,)


def _range_ips(ips):
    ips = sorted(ips, key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    first_ip = last_ip = ips[0]
    for next_ip in ips[1:]:
        if int(last_ip[3]) + 1 == int(next_ip[3]):
            last_ip = next_ip
        else:
            if first_ip == last_ip:
                yield first_ip
            else:
                yield first_ip[:3] + (first_ip[3] + '-' + last_ip[3],)
            first_ip = last_ip = next_ip
    if first_ip == last_ip:
        yield first_ip
    else:
        yield first_ip[:3] + (first_ip[3] + '-' + last_ip[3],)


# TODO: check if max_len is less than range length
def separate_list(from_list, max_len):
    list = []
    for range in from_list:
        if (_len_list(list) + len(range) + len(list)) <= max_len:
            list.append('.'.join(range))
        else:
            yield list
            list = ['.'.join(range)]
    yield list

# TODO: check if max_len is less than range length
def separate_ports(from_list, max_len):
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


def get_unranged_ports(ports, verbose=False):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    return sorted_ports


def get_ranged_ports(ports, verbose=False, step=1):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    for ranged_ports in _range_ports(ports=sorted_ports, step=step):
        yield ranged_ports


def get_unranged_ipadds(ipaddrs, verbose=False):
    unranged_ipaddrs = _unrange_ips(ipaddrs)
    sorted_ipaddrs = sorted(set(unranged_ipaddrs), key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    return sorted_ipaddrs


def get_ranged_ips(ips, verbose=False):
    unranged_ips = _unrange_ips(ips)
    sorted_ips = sorted(set(unranged_ips), key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    for grouped_ips in _group_ipaddrs_by_octet(ipaddrs=sorted_ips, octet=3):
        for ranged_ips in _range_ips(ips=grouped_ips):
            yield ranged_ips


def get_cidr_block(ipaddrs):
    groups = _group_ipaddrs_by_octet_slow(ipaddrs).keys()
    sorted_groups = sorted(groups, key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2])))
    for group in sorted_groups:
        yield group + ('0/24',)


def _group_ipaddrs_by_octet_slow(ipaddrs, octet=3):
    groups = {}
    for ipaddr in ipaddrs:
        if ipaddr[:octet] not in groups:
            groups[ipaddr[:octet]] = []
        groups[ipaddr[:octet]].append(ipaddr[3])

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


def shorten(ipaddrs):
    for group, ipaddrs in _group_ipaddrs_by_octet_slow(ipaddrs).items():
        yield group + (';'.join(ipaddrs),)
