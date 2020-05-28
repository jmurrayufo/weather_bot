#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import weather
import os

cities = ['80501', '04071', '01468']

# IMPORTANT: Names cannot have spaces or commas. Use - or _ 
cities = {
    '80501':{
        "name": "Longmont",
        "state": "CO",
        "lat": 40.18,
        "lon":-105.1,
    },
    '04071':{
        "name": "Raymond",
        "state": "ME",
        "lat": 43.92,
        "lon": -70.45,
    },
    '01468':{
        "name": "Templeton",
        "state": "MA",
        "lat": 42.55,
        "lon": -72.06,
    },
}

os.chdir(os.path.dirname(__file__))

for zip_code in cities:
    print(zip_code, cities[zip_code])
    city = cities[zip_code]
    w = weather.Influx(zip_code, lat=city['lat'], lon=city['lon'], name=city['name'], state=city['state'])
    w.pull()
    # pprint(w.data)
    w.save()