# IRR Generator
> Generate IRR Route Objects at scale quickly and without error

![Build][build]
[![Latest Version][irrversion-button]][irr-pypi]
[![Python Versions][pyversion-button]][irr-pypi]

Lightweight Python script designed to automate the generation of IRR Objects. Essential for the toolkit of any Network Engineers maintaining route objects.

## How
By passing a list of Supernets & Origin ASNs, IRR Generator will auto expand the Supernet and append its Subnets for route object generation.  

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install IRR Generator.
```bash
pip install irr-generator
```

## Usage
### CLI
IRR Generator can be run directly on the CLI via `irrgenerator`. In doing so, a full or relative path to a file containing the prefix data must be passed using the `--file` option (this will default to `subnets.txt` locally otherwise). The response will be directly printed to terminal for easy copy and paste.

When running IRR Generator via the CLI, `NOTIFY_EMAIL`, `MAINT_OBJECT` & `IRR_SOURCE` can directly be overriden at the top of `generate_irr.py`. Alternatively, arguments can be passed via the CLI.

```
optional arguments:
  -h, --help            show this help message and exit
  -f FILE_NAME, --file_name FILE_NAME
                        Full or Relative path to file
  -e NOTIFY_EMAIL, --notify_email NOTIFY_EMAIL
                        Notify email address set in route object
  -m MAINT_OBJECT, --maint_object MAINT_OBJECT
                        Maintainer set in route object
  -s IRR_SOURCE, --irr_source IRR_SOURCE
                        IRR Source set in route object
```

#### Example
```bash
(test-env) ╭─jamesditrapani@maximus ~/development/irr-generator
╰─$ irrgenerator -f subnets.txt -e "myemail@example.com" -m "MAINT-04" -s "NTT"
route: 1.1.1.0/24
descr: IANA-ASSIGNED
origin: AS444
notify: myemail@example.com
mnt-by: MAINT-04
changed: myemail@example.com 20210111
source: NTT
```



### Python API
IRR Generator can act as a Python API if needed. When instantiating `IRRGenerator()`, some form of data must be passed. This can be via a relative/full file path expected in `file_name` or via a dictionary of prefix/asn combos expected in `prefixes`. On init of the `IRRGenerator()` class it is also important that you pass variables to define `MAINT_OBJECT`, `NOTIFY_EMAIL` & `IRR_SOURCE` that are used when returning formatted data.

#### Examples

##### File Example
```python
from irrgenerator.irrgenerator import IRRGenerator

irr = IRRGenerator(file_name='subnets.txt')
irr.NOTIFY_EMAIL = 'example1@example.com'
irr.MAINT_OBJECT = 'MY-MAINT-01'
irr.IRR_SOURCE = 'RADB'

response = irr.create()

print(response)
```

```bash
{'1.1.1.0/24': {1: {'route': '1.1.1.0/24', 'descr': 'OVERTHEWIRE-AS-AP', 'origin': 'AS9268', 'notify': 'noc@example.com', 'mnt-by': 'MAINT-EXAMPLE-01', 'changed': 'noc@example.com 20210111', 'source': 'EXAMPLE-NTT'}}}
```

#### Dict Example
```python
from irrgenerator.irrgenerator import IRRGenerator

myprefixes = {
  '1.1.1.0/24': 'AS111',
  '2.2.2.0/23': 'AS123'
}

irr = IRRGenerator(prefixes=myprefixes)
irr.NOTIFY_EMAIL = 'test@example.com'
irr.MAINT_OBJECT = 'MY-MAINT-02'
irr.IRR_SOURCE = 'NTT'

response = irr.create()
print(response)
```

```bash
{'1.1.1.0/24': {1: {'route': '1.1.1.0/24', 'descr': 'BOSTONU-AS', 'origin': 'AS111', 'notify': 'noc@example.com', 'mnt-by': 'MAINT-EXAMPLE-01', 'changed': 'noc@example.com 20210111', 'source': 'EXAMPLE-NTT'}}, '2.2.2.0/23': {1: {'route': '2.2.2.0/23', 'descr': 'LOGAIRCOMNET-AS', 'origin': 'AS123', 'notify': 'noc@example.com', 'mnt-by': 'MAINT-EXAMPLE-01', 'changed': 'noc@example.com 20210111', 'source': 'EXAMPLE-NTT'}, 2: {'route': '2.2.2.0/24', 'descr': 'LOGAIRCOMNET-AS', 'origin': 'AS123', 'notify': 'noc@example.com', 'mnt-by': 'MAINT-EXAMPLE-01', 'changed': 'noc@example.com 20210111', 'source': 'EXAMPLE-NTT'}, 3: {'route': '2.2.3.0/24', 'descr': 'LOGAIRCOMNET-AS', 'origin': 'AS123', 'notify': 'noc@example.com', 'mnt-by': 'MAINT-EXAMPLE-01', 'changed': 'noc@example.com 20210111', 'source': 'EXAMPLE-NTT'}}}
```


#### Response Schema
```python
{
  'prefix/cidr': {
    int: {
      'route': str,
      'descr': str,
      'origin': str,
      'notify': str,
      'mnt-by': str,
      'changed': str,
      'source': str
    }
  }
}

```


## Release History
* 0.0.4
    * Beta

## Meta

James Di Trapani – [@jamesditrapani](https://twitter.com/jamesditrapani) – james[at]ditrapani.com.au

[https://github.com/jamesditrapani/](https://github.com/jamesditrapani/)


## License
[GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)


<!-- Markdown link & img dfn's -->
[build]: https://img.shields.io/github/checks-status/jamesditrapani/irr-object-creation/master
[irrversion-button]: https://img.shields.io/pypi/v/irr-generator
[irr-pypi]: https://pypi.org/project/irr-generator/
[pyversion-button]: https://img.shields.io/pypi/pyversions/irr-generator
