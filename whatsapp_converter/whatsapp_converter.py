'''whatsapp-converter

Use this application to convert your exported WhatsApp chat to a CSV or Excel file.

1. The conversion is done locally. No data is shared with the internet!
2. The resultset is a CSV file which you can import into your favorite calculation application such as Excel or LibreOffice. You can also directly export to a XLS spreadsheet file.

'''
import os
import io
import re
import sys
import argparse
import datetime
from datetime import date
import xlwt
from tqdm import tqdm
from typing import Dict

# the path to the directory this file is in
_MODULE_PATH = os.path.dirname(__file__)

VERSION: Dict[str, str] = {}
with open(_MODULE_PATH + "/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)


# Add colors to output
bcolors = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m"
}

lastentry = {
    "lastdate": date.today(),
    "lasttime": date.today(),
    "lastname": ""
}

# Define export file header
header = [
    'Date and Time',
    'Date',
    'Time',
    'Name',
    'Message'
]

def parse(line, local_args):
    '''Parse each line

    line = Single line to parse
    args = Arguments from the command line. In this case only verbose and debug switches.
    '''
    patterndate = "^((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,2}))\,\ (\d{1,2}:\d{1,2})(?::\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ ][^:])(.+?)\:"
    pattern = "^((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,2}))\,\ (\d{1,2}:\d{1,2})(?::\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ ][^:])(.+?)\:\ (.*)"

    dataset = ['empty', '', '', '', '', '']
    # if verbose: print(prefix + line)
    # if verbose: print(BColors.FAIL + prefix + line)
    # Identify the date format in the chat line

    if re.match(re.compile(patterndate, re.VERBOSE), line):
        # Make the match, assign to the groups
        match = re.match(re.compile(pattern, re.VERBOSE), line)

        if match and match.group(9) != 'M':
            # 21/12/19 Date Format
            if match.group(3) == '/' and match.group(8) == ': ':
                date = datetime.datetime.strptime(match.group(1), "%d/%m/%y").date()
            # 12/21/19 Date Format
            elif match.group(3) == '/' and (match.group(8) == ' -' or match.group(8) == '- '):
                date = datetime.datetime.strptime(match.group(1), "%m/%d/%y").date()
            # 21.12.19 Date Format
            else:
                date = datetime.datetime.strptime(match.group(1), "%d.%m.%y").date()

            if match.group(7):
                time = datetime.datetime.strptime(match.group(6) + " " + match.group(7), "%I:%M %p").time()
            else:
                time = datetime.datetime.strptime(match.group(6), "%H:%M").time()

            # Buffer date, time, name for next line messages
            lastentry["lastdate"] = date.strftime("%Y-%m-%d")
            lastentry["lasttime"] = time.strftime("%H:%M")
            lastentry["lastname"] = match.group(9)

            # Create the dataset for the new message
            dataset = ['new', date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), str(match.group(9)), match.group(10)]
            if local_args.verbose | local_args.debug:
                print(dataset)

    elif re.match(re.compile(r"^[\t ]*\n", re.VERBOSE), line):
        # Empty line
        if local_args.debug:
            print("Empty line removed")

    else:
        if local_args.debug:
            print("Appending line found")

        newline = (re.match(re.compile(r"^(.*)", re.VERBOSE), line))

        # Create the dataset if commandline argument was to create a new line
        # TODO if (local_args.newline):
        # if 1:
        #     dataset = ['new', str(lastentry["lastdate"]), str(lastentry["lasttime"]), lastentry["lastname"], newline.group(0)]
        dataset = ['new', str(lastentry["lastdate"]), str(lastentry["lasttime"]), lastentry["lastname"], newline.group(0)]
        #     # if local_args.verbose | local_args.debug:
        #           print(dataset)
        #
        # else:
        #     # Otherwise make sure it is appended to the existing line
        #     dataset = ['append', '', '', '', newline.group(0)]
        #     if local_args.verbose | local_args.debug:
        #          print(dataset)

    return dataset

class CSVResultSet:
    def __init__(self, local_args, header):
        self.__type = "CSV"
        self.__file = local_args.resultset
        self.__file_object = io.open(self.__file, "w", encoding="utf-8")
        self.__file_object.write(header[0] + '|' + header[1] + '|' + header[2] + '|' + header[3] + '|' + header[4] + '|' + '\n')

    def __enter__(self):
        return self

    def __exit__(self, type, val, tb):
        print("Exit")

    def __del__(self):
        self.__file_object.close()

    def write(self, dataset):
        self.__file_object.write(dataset[1] + ' ' + dataset[2] + '|' + dataset[1] + '|' + dataset[2] + '|' + dataset[3] + '|' + dataset[4] + '\n')

    def get_type(self):
        return "CSV"

