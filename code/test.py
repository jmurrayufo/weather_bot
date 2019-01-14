#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import weather
import my_email

# 
cities = ['80501', '04071', '01468']
for idx, city in enumerate(cities):
    cities[idx] = weather.Weather(zip_code=city)

for city in cities:
    city.pull()
    print(f"Pulling weather for {city}")
    # time.sleep(1)

s = sql.sql()

s.db_setup()

for city in cities: 
    city.save(s)

e = my_email.email("/home/jmurray/.ssh/weather_bot.json")

message = "Weather report:\n"
for city in cities:
    message += f"{city.zip_code}: {city.temperature[2]:5.1f} F  ({city.temperature[0]:5.1f} K,  {city.temperature[1]:5.1f} C)   \n"


e.send(("dmurray@facitilysolutions.us", "jmurrayufo@gmail.com"), "Weatherbot: Message format test", message)

print(message)
