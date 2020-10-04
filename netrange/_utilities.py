def len_list(_list):
    _max = 0
    for i in _list:
        _max += len(i)
    return _max


def separate_list(_list, max_len, delimiter):
    separated_list = []
    tmp = []
    for item in _list:
        if (len_list(tmp) + len(item) + len(tmp)) <= max_len:
            tmp.append(item)
        else:
            separated_list.append(delimiter.join(tmp))
            tmp = [item]
    separated_list.append(delimiter.join(tmp))
    return separated_list


def sort_ips(ip):
    first_part = ip[3].split(';')[0]
    if '-' in first_part:
        left, right = first_part.split('-')
        return int(ip[0]), int(ip[1]), int(ip[2]), int(left), int(right)
    elif '/' in first_part:
        left, right = first_part.split('/')
        return int(ip[0]), int(ip[1]), int(ip[2]), int(left), int(right)
    else:
        left = first_part
        return int(ip[0]), int(ip[1]), int(ip[2]), int(left), 0
