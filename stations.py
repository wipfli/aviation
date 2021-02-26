import requests
import pandas as pd
from io import StringIO
import json

r = requests.get('https://data.geo.admin.ch/ch.meteoschweiz.messnetz-automatisch/ch.meteoschweiz.messnetz-automatisch_de.csv')

df = pd.read_csv(StringIO(r.text), sep=';')

features = []
for i in range(299):
    if df.loc[i]['Stationstyp'] == 'Wetterstation':
        name = df.loc[i]['Station']
        wigos_id = df.loc[i]['WIGOS-ID']
        altitude = df.loc[i]['Stationshöhe m. ü. M.']
        latitude = df.loc[i]['Breitengrad']
        longitude = df.loc[i]['Längengrad']
        
        properties = {
            'name': str(name),
            'id': str(wigos_id),
            'altitude': str(altitude),
            'longitude': ('%.4f' % longitude),
            'latitude': ('%.4f' % latitude),
        }
        feature = {
            'type': 'Feature',
            'properties': properties,
            'geometry': {
                'type': 'Point',
                'coordinates': [float('%.4f' % longitude), float('%.4f' % latitude)]
            },
        }
        features += [feature]

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

with open('stations.geojson', 'w') as f:
    json.dump(geojson, f)
