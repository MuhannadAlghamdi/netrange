import re


def load_ipaddrs(path):
    with open('hosts', 'r') as f:
        contents = f.read()
        regex = r'([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})\.([0-9]{1,3})'
        ipaddrs = re.findall(pattern=regex, string=contents)
        return ipaddrs


def group_ipaddrs(ipaddrs, cidr):
    group = [ipaddrs[0]]
    for ip in ipaddrs[1:]:
        if ip[:cidr] == group[-1][:cidr]:
            group.append(ip)
        else:
            yield group
            group = [ip]
    yield group


def create_range(l):
    first = last = l[0]
    for next in l[1:]:
        if int(next[3]) - 1 == int(last[3]):
            last = next
        else:
            yield '.'.join(first) + '-' + last[3]
            first = last = next
    yield '.'.join(first) + '-' + last[3]


def get_ranged_ipadds(ipaddrs_list):
    ipaddrs = load_ipaddrs(path=ipaddrs_list)
    ipaddrs = sorted(ipaddrs)
    for ip_group in group_ipaddrs(ipaddrs=ipaddrs, cidr=3):
        for range in create_range(ip_group):
            print(range)


def main():
    get_ranged_ipadds('hosts')


if __name__ == '__main__':
    main()
