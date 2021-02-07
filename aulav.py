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

def recursive_map_coordinates(obj):
    if isinstance(obj[0], list):
        return [recursive_map_coordinates(o) for o in obj]
    else:
        return LV95_to_lon_lat(obj)

categories = ['auen', 'jagdbanngebiete', 'moorlandschaften', 'uebrige']
features = []

for category in categories:
    with open('aulav/' + category + '-lv95.geojson') as f:
        data = json.load(f)
    for feature in data['features']:
        features += [{
            'type': 'Feature',
            'properties': feature['properties'],
            'geometry': {
                'type': feature['geometry']['type'],
                'coordinates': recursive_map_coordinates(feature['geometry']['coordinates'])
            }
        }]

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

with open('aulav-overlapping.geojson', 'w') as f:
    json.dump(geojson, f)
