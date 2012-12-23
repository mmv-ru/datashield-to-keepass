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
    return dict(map(lambda x: (x['id'], {'id': x['id'], 'rid': x['rid'],
                                             'name': x.string.strip() }),
                    soup.findAll('category')
                   )
               )

def ParseTemplates(soup):
    """Parse templates"""
    return dict(map(lambda x: (x['id'], {'id': x['id'], 'name': x['name'], 'flags': x['flags'],
                                        'fields': ParseFields(x) }),
                    soup.findAll('template')))

def ParseFields(fields):
    """Parse fields"""
    #print(fields.findAll('field'))
    return dict(map(lambda x: (x['id'], {'id': x['id'], 'encrypt': x.get('encrypt', u'0'),
                                        'FieldName': x.string.strip() }),
                    fields.findAll('field'))
               )

def ParseRecords(records):
    """Parse records
    
    >>> ParseRecords(records)
    
    """
    print repr(records)
    return map(lambda x: dict_merge({'id': x['id'], 'template': x['template'],
                                     'category': x['category'], 'created': x['created'] },
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
    return dict(map(lambda x: (x['id'],x.string),
                    values.findAll('value'))
               )
                         
def openfile(Filename):
    """Open file as BeautifulStoneSoup"""
#    with open(Filename) as file: #not supported in python before 2.6
    try:
        file = open(Filename, 'rb')
        soup = BeautifulStoneSoup( decode(file.read()) )
    finally:
        file.close
    return soup

def decode(str):
    """Decode text with urlencoded inserts in cp1251
    possible need to be changed to correct charset
    
    >>> decode("%cd%e5%f4%f2%fc%20%d0%ee%f1%f1%e8%e8")
    u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438'
    """
    charset = 'cp1251' # possible need to be changed to correct charset
    return unicode(urllib.unquote(str.encode(charset)), charset)

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