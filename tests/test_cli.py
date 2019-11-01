from netrange.cli import dispatch


def test_ips():
    output = dispatch('ip')
    assert output == 'args'
