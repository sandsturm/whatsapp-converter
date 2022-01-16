'''whatsapp-converter

Use this application to convert your exported WhatsApp chat to a CSV or Excel file.

1. The conversion is done locally. No data is shared with the internet!
2. The resultset is a CSV file which you can import into your favorite calculation application such as Excel or LibreOffice. You can also directly export to a XLS spreadsheet file.

'''

import io
import sys
import re
import datetime
from datetime import date
import pyexcel
from tqdm import tqdm

from whatsapp_converter.colors import BCOLORS

lastentry = {
    "lastdate": date.today(),
    "lasttime": date.today(),
    "lastname": ""
}

# ---------------------------------------------
# Define export file header
header = [
    "Date and Time",
    "Date",
    "Time",
    "Name",
    "Message"
]

formaterrors = {
    "mdyS": False,
    "process_again": True,
}


def check_monthfirst(dateformat):
    if dateformat[1:2] not in ('.', '/'):
        if int(dateformat[0:2]) > 12:
            return True
        else:
            return False


def parse(line, local_args):
    '''Parse each line

    line = Single line to parse
    args = Arguments from the command line. In this case only verbose and debug switches.
    '''

    # ---------------------------------------------
    # The main regex logic to identify the date and message
    pattern_date = '^\[?((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,4}))\,?\ (\d{1,2}[:|.]\d{1,2})([:|.]\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ |\]\ ][^:])'
    pattern = pattern_date + '(.+?)\:\ (.*)'

    dataset = ['empty', '', '', '', '', '']

    # ---------------------------------------------
    # if verbose: print(prefix + line)
    # if verbose: print(BCOLORS.FAIL + prefix + line)
    # Identify the date format in the chat line

    if re.match(re.compile(pattern, re.VERBOSE), line):

        # ---------------------------------------------
        # Make the match, assign to the groups
        match = re.match(re.compile(pattern, re.VERBOSE), line)

        if match and match.group(10) !=  'M':

            # ---------------------------------------------
            # 21/12/19 Date Format
            if match.group(3) == '/' and match.group(9) == ': ':
                if local_args.debug:
                    print("d/m/y Date Format")
                if len(match.group(5)) == 4:
                    date = datetime.datetime.strptime(match.group(1), "%d/%m/%Y").date()
                else:
                    date = datetime.datetime.strptime(match.group(1), "%d/%m/%y").date()

            # ---------------------------------------------
            # 12/21/19 Date Format
            elif match.group(3) == '/' and (match.group(9) == ' -' or match.group(9) == '- '):
                if local_args.debug:
                    print("m/d/y Date Format")
                if len(match.group(5)) == 4 and match.group(7) is None:
                    date = datetime.datetime.strptime(match.group(1), "%d/%m/%Y").date()
                else:
                    date = datetime.datetime.strptime(match.group(1), "%m/%d/%y").date()

            # ---------------------------------------------
            # 21/12/2019 Date Format with square brackets and am
            elif match.group(3) == '/' and match.group(9) == '] ' and (match.group(8) == 'am' or match.group(8) == 'pm'):
                if local_args.debug:
                    print("d/m/Y Date Format with [square brackets] and am/pm")
                date = datetime.datetime.strptime(match.group(1), "%d/%m/%Y").date()

            # ---------------------------------------------
            # 12/21/2019 Date Format with square brackets
            elif match.group(3) == '/' and match.group(9) == '] ':
                if local_args.debug:
                    print("m/d/Y Date Format with [square brackets]")
                if check_monthfirst(match.group(1)) and not formaterrors["mdyS"]:
                    formaterrors["mdyS"] = True
                    formaterrors["process_again"] = True
                    print("Restart processing due to invalid date format")
                if formaterrors["mdyS"]:
                    if len(match.group(5)) == 4:
                        date = datetime.datetime.strptime(match.group(1), "%d/%m/%Y").date()
                    else:
                        date = datetime.datetime.strptime(match.group(1), "%d/%m/%y").date()
                else:
                    if len(match.group(5)) == 4:
                        date = datetime.datetime.strptime(match.group(1), "%m/%d/%Y").date()
                    else:
                        date = datetime.datetime.strptime(match.group(1), "%m/%d/%y").date()

            # ---------------------------------------------
            # 21.12.19 Date Format
            else:
                if local_args.debug:
                    print("d.m.y Date Format")
                if len(match.group(5)) == 4:
                    date = datetime.datetime.strptime(match.group(1), "%d.%m.%Y").date()
                else:
                    date = datetime.datetime.strptime(match.group(1), "%d.%m.%y").date()

            if match.group(8):
                time = datetime.datetime.strptime(match.group(6) + " " + match.group(8), "%I:%M %p").time()
            elif match.group(6).find(":") > 0:
                time = datetime.datetime.strptime(match.group(6), "%H:%M").time()
            elif match.group(6).find(".") > 0:
                time = datetime.datetime.strptime(match.group(6), "%H.%M").time()

            # ---------------------------------------------
            # Buffer date, time, name for next line messages
            lastentry["lastdate"] = date.strftime("%Y-%m-%d")
            lastentry["lasttime"] = time.strftime("%H:%M")
            lastentry["lastname"] = match.group(10)

            # ---------------------------------------------
            # Create the dataset for the new message
            dataset = ['new', date.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M"), date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), str(match.group(10)), match.group(11)]

            if local_args.verbose | local_args.debug:
                print(dataset)

    elif re.match(re.compile(r"^[\t ]*\n", re.VERBOSE), line):

        # ---------------------------------------------
        # Empty line
        if local_args.debug:
            print("Empty line removed")

    # ---------------------------------------------
    # Check if there is
    elif not re.match(re.compile(r"^\[?((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,4}))\,?\ (\d{1,2}[:|.]\d{1,2})(?:[:|.]\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ |\]\ ][^:])", re.VERBOSE), line):

        if local_args.debug:
            print("Appending line found")

        newline = (re.match(re.compile(r"^(.*)", re.VERBOSE), line))

        # ---------------------------------------------
        # Create the dataset if commandline argument was to create a new line
        # TODO if (local_args.newline):
        dataset = ['append', str(lastentry["lastdate"]) + " " + str(lastentry["lasttime"]), str(lastentry["lastdate"]), str(lastentry["lasttime"]), lastentry["lastname"], newline.group(0)]

    return dataset


def convert(local_args):
    '''Convert the input file

    1. Open the file
    2. Loop to input line by line and send it to parser
    3. Close the file

    '''
    # ---------------------------------------------
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
                # ---------------------------------------------
                # Explicetly opened the file two times to show progress in user interface
                line_count += 1

                # ---------------------------------------------
                # Read lines into a list
                content.append(line)

    except IOError as e:
        print("File \"" + local_args.filename + "\" cannot be found.")
        sys.exit()

    print("Converting data now")

    # ---------------------------------------------
    # Count number of chatlines without  linesError: Excel 2003 only supports a maximum of 65535 lines.
    # Whatsapp-converter found more than 65535 lines for input which might lead to an error.\n
    counter = 0

    if local_args.debug:
        print('Open export file ' + local_args.resultset)

    # ---------------------------------------------
    # Select export formats
    if str(local_args.resultset).endswith('.xls'):
        if line_count > 65535:
            print(f'\n{BCOLORS["FAIL"]}Error: Excel 2003 only supports a maximum of 65535 lines. Whatsapp-converter found more than 65535 lines for input which might lead to an error.{BCOLORS["ENDC"]}\n')
            print("")
            sys.exit()

    dataset = []

    while formaterrors["process_again"]:

        formaterrors["process_again"] = False

        dataset.clear()
        dataset.append(header)

        # ---------------------------------------------
        # TODO Append line with buffer before writing
        # Show progress via tqdm
        for line in tqdm(content, total=line_count, ncols=120):
            if local_args.debug and line == '':
                print(line)

            buffer = parse(line, local_args)

            if formaterrors["process_again"]:
                break

            if buffer[0] != 'empty':

                # ---------------------------------------------
                # Write to dataset
                if buffer[0] == 'new' or (local_args.newline and buffer[0] == 'append'):
                    dataset.append(buffer[1:])
                # Default multiline appended to previous converted message
                else:
                    dataset[-1][-1] = dataset[-1][-1] + " " + buffer[-1]

            # ---------------------------------------------
            # Print progress
            if line.strip():
                counter += 1

        print('Writing to ' + str(local_args.resultset))

    # ---------------------------------------------
    # Select export formats
    if str(local_args.resultset).endswith('.csv'):
        pyexcel.save_as(array=dataset, dest_file_name=str(local_args.resultset), dest_delimiter='|')

    elif str(local_args.resultset).endswith('.xls'):
        pyexcel.save_as(array=dataset, dest_file_name=str(local_args.resultset))

    elif str(local_args.resultset).endswith('.xlsx'):
        pyexcel.save_as(array=dataset, dest_file_name=str(local_args.resultset))

    elif str(local_args.resultset).endswith('.ods'):
        print(f'{BCOLORS["WARNING"]}NOTE: The writing of the ODS file takes some time. Your terminal did not crash. Please wait ...{BCOLORS["ENDC"]}')
        pyexcel.save_as(array=dataset, dest_file_name=str(local_args.resultset))

    print('Wrote ' + str(counter) + ' lines')
