#!/usr/bin/python
import pygeoip, sys
try:
	ipfile = sys.argv[1]#get operands
	outfile = sys.argv[2]#
except:
	print "Usage: geoip.py <txt file of ips> <name>"#if wrong give help message
	print "Note: .kml is appended to file name automatically"
	quit()
geo = pygeoip.GeoIP('GeoLiteCity.dat')
def KMLheader(): # create the header of kml file
	tmpkml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
	tmpkml += u"<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n"
	tmpkml += u"<Document>\n"
	return tmpkml
def KMLfooter():
	return u"</Document>\n</kml>"
def loadFile(filename):
	fileOb = open(filename, "r") #open file specified
	return fileOb.readlines()
def saveFile(tmpkml):
	fileOb = open(outfile + ".kml", "w")#auto add .kml extension
	fileOb.write(tmpkml.encode("UTF-8")) #save in utf
def coords(lat, lon):
	result = "25,71"
	if(lat != None):
		if(lon != None):
			result = str(lon) + "," + str(lat)
	return result
def mapIps():
	McKML = u""
	for IP in loadFile(ipfile):
		geodata = geo.record_by_addr(IP)  #get IP geo info
		tmpkml = u"\t<Placemark>\n" #create Placemark entry for each ip specified in file
		tmpkml += u"\t\t<name>%s</name>\n" % (IP)
		try:
			tmpkml += u"\t\t<description>%s, %s</description>\n" % (geodata['city'], geodata['country_name'])
		except:
			tmpkml += u"\t\t<description>unknown</description>\n"
		try:
			tmpkml += u"\t\t<Point>\n\t\t\t<coordinates>%s</coordinates>\n\t\t</Point>\n" % (coords(geodata['latitude'], geodata['longitude']))
		except:
			tmpkml += u"\t\t<Point>\n\t\t\t<coordinates>25,71</coordinates>\n\t\t</Point>\n"
		tmpkml += u"\t</Placemark>\n"
		McKML += tmpkml
	return McKML
def run():#tie functions together
	kmlFile = KMLheader() #create file to be saved
	kmlFile += mapIps() # add ip info to map
	kmlFile += KMLfooter() # add ending info
	saveFile(kmlFile) # save
run()

