#!/usr/bin/env python

# Standard Library
from pprint import pprint
import argparse
import datetime
import os
import time

# Local imports
import weather

cities = ['80501', '04071', '01468']

parser = argparse.ArgumentParser()
parser.add_argument(
    "--onecall", 
    action="store_true",
    help="Use the one call interface",
    )
parser.add_argument(
    "-v", 
    "--verbose", 
    action="count", 
    default=0,
    help="increase output verbosity",
    )
args = parser.parse_args()
if args.verbose > 2:
    print(args)

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
    city = cities[zip_code]
    if args.verbose > 0:
        print(f"Pulling: {city['name']}")
    w = weather.Influx(args, zip_code, lat=city['lat'], lon=city['lon'], name=city['name'], state=city['state'])
    if args.onecall:
        w.pull_onecall()
    else:
        w.pull_weather()
    # pprint(w.data)
    w.save()
    if args.verbose > 1:
        print(f"Saved: {city['name']}\n")

