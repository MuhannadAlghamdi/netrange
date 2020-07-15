from netrange.cli import parse_args


def test_ips():
    output = parse_args('ip')
    assert output == 'args'
