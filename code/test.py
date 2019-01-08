#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import weather


cities = [
    weather.Weather(zip_code='80501'),
    weather.Weather(zip_code='04071')
]

for city in cities:
    city.pull()
    time.sleep(2)

s = sql.sql()

s.db_setup()

for city in cities: 
    city.save(s)