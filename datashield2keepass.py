#!pyton
# -*- coding: utf-8 -*-
# Tested on Python Release 2.5 Win32

version = "0.0.1"

# BeautifulSoup 3
# http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
from BeautifulSoup import BeautifulStoneSoup
#import string
import sys
# http://docs.python.org/library/quopri.html
import quopri
import urllib
# parse record
import traceback
# CSV output
import csv
import cStringIO
import codecs
import os
import re
# format template
import pprint
import os.path

# Key parameters
InputXMLFile = u"Datashield Export.xml"
# Charset for decoding strings in DataShield XML.
# Change to correct charset !!!
# http://docs.python.org/2/library/codecs.html#standard-encodings
charset = 'cp1251' 

# Optional parameters
OutputCSVFile = u"keepass.csv"
FormatsFile = u"formats.txt"
NewFormatsFile = u"new_formats.txt"

def main():
    soup=openfile(InputXMLFile)
#    print(soup.findAll('category'))
#    print(soup.findAll('template'))
#    print(soup.findAll('record'))
    assert(repr(u'тест') == "u'\u0442\u0435\u0441\u0442'") # test UTF-8 literal encoding
    #categories = ParseCategories(soup)
    #print('category[9] ', pprint.pformat(categories['9']['name']))
    print("Parse Templates")
    templates = ParseTemplates(soup)
    #print('template["32767"] ', templates['32767'])
    print("Templates parsed: %s" % len(templates))
    print("Parse Records")
    records, stats = ParseRecords(soup)
    #print "Records: ", pprint.pformat(records)
    print("Records:\n  parsed %(loaded)s\n  empty records %(emptyrecords)s" % stats)
    print("Load formats from file: %s" % FormatsFile)
    formats = importformats(FormatsFile)
    print("Formats loaded: %s" % len(formats))
    print("Write new formats to file: %s" % NewFormatsFile)
    new_formats = unknown_templates(records, templates, formats)
    #print pprint.pprint(new_formats)
    outputNewFormats(new_formats, NewFormatsFile)
    print("Missing formats: %s" % len(new_formats))
    if len(new_formats):
        print("""
    Missing formats saved to %s.
    Add this formats to %s
""" % (NewFormatsFile, FormatsFile))
        return
    print("Output records to KeepasCSV-file: %s" % OutputCSVFile)
    outputCSV(OutputCSVFile, records, templates, formats)
    print("All Done.")
    

def ParseCategories(soup):
    """Parse categories"""
    # Here x - formal parameter for lambda function, applied to each item of list (soup.findAll('category'))
    return dict(map(lambda x: (unescape(x['id']), {'id': unescape(x['id']), 'rid': unescape(x['rid']),
                                             'name': unescape(x.string) }),
                    soup.findAll('category')
                   )
               )

def ParseTemplates(soup):
    """Parse templates"""
    return dict(map(lambda x: (unescape(x['id']), {'id': unescape(x['id']), 'name': unescape(x['name']),
                                                  'flags': unescape(x['flags']), 'fields': ParseFields(x) }),
                    soup.findAll('template')))

def ParseFields(fields):
    """Parse fields"""
    #print(fields.findAll('field'))
    return dict(map(lambda x: (unescape(x['id']), {'encrypt': unescape(x.get('encrypt', u'0')),
                                        'FieldName': unescape(x.string) }),
                    fields.findAll('field'))
               )

def ParseNote(note_soup):
    """Parse record note"""
    note = ''
    if len(note_soup):
        note = unescape(note_soup[0].string)
    result = {'note': note}
    return result

def ParseRecords(records_soup):
    """Parse records
       return: (records, statistic)
    """
    #print repr(records)
    records = []
    prevrecno=0
    prevrecid=''
    emptyrecords = 0
    for record in records_soup.findAll('record'):
        try:
            recordNote = ParseNote(record.findAll('note', limit=1))
            recordValues = ParseValues(record.findAll('values', limit=1))
            if len(''.join(recordNote.values()) + ''.join(recordValues.values()))  :
                records.append(dict_merge({'id': unescape(record['id']), 'template': unescape(record['template']),
                                           'category': unescape(record.get('category', '')), 'created': unescape(record['created'])},
                                           recordNote,
                                           recordValues
                                         )
                           )
                prevrecid=unescape(record['id'])
            else:
                print("Empty record %d skipped." % (prevrecno+1))
                pprint.pprint(record)
                emptyrecords += 1
        except Exception, e:
            print("Error in parsing XML record:")
            pprint.pprint(record)
            print("\nlast successfull record - %s id=%s" % (prevrecno, prevrecid))
            raise
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # traceback.print_exception(exc_type, exc_value, exc_traceback,
                              # limit=1, file=sys.stdout)
        prevrecno+=1
    return records, {'loaded': len(records), 'emptyrecords': emptyrecords}

