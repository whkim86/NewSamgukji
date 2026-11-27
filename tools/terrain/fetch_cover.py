"""Sample real WorldCover 2021 COGs to a bounded categorical grid (nearest).
Modern, downsampled land cover; not historical geography or a 10m output.
"""
import json, pathlib, hashlib
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.enums import Resampling
ROOT=pathlib.Path(__file__).resolve().parents[2]
cache=ROOT/'cover-cache';cache.mkdir(exist_ok=True)
from urllib.request import urlretrieve
width,height=500,340
out=np.zeros((height,width),dtype=np.uint8);sources=[]
for west,east,cols in [(112,114,(0,400)),(114,114.5,(400,500))]:
 name=f'ESA_WorldCover_10m_2021_v200_N33E{111 if west==112 else 114}_Map.tif'
 url=f'https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/{name}'
 path=cache/name
 if not path.exists():
  temp=path.with_suffix('.part');urlretrieve(url,temp);temp.replace(path)
 with rasterio.open(path) as ds:
  assert ds.crs.to_epsg()==4326
  out[:,cols[0]:cols[1]]=ds.read(1,window=from_bounds(west,33.5,east,35.2,ds.transform),out_shape=(height,cols[1]-cols[0]),resampling=Resampling.nearest)
 sources.append({'url':url,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size})
assert np.isin(out,[10,20,30,40,50,60,70,80,90,95,100]).all()
data=dict(source='ESA WorldCover 2021',license='CC BY 4.0; https://creativecommons.org/licenses/by/4.0/',attribution='© ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium',citation='https://doi.org/10.5281/zenodo.7254221',bounds=[112,33.5,114.5,35.2],width=width,height=height,classes=out.ravel().tolist(),sampling='nearest at output cell centers, 0.005 degrees; not native 10m',sources=sources)
(ROOT/'public/data/henan-central-landcover.json').write_text(json.dumps(data,separators=(',',':'),ensure_ascii=False),encoding='utf-8')
print(json.dumps({'classes':dict(zip(*[x.tolist() for x in np.unique(out,return_counts=True)])),'sources':sources},indent=2))
