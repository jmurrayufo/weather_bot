
import datetime
import requests
import json
from pprint import pprint

class ECO_BEE:

    dt_fmt = "%Y-%m-%dT%H:%M:%S"
    api_base_url = "https://api.ecobee.com"
    influxDB_host = "http://192.168.4.3:8086"

    def __init__(self):
        pass
        self.data = {}


    @property
    def access_token(self):
        # load JSON
        with open("/home/jmurray/.ssh/eco_bee.json") as fp:
            data = json.load(fp)

        access_token_dt = datetime.datetime.strptime(
            data['access_token_dt'],
            self.dt_fmt,
            )

        if datetime.datetime.now() - access_token_dt > datetime.timedelta(minutes=55):
            url = "https://api.ecobee.com/token"
            
            params = {
                "grant_type": "refresh_token",
                "code":data['refresh_token'],
                "client_id":data['api_key'],
            }

            r = requests.post(url, params=params)

            data['refresh_token'] = r.json()['refresh_token']
            data['access_token_dt'] = datetime.datetime.now().strftime(self.dt_fmt)
            data['access_token'] = r.json()['access_token']
            with open("/home/jmurray/.ssh/eco_bee.json",'w') as fp:
                json.dump(data, fp, indent=2)

        return data['access_token']

    def thermostat(self):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "json":'{"selection":{"selectionType":"registered","selectionMatch":"","includeRuntime":"true","includeExtendedRuntime":"true"}}'
        }
        r = requests.get(
            self.api_base_url+"/1/thermostat",
            headers=headers,
            params=params,
            )
        self.data = r.json()
        return self.data


    def thermostat_summary(self):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "json":'{"selection":{"selectionType":"registered","selectionMatch":""}}'
        }
        r = requests.get(
            self.api_base_url+"/1/thermostatSummary",
            headers=headers,
            params=params,
            )
        return r.json()


    @staticmethod
    def f10_to_c(f):
        return round((f/10.0 - 32) * 5 / 9,3)


    def update(self):
        raw_data = self.thermostat()
        save_data = {}
        # pprint(raw_data)


        offsets = [10*60, 5*60, 0]

        name = raw_data['thermostatList'][0]['name']
        raw_data = raw_data['thermostatList'][0]['extendedRuntime']
        now = datetime.datetime.now()

        target_times = [
            now.replace(second=0, microsecond=0).replace(minute=(raw_data['runtimeInterval']*5-10)%60),
            now.replace(second=0, microsecond=0).replace(minute=(raw_data['runtimeInterval']*5-5)%60),
            now.replace(second=0, microsecond=0).replace(minute=(raw_data['runtimeInterval']*5)%60),
        ]

        for i in range(3):
            if target_times[i] > now:
                target_times[i] -= datetime.timedelta(hours=1)

        for i in range(3):

            save_data['cool1'] = raw_data['cool1'][i]/300.0
            save_data['humidity'] = raw_data['actualHumidity'][i]
            save_data['temperature'] = self.f10_to_c(raw_data['actualTemperature'][i])
            save_data['target_cool'] = self.f10_to_c(raw_data['desiredCool'][i])
            save_data['target_heat'] = self.f10_to_c(raw_data['desiredHeat'][i])
            save_data['fan'] = raw_data['fan'][i]/300.0

            data = []

            for element in save_data:
                data.append(f"{element}={save_data[element]}")
            ts = target_times[i]
            # print(ts)
            ts = str(int(ts.timestamp()))
            data = f"eco_bee,name={name} " + ",".join(data) + " " + ts
            # if self.args.verbose > 1:
            #     print(data)
            data += "\n"
            # print(data)

            host = self.influxDB_host + '/write'
            params = {"db":"weather","precision":"s"}
            try:
                r = requests.post( host, params=params, data=data, timeout=1)
                r.raise_for_status()
            except Exception as e:
                print("Error",e)