def dict_merge(*args):                         
    result = {}
    for d in args: result.update(d)
    return result
    
def ParseValues(values):
    """ Parse Values"""
    #print "Values ", values 
    if len(values):
        return dict(map(lambda x: (unescape(x['id']),unescape(x.string)),
                        values[0].findAll('value'))
                   )
    else:
        return {}
                         
def openfile(Filename):
    """Open file as BeautifulStoneSoup"""
#    with open(Filename) as file: #not supported in python before 2.6
    try:
        file = open(Filename, 'rb')
        soup = BeautifulStoneSoup(file)
    finally:
        file.close
    return soup

def unescape(str):
    """Decode text with urlencoded inserts in cp1251
    possible need to be changed to correct charset
    
    >>> decode("%cd%e5%f4%f2%fc%20%d0%ee%f1%f1%e8%e8")
    u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438'
    """
    return unicode(urllib.unquote(str.strip().encode(charset)), charset)

def importformats(filename):
    """ 
    formats = {'template': {'t_name': 'template name (for reference)',
                            'f_names': {'field_id': 'field name (for reference)'}
                            '1_Account': 'format',
                            '2_Login Name': 'format',
                            '3_Password': 'format',
                            '4_Web Site': 'format',
                            '5_Comments': 'Description: %(257)s\nCode: %(258)s\n '
                           }}
    """
    if os.path.isfile(filename): 
        file = open(filename, 'r')
        try:
            formats = eval(file.read(), {})
        finally:
            file.close
    else:
        print("Formats file ""%s"" missing. Empty." % (filename))
        formats = {}
    return formats

def unknown_templates(records, templates, formats):
    """generate format for unknown templates
    """
    new_templates = []
    for record in records:
        template = record['template']
        if not ((template in formats) or (template in new_templates)):
            new_templates.append(template)
    new_formats = {}
    for template_id in new_templates:
        new_formats[template_id] = {'t_name': templates[template_id]['name'],
                                    'f_names': templates[template_id]['fields'],
                                    '1_Account': '',
                                    '2_Login Name': '',
                                    '3_Password': '',
                                    '4_Web Site': '',
                                    '5_Comments': AllFieldsInFormat(templates[template_id]['fields'], templates) + '%(note)s'
                                    }
    return new_formats

def outputNewFormats(new_formats, New_Formats_File):
    """Save new formats to file
    """
    if len(new_formats):
        file = open(New_Formats_File, "w")
        try:
            file.write(pprint.pformat(new_formats))
        finally:
            file.close()
    else:
        # May be is good remove new_formats.txt here?
        pass
    
def AllFieldsInFormat(fields, templates):
    """ Build format line with all fields
    """
    format = ''
    for k in sorted(fields.keys()):
        format += '%s: %%(%s)s\n' % (fields[k]['FieldName'], k)
    return format

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """
    
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)    

class KeepassDialect(csv.Dialect):
    """
    http://keepass.info/help/base/importexport.html#csv
    """
    quotechar = '"'
    delimiter = ','
    lineterminator = os.linesep
    doublequote = False
    skipinitialspace = True
    quoting = csv.QUOTE_ALL
    escapechar = '\\'

def add_default(record, templates):
    """ Add to record all fields presented in template
    """
    for key in templates[record['template']]['fields'].keys():
        record.setdefault(key, '')
   
def outputCSV(File, records, templates, formats):
    """Output in Keepass CSV
    """
    f = open(File, "wb")
    # f = open(File, "w", newline="") # for python 3
    try:
        writer = UnicodeWriter(f, dialect=KeepassDialect())
        for record in records:
            format = formats[record['template']]
            add_default(record, templates)
            try:
                writer.writerow(map(lambda x: Keepass1CSVEscape(format[x] % record),
                                    ['1_Account', '2_Login Name', '3_Password', '4_Web Site', '5_Comments']))
#                    (Keepass1CSVEscape(format['1_Account'] % record) ,
#                                 Keepass1CSVEscape(format['2_Login Name'] % record) ,
#                                 Keepass1CSVEscape(format['3_Password'] % record) ,
#                                 Keepass1CSVEscape(format['4_Web Site'] % record) ,
#                                 Keepass1CSVEscape(format['5_Comments'] % record)))
            except:
#            except KeyError:
                print("\nError in converting record:")
                print(pprint.pformat(record))
                print("\nFormat:")
                print(pprint.pformat(format))
                raise
    finally:
        f.close()

def Keepass1CSVEscape(str):
    """ KeepassCSV require Replace " bu \" and \ by \\ 
        http://keepass.info/help/base/importexport.html#csv
        But " replaced automaticaly by CSV Dialect """
    return re.sub(r'([\\])', r'\\\1', str)

if __name__ == '__main__':
    main()