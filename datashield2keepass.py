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

def main():
  soup=openfile(u"Datashield Export_Example.xml")
#  print(soup.findAll('category'))
#  print(soup.findAll('template'))
  print(soup.findAll('record'))
  pass

def openfile(Filename):
#  with open(Filename) as file:
    file = open(Filename)
    return BeautifulStoneSoup(file)
  
if __name__ == '__main__':
    main()