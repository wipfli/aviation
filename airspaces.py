import requests
import json

r = requests.get('https://www.openaipgeojson.com/getFile.php?fname=countries.json')

countries = json.loads(r.text)

for country in countries:
    print('download ' + country['name'] + '...')
    url = 'https://www.openaipgeojson.com/getFile.php?fname=' + country['name'] + '.geojson'
    r = requests.get(url)
    with open('airspaces/' + country['name'] + '.geojson', 'w') as f:
        f.write(r.text)
        
all_features = []
for country in countries:
    print('parse ' + country['name'] + '...')
    with open('airspaces/' + country['name'] + '.geojson') as f:
        data = json.load(f)
        all_features += data['features']
        
geojson = {'type': 'FeatureCollection', 'features': all_features}

print('write airspaces.geojson...')
with open('airspaces.geojson', 'w') as f:
    json.dump(geojson, f)
        