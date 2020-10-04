from netrange.dump import dump_ips
from netrange.dump import dumps_ips
from netrange.dump import dump_ports
from netrange.dump import dumps_ports
from netrange.load import load_ips_from_file
from netrange.load import load_ports_from_file
from netrange.load import loads_ips
from netrange.load import loads_ports
from netrange import exceptions

__version__ = '0.0.18'
__description__ = 'A simple package for reading and ranging IPs and ports.'
__all__ = [
    '__version__',
    '__description__',
    'dump_ips',
    'dumps_ips',
    'dump_ports',
    'dumps_ports',
    'load_ips_from_file',
    'load_ports_from_file',
    'loads_ips',
    'loads_ports',
    'exceptions'
]
