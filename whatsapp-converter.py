import io
import re
import sys
import argparse
import datetime
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the WhatsApp file containing the exported chat")
parser.add_argument("resultset", help="filename of the resultset", default="whatsapp_converted.csv", nargs='*')
parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
parser.add_argument("-d", "--debug", help="increase output verbosity to debug", action="store_true")
parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
args = parser.parse_args()

if args.verbose:
   print("Verbosity turned on")

if args.debug:
   print("Debug turned on")

try:
    with io.open(args.filename, "r", encoding="utf-8") as file:
        content = file.readlines()

except IOError as e:
    print("File \"" + args.filename + "\" cannot be found.")
    sys.exit()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERchatline = '\033[4m'

class dateFormats:
    # Define the time formats
    # English
    dateStrEN = "EN"
    dateEN = r"""^((\d{1,2})\/(\d{1,2})\/(\d{1,2}))"""
    dateFormatEN = "%d/%m/%y"
    timeFormatEN = "%I:%M:%S %p"
    # patternEN = dateEN + r"""\,\ \b((1[0-2]|0?[1-9])\:([0-5][0-9])\:([0-5][0-9])\ ([AaPp][Mm]))\:\ (.*)\:\ (.*)"""
    patternEN = dateEN + r"""\,\ \b((1[0-2]|0?[1-9])\:([0-5][0-9])\:([0-5][0-9])\ ([AaPp][Mm]))\:[^:](.+?)\:\ (.*)"""

    # German
    dateStrDE = "DE"
    dateDE = r"""^((\d{1,2})\.(\d{1,2})\.(\d{1,2}))"""
    dateFormatDE = "%d.%m.%y"
    timeFormatDE = "%H:%M:%S"
    patternDE = dateDE + r"""\,\ \b((1[0-2]|0?[1-9])\:([0-5][0-9])\:([0-5][0-9])())\:\ (.*)\:\ (.*)"""

class lastentry:
    lastlang = ""
    lastdate = date.today()
    lasttime = date.today()
    lastname = ""

def parse(chatline, verbose, debug):
    prefix = "***"
    dateLANG = dateFormats.dateEN
    dateFormatLANG = dateFormats.dateFormatEN
    timeFormatLANG = dateFormats.timeFormatEN
    pattern = dateFormats.patternEN
    found = ""
    type = "empty"
    dataset = ""
    # if verbose: print(prefix + chatline)
    # if verbose: print(bcolors.FAIL + prefix + chatline)
    # Identify the date format in the chat line

    if (re.match(re.compile(dateFormats.dateEN, re.VERBOSE), chatline)):
        # English
        dateStr = dateFormats.dateStrEN
        dateLANG = dateFormats.dateEN
        dateFormatLANG = dateFormats.dateFormatEN
        timeFormatLANG = dateFormats.timeFormatEN
        pattern = dateFormats.patternEN
        found = dateFormats.dateStrEN

    elif (re.match(re.compile(dateFormats.dateDE, re.VERBOSE), chatline)):
        # German
        dateStr = dateFormats.dateStrDE
        dateLANG = dateFormats.dateDE
        dateFormatLANG = dateFormats.dateFormatDE
        timeFormatLANG = dateFormats.timeFormatDE
        pattern = dateFormats.patternDE
        found = dateFormats.dateStrDE

    elif (re.match(re.compile(r"^[\t ]*\n", re.VERBOSE), chatline)):
        # Empty line
        if debug: print("Empty chatline removed")

    else:
        if debug: print("Appending chatline found")
        newchatline = (re.match(re.compile(r"^(.*)", re.VERBOSE), chatline))

        # Create the dataset if commandline argument was to create a new line
        if (args.newline):
            dataset = lastentry.lastlang + '|' + lastentry.lastdate + '|' + lastentry.lasttime + '|' + lastentry.lastname + '|' + newchatline.group( 0)
            # if (verbose | debug): print(dataset)
            type = 'new'

        else:
            # Otherwise make sure it is appended to the existing line
            dataset = newchatline.group(0)
            if (verbose | debug): print(dataset)
            type = 'append'

    if (len(found) > 0):
        # Make the match, assign to the groups
        match = re.match(re.compile(pattern, re.VERBOSE), chatline)
        if (match):
            date = datetime.datetime.strptime(match.group(1), dateFormatLANG).date()
            time = datetime.datetime.strptime(match.group(5), timeFormatLANG).time()
            lastentry.lastlang = dateStr
            lastentry.lastdate = date.strftime("%Y-%m-%d")
            lastentry.lasttime = time.strftime("%H:%M:%S")
            lastentry.lastname = match.group(10)

            # Create the dataset for the new message
            dataset = dateStr + '|' + date.strftime("%Y-%m-%d") + '|' + time.strftime("%H:%M:%S") + '|' + match.group(10) + '|' + match.group(11)
            if (verbose | debug): print(dataset)

            type = 'new'

    return [type, dataset]

print("Converting data now")
counter = 0

if (args.debug): print ("Open export file " + args.resultset)
resultset = open (args.resultset, "w")

for chatline in content:
    dataset = parse(chatline, args.verbose, args.debug)
    if (dataset[0] != 'empty'):
        counter += 1
        resultset.write(dataset[1] + '\n')
print('Wrote ' + str(counter) + ' lines')
resultset.close()
