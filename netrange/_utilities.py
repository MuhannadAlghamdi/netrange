def len_list(_list):
    _max = 0
    for i in _list:
        _max += len(i)
    return _max


def separate_list(_list, max_len, line_sep):
    separated_list = []
    tmp = []
    for item in _list:
        if (len_list(tmp) + len(item) + len(tmp)) <= max_len:
            tmp.append(item)
        else:
            separated_list.append(line_sep.join(tmp))
            tmp = [item]
    separated_list.append(line_sep.join(tmp))
    return separated_list


def sort_ips(ip):
    splitted_ip = ip.split('.')
    last_octet = splitted_ip[3].split(';')[0]
    if '-' in last_octet:
        left, right = last_octet.split('-')
        return int(splitted_ip[0]), int(splitted_ip[1]), int(splitted_ip[2]), int(left), int(right)
    elif '/' in last_octet:
        left, right = last_octet.split('/')
        return int(splitted_ip[0]), int(splitted_ip[1]), int(splitted_ip[2]), int(left), int(right)
    else:
        left = last_octet
        return int(splitted_ip[0]), int(splitted_ip[1]), int(splitted_ip[2]), int(left), 0
