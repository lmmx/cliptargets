# cliptargets

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pdm-managed](https://img.shields.io/badge/pdm-managed-blueviolet)](https://pdm.fming.dev)
[![PyPI](https://img.shields.io/pypi/v/cliptargets.svg)](https://pypi.org/project/cliptargets/)
[![Python Version](https://img.shields.io/pypi/pyversions/cliptargets.svg)](https://pypi.org/project/cliptargets/)
[![License](https://img.shields.io/pypi/l/cliptargets.svg)](https://github.com/lmmx/cliptargets/blob/main/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lmmx/cliptargets/master.svg)](https://results.pre-commit.ci/latest/github/lmmx/cliptargets/master)

**Enumerate multiple X11 clipboard targets (formats).**

Python package for enumerating and accessing multiple clipboard targets (formats) in X11.

## Background

In the [X Window System](https://en.wikipedia.org/wiki/X_Window_System), a clipboard can hold data
in multiple different formats simultaneously—in
*[superposition](https://en.wikipedia.org/wiki/Quantum_superposition)*. Each format (such as plain
text, UTF-8 text, or images) is identified by a *target*, with a label that is sometimes a [MIMEtype](https://en.wikipedia.org/wiki/Media_type).

- The program that owns the clipboard, such as [xclip](https://en.wikipedia.org/wiki/Xclip),
  announces these available targets to other applications.
- When another application wants to paste, it requests the clipboard data in a specific target format.
- The clipboard owner then converts and provides the data in the requested format.
- Although the clipboard owner stores only one original copy of the data, it can supply this data in
  various formats, depending on what the requesting application needs.

> See [How It Works](https://github.com/lmmx/cliptargets/blob/master/docs/how-it-works.md) for more details

cliptargets handles encoding (some clipboard targets may be non-UTF8) as either a CLI or Python API for inspecting the clipboard's contents across all available formats.

## Features

- **Comprehensive Target Discovery**: Enumerate all available clipboard targets/formats
- **Intelligent Encoding Detection**: Automatically detects and properly handles various encodings (UTF-8, UTF-16LE, Latin-1)
- **Format-Specific Handling**: Special handling for Mozilla-specific formats and other binary formats
- **Simple CLI**: Command-line interface for quick clipboard inspection
- **Clean Python API**: Programmatic access to clipboard targets
- **JSON Output**: Option to export all targets and values as JSON
- **Zero Dependencies**: Core functionality has no external dependencies (beyond xclip)

## Installation

```bash
pip install cliptargets
```

### Requirements

- Python 3.10+
- `xclip`

> Note: The `xclip` command-line tool must be installed on your system separately.
> - On Debian/Ubuntu: `sudo apt install xclip`
> - On Fedora/RHEL: `sudo dnf install xclip`
> - On Arch Linux: `sudo pacman -S xclip`

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

### Use in Scripts

```python
import cliptargets
import json

# Get HTML content from clipboard if available
html_content = cliptargets.get_target_value("text/html")
if html_content:
    print("HTML content found in clipboard!")
    # Process the HTML...

# Check if a URL is in the clipboard
url = cliptargets.get_target_value("text/x-moz-url-priv")
if url:
    print(f"URL found: {url}")

# Export all clipboard data to a JSON file
all_targets = cliptargets.get_all_targets()
with open("clipboard_data.json", "w") as f:
    json.dump(all_targets, f, indent=2)
```

## Why Use This Library?

X11 clipboard can store data in multiple formats simultaneously, but most tools only access the default text format. This library lets you:

1. **Discover Hidden Data**: Access formats like HTML, URLs, and application-specific data
2. **Debug Copy/Paste Issues**: Diagnose why copy/paste operations work differently between applications
3. **Handle Encoding Correctly**: Avoid encoding problems with UTF-16LE and other formats
4. **Access Raw Data**: Get direct access to clipboard data without application interference
5. **Build Better Tools**: Create clipboard managers and data transfer tools with access to all formats

## Example Output

### STDOUT

```
Found 9 clipboard targets:

COMPOUND_TEXT            : Hello World
MULTIPLE                 : <not available>
STRING                   : Hello World
TARGETS                  :
TIMESTAMP\nTARGETS\nMULTIPLE\nUTF8_STRING\nCOMPOUND_TEXT\nTEXT\nSTRING\ntext/plain;charset=utf-8\ntext/plain\n
TEXT                     : Hello World
TIMESTAMP                : 62401715\n
UTF8_STRING              : Hello World
text/plain               : Hello World
text/plain;charset=utf-8 : Hello World
```

### JSON

```json
{
  "TIMESTAMP": "62401715\n",
  "TARGETS":
"TIMESTAMP\nTARGETS\nMULTIPLE\nUTF8_STRING\nCOMPOUND_TEXT\nTEXT\nSTRING\ntext/plain;charset=utf-8\ntext/plain\n",
  "MULTIPLE": null,
  "UTF8_STRING": "Hello World",
  "COMPOUND_TEXT": "Hello World",
  "TEXT": "Hello World",
  "STRING": "Hello World",
  "text/plain;charset=utf-8": "Hello World",
  "text/plain": "Hello World"
}
```

## Project Structure

- `cliptargets/core.py`: Core functionality for handling clipboard targets and encoding
- `cliptargets/cli.py`: Command-line interface implementation
- `cliptargets/__init__.py`: Package exports and version information

## Standard X11 Selection Targets

The ICCCM (Inter-Client Communication Conventions Manual) defines a comprehensive set of standard selection targets. Below is a table of these targets as defined in the X Consortium standards:

| Target Atom | Type | Data Received |
|-------------|------|---------------|
| ADOBE_PORTABLE_DOCUMENT_FORMAT | STRING | PDF content |
| APPLE_PICT | APPLE_PICT | Apple PICT format image data |
| BACKGROUND | PIXEL | A list of pixel values |
| BITMAP | BITMAP | A list of bitmap IDs |
| CHARACTER_POSITION | SPAN | The start and end of the selection in bytes |
| CLASS | TEXT | Window class information |
| CLIENT_WINDOW | WINDOW | Any top-level window owned by the selection owner |
| COLORMAP | COLORMAP | A list of colormap IDs |
| COLUMN_NUMBER | SPAN | The start and end column numbers |
| COMPOUND_TEXT | COMPOUND_TEXT | Compound Text |
| DELETE | NULL | Special target with side effect (selection deletion) |
| DRAWABLE | DRAWABLE | A list of drawable IDs |
| ENCAPSULATED_POSTSCRIPT | STRING | EPS data |
| ENCAPSULATED_POSTSCRIPT_INTERCHANGE | STRING | EPSI data |
| FILE_NAME | TEXT | The full path name of a file |
| FOREGROUND | PIXEL | A list of pixel values |
| HOST_NAME | TEXT | The hostname of the client machine |
| INSERT_PROPERTY | NULL | Special target with side effect |
| INSERT_SELECTION | NULL | Special target with side effect |
| LENGTH | INTEGER | The number of bytes in the selection |
| LINE_NUMBER | SPAN | The start and end line numbers |
| LIST_LENGTH | INTEGER | The number of disjoint parts of the selection |
| MODULE | TEXT | The name of the selected procedure |
| MULTIPLE | ATOM_PAIR | For requesting multiple targets in one operation |
| NAME | TEXT | Window name information |
| ODIF | TEXT | ISO Office Document Interchange Format |
| OWNER_OS | TEXT | The operating system of the owner client |
| PIXMAP | PIXMAP | A list of pixmap IDs |
| POSTSCRIPT | STRING | PostScript data |
| PROCEDURE | TEXT | The name of the selected procedure |
| PROCESS | INTEGER, TEXT | The process ID of the owner |
| STRING | STRING | ISO Latin-1 (+TAB+NEWLINE) text |
| TARGETS | ATOM | A list of valid target atoms (required) |
| TASK | INTEGER, TEXT | The task ID of the owner |
| TEXT | TEXT | The text in the owner's choice of encoding |
| TIMESTAMP | INTEGER | The timestamp used to acquire the selection (required) |
| USER | TEXT | The name of the user running the owner |

These targets allow for rich data exchange between X11 applications. The most commonly used are STRING, UTF8_STRING, and text/plain, but applications should be prepared to handle any of these targets.

Selection owners are required to support at least TARGETS (which returns the list of supported targets) and TIMESTAMP (which returns the time the selection was acquired).

For more comprehensive details, see the [X Consortium: _Inter-Client Communication Conventions Manual_](https://x.org/releases/X11R7.6/doc/xorg-docs/specs/ICCCM/icccm.html).

## Contributing

Contributions are welcome!

1. **Issues & Discussions**: Please open a GitHub issue for bugs, feature requests, or questions.
2. **Pull Requests**: PRs are welcome!
   - Install the dev dependencies with `pip install -e ".[dev]"`
   - Make sure tests pass with `pytest`
   - Format code with `pre-commit run --all-files`

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Credits

The original inspiration for this tool came from troubleshooting complex clipboard encoding issues with X11 applications. Special thanks to the X.org community and the ICCCM documentation.
