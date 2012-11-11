#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Clouds & Concerts - 2012 
Ola Loevholm




Called from command line: 
The script reads a file named "topp1000_artister.csv" consisting of a list of artists and then tries to find out which country each artist comes from based on the name. 
The name is given in the second column of the CSV file.

Called as a module: 
The method getCountry() takes an artist name and checks this with musicbrainz seach engine. Returns the country if a) artist is found through the search engine b) artist has a country associated to the profile


"""

import sys, urllib, string, csv, time
import xml.etree.ElementTree as ET

# Loads a dictionary with ISO 3166-1 abbreviations and codes
COUNTRIES = {"AF":"AFGHANISTAN","AX":"ÅLAND ISLANDS","AL":"ALBANIA","DZ":"ALGERIA","AS":"AMERICAN SAMOA","AD":"ANDORRA","AO":"ANGOLA","AI":"ANGUILLA","AQ":"ANTARCTICA","AG":"ANTIGUA AND BARBUDA","AR":"ARGENTINA","AM":"ARMENIA","AW":"ARUBA","AU":"AUSTRALIA","AT":"AUSTRIA","AZ":"AZERBAIJAN","BS":"BAHAMAS","BH":"BAHRAIN","BD":"BANGLADESH","BB":"BARBADOS","BY":"BELARUS","BE":"BELGIUM","BZ":"BELIZE","BJ":"BENIN","BM":"BERMUDA","BT":"BHUTAN","BO":"BOLIVIA, PLURINATIONAL STATE OF","BQ":"BONAIRE, SINT EUSTATIUS AND SABA","BA":"BOSNIA AND HERZEGOVINA","BW":"BOTSWANA","BV":"BOUVET ISLAND","BR":"BRAZIL","IO":"BRITISH INDIAN OCEAN TERRITORY","BN":"BRUNEI DARUSSALAM","BG":"BULGARIA","BF":"BURKINA FASO","BI":"BURUNDI","KH":"CAMBODIA","CM":"CAMEROON","CA":"CANADA","CV":"CAPE VERDE","KY":"CAYMAN ISLANDS","CF":"CENTRAL AFRICAN REPUBLIC","TD":"CHAD","CL":"CHILE","CN":"CHINA","CX":"CHRISTMAS ISLAND",
"CC":"COCOS (KEELING) ISLANDS","CO":"COLOMBIA","KM":"COMOROS","CG":"CONGO","CD":"CONGO, THE DEMOCRATIC REPUBLIC OF THE","CK":"COOK ISLANDS","CR":"COSTA RICA","CI":"CÔTE D'IVOIRE","HR":"CROATIA","CU":"CUBA","CW":"CURAÇAO","CY":"CYPRUS","CZ":"CZECH REPUBLIC","DK":"DENMARK","DJ":"DJIBOUTI","DM":"DOMINICA","DO":"DOMINICAN REPUBLIC","EC":"ECUADOR","EG":"EGYPT","SV":"EL SALVADOR","GQ":"EQUATORIAL GUINEA","ER":"ERITREA","EE":"ESTONIA","ET":"ETHIOPIA","FK":"FALKLAND ISLANDS (MALVINAS)","FO":"FAROE ISLANDS","FJ":"FIJI","FI":"FINLAND","FR":"FRANCE","GF":"FRENCH GUIANA","PF":"FRENCH POLYNESIA","TF":"FRENCH SOUTHERN TERRITORIES","GA":"GABON","GM":"GAMBIA","GE":"GEORGIA","DE":"GERMANY","GH":"GHANA","GI":"GIBRALTAR","GR":"GREECE","GL":"GREENLAND","GD":"GRENADA","GP":"GUADELOUPE","GU":"GUAM","GT":"GUATEMALA","GG":"GUERNSEY","GN":"GUINEA","GW":"GUINEA-BISSAU","GY":"GUYANA","HT":"HAITI","HM":"HEARD ISLAND AND MCDONALD ISLANDS",
"VA":"HOLY SEE (VATICAN CITY STATE)","HN":"HONDURAS","HK":"HONG KONG","HU":"HUNGARY","IS":"ICELAND","IN":"INDIA","ID":"INDONESIA","IR":"IRAN, ISLAMIC REPUBLIC OF","IQ":"IRAQ","IE":"IRELAND","IM":"ISLE OF MAN","IL":"ISRAEL","IT":"ITALY","JM":"JAMAICA","JP":"JAPAN","JE":"JERSEY","JO":"JORDAN","KZ":"KAZAKHSTAN","KE":"KENYA","KI":"KIRIBATI","KP":"KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF","KR":"KOREA, REPUBLIC OF","KW":"KUWAIT","KG":"KYRGYZSTAN","LA":"LAO PEOPLE'S DEMOCRATIC REPUBLIC","LV":"LATVIA","LB":"LEBANON","LS":"LESOTHO","LR":"LIBERIA","LY":"LIBYA","LI":"LIECHTENSTEIN","LT":"LITHUANIA","LU":"LUXEMBOURG","MO":"MACAO","MK":"MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF","MG":"MADAGASCAR","MW":"MALAWI","MY":"MALAYSIA","MV":"MALDIVES","ML":"MALI","MT":"MALTA","MH":"MARSHALL ISLANDS","MQ":"MARTINIQUE","MR":"MAURITANIA","MU":"MAURITIUS","YT":"MAYOTTE","MX":"MEXICO","FM":"MICRONESIA, FEDERATED STATES OF",
"MD":"MOLDOVA, REPUBLIC OF","MC":"MONACO","MN":"MONGOLIA","ME":"MONTENEGRO","MS":"MONTSERRAT","MA":"MOROCCO","MZ":"MOZAMBIQUE","MM":"MYANMAR","NA":"NAMIBIA","NR":"NAURU","NP":"NEPAL","NL":"NETHERLANDS","NC":"NEW CALEDONIA","NZ":"NEW ZEALAND","NI":"NICARAGUA","NE":"NIGER","NG":"NIGERIA","NU":"NIUE","NF":"NORFOLK ISLAND","MP":"NORTHERN MARIANA ISLANDS","NO":"NORWAY","OM":"OMAN","PK":"PAKISTAN","PW":"PALAU","PS":"PALESTINIAN TERRITORY, OCCUPIED","PA":"PANAMA","PG":"PAPUA NEW GUINEA","PY":"PARAGUAY","PE":"PERU","PH":"PHILIPPINES","PN":"PITCAIRN","PL":"POLAND","PT":"PORTUGAL","PR":"PUERTO RICO","QA":"QATAR","RE":"RÉUNION","RO":"ROMANIA","RU":"RUSSIAN FEDERATION","RW":"RWANDA","BL":"SAINT BARTHÉLEMY","SH":"SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA","KN":"SAINT KITTS AND NEVIS","LC":"SAINT LUCIA","MF":"SAINT MARTIN (FRENCH PART)","PM":"SAINT PIERRE AND MIQUELON","VC":"SAINT VINCENT AND THE GRENADINES",
"WS":"SAMOA","SM":"SAN MARINO","ST":"SAO TOME AND PRINCIPE","SA":"SAUDI ARABIA","SN":"SENEGAL","RS":"SERBIA","SC":"SEYCHELLES","SL":"SIERRA LEONE","SG":"SINGAPORE","SX":"SINT MAARTEN (DUTCH PART)","SK":"SLOVAKIA","SI":"SLOVENIA","SB":"SOLOMON ISLANDS","SO":"SOMALIA","ZA":"SOUTH AFRICA","GS":"SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS","SS":"SOUTH SUDAN","ES":"SPAIN","LK":"SRI LANKA","SD":"SUDAN","SR":"SURINAME","SJ":"SVALBARD AND JAN MAYEN","SZ":"SWAZILAND","SE":"SWEDEN","CH":"SWITZERLAND","SY":"SYRIAN ARAB REPUBLIC","TW":"TAIWAN, PROVINCE OF CHINA","TJ":"TAJIKISTAN","TZ":"TANZANIA, UNITED REPUBLIC OF","TH":"THAILAND","TL":"TIMOR-LESTE","TG":"TOGO","TK":"TOKELAU","TO":"TONGA","TT":"TRINIDAD AND TOBAGO","TN":"TUNISIA","TR":"TURKEY","TM":"TURKMENISTAN","TC":"TURKS AND CAICOS ISLANDS","TV":"TUVALU","UG":"UGANDA","UA":"UKRAINE","AE":"UNITED ARAB EMIRATES","GB":"UNITED KINGDOM","US":"UNITED STATES",
"UM":"UNITED STATES MINOR OUTLYING ISLANDS","UY":"URUGUAY","UZ":"UZBEKISTAN","VU":"VANUATU","VE":"VENEZUELA, BOLIVARIAN REPUBLIC OF","VN":"VIET NAM","VG":"VIRGIN ISLANDS, BRITISH","VI":"VIRGIN ISLANDS, U.S.","WF":"WALLIS AND FUTUNA","EH":"WESTERN SAHARA","YE":"YEMEN","ZM":"ZAMBIA","ZW":"ZIMBABWE"}
	

# Iterates through XML-structure and removes the namespace, for easier navigation in getCountry()s ElementTree.findall()
def remove_namespace(doc, namespace):
	"""Remove namespace in the passed document in place."""
	ns = u'{%s}' % namespace
	nsl = len(ns)
	for elem in doc.getiterator():
		if elem.tag.startswith(ns):
			elem.tag = elem.tag[nsl:]

# getCountry - where the magic happens. Encodes string with artistname to url, then query musicbrainz search engine. 
# parses the XML-answer and get the name, id and country of the first returned element (with highest weight)
# returns country name i a) artist is found through the search engine b) artist has a country associated to the profile, otherwise returns False
def getCountry(name):
	name = urllib.quote_plus(name)
	BASE_URL = "http://musicbrainz.org/ws/2/artist/?query=%s&format=xml&method=advanced" % (name)
	print "Querying: %s" % (BASE_URL)
	try:
		search_input = urllib.urlopen(BASE_URL)
		# Checks whether HTTP Request Code is 200 - if not goes to sleep for 5 seconds // Inded for 503 Code
		http_code = search_input.code
		if http_code != 200:
#			print "Could not access: %s \t Got HTTP Code: %s. 5 second cool-down" % (name, http_code)
			time.sleep(5)
			getCountry(name)
	except Exception: 
		print "GETTING_ERROR: Something went wrong while getting HTTP"
		return False
	#search_xml = search_input.read()
	#print search_xml
	try:
		tree = ET.parse(search_input)
		remove_namespace(tree, u'http://musicbrainz.org/ns/mmd-2.0#')
		feed = tree.getroot()
		elem = feed.findall("./artist-list/")
		#print elem[0].find('name').text
		#print elem[0].get('id')
	except Exception:
		print "PARSE_ERROR: Something went wrong while parsing HTTP"
		return False
	try:
		if elem[0].find('country') != None:
#			print COUNTRIES[elem[0].find('country').text]
			try:
				country = COUNTRIES[elem[0].find('country').text]
			except Exception: 
				print "Could not find key in countrylist error"
				return False
			return [country,elem[0].get('id'),elem[0].find('name').text]
		else:
			print elem[0].find('name').text + " has not any country associated\n"
			return False
	except IndexError, ValueError:
		print "ERROR - COULD NOT GET DATA FROM %s\n" % (name)
		return False
	
# If method is called from terminal. Iterates through topp1000 artists contained in a CSV-file in same directory. 
if __name__ == "__main__":
	#name = sys.argv[1]
	csvfile = open("topp1000_artister.csv")
	outfile = open("topp1000_output.csv","w")
	artistlist = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in artistlist:
		result = getCountry(line[1])
		try:
			if result != False:
				result_string = "%s,%s,%s,%s,%s,%s\n" % (line[0],line[1],line[2],result[0],result[1],result[2])
#				print result_string
			else:
				result_string = "%s,%s,%s,%s\n" % (line[0],line[1],line[2],"No Country Found or fail occured")
#				print result_string
		except IndexError, ValueError:
			print e
			result_string = "Error on element: %s\n" % line[1]
		try:	
			outfile.write(result_string)
		except:
			print "Write error happened with %s" % line[1]
		