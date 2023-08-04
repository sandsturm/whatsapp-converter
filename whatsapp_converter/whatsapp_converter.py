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


# ---------------------------------------------
# The main regex logic to identify the date and message
pattern_date = '^\[?((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,4}))\,?\ (\d{1,2}[:|.]\d{1,2})([:|.]\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ |\]\ ][^:])'
pattern = pattern_date + '(.+?)\:\ (.*)'

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

date_formats = {
    "mdyS": False,
    "process_again": True,
    "data_format": "",
}


def check_monthfirst(dateformat):
    if dateformat[1:2] not in ('.', '/'):
        if int(dateformat[0:2]) > 12:
            return True
        else:
            return False


def parse(line, filename, resultset, newline, verbose, debug):
    '''Parse each line

    line = Single line to parse
    args = Arguments from the command line. In this case only verbose and debug switches.
    '''

    # ---------------------------------------------
    # The main regex logic to identify the date and message
    pattern_date = re.compile('^\[?((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,4}))\,?\ (\d{1,2}[:|.]\d{1,2})([:|.]\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ |\]\ ][^:])(.+?)\:\ (.*)')
    match = pattern_date.match(line)
    dataset = ['empty', '', '', '', '', '']

    # ---------------------------------------------
    # if verbose: print(prefix + line)
    # if verbose: print(BCOLORS.FAIL + prefix + line)
    # Identify the in the chat line

    if match:

        if match and match.group(10) !=  'M':

            date = datetime.datetime.strptime(match.group(1), date_formats["date_format"]).date()

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

            if verbose or debug:
                print(dataset)

    elif re.match(re.compile(r"^[\t ]*\n", re.VERBOSE), line):

        # ---------------------------------------------
        # Empty line
        if debug:
            print("Empty line removed")

    # ---------------------------------------------
    # Check if there is
    elif not re.match(re.compile(r"^\[?((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,4}))\,?\ (\d{1,2}[:|.]\d{1,2})(?:[:|.]\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ |\]\ ][^:])", re.VERBOSE), line):

        if debug:
            print("Appending line found")

        text = (re.match(re.compile(r"^(.*)", re.VERBOSE), line))

        # ---------------------------------------------
        # Create the dataset if commandline argument was to create a new line
        # TODO if (newline):
        # print(newline)
        if newline:
            dataset = ['new', str(lastentry["lastdate"]) + " " + str(lastentry["lasttime"]), str(lastentry["lastdate"]), str(lastentry["lasttime"]), lastentry["lastname"], text.group(0)]

        else:
            dataset = ['append', str(lastentry["lastdate"]) + " " + str(lastentry["lasttime"]), str(lastentry["lastdate"]), str(lastentry["lasttime"]), lastentry["lastname"], text.group(0)]

    return dataset


