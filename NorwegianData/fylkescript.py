#!/usr/bin/env python
# encoding: utf-8
"""
fylkescript.py

For Clouds & Concerts / by Ola Loevholm 2013
Combines CSV with data where first element is fylkesnummer (two digits) and second element is number. 
This is combined with data from Statistics Norway: 
http://ssb.no/befolkning/statistikker/folkemengde/aar/2013-02-21?fane=tabell#content
Folkemengde etter fylke.

Can be used as a scaffold for processing more data, as datastructure is ready
"""

import sys
import os
import csv
import pickle

class Fylke:
  user_number = 0
  inhabitants_number = 0
  fylkes_number = 0
  fylkesnavn = ""
  
  def __init__(self,flknbr,flknavn):
    self.fylkes_number = flknbr
    self.fylkesnavn = flknavn
    
  
  def get_user_number(self):
    return self.user_number
  def set_user_number(self,usr):
    self.user_number = usr
    
  def get_inhabitants_number(self):
    return self.inhabitants_number
  def set_inhabitants_number(self,ihbt):
    self.inhabitants_number = ihbt
    
  def get_fylkes_number(self):
    return self.fylkes_number
    
  def get_name(self):
    return self.fylkesnavn
    
  
  
  


def main():
  fylker = {}
  try:
    with open('folketall_fylke.csv', 'rU') as csvfile:
      dialect = csv.Sniffer().sniff(csvfile.read(1024))
      csvfile.seek(0)
      fylkesreader = csv.reader(csvfile, dialect)
      for row in fylkesreader:
        fylker[row[0]] = Fylke(row[0],row[1])
        fylker[row[0]].set_inhabitants_number(row[2])
  except KeyError as e:
    print e
  try:  
    with open('fylkesnummer_18dagerbruk.dsv', 'rU') as csvfile:
      dialect = csv.Sniffer().sniff(csvfile.read(1024))
      csvfile.seek(0)
      fylkesreader = csv.reader(csvfile, dialect)
      for row in fylkesreader:
        fylker[row[0]].set_user_number(row[2])
  except KeyError as e:
    print e
    

    
  with open('fylker_out.txt', 'w') as csvfile:
    for fylke in fylker:
      temp = "%s,%s,%s,%s\n" % (fylker[fylke].get_fylkes_number(), fylker[fylke].get_name(), fylker[fylke].get_inhabitants_number(), fylker[fylke].get_user_number())
      csvfile.write(temp)
	


if __name__ == '__main__':
	main()

