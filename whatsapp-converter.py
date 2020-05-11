import io
import re
import sys
import argparse
import datetime
import xlwt
from datetime import date
from tqdm import tqdm

class constant:
    version = 'v0.3.5'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class lastentry:
    lastdate = date.today()
    lasttime = date.today()
    lastname = ""

def parse(line, verbose, debug):
    prefix = "***"
    patternDate = "^((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,2}))\,\ (\d{1,2}:\d{1,2})(?::\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ ][^:])(.+?)\:"
    pattern = "^((\d{1,2})([\/|\.])(\d{1,2})[\/|\.](\d{1,2}))\,\ (\d{1,2}:\d{1,2})(?::\d{1,2})?\ ?(AM|PM|am|pm)?([\:\ |\ \-\ ][^:])(.+?)\:\ (.*)"
    found = False
    dataset = ['empty', '', '', '', '', '']
    # if verbose: print(prefix + line)
    # if verbose: print(bcolors.FAIL + prefix + line)
    # Identify the date format in the chat line

    if (re.match(re.compile(patternDate, re.VERBOSE), line)):
        found = True

    elif (re.match(re.compile(r"^[\t ]*\n", re.VERBOSE), line)):
        # Empty line
        if debug: print("Empty line removed")

    else:
        if debug: print("Appending line found")
        newline = (re.match(re.compile(r"^(.*)", re.VERBOSE), line))

        # Create the dataset if commandline argument was to create a new line
        # TODO if (args.newline):
        if (1):
            dataset = ['new', str(lastentry.lastdate), str(lastentry.lasttime), lastentry.lastname, newline.group(0)]
            # if (verbose | debug): print(dataset)

        else:
            # Otherwise make sure it is appended to the existing line
            dataset = ['append', '', '', '', newline.group(0)]
            if (verbose | debug): print(dataset)

    if (found):
        # Make the match, assign to the groups
        match = re.match(re.compile(pattern, re.VERBOSE), line)

        if (match and match.group(9) != 'M'):
            # 21/12/19 Date Format
            if (match.group(3) == '/' and match.group(8) == ': '):
                date = datetime.datetime.strptime(match.group(1), "%d/%m/%y").date()
            # 12/21/19 Date Format
            elif (match.group(3) == '/' and (match.group(8) == ' -' or match.group(8) == '- ')):
                date = datetime.datetime.strptime(match.group(1), "%m/%d/%y").date()
            # 21.12.19 Date Format
            else:
                date = datetime.datetime.strptime(match.group(1), "%d.%m.%y").date()

            if (match.group(7)):
                time = datetime.datetime.strptime(match.group(6) + " " + match.group(7), "%I:%M %p").time()
            else:
                time = datetime.datetime.strptime(match.group(6), "%H:%M").time()

            # Buffer date, time, name for next line messages
            lastentry.lastdate = date.strftime("%Y-%m-%d")
            lastentry.lasttime = time.strftime("%H:%M")
            lastentry.lastname = match.group(9)

            # Create the dataset for the new message
            dataset = ['new', date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), str(match.group(9)), match.group(10)]
            if (verbose | debug): print(dataset)

    return dataset

def convert(filename, resultset, verbose=False, debug=False):
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

    # Count number of chatlines without empty lines
    counter = 0

    if (debug): print ('Open export file ' + resultset)

    # Define export file header
    header = ['Date and Time', 'Date', 'Time', 'Name', 'Message']

    # Select export formats
    if str(resultset).endswith('.csv'):

        # Open result filename
        csv = io.open (resultset, "w", encoding="utf-8")

        # Write headers
        csv.write(header[0] + '|' + header[1] + '|' + header[2] + '|' + header[3] + '|' + header[4] + '|' + '\n')

    elif str(resultset).endswith('.ods'):
        wb = xlwt.Workbook()
        ws = wb.add_sheet(filename)

        ws.write(0, 0, header[0])
        ws.write(0, 1, header[1])
        ws.write(0, 2, header[2])
        ws.write(0, 3, header[3])
        ws.write(0, 4, header[4])

        ws_counter = 1

    # TODO Append line with buffer before writing
    # Show progress via tqdm
    for line in tqdm(content, total=line_count, ncols=120):
        if (debug and line == ''): print(line)
        dataset = parse(line, verbose, debug)
        if (dataset[0] != 'empty'):

            # Write to .csv file
            if str(resultset).endswith('.csv'):
                csv.write(dataset[1] + ' ' + dataset[2] + '|' + dataset[1] + '|' + dataset[2] + '|' + dataset[3] + '|' + dataset[4] + '\n')

            # Write to .ods file
            elif str(resultset).endswith('.ods'):
                ws.write(ws_counter, 0, counter)
                ws.write(ws_counter, 1, dataset[1] + ' ' + dataset[2])
                ws.write(ws_counter, 2, dataset[2])
                ws.write(ws_counter, 3, dataset[3])
                ws.write(ws_counter, 4, dataset[4])
                ws_counter += 1

        # Print progress
        if line.strip():
            counter += 1
            # print('Wrote ' + str(counter) + ' lines of ' + str(line_count) + ' lines', end='\r')

    print('Wrote ' + str(counter) + ' lines')

    # Close the resultfiles
    if str(resultset).endswith('.csv'):
        csv.close()

    elif str(resultset).endswith('.ods'):
        wb.save('resultset.ods')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='whatsapp-converter', epilog='For reporting bugs or requesting features, please visit https://github.com/sandsturm/whatsapp-converter/ and create an issue')
    parser.add_argument('filename', metavar='filename', type=str, help='the WhatsApp file containing the exported chat')
    parser.add_argument('resultset', default='resultset.csv', nargs='?', help='filename of the resultset, default resultset.csv. Use .csv to write a comma separated file. Use .ods to write to a LibreOffice spreadsheet file')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-d', '--debug', help='increase output verbosity to debug', action='store_true')

    # parser.add_argument("-nl", "--newline", help="message across various lines is counted as a new message", action="store_true")
    args = parser.parse_args()

    convert(filename=args.filename, resultset=args.resultset, verbose=args.verbose, debug=args.debug)
