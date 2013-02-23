#!pyton
# -*- coding~: utf8 -*-
# Tested on Python Release 2.5 Win32

# It used by nose test
# To run tests, run nosetests in project root
# To run tests with coverage run "nosetests --with-coverage"
# Test use Datashield Export_Example.xml as data source

import datashield2keepass

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises


#datashield2keepass.charset = 'cp1251'

def test_import():
  soup=datashield2keepass.openfile(u"Datashield Export_Example.xml")
  assert_equal(datashield2keepass.ParseCategories(soup)['9']['name'], 
               u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438' )
  assert_equal(datashield2keepass.ParseTemplates(soup)['32767']['name'],
               u'4t Nox' )
  # simple data
  assert_equal(datashield2keepass.ParseRecords(soup)[0][0],
              {'category': u'7', 'note': '', u'260': u'6twz6lr',
               'template': u'32767', 'created': u'28.05.2004 18:00:38',
               u'259': u'ivang', 'id': u'70'}  )
  # escaped data
  assert_equal(datashield2keepass.ParseRecords(soup)[0][1],
              {'category': u'7', 'note': '', u'260': u'sword"',
              'template': u'32767', 'created': u'28.05.2004 18:00:38',
              u'259': u'gmc\\user', 'id': u'68'})
  assert_equal(datashield2keepass.ParseRecords(soup)[1],
              {'loaded': 10, 'emptyrecords': 1}  )
  
def test_unescape():
    assert (datashield2keepass.unescape("\r\n     %cd%e5%f4%f2%fc%20%d0%ee%f1%f1%e8%e8\r\n      ") ==
            u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438')

def test_KeepassCSVEscape():
    assert_equal(datashield2keepass.Keepass1CSVEscape(r'a"b\c"~[]{}<>d!$@^%#&*()-_+'),
                 r'a"b\\c"~[]{}<>d!$@^%#&*()-_+')