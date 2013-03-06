#!/usr/bin/env python
# encoding: utf-8
"""
kommunescript.py

For Clouds & Concerts / by Ola Loevholm 2013
Combines CSV with data where first element is kommunenummer (two digits) and second element is number. 
This is combined with data from Statistics Norway: 
http://ssb.no/befolkning/statistikker/folkemengde/aar/2013-02-21?fane=tabell#content
Folkemengde i kommunene.

Can be used as a scaffold for processing more data, as datastructure is ready
"""

import sys
import os
import csv
import pickle

class Kommune:
  user_number = 0
  inhabitants_number = 0
  kommune_number = 0
  kommunenavn = ""
  
  def __init__(self,komnum,komname):
    self.kommune_number = komnum
    self.kommunenavn = komname
    
  
  def get_user_number(self):
    return self.user_number
  def set_user_number(self,usr):
    self.user_number = usr
    
  def get_inhabitants_number(self):
    return self.inhabitants_number
  def set_inhabitants_number(self,ihbt):
    self.inhabitants_number = ihbt
    
  def get_kommune_number(self):
    return self.kommune_number
    
  def get_name(self):
    return self.kommunenavn
    
  def __str__(self):
      return "<Kommune nummer:%s navn:%s>" % (self.kommune_number, self.kommunenavn)
  
  
  


def main():
  kommuner = {}
  try:
    with open('folketall_kommune.csv', 'rU') as csvfile:
      dialect = csv.Sniffer().sniff(csvfile.read(1024))
      csvfile.seek(0)
      kommunereader = csv.reader(csvfile, dialect)
      for row in kommunereader:
        kommuner[row[0][:4]] = Kommune(row[0][:4],row[0][4:])
        kommuner[row[0][:4]].set_inhabitants_number(row[2])
        print row[0][:4]
  except KeyError as e:
    print e
    
  print "Finished reading"
    

  try:  
    with open('kommunenummer_min100str.dsv', 'rU') as csvfile:
      dialect = csv.Sniffer().sniff(csvfile.read(1024))
      csvfile.seek(0)
      kommunereader = csv.reader(csvfile, dialect)
      for row in kommunereader:
        kommuner[row[0].zfill(4)].set_user_number(row[1].zfill(4))
        print kommuner[row[0].zfill(4)]
  except KeyError as e:
    print e
    
    
  with open('kommuner_out.txt', 'w') as csvfile:
    for kommune in kommuner:
      temp = "%s,%s,%s,%s\n" % (kommuner[kommune].get_kommune_number(), kommuner[kommune].get_name(), kommuner[kommune].get_inhabitants_number(), kommuner[kommune].get_user_number())
      csvfile.write(temp)
	


if __name__ == '__main__':
	main()