#!pyton
# -*- coding~: utf8 -*-
# Tested on Python Release 2.5 Win32

import datashield2keepass

def test():
  soup=datashield2keepass.openfile(u"Datashield Export_Example.xml")
  print("test")
  print(soup)