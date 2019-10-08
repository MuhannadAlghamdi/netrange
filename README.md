# NetRange

[![PyPI version](https://badge.fury.io/py/netrange.svg)](https://badge.fury.io/py/netrange)
![Travis (.org)](https://img.shields.io/travis/muhannadalghamdi/netrange)
![PyPI - Downloads](https://img.shields.io/pypi/dd/netrange)
![GitHub](https://img.shields.io/github/license/muhannadalghamdi/netrange)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/netrange)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/netrange)

## Installation

Run the following to install:

```bash
pip install netrange
```

## Usage

### From CLI

```bash
netrange ip --args 192.168.1.2 192.168.1.3 192.168.1.4
192.168.1.2-4
```

### From Module

```python
import netrange


ips = netrange.load_ipaddrs(from_file=file)
ranged_ips = netrange.dump(ips)
```
