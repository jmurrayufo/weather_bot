
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
            INSERT OR IGNORE INTO cities (name,lat,lon,city_id) VALUES (?,?,?,?)
        """
        values = (self.data['name'],
                  self.data['coord']['lat'],
                  self.data['coord']['lon'],
                  self.data['id'],
                  )
        cursor.execute(cmd, values)
        db.conn.commit()

        cmd = """
            INSERT OR IGNORE INTO weather (dt,city_id,temperature) VALUES (?,?,?)
        """
        values = (self.data['dt'],
                  self.data['id'],
                  self.data['main']['temp']
                  )
        cursor.execute(cmd, values)
        db.conn.commit()
