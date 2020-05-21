#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import weather
import os

cities = ['80501', '04071', '01468']

os.chdir(os.path.dirname(__file__))

for idx, city in enumerate(cities):
    cities[idx] = weather.Weather(zip_code=city)

s = sql.sql()

s.db_setup()

for city in cities:
    try:
        city.pull()
    except:
        continue
    city.save(s)
    time.sleep(1)

