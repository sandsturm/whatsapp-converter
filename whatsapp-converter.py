import io
import re
import sys
import argparse
import datetime
from datetime import date

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="WhatsApp chat file to be converted")
parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
parser.add_argument("-d", "--debug", help="increase output verbosity to debug",
                    action="store_true")
args = parser.parse_args()

if args.verbose:
   print("Verbosity turned on")

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
    dateStrEN = "EN"
    dateEN = "^(\d{1,2})\/(\d{1,2})\/(\d{1,2})"
    formatEN = "%d/%m/%y"
    dateStrDE = "DE"
    dateDE = "^(\d{1,2})\.(\d{1,2})\.(\d{1,2})"
    formatDE = "%d.%m.%y"

def parse(chatline, verbose, debug):
    prefix = "***"
    dateLANG = dateFormats.dateEN
    formatLANG = dateFormats.formatEN

    # if verbose: print(prefix + chatline)
    # if verbose: print(bcolors.FAIL + prefix + chatline)
    # Identify the date format in the chat line
    if (re.match(re.compile(dateFormats.dateEN, re.VERBOSE), chatline)):
        dateStr = dateFormats.dateStrEN
        dateLANG = dateFormats.dateEN
        formatLANG = dateFormats.formatEN
    elif (re.match(re.compile(dateFormats.dateDE, re.VERBOSE), chatline)):
        dateStr = dateFormats.dateStrDE
        dateLANG = dateFormats.dateDE
        formatLANG = dateFormats.formatDE

    match = re.match(re.compile(dateLANG, re.VERBOSE), chatline)
    if (match):
        date = datetime.datetime.strptime(match.group(), formatLANG).date()
        if debug: print(dateStr + " " + date.strftime("%Y-%m-%d"))

print("Converting data now")

for chatline in content:
    parse(chatline, args.verbose, args.debug)
