# WhatsApp-converter


## Introduction
Use this application to convert your exported WhatsApp chat to a CSV file.
1. The conversion is done locally. No data is shared with the internet!
2. The resultset is a CSV file which you can import into your favorite calculation application such as Excel or LibreOffice.

## Usage
Use the following command on the command line to get an overview of the available arguments.
```shell
python WhatsApp-converter.py -h
```

The easy start is just to provide the filename of the exported WhatsApp chat. The application will process the chat and create a CSV file named *resultset.csv*.
```shell
python WhatsApp-converter.py filename.txt
```

Here is the list of all available options:
```shell
WhatsApp-converter.py [-h] [-v] [-d] [-nl] filename [resultset.csv]
```

#### Mandatory Arguments
```shell
filename       The WhatsApp file containing the exported chat
resultset       The filename of the resultset
```

#### Optional Arguments
```shell
  -h, --help      show this help message and exit
  -v, --verbose   increase output verbosity
  -d, --debug     increase output verbosity to debug
```

## Conversion from to

Each line of the dataset will be converted to structured data which can be imported into your Excel or LibreOffice sheet.
```shell
21/8/19, 11:28:51 PM: Jon Doe: Waste out of wealth 😂
21.12.16, 23:29 - Alan Smith: Like a Rolex
30.11.18, 10:57 - Nachrichten in diesem Chat sowie Anrufe sind jetzt mit Ende-zu-Ende-Verschlüsselung geschützt. Tippe für mehr Infos.
30.11.18, 10:57 - Heise: Hallo :)
30.11.18, 10:58 - Heise: Jetzt bin ich gespannt auf deine Antwort ;)
1/26/19, 00:07 - Jon Doe: Schlaf gut
18.05.19, 11:50:00: Alan Smith: Hier geht es los
Das ist eine neue Zeile
```

The resultset will look like this for each line:
```shell
Date Format|Date|Time|Name|Message
EN|2019-8-21|23:28|Jon Doe|Waste out of wealth 😂
DE|2016-12-21|23:29|Alan Smith|Like a Rolex
DE|2018-11-30|10:57|Heise|Hallo :)
DE|2018-11-30|10:58|Heise|Jetzt bin ich gespannt auf deine Antwort ;)
EN|2019-01-26|00:07|Jon Doe|Schlaf gut
DE|2019-05-18|11:50|Alan Smith|Hier geht es los
DE|2019-05-18|11:50|Alan Smith|Das ist eine neue Zeile
```
