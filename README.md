# gt-itemsdat-exporter
Tool for exporting Growtopia's items.dat file to other formats.

## Usage
Simply run the `itemsdat-export.py` wrapper script:
```bash
python itemsdat-export.py <path to items.dat> [options]
```
Keep in mind that the tool writes exclusively to stdout. If you want to save the output to a file, you must redirect 
it yourself.

To see all available options, view the help message by running:
```bash
python itemsdat-export.py -h
```

## Install
You may install the tool system-wide by running:
```
pip install .
```
Once installed, the exporter can be invoked like this:
```
itemsdat-export <path to items.dat> [options]
```

## Future Compatibility
This project may be slow to support future items.dat versions. However, you may use the tool's `-V` and `-d` flags to 
force an export of unsupported versions and diagnose structure changes. 

For example, if a future update adds a 4-byte field at the end of an item definition, you can bypass the version check 
and skip these bytes manually:
```bash
python itemsdat-export.py <path to items.dat> -f <format> -V -d 4
```
PRs that introduce support for new versions are always appreciated.

## Acknowledgements
This tool was largely made possible by the reverse-engineering work provided by [Cernodile](https://github.com/cernodile).
