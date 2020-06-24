#!/usr/bin/env python

# Standard Library
from pprint import pprint
import argparse
import datetime
import os
import time
import logging
import sys

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

# create log with 'spam_application'
log = logging.getLogger()
log.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '{asctime} - {levelname} - {filename}:{funcName}[{lineno}] {message}',
    style="{")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the log
# log.addHandler(fh)
log.addHandler(ch)

log.info("Booted")

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
    {
        "zip_code": 'N/A',
        "state": "FR",
        "name": "Toulouse",
        "lon": 1.4442,
        "lat": 43.6047,
    },
]

os.chdir(os.path.dirname(__file__))

try:
    for city in cities:
        log.info(f"Pulling data for {city['name']}")
        if args.verbose > 0:
            print(f"Pulling: {city['name']}")
        w = weather.Influx(args, city['zip_code'], lat=city['lat'], lon=city['lon'], name=city['name'], state=city['state'])
        if args.onecall:
            log.info("Making One Call call")
            w.pull_onecall()
        else:
            log.info("Making Normal call")
            w.pull_weather()
        # pprint(w.data)
        w.save()
        log.info(f"Saved: {city['name']}")
except Exception as e:
    log.error(f"Errored out with {e}")
    sys.exit(-1)