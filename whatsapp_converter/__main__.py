# __main__.py

# from importlib import resources  # Python 3.7+
# import sys

import os
import argparse
from typing import Dict
from whatsapp_converter import whatsapp_converter

# the path to the directory this file is in
_MODULE_PATH = os.path.dirname(__file__)

VERSION: Dict[str, str] = {}
with open(_MODULE_PATH + "/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

SUPPORTED = (
    ".csv",
    ".xls",
    ".xlsx",
    ".ods"
)

def main():
    parser = argparse.ArgumentParser(prog='whatsapp-converter', description='Use whatsapp-converter to convert your exported WhatsApp chat to a CSV, ODS (LibreOffice) or XLS (Excel) file.', epilog='For reporting bugs or requesting features, please visit https://github.com/sandsturm/whatsapp-converter/ and create an issue')
    parser.add_argument('filename', metavar='filename', type=str, help='the WhatsApp file containing the exported chat')
    parser.add_argument('resultset', default='resultset.csv', nargs='?', help='filename of the resultset, default resultset.csv. Use .csv to write a comma separated file. Use .xls or .xlsx to write to an Excel spreadsheet file. Use .ods to write to a LibreOffice file.')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-d', '--debug', help='increase output verbosity to debug', action='store_true')
    parser.add_argument('--version', action='version', version="v" + VERSION["VERSION"])

    # parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
    args = parser.parse_args()

    if not str(args.filename):
        print(f'{bcolors["FAIL"]}ERROR: whatsapp-converter needs at least an import file.{bcolors["ENDC"]}')
        sys.exit()

    if not str(args.resultset).endswith(SUPPORTED):
        print(f'{bcolors["FAIL"]}ERROR: whatsapp-converter only supports the following fileformats:{bcolors["ENDC"]}')
        # TODO iterate over tuple
        print(SUPPORTED)
        sys.exit()

    whatsapp_converter.convert(args)

if __name__ == "__main__":
    main()
