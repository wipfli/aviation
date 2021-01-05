# airspaces
Download airspaces and convert them to .mbtiles

## tippecanoe
```bash
git clone https://github.com/mapbox/tippecanoe.git
cd tippecanoe
make -j
```

## download data

```python
python download.py
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
