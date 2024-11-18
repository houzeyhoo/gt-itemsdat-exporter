# gt-itemsdat-json
Python 3.11 tool to convert/parse Growtopia's items.dat file into a JSON format.

### Usage
Ensure you have Python 3.11 installed. To run the script, use the following command:
`python itemsdat-json <path to items.dat>`
The script outputs to `stdout`, you might want to pipe it to a file via your shell.

### Troubleshooting
If you encounter any issues, the parser may be outdated. In that case, consider editing the template.py file to accommodate any changes. Additionally, you can try using the itemsdat-info script to see what changes the new version introduces:
`python itemsdat-info <path to items.dat>`

### Documentation
For detailed information about Growtopia's items.dat file format, consider the following sources:
- [growtopia-docs specification](https://github.com/H-pun/growtopia-docs/tree/master/items_dat)
- [GrowDocs specification](https://github.com/iProgramMC/GrowDocs/tree/master/items_dat) 
