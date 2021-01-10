#!/usr/bin/env python
# coding: utf-8

# In[4]:


import glob
import json


# In[111]:


get_ipython().system(' mkdir /scratch/wipfli/maps/airspaces_processed')


# In[114]:


path_in = '/scratch/wipfli/maps/airspaces/'
path_out = '/scratch/wipfli/maps/airspaces_processed/'
filenames = [path.split('/')[-1] for path in glob.glob(path_in + '*')]


# In[115]:


filenames


# In[ ]:





# In[214]:


remove = {
    'france_fr.geojson': [
        314327,
        314187,
        314360,
        314359,
        314362,
        314361,
        314364,
        314363,
        314333,
        314329,
        314331,
    ],
    'germany_de.geojson': [
        307563,
        307638,
        307639,
        307640,
    ]
}


# In[189]:


# ['original', 'new']
replacements = {
    'france_fr.geojson': [
        ['Bale10 119.35', 'Bale 10 TMA 130.9'],
        ['Bale1 119.35', 'Bale 1 TMA 130.9'],
        ['Bale2 119.35', 'Bale 2 TMA 130.9'],
        ['Bale3 119.35', 'Bale 3 TMA 130.9'],
        ['Bale4 119.35', 'Bale 4 TMA 130.9'],
        ['Bale5 119.35', 'Bale 5 TMA 130.9'],
        ['Bale5 119.35', 'Bale 5 TMA 130.9'],
        ['Bale6 119.35', 'Bale 6 TMA 130.9'],
        ['Bale7 119.35', 'Bale 7 TMA 130.9'],
        ['Bale8 119.35', 'Bale 8 TMA 130.9'],
        ['Bale9 119.35', 'Bale 9 TMA 130.9'],
        ['Bale AZ4T1 134.67', 'Bale T1 TMA HX 134.68'],
        ['Bale AZ4T2 134.67', 'Bale T2 TMA HX 134.68'],
        ['Bale AZ4T3 134.67', 'Bale T3 TMA HX 134.68'],
        ['CTR BALE', 'Bale CTR 118.3']
    ],
    'switzerland_ch.geojson': [
        ['ZURICH 10 TMA 118.1', 'ZURICH 10 TMA 124.7'],
        ['ZURICH 11 TMA 118.1', 'ZURICH 11 TMA 124.7'],
        ['ZURICH 12 TMA 118.1', 'ZURICH 12 TMA 124.7'],
        ['ZURICH 13 TMA 118.1', 'ZURICH 13 TMA 124.7'],
        ['ZURICH 14 TMA 118.1', 'ZURICH 14 TMA HX 127.755'],
        ['ZURICH 15 TMA 118.1', 'ZURICH 15 TMA HX 127.755'],
        ['ZURICH 1 TMA 118.1', 'ZURICH 1 TMA 124.7'],
        ['ZURICH 2 CTR 118.1', 'ZURICH 2 CTR HX 118.975'],
        ['ZURICH 2 TMA 118.1', 'ZURICH 2 TMA 124.7'],
        ['ZURICH 3 TMA 118.1', 'ZURICH 3 TMA 124.7'],
        ['ZURICH 4A TMA 118.1', 'ZURICH 4A TMA 124.7'],
        ['ZURICH 4B TMA 118.1', 'ZURICH 4B TMA 124.7'],
        ['ZURICH 4C TMA 118.1', 'ZURICH 4C TMA 124.7'],
        ['ZURICH 5 TMA 118.1', 'ZURICH 5 TMA 124.7'],
        ['ZURICH 6 TMA 118.1', 'ZURICH 6 TMA 124.7'],
        ['ZURICH 7 TMA 118.1', 'ZURICH 7 TMA 124.7'],
        ['ZURICH 8 TMA 118.1', 'ZURICH 8 TMA 124.7'],
        ['ZURICH 9 TMA 118.1', 'ZURICH 9 TMA 124.7'],

        ['BERN 1 TMA 121.025', 'BERN 1 TMA HX 127.325'],
        ['BERN 2 TMA 121.025', 'BERN 2 TMA HX 127.325'],
        ['BERN CTR 121.025', 'BERN CTR HX 121.025'],

        ['EMMEN 1 CTR 120.425', 'EMMEN 1 CTR HX 120.425'],
        ['EMMEN 1 TMA 120.425', 'EMMEN 1 TMA HX 134.130'],
        ['EMMEN 2 CTR 120.425', 'EMMEN 2 CTR HX 120.425'],
        ['EMMEN 2 TMA 120.425', 'EMMEN 2 TMA HX 134.130'],
        ['EMMEN 3 TMA 120.425', 'EMMEN 3 TMA HX 134.130'],
        ['EMMEN 4 TMA 120.425', 'EMMEN 4 TMA HX 134.130'],
        ['EMMEN 5 TMA 120.425', 'EMMEN 5 TMA HX 134.130'],
        ['EMMEN 6 TMA 120.425', 'EMMEN 6 TMA HX 134.130'],
    ]
}


# In[218]:


for filename in filenames:
    print(filename)
    
    with open(path_in + filename) as f:
        data = json.load(f)
            
    if filename in replacements:
        targets = [r[0] for r in replacements[filename]]
        
        for feature in data['features']:
            if feature['properties']['N'] in targets:
                print('replace ' + feature['properties']['N'] + '...')
                feature['properties']['N'] = next(x for x in replacements[filename] if x[0] == feature['properties']['N'])[1]
                
    if filename in remove:
        features_out = [f for f in data['features'] if int(f['properties']['ID']) not in remove[filename]]
    else:
        features_out = data['features']
    print('removed ' + str(len(data['features']) - len(features_out)) + ' features')
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features_out
    }
    print('write ' + filename + '...')
    with open(path_out + filename, 'w') as f:
        json.dump(geojson, f)


# In[219]:


all_features = []
for filename in filenames:
    print('read ' + filename + '...')
    with open(path_out + filename) as f:
        all_features += json.load(f)['features']
print('write airspaces.geojson...')
with open('/scratch/wipfli/maps/airspaces.geojson', 'w') as f:
    json.dump({
        'type': 'FeatureCollection',
        'features': all_features
    }, f)
print('done')


# In[ ]:




