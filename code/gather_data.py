#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import weather

cities = ['80501', '04071', '01468']

for idx, city in enumerate(cities):
    cities[idx] = weather.Weather(zip_code=city)

for city in cities:
    city.pull()
    #print(f"Pulling weather for {city}")
    time.sleep(1)

s = sql.sql()

s.db_setup()

for city in cities: 
    city.save(s)
