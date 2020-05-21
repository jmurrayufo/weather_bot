
import sqlite3

class sql:

    __shared_state = {}
    
    def __init__(self, row_factory=None):
        self.__dict__ = self.__shared_state
        if "inited" not in self.__shared_state:

            self.conn = sqlite3.connect('weather.db')
            self.inited = True
            if row_factory:
                self.conn.row_factory = row_factory


    def db_setup(self):

        cursor = self.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities 
            (   
                name TEXT,
                zip_code TEXT UNIQUE,
                lat FLOAT,
                lon FLOAT,
                city_id INT
            )
            """)
        self.conn.commit()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather 
            (   
                dt INT,
                zip_code INT,
                temperature FLOAT,
                temperature_min FLOAT,
                temperature_max FLOAT,
                pressure FLOAT,
                ground_pressure FLOAT,
                humidity FLOAT,
                wind_speed FLOAT,
                wind_deg FLOAT,
                rain_1h FLOAT,
                rain_3h FLOAT,
                snow_1h FLOAT,
                snow_3h FLOAT,
                clouds FLOAT,
                UNIQUE(dt, zip_code),
                FOREIGN KEY(zip_code) REFERENCES cities
            )
            """)
        self.conn.commit()


    def cursor(self):
        return self.conn.cursor()


    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
