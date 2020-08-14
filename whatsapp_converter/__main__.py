# __main__.py

# from importlib import resources  # Python 3.7+
# import sys

import argparse
from whatsapp_converter import whatsapp_converter

def main():
    parser = argparse.ArgumentParser(prog='whatsapp-converter', epilog='For reporting bugs or requesting features, please visit https://github.com/sandsturm/whatsapp-converter/ and create an issue')
    parser.add_argument('filename', metavar='filename', type=str, help='the WhatsApp file containing the exported chat')
    parser.add_argument('resultset', default='resultset.csv', nargs='?', help='filename of the resultset, default resultset.csv. Use .csv to write a comma separated file. Use .ods to write to a LibreOffice spreadsheet file')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-d', '--debug', help='increase output verbosity to debug', action='store_true')

    # parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
    args = parser.parse_args()

    print ("WhatsApp Converter to read exported chat files from WhatsApp and convert them to a CSV file")
    whatsapp_converter.convert(args)

if __name__ == "__main__":
    main()
