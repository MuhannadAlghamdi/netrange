# NetRange

A simple package for reading and ranging IPs and ports.

[![PyPI](https://img.shields.io/pypi/v/netrange)](https://pypi.org/project/netrange/)
![Travis (.org)](https://img.shields.io/travis/muhannadalghamdi/netrange)
![PyPI - Downloads](https://img.shields.io/pypi/dd/netrange)
![GitHub](https://img.shields.io/github/license/muhannadalghamdi/netrange)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netrange)](https://pypi.org/project/netrange/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/netrange)](https://pypi.org/project/netrange/#files)

## Installation

Run the following to install:

```bash
pip install netrange
```

## Usage

### From CLI

```bash
$ netrange --help
usage: IP Range [-h] [--version] [--verbose] {ip,port} ...

A simple package for reading and ranging IPs and ports.

positional arguments:
  {ip,port}   choose one option

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
  --verbose
```

### From Module

```python
import netrange


ips = ip.load(from_file=file)
ranged_ips = ip.dump(ips)
```
