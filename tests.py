﻿#!pyton
# -*- coding~: utf8 -*-
# Tested on Python Release 2.5 Win32

import datashield2keepass

def test():
  soup=datashield2keepass.openfile(u"Datashield Export_Example.xml")
  assert (datashield2keepass.ParseCategories(soup)['9']['name'] ==
          u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438' )
  assert (datashield2keepass.ParseTemplates(soup)['32767']['name'] == u'4t Nox' )
  
def test_decode():
    assert (datashield2keepass.decode("%cd%e5%f4%f2%fc%20%d0%ee%f1%f1%e8%e8") ==
            u'\u041d\u0435\u0444\u0442\u044c \u0420\u043e\u0441\u0441\u0438\u0438')