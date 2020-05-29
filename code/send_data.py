#!/usr/bin/env python

from pprint import pprint
import datetime
import time
import my_email
import os
import requests

# Cities to send data on
cities = ['80501', '04071', '01468']

# Book ends for date range to grab for each city
target_date = datetime.datetime.now()-datetime.timedelta(days=1)
t0 = target_date.replace(hour=0, second=0, minute=0, microsecond=0)
t1 = t0 + datetime.timedelta(hours=24)

influxDB_host = "http://192.168.4.3:8086"

url = influxDB_host + "/query"

params = {
        "db":"weather",
        "q":f'SELECT min(temperature), max(temperature) FROM "weather" WHERE time > now() - 1d4h AND time < now() - 4h GROUP BY "name"',
        }

r = requests.post(url, params=params)

r.raise_for_status()

d = r.json()['results'][0]['series']

message = f"Weather report for {target_date.date()} ({target_date.strftime('%A')})\n"
message += "  Max temperatures:\n"
# print(message)
for result in d:
    city = result['tags']['name']
    k_min,k_max = result['values'][0][1:3]
    c_min = k_min - 273.15
    c_max = k_max - 273.15
    message += f"    {city:>10}: {c_min:5.1f} - {c_max:5.1f} C   \n"


#e = my_email.email("/home/jmurray/.ssh/mail.json")
#e.send("jmurrayufo@gmail.com, dmurray@facilitysolutions.us", "Weatherbot: Min/Max Temperatures", message)
#e.send("jmurrayufo@gmail.com", "Weatherbot: Min/Max Temperatures", message)

# e.send("dmurray@facilitysolutions.us", "Weatherbot: Max Temperatures", message)
# e.send("jmurrayufo@gmail.com", "Weatherbot: Max Temperatures", message)
print(message)
