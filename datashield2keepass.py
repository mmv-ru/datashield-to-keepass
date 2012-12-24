#!pyton
# -*- coding~: utf8 -*-
# Tested on Python Release 2.5 Win32

version = "0.0.1"

# BeautifulSoup 3
# http://www.crummy.com/software/BeautifulSoup/bs3/documentation.html
from BeautifulSoup import BeautifulStoneSoup
#import string
#import sys
#import os
# http://docs.python.org/library/quopri.html
import quopri
import urllib
# CSV output
import csv
# format template

# http://docs.python.org/2/library/codecs.html#standard-encodings
charset = 'cp1251' # possible need to be changed to correct charset


def main():
    soup=openfile(u"Datashield Export_Example.xml")
#    print(soup.findAll('category'))
#    print(soup.findAll('template'))
#    print(soup.findAll('record'))
    print(u"тест")
    categories = ParseCategories(soup)
    print('category[9] ', categories['9']['name'])
    templates = ParseTemplates(soup)
    #print('template["32767"] ', templates['32767'])
    records = ParseRecords(soup)
    print "Records", repr(records)
    pass

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
    return dict(map(lambda x: (unescape(x['id']), {'id': unescape(x['id']), 'encrypt': unescape(x.get('encrypt', u'0')),
                                        'FieldName': unescape(x.string) }),
                    fields.findAll('field'))
               )

def ParseRecords(records):
    """Parse records
    
    """
    #print repr(records)
    return map(lambda x: dict_merge({'id': unescape(x['id']), 'template': unescape(x['template']),
                                     'category': unescape(x['category']), 'created': unescape(x['created']) },
                                    ParseValues(x.findAll('values', limit=1)[0])
                                   ),
                         #} | ParseValues(x.findAll('values', limit=1)[0]),
                         records.findAll('record'))

def dict_merge(*args):                         
    result = {}
    for d in args: result.update(d)
    return result
    
def ParseValues(values):
    """ Parse Values"""
    #print "Values ", values 
    return dict(map(lambda x: (unescape(x['id']),unescape(x.string)),
                    values.findAll('value'))
               )
                         
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

formats = {'template': {'Account': 'format',
                        'Login Name': 'format',
                        'Password': 'format',
                        'Web Site': 'format',
                        'Comments': 'format'},}


def importformats(filename):
    """ 
    formats = {'template': {'Account': 'format',
                               'Login Name': 'format',
                               'Password': 'format',
                               'Web Site': 'format',
                               'Comments': 'format'},}
    """
    try:
        file = open(filename, 'r')
        formats = eval(file, {})
    finally:
        file.close

def unknown_templates(records, templates, formats):
    """generate format for unknown templates
    """
    new_formats = []
    for record in records:
        template = record['template']
        if not ((template in formats) or (template in new_format)):
            new_formats.add(template)
    print new_formats
        
def output(File, records, templates, formats):
    """Output in Keepass CSV
    """
    for record in records:
        format = formats[record['template']]
        print format
	
if __name__ == '__main__':
    main()