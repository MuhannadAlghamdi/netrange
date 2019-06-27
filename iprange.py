#!/usr/bin/env python3

import re
import argparse


def load_ports(from_file):
    with open(from_file, 'r') as f:
        contents = f.read()

    regex = r'\b([1-9]|[1-5]?[0-9]{2,4}|6[1-4][0-9]{3}|65[1-4][0-9]{2}|655[1-2][0-9]|6553[1-5]?)\b'

    ports = re.findall(pattern=regex, string=contents)
    print(f'loaded {len(ports)} ports')
    return ports


def load_ipaddrs(from_args=None, from_file=None):
    if from_args:
        contents = "\n".join(from_args)
    elif from_file:
        with open(from_file, 'r') as f:
            contents = f.read()

    regex = r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
            r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    ipaddrs = re.findall(pattern=regex, string=contents)
    print(f'loaded {len(ipaddrs)} ip addresses')
    return ipaddrs


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


def get_ranged_ports(ports):
    sorted_ports = sorted(ports, key=int)
    for ranged_ports in range_ports(ports=sorted_ports):
        yield ranged_ports


def get_ranged_ipadds(ipaddrs):
    ipaddrs = sorted(ipaddrs)
    for grouped_ipaddrs in group_ipaddrs(ipaddrs=ipaddrs, octet=3):
        for ranged_ipaddrs in range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs


def main(args):
    if args.ip:
        ipaddrs = load_ipaddrs(from_file=args.ip)
        ranged_ipaddrs_gen = get_ranged_ipadds(ipaddrs=ipaddrs)
        separated_ipaddrs_gen = separate_list(from_list=ranged_ipaddrs_gen, max_len=args.max)
        for range in separated_ipaddrs_gen:
            print(','.join(range))

    elif args.port:
        ports = load_ports(from_file=args.port)
        ranged_ports_gen = get_ranged_ports(ports=ports)
        separated_ports_gen = separate_list(from_list=ranged_ports_gen, max_len=args.max)
        for range in separated_ports_gen:
            print(','.join(range))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip')
    parser.add_argument('--port')
    parser.add_argument('--max', nargs='?', const=1, type=int, default=99)
    args = parser.parse_args()
    main(args=args)
