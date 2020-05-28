
import requests
import json
import sql
import time

class Weather:


    def __init__(self, zip_code, lat, lon, name, state):
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
    

    def pull(self):
        r = requests.get('https://api.openweathermap.org/data/2.5/weather', 
                         params={
                            'lat':self.lat, 
                            'lon':self.lon, 
                            'appid': self.key,}
                        )
        r.raise_for_status()
        self.data = r.json()
        return self


    @property
    def wind(self):
        # Return wind dict if it exists, or None load dict if empty
        if self.data is None:
            self.pull()
        if 'wind' in self.data and 'deg' in self.data['wind']:
            return self.data['wind']
        else:
            return {'speed': None, 'deg': None}


    @property
    def pressure(self):
        # Return pressure dict if it exists, or None load dict if empty
        if self.data is None:
            self.pull()
        ret_dict = {}
        ret_dict['pressure'] = self.data['main']['pressure']
        ret_dict['grnd_level'] = self.data['main']['grnd_level'] if ( 'grnd_level' in self.data['main'] ) else None
        return ret_dict


    @property
    def rain(self):
        # Return rain dict if it exists, or None load dict if empty
        if self.data is None:
            self.pull()
        ret_dict = {}
        if 'rain' in self.data and '1h' in self.data['rain']:
            ret_dict['1h'] = self.data['rain']['1h']
        else:
            ret_dict['1h'] = 0.0
        if 'rain' in self.data and '3h' in self.data['rain']:
            ret_dict['3h'] = self.data['rain']['3h']
        else:
            ret_dict['3h'] = 0.0
        return ret_dict


    @property
    def snow(self):
        # Return snow dict if it exists, or None load dict if empty
        if self.data is None:
            self.pull()
        ret_dict = {}
        if 'snow' in self.data and '1h' in self.data['snow']:
            ret_dict['1h'] = self.data['snow']['1h']
        else:
            ret_dict['1h'] = 0.0
        if 'snow' in self.data and '3h' in self.data['snow']:
            ret_dict['3h'] = self.data['snow']['3h']
        else:
            ret_dict['3h'] = 0.0
        return ret_dict



    @property
    def temperature(self):
        # Return a tuple of kelvin, ceclius and fahrenheit 
        if self.data is None:
            self.pull()
        k = self.data['current']['temp']
        c = k - 273.15
        f = (k - 273.15) * 9 / 5 + 32
        return (k, c, f)


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
        data = ""
        data += f"weather,zip_code={self.zip_code},lat={self.lat},lon={self.lon},name={self.name},state={self.state} "
        data += f"temperature={self.data['main']['temp']}"
        data += f",clouds={self.data['clouds']['all']}"
        data += f",feels_like={self.data['main']['feels_like']}"
        data += f",humidity={self.data['main']['humidity']}"
        data += f",pressure={self.data['main']['pressure']}"
        data += f",wind_deg={self.data['wind'].get('deg', 0)}"
        data += f",wind_speed={self.data['wind'].get('speed', 0)}"
        # data += f",dew_point={self.data['current']['dew_point']}"
        # data += f",uvi={self.data['current']['uvi']}"
        data += f",visibility={self.data['visibility']}"
        # data += f",wind_gust={self.data['current'].get('wind_gust', 0)}"

        try:
            data += f",rain_1h={self.data['rain']['1h']}"
        except KeyError:
            data += f",rain_1h=0"

        try:
            data += f",snow_1h={self.data['snow']['1h']}"
        except KeyError:
            data += f",snow_1h=0"

        data += "\n"

        host = self.influxDB_host + '/write'
        params = {"db":"weather","precision":"s"}
        try:
            r = requests.post( host, params=params, data=data, timeout=1)
        except Exception as e:
            print("Error",e)
            time.sleep(1)
