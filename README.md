# cliptargets

[![PyPI](https://img.shields.io/pypi/v/cliptargets.svg)](https://pypi.org/project/cliptargets/)
[![Python Version](https://img.shields.io/pypi/pyversions/cliptargets.svg)](https://pypi.org/project/cliptargets/)
[![License](https://img.shields.io/pypi/l/cliptargets.svg)](https://github.com/lmmx/cliptargets/blob/main/LICENSE)

**Enumerate multiple clipboard targets.**

A utility to retrieve data from all available clipboard targets on X11 systems, with proper encoding detection and handling.

## Requirements

- Python 3.10+
- `xclip` command-line tool (must be installed separately)

## Installation

```bash
pip install cliptargets
```

## Usage

### Command Line

```bash
# Print all clipboard targets and their values
cliptargets

# Print as JSON
cliptargets --json
```

### Python API

```python
from cliptargets import get_all_targets, get_target_value, get_targets

# Get a list of all available targets
targets = get_targets()
print(f"Available targets: {targets}")

# Get the value of a specific target
value = get_target_value("STRING")
print(f"STRING value: {value}")

# Get a dictionary of all targets and their values
all_targets = get_all_targets()
for target, value in all_targets.items():
    print(f"{target}: {value}")
```

## Why use this library?

X11 clipboard can store data in multiple formats simultaneously, but most tools only access the default text format. This library lets you:

1. Discover all available formats in the clipboard
2. Extract data from any format
3. Handle encoding issues correctly (particularly for UTF-16LE formats)

## Example Output

```
Found 13 clipboard targets:

COMPOUND_TEXT     : 'Hello World'
MULTIPLE          : <not available>
STRING            : 'Hello World'
TARGETS           : 'TIMESTAMP\nTARGETS\nMULTIPLE\ntext/html\nUTF8_STRING\nCOMPOUND_TEXT\nTEXT\nSTRING\ntext/plain;charset=utf-8\ntext/plain'
TEXT              : 'Hello World'
TIMESTAMP         : '55692985'
UTF8_STRING       : 'Hello World'
text/_moz_htmlcontext : '<html xmlns="http://www.w3.org/1999/xhtml">...</html>'
text/_moz_htmlinfo    : '0,2'
text/html         : '<meta http-equiv="content-type" content="text/html; charset=utf-8">Hello World'
text/plain        : 'Hello World'
text/plain;charset=utf-8 : 'Hello World'
text/x-moz-url-priv : 'https://example.com'
```

## License

MIT License. See [LICENSE](LICENSE) for details.
