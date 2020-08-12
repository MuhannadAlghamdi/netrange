import sys

from netrange.cli import parse_args
from netrange.exceptions import NetrangeException


def main():
    try:
        output = parse_args(sys.argv[1:])
        print(output)
        exit(0)
    except NetrangeException as e:
        message = '{}: {}'.format(e.__class__.__name__, e.args[0])
        print(message)
        sys.exit(2)
    except Exception as e:
        message = '{}: {}'.format(e.__class__.__name__, e.args[0])
        print(message)
        sys.exit(2)


if __name__ == "__main__":
    main()
