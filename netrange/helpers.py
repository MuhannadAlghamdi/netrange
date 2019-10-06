import re


def group_ipaddrs(ipaddrs, octet):
    group = [ipaddrs[0]]
    for ip in ipaddrs[1:]:
        if ip[:octet] == group[-1][:octet]:
            group.append(ip)
        else:
            yield group
            group = [ip]
    yield group


def range_ports(ports):
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
    list = []
    for range in from_list:
        if (len_list(list) + len(range) + len(list)) <= max_len:
            list.append(range)
        else:
            yield list
            list = [range]
    yield list


def len_list(list):
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
    for ranged_ports in range_ports(ports=sorted_ports):
        yield ranged_ports


def get_ranged_ipadds(ipaddrs, verbose=False):
    unduplicated_ipaddrs = list(set(ipaddrs))
    duplicated_ipaddrs = len(ipaddrs) - len(unduplicated_ipaddrs)
    if verbose:
        print(f'found {duplicated_ipaddrs} duplicated ip addresses')

    sorted_ipaddrs = sorted(unduplicated_ipaddrs)
    for grouped_ipaddrs in group_ipaddrs(ipaddrs=sorted_ipaddrs, octet=3):
        for ranged_ipaddrs in range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs
