"""Acquire Natural Earth public-domain modern vector data; no synthetic fallback."""
import subprocess,sys,tempfile
from pathlib import Path
from urllib.request import urlretrieve
import geopandas as gpd
root=Path(__file__).resolve().parents[2]
for kind,category,name in [('river','physical','ne_10m_rivers_lake_centerlines'),('road','cultural','ne_10m_roads')]:
 url=f'https://naturalearth.s3.amazonaws.com/10m_{category}/{name}.zip'
 with tempfile.TemporaryDirectory() as d:
  archive=Path(d)/'source.zip';urlretrieve(url,archive)
  frame=gpd.read_file(archive).to_crs(4326);frame=frame.cx[112:114.5,33.5:35.2];p=Path(d)/'source.json';frame.to_file(p,driver='GeoJSON')
  subprocess.run([sys.executable,str(root/'tools/terrain/prepare_layers.py'),str(p),kind,'--source',url,'--license','Natural Earth public domain; https://www.naturalearthdata.com/about/terms-of-use/'],check=True)
