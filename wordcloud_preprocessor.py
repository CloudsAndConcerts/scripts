#! /bin/python
# -*- coding: utf-8 -*-

"""
Clouds & Concerts - 2013
Ola Loevholm

Takes a CSV file. Sorts the elements after frequency, and extract the 500 most popular occurences. 
Creates a mock-up keeping the relational distance between the elements, but reduce the size to 20%. 
This text can then be fed to wordcloud generators to create a text. 
Output: <filefrominput>_result.txt

"""

import csv, sys
from collections import Counter



def findIdentical(els):
  return Counter(els)
  

### EXECUTION STARTS HERE

if len(sys.argv) < 2:
  sys.stderr.write('Usage: count_csv.py inputfile.csv \n')
  sys.exit(1)

inputfile = sys.argv[1]
outfile = open(inputfile+"_result.txt","w")

try: 
  open(inputfile)
except IOError as e:
  print "Could not open file: {0} \n".format(e.strerror)
  sys.exit(1)
  
with open(inputfile) as csvfile:
  reader = csv.reader(csvfile)
  els = []
  for row in reader:
    els.append(row[0])
  print "The total number of elements, may include headerfile with descriptions"
  print len(els)

print "what we got:"
c = findIdentical(els)
el = c.most_common(500)
print el
text = ""
for a in el:
  for e in range(0,int(a[1]/5)):
    text += "%s," % a[0]
    
outfile.write(text)
outfile.close()