import sys

from netrange.cli import parse_args


def main():
    try:
        return parse_args(sys.argv[1:])
    except Exception as exc:
        return '{}: {}'.format(exc.__class__.__name__, exc.args[0])


if __name__ == "__main__":
    sys.exit(main())
