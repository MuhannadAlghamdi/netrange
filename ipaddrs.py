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


def get_ranged_ipadds(ipaddrs):
    ipaddrs = sorted(ipaddrs)
    for ip_group in group_ipaddrs(ipaddrs=ipaddrs, cidr=3):
        for range in create_range(ip_group):
            yield range


def len_list(list):
    max = 0
    for i in list:
        max += len(i)

    return max


def seperate_list(ipaddrs, max_len):
    list = []
    for range in ipaddrs:
        if (len_list(list) + len(range)) <= max_len:
            list.append(range)
        else:
            yield list
            list = []



def main():
    ipaddrs = load_ipaddrs(path='eai')
    ipranges = [range for range in get_ranged_ipadds(ipaddrs=ipaddrs)]
    for list in seperate_list(ipaddrs=ipranges, max_len=200):
        print(list)
    #print(ipranges)


if __name__ == '__main__':
    main()
