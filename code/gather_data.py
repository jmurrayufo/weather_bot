#!/usr/bin/env python

# Standard Library
from pprint import pprint
import argparse
import datetime
import os
import time

# Local imports
import weather

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
cities = [
    {
        "zip_code": '80501',
        "state": "CO",
        "name": "Longmont",
        "lon":-105.1,
        "lat": 40.18,
    },
    {
        "zip_code": '04071',
        "state": "ME",
        "name": "Raymond",
        "lon": -70.45,
        "lat": 43.92,
    },
    {
        "zip_code": '01468',
        "state": "MA",
        "name": "Templeton",
        "lon": -72.06,
        "lat": 42.55,
    },
    {
        "zip_code": '94107',
        "state": "CA",
        "name": "San-Francisco",
        "lon": -122.3986,
        "lat": 37.7618,
    },
]

os.chdir(os.path.dirname(__file__))

for city in cities:
    if args.verbose > 0:
        print(f"Pulling: {city['name']}")
    w = weather.Influx(args, city['zip_code'], lat=city['lat'], lon=city['lon'], name=city['name'], state=city['state'])
    if args.onecall:
        w.pull_onecall()
    else:
        w.pull_weather()
    # pprint(w.data)
    w.save()
    if args.verbose > 1:
        print(f"Saved: {city['name']}\n")

