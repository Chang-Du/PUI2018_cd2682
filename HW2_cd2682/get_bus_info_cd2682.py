#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 15:26:19 2018

@author: duchang
"""
from __future__ import print_function
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib
import os
import sys
import csv
import pandas as pd

apikey = sys.argv[1]
busline = sys.argv[2]
busline_csv = sys.argv[3]
# 变量名不能出现”.“

if len(sys.argv) != 4:
    print ("Invalid number of arguments. Run as: python get_bus_info_cd2682.py apikey busline busline.csv")
    sys.exit()

mtaurl = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=%s&VehicleMonitoringDetailLevel=calls&LineRef=%s"%(apikey,busline)
print (mtaurl)
response = urllib.urlopen(mtaurl)
data = response.read().decode("utf-8")
dataDict = json.loads(data)

Buses = dataDict['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']

# this line opens a file for writing using the name you chose
# the "w" tells it you are opening for writing, not reading
# 变量命名不能使用空格，用下划线。

# define the list: latitude, longitude, stop_name, stop_status
# a list can store more values than a single variable
latitude, longitude, stop_name, stop_status = [], [], [], []

for i in range(0, len(Buses)):

# 使用append对list赋值
# latitude and longitude will never be null
    latitude.append(Buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Latitude'])
    longitude.append(Buses[i]['MonitoredVehicleJourney']['VehicleLocation']['Longitude'])

# Key error: OnwardCall means some of the OnwardCall is not exist. which means [OnwardCalls] is null. which means the len() is 0
    if len(Buses[i]['MonitoredVehicleJourney']['OnwardCalls']) == 0:
        stop_name.append('N/A')
        stop_status.append('N/A')
    else:
        stop_name.append(Buses[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['StopPointName'])
        stop_status.append(Buses[i]['MonitoredVehicleJourney']['OnwardCalls']['OnwardCall'][0]['Extensions']['Distances']['PresentableDistance'])

dic = {'Latitude' : latitude, 'Longitude' : longitude, 'Stop Name' : stop_name,'Stop Status' : stop_status}
result = pd.DataFrame(data=dic).to_csv(busline_csv, index=False)

# to_csv means output as .csv
#index=false means not show the row of panda initial. Otherwise, it will be a ',' infront of the first row
