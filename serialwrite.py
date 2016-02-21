#!/usr/bin/python
import serial
import time
import fmidata
# open serial connection
# note, also works from bash shell:
# echo -n "hello world!" > /dev/ttyACM0
# this works for some buggy linux usb drivers??
#ser = serial.Serial('/dev/ttyACM0', 9600, rtscts=1)
ser = serial.Serial('/dev/ttyACM0', 9600)
# Arduino resets when serial connection is opened so wait a little. 
time.sleep(1)
# Data terminal ready. Tells peripheral that it can send data.
ser.setDTR(level=0)
time.sleep(1)
# this takes long so if this is used for lcd control, write whole screen
# here.

#for i in range(0,100000):
#    ser.write("%d\0" % (i))
#    time.sleep(0.5)
while 1:
    # Read the page and set variables just onc
    fmidata.loadCurrent()
    t_val=fmidata.currentTemperature()
    feelslike_val=fmidata.feelslikeTemperature()
    #todennakoisyys alk. 27.5.2015
    fmidata.loadForecast()
    rain_amount=fmidata.rainAmount()
    forecast_temp=fmidata.forecastTemperature()
    
    for x in range(0,30):
        # Show the same weather info for about 5 minutes,
        # but update clock.
        # This uses network less.
        time_val=time.localtime()
        hour_val=time_val.tm_hour
        min_val=time_val.tm_min
	if (10 > hour_val):
	    hour_string='0%d' % hour_val
	else:
	   hour_string='%d' % hour_val
	if (10 > min_val):
	    min_string='0%d' % min_val
	else:
	   min_string='%d' % min_val
        ser.write('0%s:%s %sC    \0' % (hour_string, min_string, t_val))
        time.sleep(0.5)
        ser.write('1Tuntuu kuin:%sC    \0' % (feelslike_val))
        # sleep defines how long one screen is displayed
        time.sleep(10)
        forecast_hour=(hour_val+12)%24
	if (12 >= hour_val):
            ser.write('0Klo %d:%sC      \0' % (forecast_hour, forecast_temp))
        else:
            ser.write('0H.klo %d:%sC    \0'  % (forecast_hour, forecast_temp))
	
	time.sleep(0.5)
        ser.write('1%s\0' % (rain_amount))
        # sleep defines how long one screen is displayed
	#print rain_amount
        time.sleep(10)
