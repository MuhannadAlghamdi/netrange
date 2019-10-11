import argparse
import netrange


def dispatch(argv):
    parser = argparse.ArgumentParser(prog='IP Range', description=netrange.__description__)
    parser.add_argument('--version', action='version', version=netrange.__version__)
    parser.add_argument('--verbose', action='store_true')
    subparser = parser.add_subparsers(dest='options', help='choose one option', required=True)

    ip_parser = subparser.add_parser('ip')
    group = ip_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--args', nargs='+')
    group.add_argument('--file', type=argparse.FileType())
    ip_parser.add_argument('--max', nargs='?', const=1, type=int, default=None)

    port_parser = subparser.add_parser('port')
    group = port_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--args', nargs='+')
    group.add_argument('--file', type=argparse.FileType())
    port_parser.add_argument('--max', nargs='?', type=int, default=None)

    args = parser.parse_args(argv)

    if args.options == 'ip':
        if args.args:
            ipaddrs = netrange.load_ips_from_string(*list(args.args), verbose=args.verbose)
        elif args.file:
            ipaddrs = netrange.load_ips_from_file(file=args.file, verbose=args.verbose)
        ranged_ipaddrs = netrange.dump_ips_string(ipaddrs=ipaddrs, max_len=args.max, verbose=args.verbose)
        print(ranged_ipaddrs)
    elif args.options == 'port':
        if args.args:
            ports = netrange.load_ports_from_string(args.args, verbose=args.verbose)
        elif args.file:
            ports = netrange.load_ports_from_file(file=args.file, verbose=args.verbose)
        ranged_ports = netrange.dump_ports_string(ports=ports, max_len=args.max, verbose=args.verbose)
        print(ranged_ports)
