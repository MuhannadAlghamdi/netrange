import re
import ipaddress
from ipaddress import ip_network
from netrange._utilities import sort_ips
from netrange.exceptions import NetrangeParserError

port_regex = r'6553[1-5]?|655[1-2][0-9]|65[1-4][0-9]{2}|6[1-4][0-9]{3}|[1-5]?[0-9]{2,4}|[1-9]'
ip_regex = r'25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?'
cidr_regex = r'3[0-2]|[12]?[0-9]'


def parse_ports(contents):
    regex = (
        r'(?:'
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
    full_ips_regex = (
        r'(?:' + ip_regex + r')\.'                              # first octet
        r'(?:' + ip_regex + r')\.'                              # second octet
        r'(?:' + ip_regex + r')\.'                              # third octet
        r'(?:'                                                  # forth octet begin
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
    ips = re.findall(pattern=full_ips_regex, string=contents_str)
    ips = _validate_ips(ips=ips)
    ips = set(ips)
    if not ips:
        raise NetrangeParserError('No IP found.')
    return iter(ips)


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


def _validate_ip(ip):
    last_octet = ip.split('.')[3]
    if '-' in last_octet:
        left, right = last_octet.split('-')
        if int(left) >= int(right):
            return False
    elif '/' in last_octet:
        try:
            ip_network(ip)
        except ValueError:
            return False
    return True


def _validate_ips(ips):
    for ip in ips:
        last_octet = ip.split('.')[3]
        if ';' in last_octet:
            tmp_ips = [_replace_last_octet(ip, i) for i in last_octet.split(';')]
            if all(_validate_ip(tmp_ip) for tmp_ip in tmp_ips):
                yield ip
        else:
            if _validate_ip(ip):
                yield ip


def _validate_ports(ports):
    ports_list = list()
    for port in ports:
        if '-' in port:
            left, right = port.split('-')
            if int(left) < int(right):
                ports_list.append(port)
        else:
            ports_list.append(port)
    if not ports_list:
        raise NetrangeParserError('No port found.')
    return iter(ports_list)


def _unrange_ips(ips, cidr=False):
    for ip in ips:
        for last_octet in ip.split('.')[3].split(';'):
            if '-' in last_octet:
                left, right = last_octet.split('-')
                if int(left) < int(right):
                    for i in range(int(left), int(right) + 1):
                        yield _replace_last_octet(ip, i)
            elif cidr is True and '/' in last_octet:
                network = ip_network(address=ip)
                for host in network.hosts():
                    yield str(host)
            else:
                yield _replace_last_octet(ip, last_octet)


def _range_ips(ips):
    ips = sorted(ips, key=sort_ips)
    store = iter_ip = ips[0]
    for next_ip in ips[1:]:
        if '/' in iter_ip.split('.')[3]:
            # drop and reset
            yield iter_ip
            store = iter_ip = next_ip
        elif '/' in next_ip.split('.')[3]:
            # range if store and iter_ip are sequenced, drop and reset
            if store == iter_ip:
                yield store
            else:
                _range = store.split('.')[3] + '-' + iter_ip.split('.')[3]
                yield _replace_last_octet(store, _range)
            store = iter_ip = next_ip
        elif int(iter_ip.split('.')[3]) + 1 == int(next_ip.split('.')[3]):
            iter_ip = next_ip
        else:
            # range if store and iter_ip are sequenced, drop and reset
            if store == iter_ip:
                yield store
            else:
                _range = store.split('.')[3] + '-' + iter_ip.split('.')[3]
                yield _replace_last_octet(store, _range)
            store = iter_ip = next_ip
    # range if store and iter_ip are sequenced and drop
    if store == iter_ip:
        yield store
    else:
        _range = store.split('.')[3] + '-' + iter_ip.split('.')[3]
        yield _replace_last_octet(store, _range)


def get_unranged_ports(ports):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    return sorted_ports


def get_ranged_ports(ports, step=1):
    unranged_ports = _unrange_ports(ports)
    sorted_ports = sorted(set(unranged_ports), key=int)
    for ranged_ports in _range_ports(ports=sorted_ports, step=step):
        yield ranged_ports


def get_unranged_ips(ips, cidr):
    unranged_ips = _unrange_ips(ips, cidr=cidr)
    sorted_ips = sorted(unranged_ips, key=sort_ips)
    return sorted_ips


def get_subnet_ips(ips):
    nets = [ipaddress.ip_network(ip) for ip in ips]
    subnets = ipaddress.collapse_addresses(nets)
    return [str(ip) for ip in subnets]


def get_ranged_ips(ips, cidr):
    unranged_ips = _unrange_ips(ips=ips, cidr=cidr)
    # remove duplicate IPs after unrange
    unranged_ips = set(unranged_ips)
    sorted_ips = sorted(unranged_ips, key=sort_ips)
    for grouped_ips in _group_ips_by_octet(ips=sorted_ips, octet=3):
        for ranged_ips in _range_ips(ips=grouped_ips):
            yield ranged_ips


def _group_ips_by_octet_slow(ips, octet=3):
    groups = {}
    for ip in ips:
        splitted_ip = ip.split('.')
        key = '.'.join(splitted_ip[:octet])
        groups.setdefault(key, []).append(splitted_ip[3])
    return groups


def _group_ips_by_octet(ips, octet=3):
    group = [ips[0]]
    for ip in ips[1:]:
        if ip.split('.')[:octet] == group[-1].split('.')[:octet]:
            group.append(ip)
        else:
            yield group
            group = [ip]
    yield group


def shorten(ips):
    for group, ips in _group_ips_by_octet_slow(ips).items():
        yield group + '.' + ';'.join(ips)


def _convert_contents_to_str(contents):
    if isinstance(contents, str):
        return contents
    elif isinstance(contents, list):
        return '\n'.join(contents)
    elif isinstance(contents, tuple):
        return '\n'.join(contents)
    else:
        raise NetrangeParserError('Unknown parser type.')


def _replace_last_octet(ip, value):
    return '.'.join(ip.split('.')[:3]) + '.' + str(value)
