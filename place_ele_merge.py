import json
import time
import glob

path = './place_ele/'

features = []
for filename in glob.glob(path + '*.geojson'):
    print('reading ' + filename + '...')
    with open(filename) as f:
        features += json.load(f)['features']

print(len(features))

unique_features = list({f['id']: f for f in features}.values())

print(len(unique_features))

all_geojson = {
    'type': 'FeatureCollection',
    'features': unique_features
}

with open('place_ele.geojson', 'w') as f:
    json.dump(all_geojson, f)
