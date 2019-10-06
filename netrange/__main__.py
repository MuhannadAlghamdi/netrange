import sys

from netrange.cli import dispatch


def main():
    try:
        return dispatch(sys.argv[1:])
    except Exception as exc:
        return '{}: {}'.format(exc.__class__.__name__, exc.args[0])


if __name__ == "__main__":
    sys.exit(main())
