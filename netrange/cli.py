import argparse
import netrange


def dispatch(argv):
    parser = argparse.ArgumentParser(prog='IP Range', description='Script to range multiple IPs as well as ports.')
    parser.add_argument('--verbose', action='store_true')
    subparser = parser.add_subparsers(dest='options', help='choose script action', required=True)

    ip_parser = subparser.add_parser('ip', help='ip options')
    group = ip_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--args', nargs='+')
    group.add_argument('--file')
    ip_parser.add_argument('--max', nargs='?', const=1, type=int, default=None)

    port_parser = subparser.add_parser('port', help='port options')
    group = port_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--args', nargs='+')
    group.add_argument('--file')
    port_parser.add_argument('--max', nargs='?', type=int, default=None)

    args = parser.parse_args(argv)

    if args.options == 'ip':
        ipaddrs = netrange.load_ipaddrs(from_args=args.args, from_file=args.file, verbose=args.verbose)
        ranged_ipaddrs = netrange.dumps_ipaddrs(ipaddrs=ipaddrs, max_len=args.max, verbose=args.verbose)
        print(ranged_ipaddrs)
    elif args.options == 'port':
        ports = netrange.load_ports(from_args=args.args, from_file=args.file, verbose=args.verbose)
        ranged_ports = netrange.dumps_ports(ports=ports, max_len=args.max, verbose=args.verbose)
        print(ranged_ports)
