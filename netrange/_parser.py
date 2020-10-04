import re
from ipaddress import ip_network
from netrange.exceptions import NetrangeParserError


def parse_ports(contents):
    port_regex = r'6553[1-5]?|655[1-2][0-9]|65[1-4][0-9]{2}|6[1-4][0-9]{3}|[1-5]?[0-9]{2,4}|[1-9]'
    regex = (
        r'('
        r'(?:(?:' + port_regex + r')(?![-]))'
        r'|'
        r'(?:(?:' + port_regex + r')\-(?:' + port_regex + r'))'
        r')'
    )

    contents_str = _convert_contents_to_str(contents)
    ports = re.findall(pattern=r'\b(?<!\.)%s(?!\.)\b' % regex, string=contents_str)
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

    contents_str = _convert_contents_to_str(contents)
    # return a list of tuples with string type
    ips = re.findall(pattern=full_ips_regex, string=contents_str)
    valid_ips = _validate_ips(ips=ips)
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
    _list = list()
    for ip in ips:
        for part in ip[3].split(';'):
            if '-' in part:
                left, right = part.split('-')
                if int(left) < int(right):
                    _list.append(ip)
            elif '/' in part:
                try:
                    ip_network(address='.'.join(ip))
                    _list.append(ip)
                # the network has host bits set
                except ValueError:
                    pass
            else:
                _list.append(ip)
    if not _list:
        raise NetrangeParserError('No IP found.')
    return iter(_list)


def _validate_ports(ports):
    _list = list()
    for port in ports:
        if '-' in port:
            left, right = port.split('-')
            if int(left) < int(right):
                _list.append(port)
        else:
            _list.append(port)
    if not _list:
        raise NetrangeParserError('No port found.')
    return iter(_list)


def _unrange_ips(ips):
    for ip in ips:
        for part in ip[3].split(';'):
            if '-' in part:
                left, right = part.split('-')
                if int(left) < int(right):
                    for i in range(int(left), int(right) + 1):
                        yield ip[:3] + (str(i),)
            elif '/' in part:
                network = ip_network(address='.'.join(ip))
                for host in network.hosts():
                    yield tuple(str(host).split('.'))
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


def get_unranged_ports(ports):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    return sorted_ports


def get_ranged_ports(ports, step=1):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    for ranged_ports in _range_ports(ports=sorted_ports, step=step):
        yield ranged_ports


def get_unranged_ips(ips):
    unranged_ips = _unrange_ips(ips)
    sorted_ips = sorted(set(unranged_ips), key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    return sorted_ips


def get_ranged_ips(ips):
    unranged_ips = _unrange_ips(ips)
    sorted_ips = sorted(set(unranged_ips), key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2]), int(ip[3])))
    for grouped_ips in _group_ips_by_octet(ips=sorted_ips, octet=3):
        for ranged_ips in _range_ips(ips=grouped_ips):
            yield ranged_ips


def get_cidr_block(ips):
    groups = _group_ips_by_octet_slow(ips).keys()
    sorted_groups = sorted(groups, key=lambda ip: (int(ip[0]), int(ip[1]), int(ip[2])))
    for group in sorted_groups:
        yield group + ('0/24',)


def _group_ips_by_octet_slow(ips, octet=3):
    groups = {}
    for ip in ips:
        if ip[:octet] not in groups:
            groups[ip[:octet]] = []
        groups[ip[:octet]].append(ip[3])

    return groups


def _group_ips_by_octet(ips, octet=3):
    group = [ips[0]]
    for ip in ips[1:]:
        if ip[:octet] == group[-1][:octet]:
            group.append(ip)
        else:
            yield group
            group = [ip]
    yield group


def shorten(ips):
    for group, ips in _group_ips_by_octet_slow(ips).items():
        yield group + (';'.join(ips),)


def _convert_contents_to_str(contents):
    if isinstance(contents, str):
        return contents
    elif isinstance(contents, list):
        return '\n'.join(contents)
    elif isinstance(contents, tuple):
        return '\n'.join(contents)
    else:
        raise NetrangeParserError('Unknown parser type.')
