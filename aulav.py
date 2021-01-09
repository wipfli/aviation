import shapefile
import glob
import json

# The functions CHtoWGSlng and CHtoWGSlat are taken from:
# https://github.com/ValentinMinder/Swisstopo-WGS84-LV03/blob/master/scripts/py/wgs84_ch1903.py
# Thanks Valentin Minder for providing them!

# Convert CH y/x to WGS long
def CHtoWGSlng(y, x):
    # Axiliary values (% Bern)
    y_aux = (y - 600000) / 1000000
    x_aux = (x - 200000) / 1000000
    lng = (2.6779094 + (4.728982 * y_aux) + \
            + (0.791484 * y_aux * x_aux) + \
            + (0.1306 * y_aux * pow(x_aux, 2))) + \
            - (0.0436 * pow(y_aux, 3))
    # Unit 10000" to 1" and convert seconds to degrees (dec)
    lng = (lng * 100) / 36
    return lng

# Convert CH y/x to WGS lat
def CHtoWGSlat(y, x):
    # Axiliary values (% Bern)
    y_aux = (y - 600000) / 1000000
    x_aux = (x - 200000) / 1000000
    lat = (16.9023892 + (3.238272 * x_aux)) + \
            - (0.270978 * pow(y_aux, 2)) + \
            - (0.002528 * pow(x_aux, 2)) + \
            - (0.0447 * pow(y_aux, 2) * x_aux) + \
            - (0.0140 * pow(x_aux, 3))
    # Unit 10000" to 1" and convert seconds to degrees (dec)
    lat = (lat * 100) / 36
    return lat

def LV95_to_lon_lat(point):
    return [
        CHtoWGSlng(point[0] - 2e6, point[1] - 1e6),
        CHtoWGSlat(point[0] - 2e6, point[1] - 1e6)
    ]

categories = ['auen', 'jagdbanngebiete', 'moorlandschaften', 'uebrige']
features = []

for category in categories:
    shp_path = glob.glob('aulav/' + category + '/*_LV95/*.shp')[0]
    dbf_path = glob.glob('aulav/' + category + '/*_LV95/*.dbf')[0]
    
    shp = open(shp_path, 'rb')
    dbf = open(dbf_path, 'rb')
    
    r = shapefile.Reader(shp=shp, dbf=dbf)
    
    for shape in r.shapes():
        coordinates = [LV95_to_lon_lat(point) for point in shape.points]
        
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [coordinates]
            },
            'properties': {}
        }
        
        features += [feature]
        
geojson = {
    'type': 'FeatureCollection',
    'features': features
}

with open('aulav.geojson', 'w') as f:
    json.dump(geojson, f)
