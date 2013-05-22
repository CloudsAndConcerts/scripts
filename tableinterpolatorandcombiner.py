#!/usr/bin/env python
# encoding: utf-8

"""
tableinterpolatorandcombiner.py

For Clouds & Concerts / by Ola Loevholm 2013
Takes a two column CSV as imput where the line consists of two numbers the first lower than the second. 
Create a new single column where the whole integer between the first and second value for each row in input is interpolated.
"""

import csv

outfile = open("numbers_output.csv","w")

def main():
  try:
    with open('numbers_input.csv') as csvfile:
      number_reader = csv.reader(csvfile)
      for row in number_reader:
        a, b = (row[0], row[1])
        print a, b
        for x in range(int(a),int(b)+1):
          to_print =  str(x) + "\n"
          outfile.write(to_print)
  except KeyError as e:
    print e
  
  outfile.close()


if __name__ == '__main__':
  main()