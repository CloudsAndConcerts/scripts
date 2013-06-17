#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Clouds & Concerts - 2013
Ola Loevholm

Takes a semicomma delimited file, reads the artist_id and name and makes a SQL statement for each of the elements to be fed into the database. 
The names of artists may contain country in parantesis after the name. If so, the script takes the country and separates it from the name into its own column. 
The output is a .sql file with each of the elements. This can be imported into the database through SQL Developer

"""

import sys, csv, re
from string import Template


# Loads a dictionary with ISO 3166-1 abbreviations and codes	

sql_nocountry = Template("INSERT INTO oya_artists (artist_id, navn, year) VALUES ('$artid', '$name', 2011);\n")
sql = Template("INSERT INTO oya_artists  (artist_id, navn, country, year) VALUES ('$artid', '$name', '$country', 2011);\n")


	
# If method is called from terminal. Iterates through topp1000 artists contained in a CSV-file in same directory. 
if __name__ == "__main__":
	#name = sys.argv[1]
	csvfile = open("oya2011artists.txt")
	outfile = open("oya2011artists.sql","w")
	artistlist = csv.reader(csvfile, delimiter=';', quotechar='"')
	for line in artistlist:
		artist_id, name = (line[0], line[1])
		
		match = re.search("\((\w+)\)", name)
		name = name.replace("&", "/&")
		if match:
		  land =  match.group(1)
		  t2 = "(%s)" % land
		  name = name.replace(t2,"")
		  name = name.strip()
		  country = True
		else: 
		  country = False
		try:
			if country != False:
			  result_string = sql.substitute(artid=artist_id, name=name, country=land)
			else:
			  result_string = sql_nocountry.substitute(artid=artist_id, name=name)
		except (IndexError, ValueError) as e:
			print e
			#result_string = "Error on element: %s\n" % line[1]
		try:	
			outfile.write(result_string)
			print result_string
		except:
			print "Write error happened with %s" % line[1]
