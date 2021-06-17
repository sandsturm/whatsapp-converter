# whatsapp-converter

## Introduction
Use the whatsapp-converter to convert your exported WhatsApp chat to a CSV, XLS, XLSX or an ODS file.
1. The conversion is done locally. No data is shared with the internet!
2. The resultset is a CSV file which you can import into your favorite calculation application such as Excel or LibreOffice. You can also directly export to a spreadsheet file and do create a pivot table.

## Dependencies
If you want to install the dependencies manually, use pip. On some computers you might need to replace pip by pip3.
```shell
pip install tqdm pyexcel pyexcel-xlsxw pyexcel-ods3 xlwt
```

## Usage
Use the following command on the command line to get an overview of the available arguments.
```shell
python whatsapp-converter.py -h
```

### Convert WhatsApp TXT to CSV (Default Use Case)
The easy start is just to provide the filename of the exported WhatsApp chat. The application will process the chat and create a CSV file named *resultset.csv*.
```shell
python whatsapp-converter.py whatsapp-export.txt
```

### Convert WhatsApp to Excel XLS or XLSX
If you want to export to an Excel spreadsheet file instead, make sure to add the filename at the end, e.g. *resultset.xls*.
```shell
python whatsapp-converter.py whatsapp-export.txt resultset.xls
```

or

```shell
python whatsapp-converter.py whatsapp-export.txt resultset.xlsx
```

### Convert WhatsApp to LibreOffice ODS
If you want to export to a LibreOffice spreadsheet file, make sure to add the filename at the end, e.g. *resultset.ods*.
Please note that the export takes some time. The script did not crash.
```shell
python whatsapp-converter.py whatsapp-export.txt resultset.ods
```

Here is the list of all available options:
```shell
whatsapp-converter.py [-h] [-v] [-d] filename [resultset.csv|resultset.xls]
```

## Commandline Arguments

#### Mandatory Arguments
```shell
filename        The WhatsApp file containing the exported chat
resultset       Filename of the resultset, default resultset.csv. Use .csv to write a comma separated file. Use .xls to write to an Excel spreadsheet file
```

#### Optional Arguments
```shell
  -h, --help      show this help message and exit
  -n  --newline   create a new line (same date and time) in the resultset for every multiline chat message
  -v, --verbose   increase output verbosity
  -d, --debug     increase output verbosity to debug
```

##### Example Newline Argument

Consider this chat exported chat message
```shell
18.05.19, 11:50:00: Alan Smith: It starts here
This is a new line
```

By default the resultset will merge the two lines.
```shell
2019-05-18 11:50|2019-05-18|11:50|Alan Smith|It starts here This is a new line
```

If you start the application with the -n argument, a new line will be added and the date and time of the multiline message taken.
```shell
2019-05-18 11:50|2019-05-18|11:50|Alan Smith|It starts here
2019-05-18 11:50|2019-05-18|11:50|Alan Smith|This is a new line
```

## Conversion from to

Each line of the dataset will be converted to structured data which can be imported into your Excel or LibreOffice sheet.
```shell
21/8/19, 11:28:51 PM: Jon Doe: Waste out of wealth 😂
21.12.16, 23:29 - Alan Smith: Like a Rolex
30.11.18, 10:57 - Nachrichten in diesem Chat sowie Anrufe sind jetzt mit Ende-zu-Ende-Verschlüsselung geschützt. Tippe für mehr Infos.
30.11.18, 10:57 - Snoopy: Hallo :)
30.11.18, 10:58 - Snoopy: Jetzt bin ich gespannt auf deine Antwort ;)
1/26/19, 00:07 - Jon Doe: Sleep well
18.05.19, 11:50:00: Alan Smith: It starts here
This is a new line
```

The resultset file looks like this. In the default configuration new lines get the same date and time stamp and sender name as the previous line:
```shell
Date and Time|Date|Time|Name|Message
2019-8-21 23:28|2019-8-21|23:28|Jon Doe|Waste out of wealth 😂
2016-12-21 23:29|2016-12-21|23:29|Alan Smith|Like a Rolex
2018-11-30 10:57|2018-11-30|10:57|Snoopy|Hallo :)
2018-11-30 10:58|2018-11-30|10:58|Snoopy|Jetzt bin ich gespannt auf deine Antwort ;)
2019-01-26 00:07|2019-01-26|00:07|Jon Doe|Sleep well
2019-05-18 11:50|2019-05-18|11:50|Alan Smith|It starts here This is a new line
```
