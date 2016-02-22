import csv
import urllib2
import urllib
import json
import sys
import time


key = raw_input("Please enter your API key: ")
date = raw_input("Please enter Date (2016-02-08) : ")
arrive_by_time = raw_input("Please enter time of arrival (09:00) : ")
max_walk = raw_input("Please enter maximum walking distance in miles (0.25): ")

TAZCentroid= raw_input("Please paste the path to the origin file (TAZCentroid.csv) : ")
EmploymentCenter = raw_input("Please paste the path to the destination file (EmploymentCenter.csv) : ")
TravelTimeFile=raw_input("Please paste the path to the file you want to write travel time data in : ")


##Loop through TAZs to get origin point longtitude and latitude 
with open (TAZCentroid)as origin_file:
    origins = list(csv.DictReader(origin_file))
    
##Loop through Employment Centers to get desitnition point longtitude and latitude
with open (EmploymentCenter)as destination_file:
    destinations = list(csv.DictReader(destination_file))


## Define a function to get travel time
def get_travel_time(origin_lat, origin_lon, dest_lat, dest_lon, key, date, arrive_by_time, max_walk):
    param=urllib.urlencode({
        'key':key,
        'destination_lat':dest_lat,
        'destination_lon':dest_lon,
        'origin_lat':origin_lat,
        'origin_lon':origin_lon,
        'date': date,# Typical work day
        'time': arrive_by_time, # Morning peak
        'max_walk': max_walk, # 0.25 mile as Maximum walking distance
        'minimize':'time',
        'arrive_depart':'arrive'
        })
    url='https://developer.cumtd.com/api/v2.2/json/GetPlannedTripsByLatLon?'+param
    json_obj=urllib2.urlopen(url)
    data=json.load(json_obj)
    status=data['status']
    if status['msg']!="ok":
        travel_time=999
    else:
        for item in data['itineraries']:
            travel_time=item['travel_time']

    return travel_time
    pass
    

## Loop through all the origin and destination to get travel time
rows = []
ids = []
for origin in origins:
    ids.append({
        'TAZ': origin["id"]
        })

    for destination in destinations:
        rows.append({
            'travel_time': get_travel_time(origin["Latitude"],origin["Longitude"],destination["Latitude"],destination["Longitude"],str(key),str(date), str(arrive_by_time),str(max_walk))
        })
        print "Commute time from TAZ %s to employment center %s is %s." %(origin["id"], destination["Name"],get_travel_time(origin["Latitude"],origin["Longitude"],destination["Latitude"],destination["Longitude"],str(key),str(date), str(arrive_by_time),str(max_walk)))
        time.sleep(5) # Apply time.sleep to avoid sending too many requests to API server in a short peroid of time


## Write CSV

with open(TravelTimeFile,'w') as csvfile:
    fieldnames = ['TAZ',destinations[0]["Name"], destinations[1]["Name"],destinations[2]["Name"],destinations[3]["Name"],destinations[4]["Name"],destinations[5]["Name"]]
    # For more destination points, keep adding destinations[j]["Name"], till j=number of destination-1.
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(origins)):
        writer.writerow({'TAZ':ids[i]["TAZ"],destinations[0]["Name"]:rows[len(destinations)*i]["travel_time"],destinations[1]["Name"]:rows[len(destinations)*i+1]["travel_time"],destinations[2]["Name"]:rows[len(destinations)*i+2]["travel_time"],destinations[3]["Name"]:rows[len(destinations)*i+3]["travel_time"],destinations[4]["Name"]:rows[len(destinations)*i+4]["travel_time"],destinations[5]["Name"]:rows[len(destinations)*i+5]["travel_time"]})
        # For more destination points, keep adding destinations[j]["Name"]:rows[len(destinations)*i+j], till j=number of destination -1. 


