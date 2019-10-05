import argparse
from iprange import IPRange


def main():
    parser = argparse.ArgumentParser(prog='IP Range', description='Script to range multiple IPs as well as ports.')
    parser.add_argument('--verbose', action='store_true')
    subparser = parser.add_subparsers(dest='options', help='choose script action', required=True)

    ip_parser = subparser.add_parser('ip', help='ip options')
    group = ip_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--args', nargs='+')
    group.add_argument('--file', type=argparse.FileType('r'))
    ip_parser.add_argument('--max', nargs='?', const=1, type=int, default=None)

    port_parser = subparser.add_parser('port', help='port options')
    group = port_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--args', nargs='+')
    group.add_argument('--file', type=argparse.FileType('r'))
    port_parser.add_argument('--max', nargs='?', type=int, default=None)

    args = parser.parse_args()

    if args.options == 'ip':
        iprange = IPRange(from_args=args.args, from_file=args.file, verbose=args.verbose)
        ips = iprange.load_ipaddrs()
        ranged_ips = iprange.ranged_ipaddrs(ipaddrs=ips, max_len=args.max)
        print([range for range in ranged_ips])
    elif args.options == 'port':
        iprange = IPRange(from_args=args.args, from_file=args.file, verbose=args.verbose)
        ports = iprange.load_ports()
        ranged_ports = iprange.ranged_ports(ports=ports, max_len=args.max)
        print([range for range in ranged_ports])


if __name__ == "__main__":
    main()
