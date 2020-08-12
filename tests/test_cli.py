from netrange.cli import parse_args


def test_ips():
    output = parse_args(['--ip', '192.21.51.111'])
    print(output)
    assert output == '192.21.51.111'
