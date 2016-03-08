#!/bin/python
# vim: set fileencoding=utf-8 :
# Hae saatiedot ilmatieteenlaitoksen data,fmi,fi sivulta fmi apin avulla
import urllib
import urllib2
import datetime
#regular expressionit
import re 
from xml.dom.minidom import parse
import xml.dom.minidom

__TVal = 99
__WVal = 99
__FTVal = 99
__FRVal = 99

def loadCurrent(apikey):
    global __page
    global __xml_current
    global __xml_forecast

    global __TVal
    global __WVal
    
    d=datetime.datetime.utcnow()

    d_start=d-datetime.timedelta(minutes=16)
    d_end=d-datetime.timedelta(minutes=1)

    data = {}
    data['place']='Kajaani'
    data['starttime']=d_start.strftime("%Y-%m-%dT%H:%M:00Z")
    data['endtime']=d_end.strftime("%Y-%m-%dT%H:%M:00Z")
    data['timestep']=1

    #url_values=urllib.urlencode(data)
    #print url_values

    url = 'http://data.fmi.fi/fmi-apikey/'
    url = url + apikey
    url = url + '/wfs?request=getFeature&storedquery_id=fmi::observations::weather::simple'

    full_url=url + '&' + "place=%s&starttime=%s&endtime=%s&timestep=%s" % (data['place'], data['starttime'], data['endtime'], data['timestep'])

   # print full_url

    __page=urllib2.urlopen(full_url)
    
    #data =__page.read()
    #print data
    
    DOMTree = xml.dom.minidom.parse(__page)
    collection = DOMTree.documentElement
    members = collection.getElementsByTagName("wfs:member")

    for member in members:
        name = member.getElementsByTagName('BsWfs:ParameterName')[0]
    	namevalue = name.childNodes[0].data
	if namevalue == "t2m":
	    value = member.getElementsByTagName('BsWfs:ParameterValue')[0]
	    __TVal = value.childNodes[0].data
	if namevalue == "ws_10min":
	    value = member.getElementsByTagName('BsWfs:ParameterValue')[0]
	    __WVal = value.childNodes[0].data
    
    #print __TVal
    print __WVal		

    return 0

def loadForecast(apikey):

    global __FTVal
    global __FRVal

    d=datetime.datetime.utcnow()

    d_start=d+datetime.timedelta(hours=12, minutes=0)
    d_end=d+datetime.timedelta(hours=12, minutes=15)

    data = {}
    data['place']='Kajaani'
    data['starttime']=d_start.strftime("%Y-%m-%dT%H:%M:00Z")
    data['endtime']=d_end.strftime("%Y-%m-%dT%H:%M:00Z")
    data['timestep']=15

    #url_values=urllib.urlencode(data)
    #print url_values

    url = 'http://data.fmi.fi/fmi-apikey/'
    url = url + apikey
    url = url + '/wfs?request=getFeature&storedquery_id=fmi::forecast::hirlam::surface::point::simple'

    full_url=url + '&' + "place=%s&starttime=%s&endtime=%s&timestep=%s" % (data['place'], data['starttime'], data['endtime'], data['timestep'])

   # print full_url

    __page=urllib2.urlopen(full_url)
    
    #data =__page.read()
    #print data
    
    DOMTree = xml.dom.minidom.parse(__page)
    collection = DOMTree.documentElement
    members = collection.getElementsByTagName("wfs:member")

    for member in members:
        name = member.getElementsByTagName('BsWfs:ParameterName')[0]
    	namevalue = name.childNodes[0].data
	if namevalue == "Temperature":
	    value = member.getElementsByTagName('BsWfs:ParameterValue')[0]
	    __FTVal = value.childNodes[0].data
	if namevalue == "WeatherSymbol3":
	    value = member.getElementsByTagName('BsWfs:ParameterValue')[0]
	    __FRVal = value.childNodes[0].data
    
    #print __FTVal
    #print __FRVal		

    return 0

def currentTemperature():
    temp = __TVal
    return temp
    
def feelslikeTemperature():
    TVal = float(__TVal)
    WVal = float(__WVal)
    #https://fi.wikipedia.org/wiki/Pakkasen_purevuus
    if (WVal != 0):
    	tempVal = 13.12+0.6215*TVal-13.956*pow(WVal,0.16)+0.4867*TVal*pow(WVal,0.16)
    else:
	# formula above does not work if windspeed = 0
	tempVal = TVal
    tempStr = "%.1f" % tempVal
    return tempStr
 
def forecastTemperature():
    return __FTVal

def rainAmount():
    symbol = int(float(__FRVal))
    switcher = {
	1: "selkeaa",
	2: "puolipilvista",
	21: "heik sadekuuroja",
	22: "sadekuuroja",
	23: "voim sadekuuroja",
	3: "pilvista",
	31: "heik vesisadetta",
	32: "vesisadetta",
	33: "voim vesisadetta",
	41: "heik lumikuuroja",
	42: "lumikuuroja",
	43: "voim lumikuuroja",
	51: "heik lumisadetta",
	52: "lumisadetta",
	53: "voim lumisadetta",
	61: "ukkoskuuroja",
	62: "voim ukkoskuuroja",
	63: "ukkosta",
	64: "voim ukkosta",
	71: "heik rantakuuroja",
	72: "rantakuuroja",
	73: "voim rantakuuroja",
	81: "heik rantasadetta",
	82: "rantasadetta",
	83: "voim rantasadetta",
	91: "utua",
	92: "sumua",
    }

    return switcher.get(symbol, "-")
