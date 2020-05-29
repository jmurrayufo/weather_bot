
import requests
import json
import sql
import time

class Weather:


    def __init__(self, args, zip_code, lat, lon, name, state):
        self.args = args
        self.zip_code = zip_code
        self.lat = lat
        self.lon = lon
        self.name = name
        self.state = state
        self.data = None


    def __str__(self):
        return f"Weather<{self.zip_code}>: {self.data}"


    @property
    def key(self):
        with open("/home/jmurray/.ssh/weather_bot.json","r") as fp:
            data = json.load(fp)
            return data['api_token']


    def pull_weather(self):
        r = requests.get('https://api.openweathermap.org/data/2.5/weather', 
                         params={
                            'lat':self.lat, 
                            'lon':self.lon, 
                            'appid': self.key,}
                        )
        r.raise_for_status()
        request_data = r.json()
        self.data = {}

        self.data['temperature'] = request_data['main']['temp']
        self.data['clouds'] = request_data['clouds']['all']
        self.data['feels_like'] = request_data['main']['feels_like']
        self.data['humidity'] = request_data['main']['humidity']
        self.data['pressure'] = request_data['main']['pressure']
        self.data['wind_deg'] = request_data['wind'].get('deg', 0)
        self.data['wind_speed'] = request_data['wind'].get('speed', 0)
        # data += f",dew_point={self.data['current']['dew_point']}"
        # data += f",uvi={self.data['current']['uvi']}"
        # data += f",wind_gust={self.data['current'].get('wind_gust', 0)}"

        if 'visibility' in request_data:
            self.data['visibility'] = request_data['visibility']

        if 'rain' in request_data and '1h' in request_data['rain']:
            self.data['rain_1h'] = request_data['rain']['1h']
        else:
            self.data['rain_1h'] = 0

        if 'snow' in request_data and '1h' in request_data['snow']:
            self.data['snow_1h'] = request_data['snow']['1h']
        else:
            self.data['snow_1h'] = 0

        return self


    def pull_onecall(self):
        r = requests.get('https://api.openweathermap.org/data/2.5/onecall', 
                         params={
                            'lat':self.lat, 
                            'lon':self.lon, 
                            'appid': self.key,}
                        )
        r.raise_for_status()
        request_data = r.json()
        self.data = {}

        self.data['temperature'] = request_data['current']['temp']
        self.data['clouds'] = request_data['current']['clouds']
        self.data['feels_like'] = request_data['current']['feels_like']
        self.data['humidity'] = request_data['current']['humidity']
        self.data['pressure'] = request_data['current']['pressure']
        self.data['wind_speed'] = request_data['current']['wind_speed']
        self.data['wind_deg'] = request_data['current']['wind_deg']
        self.data['dew_point'] = request_data['current']['dew_point']
        self.data['uvi'] = request_data['current']['uvi']
        self.data['wind_gust'] = request_data['current'].get('wind_gust', 0)

        if 'visibility' in request_data['current']:
            self.data['visibility'] = request_data['current']['visibility']

        if 'rain' in request_data['current'] and '1h' in request_data['current']['rain']:
            self.data['rain_1h'] = request_data['current']['rain']['1h']
        else:
            self.data['rain_1h'] = 0

        if 'snow' in request_data['current'] and '1h' in request_data['current']['snow']:
            self.data['snow_1h'] = request_data['current']['snow']['1h']
        else:
            self.data['snow_1h'] = 0

        return self


class SQL(Weather):

    def save(self, db):
        cursor = db.cursor()
        cmd = """
            INSERT OR IGNORE INTO cities (name,zip_code,lat,lon,city_id) VALUES (?,?,?,?,?)
        """
        values = (self.data['name'],
                  self.zip_code,
                  self.data['coord']['lat'],
                  self.data['coord']['lon'],
                  self.data['id'],
                  )
        cursor.execute(cmd, values)
        db.conn.commit()

        cmd = """
            INSERT OR IGNORE INTO weather 
            (
                dt,
                zip_code,
                temperature,
                temperature_min,
                temperature_max,
                pressure,
                ground_pressure,
                humidity,
                wind_speed,
                wind_deg,
                rain_1h,
                rain_3h,
                snow_1h,
                snow_3h,
                clouds
            ) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """
        values = (self.data['dt'],
                  self.zip_code,
                  self.data['main']['temp'],
                  self.data['main']['temp_min'],
                  self.data['main']['temp_max'],
                  self.pressure['pressure'],
                  self.pressure['grnd_level'],
                  self.data['main']['humidity'],
                  self.wind['speed'],
                  self.wind['deg'],
                  self.rain['1h'],
                  self.rain['3h'],
                  self.snow['1h'],
                  self.snow['3h'],
                  self.clouds
                  )
        cursor.execute(cmd, values)
        db.conn.commit()

class Influx(Weather):

    influxDB_host = "http://192.168.4.3:8086"

    def save(self):
        data = []

        for element in self.data:
            data.append(f"{element}={self.data[element]}")
        data = f"weather,zip_code={self.zip_code},lat={self.lat},lon={self.lon},name={self.name},state={self.state} " + ",".join(data)
        if self.args.verbose > 1:
            print(data)
        data += "\n"

        host = self.influxDB_host + '/write'
        params = {"db":"weather","precision":"s"}
        try:
            r = requests.post( host, params=params, data=data, timeout=1)
            r.raise_for_status()
        except Exception as e:
            print("Error",e)
            time.sleep(1)
