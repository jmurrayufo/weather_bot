
from io import BytesIO
import csv
import gzip
import requests
import csv
import time
from pprint import pprint

class METAR:

    url = "https://www.aviationweather.gov/adds/dataserver_current/current/metars.cache.csv.gz"

    def __init__(self):
        pass



    def pull(self):

        r = requests.get(self.url)

        compressedFile = BytesIO()
        compressedFile.write(r.content)
        compressedFile.seek(0)

        decompressedFile = gzip.GzipFile(fileobj=compressedFile, mode='rb')

        data = str(decompressedFile.read()).split("\\n")

        print(data[5])

        c = csv.DictReader(data[5:])

        for i in c:
            if i['station_id'] in ['KLMO','KBJC','KDEN']:
                print()
                pprint(i)
