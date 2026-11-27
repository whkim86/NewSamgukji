"""Convert locally supplied, licensed WGS84 GeoJSON lines; clip to test region."""
import argparse,json
from pathlib import Path
from shapely.geometry import shape,box,mapping
p=argparse.ArgumentParser();p.add_argument('input');p.add_argument('kind',choices=['river','road']);p.add_argument('--source',required=True);p.add_argument('--license',required=True);a=p.parse_args()
bounds=box(112,33.5,114.5,35.2);data=json.loads(Path(a.input).read_text(encoding='utf-8'));out=[]
for f in data['features']:
 g=shape(f['geometry']).intersection(bounds)
 for line in getattr(g,'geoms',[g]):
  if line.geom_type=='LineString' and not line.is_empty:out.append({'type':'Feature','geometry':mapping(line),'properties':f.get('properties',{})})
root=Path(__file__).resolve().parents[2];(root/'public/data'/f'henan-central-{a.kind}.json').write_text(json.dumps({'type':'FeatureCollection','features':out,'provenance':{'kind':'modern','source':a.source,'license':a.license}},ensure_ascii=False),encoding='utf-8')
