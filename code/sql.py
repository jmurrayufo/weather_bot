
import sqlite3

class sql:

    __shared_state = {}
    
    def __init__(self):
        self.__dict__ = self.__shared_state
        if "inited" not in self.__shared_state:

            self.conn = sqlite3.connect('weather.db')
            self.inited = True


    def db_setup(self):

        cursor = self.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities 
            (   
                name TEXT,
                lat FLOAT,
                lon FLOAT,
                city_id INT UNIQUE
            )
            """)
        self.conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather 
            (   
                dt INT,
                city_id INT,
                temperature FLOAT,
                temperature_min FLOAT,
                temperature_max FLOAT,
                pressure FLOAT,
                ground_pressure FLOAT,
                humidity FLOAT,
                wind_speed FLOAT,
                wind_deg FLOAT,
                UNIQUE(dt, city_id),
                FOREIGN KEY(city_id) REFERENCES cities
            )
            """)
        self.conn.commit()


    def cursor(self):
        return self.conn.cursor()
