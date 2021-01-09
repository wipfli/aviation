# aviation
Download geospatial data of airspaces, powerlines, and aulav natural protected areas and bundle it into a .mbtile file.

## tippecanoe
```bash
git clone https://github.com/mapbox/tippecanoe.git
cd tippecanoe
make -j
```

## download airspaces

```bash
mkdir airspaces
python3 airspaces.py
```

## download powerlines

```bash
mkdir powerlines
pip3 install overpy
python3 powerlines.py
```

## download aulav

```bash
mkdir aulav
cd aulav

mkdir auen && cd auen
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_auen/data.zip
unzip data.zip && cd ..

mkdir jagdbanngebiete && cd jagdbanngebiete
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_jagdbanngebiete/data.zip 
unzip data.zip && cd ..

mkdir moorlandschaften && cd moorlandschaften
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_moorlandschaften/data.zip
unzip data.zip && cd ..

mkdir uebrige && cd uebrige
wget https://data.geo.admin.ch/ch.bafu.schutzgebiete-aulav_auen/data.zip
unzip data.zip && cd ..
```

```bash
pip3 install pyshp
python3 aulav.py
```

## convert .geojson to .mbtiles

The ```-z10``` gives a zoom level of 10 with a precision of 10 m. https://github.com/mapbox/tippecanoe#zoom-levels

```bash
./tippecanoe/tippecanoe -z10 -o airspaces.mbtiles *.geojson
```

The output file is roughly 100 MB large.

## inspect .mbtiles

```bash
sudo docker run -it -v $(pwd):/data -p 8080:80 klokantech/tileserver-gl airspaces.mbtiles
```
