import sys
import argparse
import netrange


def create_parser():
    parser = argparse.ArgumentParser(prog='IP Range', description=netrange.__description__)
    parser.add_argument('--version', action='version', version=netrange.__version__)
    parser.add_argument('--verbose', action='store_true')
    subparser = parser.add_subparsers(dest='options', help='choose one option', required=True)

    ip_parser = subparser.add_parser('ip')
    ip_parser.add_argument('args', nargs='*')
    ip_parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    ip_parser.add_argument('--file', type=argparse.FileType())
    ip_parser.add_argument('--max', nargs='?', const=1, type=int, default=None)
    ip_parser.add_argument('--range', action='store_true')

    port_parser = subparser.add_parser('port')
    port_parser.add_argument('args', nargs='*')
    port_parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    port_parser.add_argument('--file', type=argparse.FileType())
    port_parser.add_argument('--max', nargs='?', type=int, default=None)
    port_parser.add_argument('--range', action='store_true')

    return parser


def parse_args(args):
    parser = create_parser()
    args = parser.parse_args(args)
    if args.options == 'ip':
        stdin = args.args
        piped_stdin = args.stdin.read().splitlines() if not sys.stdin.isatty() else []
        from_file = netrange.load_ips_from_file(file=args.file, verbose=args.verbose) if args.file else []
        ipaddrs = netrange.loads_ips(*list(stdin + piped_stdin + from_file), verbose=args.verbose)
        ranged_ipaddrs = netrange.dumps_ips(ipaddrs=ipaddrs, max_len=args.max, verbose=args.verbose, range=args.range)
        print(ranged_ipaddrs)
        exit(0)
    elif args.options == 'port':
        stdin = args.args
        piped_stdin = args.stdin.read().splitlines() if not sys.stdin.isatty() else []
        from_file = netrange.load_ports_from_file(file=args.file, verbose=args.verbose) if args.file else []
        ports = netrange.loads_ports(*list(stdin + piped_stdin + from_file), verbose=args.verbose)
        ranged_ports = netrange.dumps_ports(ports=ports, max_len=args.max, verbose=args.verbose, range=args.range)
        print(ranged_ports)
        exit(0)
