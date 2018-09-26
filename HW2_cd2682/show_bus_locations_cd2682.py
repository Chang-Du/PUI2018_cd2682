# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import print_function
import json
try:
    import urllib2 as urllib 
except ImportError:
    import urllib.request as urllib
import os
import sys 

apikey = sys.argv[1]
busline = sys.argv[2]

if len(sys.argv) != 3:
    print ("Invalid number of arguments. Run as: python show_bus_locations_cd2682.py apikey busline")
    sys.exit()


mtaurl = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s"%(apikey,busline)
print (mtaurl)
response = urllib.urlopen(mtaurl)
data = response.read().decode("utf-8")
dataDict = json.loads(data)

'''
print (dataDict)
'''
Buses = dataDict['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

print ('Bus line: %s'%(busline))
print ('Number of Active Buses: %s'%(len(Buses)))

for i in range(0, len(Buses)):
    latitude = Buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude']
    longitude = Buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude']
    print('Bus %s is at latitude %s and longtitude %s'%(i,latitude,longitude))
    
