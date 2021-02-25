# aviation
Download geospatial data of airspaces, powerlines, aulav natural protected areas, and place elevation and bundle it into a .mbtile file.

## requirements
```bash
pip3 install overpy
npm install -g mapshaper
# for converting .shp to .geojson with ogr2ogr install gdal:
sudo add-apt-repository ppa:ubuntugis/ppa
sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install libgdal-dev
```

## download and process airspaces

```bash
mkdir airspaces
python3 airspaces.py
mkdir airspaces_processed
python3 airspace_surgery.py
```

## download powerlines

```bash
mkdir powerlines
python3 powerlines.py
```

## download place elevation

```bash
mkdir place_ele
python3 place_ele.py
python3 place_ele_merge.py
```

## download aulav

```bash
mkdir aulav
cd aulav

mkdir auen && cd auen
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_auen/data.zip
unzip data.zip && cd ..
ogr2ogr -f GeoJSON auen-lv95.geojson auen/AuLaV_Auengebiete_LV95/AuLaVAuengebiete20171101.shp

mkdir jagdbanngebiete && cd jagdbanngebiete
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_jagdbanngebiete/data.zip 
unzip data.zip && cd ..
ogr2ogr -f GeoJSON jagdbanngebiete-lv95.geojson jagdbanngebiete/AuLaV_Jagdbanngebiete_LV95/AuLaVJagdbanngebiete20171101_1.shp

mkdir moorlandschaften && cd moorlandschaften
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_moorlandschaften/data.zip
unzip data.zip && cd ..
ogr2ogr -f GeoJSON moorlandschaften-lv95.geojson moorlandschaften/AuLaV_Moorlandschaften_LV95/AuLaVMoorlandschaften20171101.shp

mkdir uebrige && cd uebrige
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_uebrige/data.zip
unzip data.zip && cd ..
ogr2ogr -f GeoJSON uebrige-lv95.geojson uebrige/AuLaV_UebrigeSchutzgebiete_LV95/AuLaVUebrigeSchutzgebiete20171101.shp
```

```bash
python3 aulav.py
mapshaper -i aulav-overlapping.geojson -dissolve2 -o aulav.geojson geojson-type=FeatureCollection
```

## download weather stations (for Switzerland)

```bash
python3 stations.py
```

## convert .geojson to .mbtiles

```bash
git clone https://github.com/mapbox/tippecanoe.git
cd tippecanoe
make -j
```

The ```-z10``` gives a zoom level of 10 with a precision of 10 m. https://github.com/mapbox/tippecanoe#zoom-levels

```bash
tippecanoe/tippecanoe -Z9 -z10 -o aviation.mbtiles powerlines.geojson aulav.geojson airspaces.geojson place_ele.geojson stations.geojson
```

The output file is roughly 155 MB large.

## inspect .mbtiles

```bash
sudo docker run -it -v $(pwd):/data -p 8080:80 klokantech/tileserver-gl
```
