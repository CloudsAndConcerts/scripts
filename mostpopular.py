#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Clouds & Concerts 2013
Ola Loevholm

Takes two CSV file - x, y -  with several elements and finds the - z - number of top occurences.
Creates a report where z element from both are listed, and the compliments of the two sets. 
The report is produced based on x and y filename.

"""

import csv, sys
from collections import Counter


def findIdentical(els):
  return Counter(els)
  
  
if len(sys.argv) < 4:
  sys.stderr.write('Usage: count_csv.py inputfile_x.csv inputfile_y #num_elements \n')
  sys.exit(1)

try:
  namex = sys.argv[1]
  namey = sys.argv[2]
  num_el = int(sys.argv[3])
  inx = open(namex, "r").close
  iny = open(namey, "r").close
except Exception as e:
  print "Please follow instructions below! error was: ", e
  sys.stderr.write('Usage: count_csv.py inputfile_x.csv inputfile_y #num_elements \n')
  sys.exit(1)

outfile = open(namex+namey+"_result.txt","w")


with open(namex) as csvfile:
  dialect = csv.Sniffer().sniff(csvfile.read(1024))
  csvfile.seek(0)
  reader = csv.reader(csvfile, dialect)
  elx = []
  for row in reader:
    elx.append(row[0])
  
with open(namey) as csvfile:
  dialect = csv.Sniffer().sniff(csvfile.read(1024))
  csvfile.seek(0)
  reader = csv.reader(csvfile, dialect)
  ely = []
  for row in reader:
    ely.append(row[0])

setx = set(elx[:num_el])
sety = set(ely[:num_el])

diffxy = list(setx - sety) 
diffyx = list(sety - setx)

## Starts making files
namefile = "%s and %s\n" % (namex, namey)
outfile.write("Result from query:")
outfile.write(namefile)


descx =  "###\n###\n In %s, but not %s\n###\n" % (namex, namey)
outfile.write(descx)
for el in diffxy: 
  temp = "%s\n" % el
  outfile.write(temp)
  

descy = "###\n###\n In %s, but not %s\n###\n" % (namey, namex)
outfile.write(descy)
for el in diffyx: 
  temp = "%s\n" % el
  outfile.write(temp)
  
print "Result in file"
