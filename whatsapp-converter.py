import io
import re
import sys
import argparse
import datetime
from datetime import date
from tqdm import tqdm

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class dateFormats:
    # Define the time formats
    # English
    dateStrEN = "EN"
    dateEN = r"""^((\d{1,2})\/(\d{1,2})\/(\d{1,2}))"""
    dateFormatEN = "%d/%m/%y"
    timeFormatEN = "%I:%M:%S %p"
    # patternEN = dateEN + r"""\,\ \b((1[0-2]|0?[1-9])\:([0-5][0-9])\:([0-5][0-9])\ ([AaPp][Mm]))\:\ (.*)\:\ (.*)"""
    patternEN = dateEN + r"""\,\ \b((1[0-9]|0?[1-9])\:([0-5][0-9])\:([0-5][0-9])\ ([AaPp][Mm]))\:[^:](.+?)\:\ (.*)"""

    # German
    dateStrDE = "DE"
    dateDE = r"""^((\d{1,2})\.(\d{1,2})\.(\d{1,2}))"""
    dateFormatDE = "%d.%m.%y"
    timeFormatDE = "%H:%M"
    patternDE = dateDE + r"""\,\ \b((1[0-9]|0?[1-9])\:([0-5][0-9])()())\ \-\ (.*)\:\ (.*)"""

class lastentry:
    lastlang = ""
    lastdate = date.today()
    lasttime = date.today()
    lastname = ""

def parse(line, verbose, debug):
    prefix = "***"
    dateLANG = dateFormats.dateEN
    dateFormatLANG = dateFormats.dateFormatEN
    timeFormatLANG = dateFormats.timeFormatEN
    pattern = dateFormats.patternEN
    pattern = "^((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,2}))\,\ (\d{1,2}:\d{1,2})(?::\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ ][^:])(.+?)\:\ (.*)"
    found = ""
    type = "empty"
    dataset = ""
    # if verbose: print(prefix + line)
    # if verbose: print(bcolors.FAIL + prefix + line)
    # Identify the date format in the chat line

    if (re.match(re.compile(dateFormats.dateEN, re.VERBOSE), line)):
        # English
        dateStr = dateFormats.dateStrEN
        dateLANG = dateFormats.dateEN
        dateFormatLANG = dateFormats.dateFormatEN
        timeFormatLANG = dateFormats.timeFormatEN
        # pattern = dateFormats.patternEN
        found = dateFormats.dateStrEN

    elif (re.match(re.compile(dateFormats.dateDE, re.VERBOSE), line)):
        # German
        dateStr = dateFormats.dateStrDE
        dateLANG = dateFormats.dateDE
        dateFormatLANG = dateFormats.dateFormatDE
        timeFormatLANG = dateFormats.timeFormatDE
        # pattern = dateFormats.patternDE
        found = dateFormats.dateStrDE

    elif (re.match(re.compile(r"^[\t ]*\n", re.VERBOSE), line)):
        # Empty line
        if debug: print("Empty line removed")

    else:
        if debug: print("Appending line found")
        newline = (re.match(re.compile(r"^(.*)", re.VERBOSE), line))

        # Create the dataset if commandline argument was to create a new line
        # TODO if (args.newline):
        if (1):
            dataset = lastentry.lastdate + ' ' + lastentry.lasttime + '|' + lastentry.lastdate + '|' + lastentry.lasttime + '|' + lastentry.lastname + '|' + newline.group(0)
            # if (verbose | debug): print(dataset)
            type = 'new'

        else:
            # Otherwise make sure it is appended to the existing line
            dataset = newline.group(0)
            if (verbose | debug): print(dataset)
            type = 'append'

    if (len(found) > 0):
        # Make the match, assign to the groups
        match = re.match(re.compile(pattern, re.VERBOSE), line)

        # TODO Wrong assignment of group 9 25/6/15, 1:42:12 AM: ‎Vishnu Gaud created this group
        if (match and match.group(9) != 'M'):
            # 21/12/19 Date Format
            if (match.group(3) == '/' and match.group(8) == ': '):
                date = datetime.datetime.strptime(match.group(1), "%d/%m/%y").date()
            # 12/21/19 Date Format
            elif (match.group(3) == '/' and match.group(8) == '- '):
                date = datetime.datetime.strptime(match.group(1), "%m/%d/%y").date()
            # 21.12.19 Date Format
            else:
                date = datetime.datetime.strptime(match.group(1), "%d.%m.%y").date()

            if (match.group(7)):
                time = datetime.datetime.strptime(match.group(6) + " " + match.group(7), "%I:%M %p").time()
            else:
                time = datetime.datetime.strptime(match.group(6), "%H:%M").time()

            # Buffer date, time, name for next line messages
            lastentry.lastlang = dateStr
            lastentry.lastdate = date.strftime("%Y-%m-%d")
            lastentry.lasttime = time.strftime("%H:%M")
            lastentry.lastname = match.group(9)

            # Create the dataset for the new message
            dataset = date.strftime("%Y-%m-%d") + ' ' + time.strftime("%H:%M") + '|' + date.strftime("%Y-%m-%d") + '|' + time.strftime("%H:%M") + '|' + str(match.group(9)) + '|' + match.group(10)
            if (verbose | debug): print(dataset)

            type = 'new'

    return [type, dataset]

def convert(filename, resultset='resultset.csv', verbose=False, debug=False):
    # Store the number of lines of the input file
    line_count = 0

    if verbose:
       print("Verbosity turned on")

    if debug:
       print("Debug turned on")

    try:
        # Count the number of total lines
        with io.open(filename, "r", encoding="utf-8") as file:
            for line in file:
                # if line.strip():
                line_count += 1

        # Convert lines to csv
        with io.open(filename, "r", encoding="utf-8") as file:
            content = file.readlines()

    except IOError as e:
        print("File \"" + filename + "\" cannot be found.")
        sys.exit()

    print("Converting data now")
    counter = 0

    if (debug): print ("Open export file " + resultset)

    # Open result filename
    resultset = open (resultset, "w")

    # Write headers
    resultset.write('Date and Time|Date|Time|Name|Message' + '\n')


    # TODO Append line with buffer before writing
    # Show progress via tqdm
    for line in tqdm(content, total=line_count, ncols=120):
        if (debug and line == ''): print(line)
        dataset = parse(line, verbose, debug)
        if (dataset[0] != 'empty'):
            resultset.write(dataset[1] + '\n')

        # Print progress
        if line.strip():
            counter += 1
        # print('Wrote ' + str(counter) + ' lines of ' + str(line_count) + ' lines', end='\r')

    print('Wrote ' + str(counter) + ' lines')
    resultset.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="the WhatsApp file containing the exported chat")
    parser.add_argument("resultset", help="filename of the resultset", default="resultset.csv", nargs='*')
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--debug", help="increase output verbosity to debug", action="store_true")

    # parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
    args = parser.parse_args()

    convert(filename=args.filename, resultset=args.resultset, verbose=args.verbose, debug=args.debug)
