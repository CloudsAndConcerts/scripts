#! /bin/python
#-*- charset:uft-8 -*-

import csv, sys

if len(sys.argv) < 2:
  sys.stderr.write('Usage: count_csv.py inputfile.csv \n')
  sys.exit(1)

inputfile = sys.argv[1]
try: 
  open(inputfile)
except IOError as e:
  print "Could not open file: {0} \n".format(e.strerror)
  sys.exit(1)
  
with open(inputfile) as csvfile:
  dialect = csv.Sniffer().sniff(csvfile.read(1024))
  csvfile.seek(0)
  reader = csv.reader(csvfile, dialect)
  a = []
  for row in reader:
    a.append(row)
  print "The total number of elements, may include headerfile with descriptions"
  print len(a)