class XLSResultSet:
    def __init__(self, local_args, header):
        self.__type = "XLS"
        self.__file = local_args.resultset
        self.__workbook = xlwt.Workbook()
        self.__worksheet = self.__workbook.add_sheet('Resultset')
        self.__worksheet.write(0, 0, header[0])
        self.__worksheet.write(0, 1, header[1])
        self.__worksheet.write(0, 2, header[2])
        self.__worksheet.write(0, 3, header[3])
        self.__worksheet.write(0, 4, header[4])
        self.__ws_counter = 1

    def __enter__(self):
        return self

    def __exit__(self, type, val, tb):
        print("Exit")

    def __del__(self):
        self.__workbook.save(self.__file)

    def write(self, dataset):
        #self.__worksheet.write(self.__ws_counter, 0, counter)
        self.__worksheet.write(self.__ws_counter, 1, dataset[1] + ' ' + dataset[2])
        self.__worksheet.write(self.__ws_counter, 2, dataset[2])
        self.__worksheet.write(self.__ws_counter, 3, dataset[3])
        self.__worksheet.write(self.__ws_counter, 4, dataset[4])
        self.__ws_counter += 1

    def get_type(self):
        return "XLS"

def convert(local_args):
    '''Convert the input file

    1. Open the file
    2. Loop to input line by line and send it to parser
    3. Close the file

    '''
    # Store the number of lines of the input file
    line_count = 0

    if local_args.verbose:
        print("Verbosity turned on")

    if local_args.debug:
        print("Debug turned on")

    try:
        with io.open(local_args.filename, "r", encoding="utf-8") as file:
            print("Reading import file")

            content = []

            for line in file:
                # Explicetly opened the file two times to show progress in user interface
                line_count += 1

                # Read lines into a list
                content.append(line)

    except IOError as e:
        print("File \"" + local_args.filename + "\" cannot be found.")
        sys.exit()


    print("Converting data now")

    # Count number of chatlines without  linesError: Excel 2003 only supports a maximum of 65535 lines. Whatsapp-converter found more than 65535 lines for input which might lead to an error.\n
    counter = 0

    if local_args.debug:
        print('Open export file ' + local_args.resultset)

    # Create resultset object
    resultset = 0

    # Select export formats
    if str(local_args.resultset).endswith('.csv'):
        resultset = CSVResultSet(local_args, header)

    elif str(local_args.resultset).endswith('.xls'):
        if line_count > 65535:
            print(f'\n{bcolors["FAIL"]}Error:{bcolors["ENDC"]} Excel 2003 only supports a maximum of 65535 lines. Whatsapp-converter found more than 65535 lines for input which might lead to an error.\n')
            print("")
            sys.exit()

        resultset = XLSResultSet(local_args, header)

    # TODO Append line with buffer before writing
    # Show progress via tqdm
    for line in tqdm(content, total=line_count, ncols=120):
        if local_args.debug and line == '':
            print(line)

        dataset = parse(line, local_args)

        if dataset[0] != 'empty':
            # Write to file
            resultset.write(dataset)

        # Print progress
        if line.strip():
            counter += 1
            # print('Wrote ' + str(counter) + ' lines of ' + str(line_count) + ' lines', end='\r')

    print('Wrote ' + str(counter) + ' lines')

    # Close the resultset object
    resultset = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='whatsapp-converter', description='Use whatsapp-converter to convert your exported WhatsApp chat to a CSV or XLS (Excel) file.', epilog='For reporting bugs or requesting features, please visit https://github.com/sandsturm/whatsapp-converter/ and create an issue')
    parser.add_argument('filename', metavar='filename', type=str, help='the WhatsApp file containing the exported chat')
    parser.add_argument('resultset', default='resultset.csv', nargs='?', help='filename of the resultset, default resultset.csv. Use .csv to write a comma separated file. Use .xls to write to an Excel spreadsheet file')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-d', '--debug', help='increase output verbosity to debug', action='store_true')
    parser.add_argument('--version', action='version', version="v" + VERSION["VERSION"])

    # parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
    args = parser.parse_args()

    convert(args)
