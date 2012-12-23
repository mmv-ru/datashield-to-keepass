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
    cat = ParseCategories(soup)
    #print('9 ', cat['9']['name'])
    templates = ParseTemplates(soup)
    #print('template["32767"] ', templates['32767'])
    records = ParseRecords(soup)
    pass

def ParseCategories(soup):
    """Parse categories"""
    return dict(map(lambda cat: (cat['id'], {'id': cat['id'], 'rid': cat['rid'],
                                             'name': cat.string.strip() }),
                    soup.findAll('category')
                   )
               )

def ParseTemplates(soup):
    """Parse templates"""
    return dict(map(lambda cat: (cat['id'], {'id': cat['id'], 'name': cat['name'], 'flags': cat['flags'],
                                        'fields': ParseFields(cat) }),
                    soup.findAll('template')))

def ParseFields(fields):
    """Parse fields"""
    #print(fields.findAll('field'))
    return dict(map(lambda cat: (cat['id'], {'id': cat['id'], 'encrypt': cat.get('encrypt', u'0'),
                                        'FieldName': cat.string.strip() }),
                    fields.findAll('field')))

def ParseRecords(records):
    """Parse records"""
    print(records.findAll('record'))
                    
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
    
    >>> decode("%cd%e5%f4%f2%fc%20%d0%ee%f1%f1%e8%e8")
    u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438'
    """
    return unicode(urllib.unquote(str.encode('cp1251')), 'cp1251')

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