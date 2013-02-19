#!/usr/bin/python
# -*- coding:utf-8 -*-

import csv, sys


# python adaption of strike a match: https://gist.github.com/1063364/8b8970bb617c2f8689fedc50721e7bcc60767df8
def _get_character_pairs(text):

    if not hasattr(text, "upper"):
        raise ValueError("Invalid argument")

    results = dict()

    for word in text.upper().split():
        for pair in [word[i]+word[i+1] for i in range(len(word)-1)]:
            if pair in results:
                results[pair] += 1
            else:
                results[pair] = 1
    return results

def compare_strings(string1, string2):

    s1_pairs = _get_character_pairs(string1)
    s2_pairs = _get_character_pairs(string2)

    s1_size = sum(s1_pairs.values())
    s2_size = sum(s2_pairs.values())

    intersection_count = 0

    if s1_size < s2_size:
        smaller_dict = s1_pairs
        larger_dict = s2_pairs
    else:
        smaller_dict = s2_pairs
        larger_dict = s1_pairs

    for pair, smaller_pair_count in smaller_dict.items():
        if pair in larger_dict and larger_dict[pair] > 0:
            if smaller_pair_count < larger_dict[pair]:
                intersection_count += smaller_pair_count
            else:
                intersection_count += larger_dict[pair]
    
    if s1_size > 0 or s2_size > 0:
      return (2.0 * intersection_count) / (s1_size + s2_size)
    else:
      print "Wohoo. Shit went down"
      return 0 
    
    


if len(sys.argv) < 2:
  sys.stderr.write('Usage: count_csv.py inputfile.csv \n')
  sys.exit(1)

inputfile = sys.argv[1]

try: 
  open(inputfile,"r")
except IOError as e:
  print "Could not open file: {0} \n".format(e.strerror)
  sys.exit(1)

a = []
with open(inputfile,"r") as csvfile:
  dialect = csv.Sniffer().sniff(csvfile.read(1024))
  csvfile.seek(0)
  reader = csv.reader(csvfile, dialect)
  for row in reader:
    a.append(row[0])
  
  
print "The total number of elements, may include headerfile with descriptions"
print len(a)

# Going through every element to search for similarities
for el in a:
  for iel in a:
    if compare_strings(iel,el) > 0.5:
      print "%s    #    %s" % (el,iel)
