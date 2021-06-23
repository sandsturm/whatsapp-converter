# __main__.py

# from importlib import resources  # Python 3.7+
# import sys

import os
import sys
import argparse
import platform
from typing import Dict

from whatsapp_converter import whatsapp_converter
from whatsapp_converter import colors

# the path to the directory this file is in
_MODULE_PATH = os.path.dirname(__file__)

VERSION: Dict[str, str] = {}
with open(_MODULE_PATH + "/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

# ---------------------------------------------
# Supported filetypes for the resultset
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
    parser.add_argument('-n', '--newline', help='create a new line (same date and time) in the resultset for every multline chat message', action='store_true')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-d', '--debug', help='increase output verbosity to debug', action='store_true')
    parser.add_argument('--version', action='version', version="v" + VERSION["VERSION"])

    # parser.add_argument("-nl", "--newline", help = "message across various lines is counted as a new message", action = "store_true")
    args = parser.parse_args()

    if not str( args.filename ):
        if( platform.system() == "Linux" ):
            print(f'{colors.BCOLORS["FAIL"]}ERROR: whatsapp-converter needs at least an import file.{colors.BCOLORS["ENDC"]}')
        else:
            print("ERROR: whatsapp-converter needs at least an import file.")
        sys.exit()

    if not str( args.resultset ).endswith( SUPPORTED ):
        if( platform.system() == "Linux" ):
            print(f'{colors.BCOLORS["FAIL"]}ERROR: whatsapp-converter only supports the following fileformats:{colors.BCOLORS["ENDC"]}')
        else:
            print("ERROR: whatsapp-converter only supports the following fileformats:")

        # TODO iterate over tuple
        print(SUPPORTED)
        sys.exit()

    whatsapp_converter.convert(args)


if __name__ == "__main__":
    main()
