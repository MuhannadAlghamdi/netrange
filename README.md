# NetRange

This is a library that can load IP addresses and ports from list or file and return a list of ranges.

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

### From Modual

```python
import netrange


ips = netrange.load_ipaddrs(from_file=file)
ranged_ips netrange.dump(ips)
```
