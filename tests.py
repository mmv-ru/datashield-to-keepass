#!pyton
# -*- coding~: utf8 -*-
# Tested on Python Release 2.5 Win32

# It used by nose test
# To run tests, run nosetests in project root
# To run tests with coverage run "nosetests --with-coverage"

import datashield2keepass

def test():
  soup=datashield2keepass.openfile(u"Datashield Export_Example.xml")
  assert (datashield2keepass.ParseCategories(soup)['9']['name'] ==
          u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438' )
  assert (datashield2keepass.ParseTemplates(soup)['32767']['name'] == u'4t Nox' )
  assert (datashield2keepass.ParseRecords(soup)['0'] == 
          {'category': u'7', u'260': u'6twz6lr',
           'template': u'32767', 'created': u'28.05.2004 18:00:38',
           u'259': u'ivang', 'id': u'70'}  )
  
def test_decode():
    assert (datashield2keepass.decode("%cd%e5%f4%f2%fc%20%d0%ee%f1%f1%e8%e8") ==
            u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438')