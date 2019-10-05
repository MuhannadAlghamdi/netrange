import argparse
import iprange


def main():
    parser = argparse.ArgumentParser(prog='IP Range', description='Script to range multiple IPs as well as ports.')
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
        ips = iprange.load_ipaddrs(from_args=args.args, from_file=args.file)
        post_range = iprange.ranged_ipaddrs(ipaddrs=ips, max_len=args.max)
        print([range for range in post_range])
    elif args.options == 'port':
        ports = iprange.load_ports(from_args=args.args, from_file=args.file)
        ranged_ports = iprange.ranged_ports(ports=ports, max_len=args.max)
        print([range for range in ranged_ports])


if __name__ == "__main__":
    main()
