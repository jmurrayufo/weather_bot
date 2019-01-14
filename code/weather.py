
import requests
import json
import sql

class Weather:

    _key = None

    def __init__(self, zip_code=None, lat=None, lon=None, city=None):
        self.zip_code = zip_code
        self.lat = lat
        self.lon = lon
        self.city = city
        self.data = None

    @property
    def key(self):
        if Weather._key == None:
            with open("/home/jmurray/.ssh/weather_bot.json","r") as fp:
                data = json.load(fp)
            Weather._key = data['api_token']
        return Weather._key

    def __str__(self):
        return f"Weather<{self.zip_code}>"
    
    def pull(self):
        r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'zip':self.zip_code, 'appid': self.key})
        self.data = r.json()


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
                city_id,
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
                  self.data['id'],
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
    def clouds(self):
        # Return pressure dict if it exists, or None load dict if empty
        if self.data is None:
            self.pull()
        ret_dict = {}
        if 'clouds' in ret_dict:
            return self.data['clouds']['all']
        else:
            return 0

    @property
    def temperature(self):
        # Return a tuple of kelvin, ceclius and fahrenheit 
        if self.data is None:
            self.pull()
        k = self.data['main']['temp']
        c = k - 273.15
        f = (k - 273.15) * 9 / 5 + 32
        return (k, c, f)
