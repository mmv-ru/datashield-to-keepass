Datashield2Keepass
==================

Converter for Ultrasoft Datashield XML export format to Keepass CSV

Convertor for migration from PalmOS to Android

For installation and documentation, please refer to:

Project at github: https://github.com/mmv-ru/datashield-to-keepass

Authors: Mikhail Moskalev <mmv.rus@gmail.com>

## License
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See the LICENSE file for details

## Documentation
Script in alpha stage.
Keep your old Datashield backup before you shure enought in converted data.

Look TODO for roadmap and development status

### Quick HOWTO
Now no command line parameters. All set in script.

    InputXMLFile = u"Datashield Export_Example.xml"
    charset = 'cp1251' 
    OutputCSVFile = u"keepass.csv"

Run in working directory

    python datashield2keepass.py

Records containing no user data is skipped.
    
* First Pass: generate new_formats.txt with definition of formats missing in formats.txt

* new_formats.txt manually renamed to formats.txt and edited as wished. By default all Datashield fields writen to Keepass Comment.
Look at formats-example.txt for example what you can do.

* Second Pass: Make conversion from DatashieldXML to KeepassCSV using formats defined in formats.txt