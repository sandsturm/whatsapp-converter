# whatsapp-converter

## Introduction
Use this application to convert your exported WhatsApp chat to a CSV file.
1. The conversion is done locally. No data is shared with the internet!
2. The resultset is a CSV file which you can import into your favorite calculation application such as Excel or LibreOffice.

## Usage
Use the following command on the command line to get an overview of the available arguments.
```shell
python whatsapp-converter.py -h
```

The easy start is just to provide the filename of the exported WhatsApp chat. The application will process the chat and create a CSV file named *resultset.csv*.
```shell
python whatsapp-converter.py filename.txt
```

Here is the list of all available options:
```shell
whatsapp-converter.py [-h] [-v] [-d] filename [resultset.csv]
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
30.11.18, 10:57 - Heise: Was geht ab?
30.11.18, 10:58 - Heise: Mir geht es echt gut :)
1/26/19, 00:07 - Jon Doe: Schlaf gut
18.05.19, 11:50:00: Alan Smith: Hier geht es los
Das ist eine neue Zeile
```

The resultset file looks like this. In the default configuration new lines get the same date and time stamp and sender name as the previous line:
```shell
Date and Time|Date|Time|Name|Message
2019-8-21 23:28|2019-8-21|23:28|Jon Doe|Waste out of wealth 😂
2016-12-21 23:29|2016-12-21|23:29|Alan Smith|Like a Rolex
2018-11-30 10:57|2018-11-30|10:57|Heise|Was geht ab?
2018-11-30 10:58|2018-11-30|10:58|Heise|Mir geht es echt gut :)
2019-01-26 00:07|2019-01-26|00:07|Jon Doe|Schlaf gut
2019-05-18 11:50|2019-05-18|11:50|Alan Smith|Hier geht es los
2019-05-18 11:50|2019-05-18|11:50|Alan Smith|Das ist eine neue Zeile
```