def convert(filename, resultset="resultset.csv", newline=False, verbose=False, debug=False):
    '''Convert the input file

    1. Open the file
    2. Loop to input line by line and send it to parser
    3. Close the file

    '''
    # ---------------------------------------------
    # Store the number of lines of the input file
    line_count = 0

    if verbose:
        print("Verbosity turned on")

    if debug:
        print("Debug turned on")

    try:
        with io.open(filename, "r", encoding="utf-8") as file:
            print("Reading import file")

            content = file.readlines()  # Read all lines at once
            line_count = len(content)  # Get the number of read lines
            confirmed_date = False  # Exit condition for For loop based on a date > 12

            for line in content:

                if confirmed_date == True:
                    break

                if not line.strip():  # Check if the line is empty or contains only whitespace
                    continue  # Skip the rest of the loop and move to the next iteration

                # ---------------------------------------------
                # Make the match, assign to the groups
                match = re.match(re.compile(pattern, re.VERBOSE), line)
                
                if match:

                    # ---------------------------------------------
                    # 21/12/19
                    if match.group(3) == '/' and (match.group(9) == ' -' or match.group(9) == '- ' or match.group(9) == ': '):
                        if debug:
                            print("Date format d/m/y")
                        if len(match.group(5)) == 4:
                            date_formats["date_format"] = "%d/%m/%Y"
                        else:
                            date_formats["date_format"] = "%d/%m/%y"

                    # ---------------------------------------------
                    # 12/21/19
                    elif match.group(3) == '/' and (match.group(9) == ' -' or match.group(9) == '- '):
                        if debug:
                            print("Date format m/d/y")
                        if len(match.group(5)) == 4 and match.group(7) is None:
                            date_formats["date_format"] = "%m/%d/%Y"
                        else:
                            date_formats["date_format"] = "%m/%d/%y"

                    # ---------------------------------------------
                    # 21/12/2019 with square brackets and am
                    elif match.group(3) == '/' and match.group(9) == '] ' and (match.group(8) == 'am' or match.group(8) == 'pm'):
                        if debug:
                            print("Date format d/m/Y with [square brackets] and am/pm")
                        date_formats["date_format"] = "%d/%m/%Y"

                    # ---------------------------------------------
                    # 12/21/2019 with square brackets
                    elif match.group(3) == '/' and match.group(9) == '] ':
                        if debug:
                            print("Date format m/d/Y with [square brackets]")
                        if check_monthfirst(match.group(1)) and not date_formats["mdyS"]:
                            date_formats["mdyS"] = True
                            date_formats["date_format"] = "%d/%m/%Y"
                        if date_formats["mdyS"]:
                            if len(match.group(5)) == 4:
                                date_formats["date_format"] = "%d/%m/%Y"
                            else:
                                date_formats["date_format"] = "%d/%m/%y"
                        else:
                            if len(match.group(5)) == 4:
                                date_formats["date_format"] = "%m/%d/%Y"
                            else:
                                date_formats["date_format"] = "%m/%d/%y"

                    # ---------------------------------------------
                    # 21.12.19
                    else:
                        if debug:
                            print("Date format d.m.y")
                        if len(match.group(5)) == 4:
                            date = datetime.datetime.strptime(match.group(1), "%d.%m.%Y").date()
                            date_formats["date_format"] = "%d.%m.%Y"
                        else:
                            date_formats["date_format"] = "%d.%m.%y"

    except IOError as e:
        print("File \"" + filename + "\" cannot be found.")
        sys.exit()

    print("Converting data now with data format " + date_formats["date_format"])

    # ---------------------------------------------
    # Count number of chatlines without  linesError: Excel 2003 only supports a maximum of 65535 lines.
    # Whatsapp-converter found more than 65535 lines for input which might lead to an error.\n
    counter = 0

    if debug:
        print('Open export file ' + resultset)

    # ---------------------------------------------
    # Select export formats
    if str(resultset).endswith('.xls'):
        if line_count > 65535:
            print(f'\n{BCOLORS["FAIL"]}Error: Excel 2003 only supports a maximum of 65535 lines. Whatsapp-converter found more than 65535 lines for input which might lead to an error.{BCOLORS["ENDC"]}\n')
            print("")
            sys.exit()#

    dataset = []
    dataset.append(header)

    # ---------------------------------------------
    # TODO Append line with buffer before writing
    # Show progress via tqdm
    for line in tqdm(content, total=line_count, ncols=120):
        if debug and line == '':
            print(line)

        buffer = parse(line, filename, resultset, newline, verbose, debug)

        if buffer[0] != 'empty':

            # ---------------------------------------------
            # Write to dataset
            if buffer[0] == 'new' or (newline and buffer[0] == 'append'):
                dataset.append(buffer[1:])
            # Default multiline appended to previous converted message
            else:
                dataset[-1][-1] = dataset[-1][-1] + " " + buffer[-1]

        # ---------------------------------------------
        # Print progress
        if line.strip():
            counter += 1

    print('Writing to ' + str(resultset))

    # ---------------------------------------------
    # Select export formats
    if str(resultset).endswith('.csv'):
        pyexcel.save_as(array=dataset, dest_file_name=str(resultset), dest_delimiter='|')

    elif str(resultset).endswith('.xls'):
        pyexcel.save_as(array=dataset, dest_file_name=str(resultset))

    elif str(resultset).endswith('.xlsx'):
        pyexcel.save_as(array=dataset, dest_file_name=str(resultset))

    elif str(resultset).endswith('.ods'):
        print(f'{BCOLORS["WARNING"]}NOTE: The writing of the ODS file takes some time. Your terminal did not crash. Please wait ...{BCOLORS["ENDC"]}')
        pyexcel.save_as(array=dataset, dest_file_name=str(resultset))

    print('Wrote ' + str(counter) + ' lines')
