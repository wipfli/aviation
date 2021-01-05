import requests
import json

r = requests.get('https://www.openaipgeojson.com/getFile.php?fname=countries.json')

countries = json.loads(r.text)

for country in countries:
    url = 'https://www.openaipgeojson.com/getFile.php?fname=' + country['name'] + '.geojson'
    r = requests.get(url)
    with open(country['name'] + '.geojson', 'w') as f:
        f.write(r.text)
        
