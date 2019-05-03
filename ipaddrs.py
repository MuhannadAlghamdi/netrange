import re


def load_ipaddrs(path):
    with open(path, 'r') as f:
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


def separate_list(ipaddrs, max_len):
    list = []
    for range in ipaddrs:
        if (len_list(list) + len(range)) <= max_len:
            list.append(range)
        else:
            yield list
            list = []
    yield list


def len_list(list):
    max = 0
    for i in list:
        max += len(i)

    return max


def get_ranged_ipadds(ipaddrs):
    ipaddrs = sorted(ipaddrs)
    for grouped_ipaddrs in group_ipaddrs(ipaddrs=ipaddrs, octet=3):
        for ranged_ipaddrs in range_ipaddrs(ipaddrs=grouped_ipaddrs):
            yield ranged_ipaddrs


def main():
    ipaddrs = load_ipaddrs(path='eai')
    ranged_ipaddrs_gen = get_ranged_ipadds(ipaddrs=ipaddrs)
    separated_ipaddrs_gen = separate_list(ipaddrs=ranged_ipaddrs_gen, max_len=350)

    for range in separated_ipaddrs_gen:
        print(','.join(range))


if __name__ == '__main__':
    main()
