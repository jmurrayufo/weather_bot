#!/usr/bin/env python

import eco_bee
from pprint import pprint

e = eco_bee.ECO_BEE()

e.pull()
exit()


import requests

API_KEY = "TZRZoAwxdq6syrj35K4GTUwVg78oyZcI"
auth_code = "wmL1Xerhr0Ayc9MoQoKqoja5ouS6DVtj"

url = "https://api.ecobee.com/authorize"

params = {
    "response_type":"ecobeePin",
    "client_id": API_KEY,
    "scope":"smartWrite",
}

# r = requests.get(url, params=params)

# print(r)
# print(r.json())


url = "https://api.ecobee.com/token"


params = {
    "grant_type":"ecobeePin",
    "client_id": API_KEY,
    "code": auth_code,
}
r = requests.post(url, params=params)

print(r)
print(r.json())