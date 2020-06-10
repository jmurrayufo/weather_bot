#!/usr/bin/env python

from pprint import pprint
import datetime
import sql
import time
import os

# cd to this scripts directory
os.chdir(os.path.dirname(__file__))

s = sql.sql(sql.sql.dict_factory)

cursor = s.cursor()

cities = cursor.execute("SELECT city_id,name,zip_code FROM cities").fetchall()
weather = cursor.execute("SELECT * FROM weather LEFT JOIN cities ON cities.city_id = weather.city_id ORDER BY dt ").fetchall()

data = []
for elm in weather:
    if elm['zip_code'] != '80501':
        continue
    data.append((elm['dt'],elm['temperature']-273.15))
# pprint(data)
x,y = tuple(zip(*data))

import matplotlib.pyplot as plt

plt.plot(x,y)
plt.show()