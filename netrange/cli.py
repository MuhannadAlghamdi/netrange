import sys
import argparse
import netrange


def create_parser():
    parser = argparse.ArgumentParser(prog='IP Range', description=netrange.__description__)
    parser.add_argument('--version', action='version', version=netrange.__version__)
    parser.add_argument('args', nargs='*')
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('--file', type=argparse.FileType())
    parser.add_argument('--max', nargs='?', const=1, type=int, default=None)
    parser.add_argument('-d', '--delimiter', default='\n')
    parser.add_argument('--shorter', action='store_true')
    parser.add_argument('--step', nargs='?', const=1, type=int, default=1)
    primary_group = parser.add_mutually_exclusive_group(required=True)
    primary_group.add_argument('--ip', action='store_true')
    primary_group.add_argument('--port', action='store_true')
    optional_group = parser.add_mutually_exclusive_group()
    optional_group.add_argument('--range', action='store_true')
    optional_group.add_argument('--unrange', action='store_true')
    optional_group.add_argument('--cidr', action='store_true')
    return parser


def parse_args(args):
    parser = create_parser()
    args = parser.parse_args(args)
    stdin = args.args
    piped_stdin = args.stdin.read().splitlines() if not sys.stdin.isatty() else []
    from_file = args.file.read() if args.file else []

    if args.ip:
        ranged_ips = netrange.dumps_ips(*list(stdin + piped_stdin + from_file), max_len=args.max, _range=args.range, cidr=args.cidr, unrange=args.unrange, delimiter=args.delimiter, shorter=args.shorter)
        return ranged_ips
    elif args.port:
        ranged_ports = netrange.dumps_ports(*list(stdin + piped_stdin + from_file), max_len=args.max, _range=args.range, unrange=args.unrange, delimiter=args.delimiter, step=args.step)
        return ranged_ports
