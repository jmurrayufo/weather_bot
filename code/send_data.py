#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import my_email
import os

# Cities to send data on
cities = ['80501', '04071', '01468']

# cd to this scripts directory

os.chdir(os.path.dirname(__file__))

s = sql.sql()

cursor = s.cursor()

cities = cursor.execute("SELECT city_id,name,zip_code FROM cities").fetchall()

# Book ends for date range to grab for each city
target_date = datetime.datetime.now()-datetime.timedelta(days=1)
t0 = target_date.replace(hour=0, second=0, minute=0, microsecond=0)
t1 = t0 + datetime.timedelta(hours=24)

message = f"Weather report for {target_date.date()} ({target_date.strftime('%A')})\n"
message += "  Max temperatures:\n"
# print(message)
for city in cities:
    weather = cursor.execute(f"SELECT temperature,dt FROM weather WHERE city_id = {city[0]} AND dt < {t1.timestamp()} AND dt > {t0.timestamp()} ORDER BY temperature DESC LIMIT 1").fetchone()
    if weather is None:
        message += f"    {city[2]}: No data found!\n"
        continue
    k = weather[0]
    c = k - 273.15
    f = (k - 273.15) * 9 / 5 + 32
    message += f"    {city[2]}: {f:5.1f} F  ({k:5.1f} K,  {c:5.1f} C)   \n"


e = my_email.email("/home/jmurray/.ssh/weather_bot.json")
e.send("jmurrayufo@gmail.com, dmurray@facilitysolutions.us", "Weatherbot: Max Temperatures", message)
# e.send("dmurray@facilitysolutions.us", "Weatherbot: Max Temperatures", message)
# e.send("jmurrayufo@gmail.com", "Weatherbot: Max Temperatures", message)
# print(message)
