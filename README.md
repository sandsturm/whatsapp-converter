# WhatsApp-converter


## Introduction
Use this application to convert your exported WhatsApp chat into a CSV file.
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
```

The resultset will look like this for each line:
```shell
Date Format|Date|Time|Name|Message
EN|2019-8-21|23:28|Jon Doe|Waste out of wealth 😂
DE|2016-12-21|23:29|Alan Smith|Like a Rolex
```
