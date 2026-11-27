"""Compare published grids against native DEM samples; never overwrite published data."""
import json, pathlib, argparse
import numpy as np
import rasterio
from rasterio.merge import merge
from contextlib import ExitStack
ROOT=pathlib.Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser();p.add_argument('--cache',default='dem-cache');p.add_argument('--output',default='dem-validation.json');args=p.parse_args()
 folder=ROOT/'public/assets/terrain/henan-central';m=json.loads((folder/'metadata.json').read_text(encoding='utf-8'));w,s,e,n=m['bounds'];region=json.loads((ROOT/'public/data/regions.json').read_text(encoding='utf-8'))['regions'][0];assert m['bounds']==region['bounds'] and m['source']==region['source']
 paths=sorted(pathlib.Path(args.cache).glob('*.tif'));assert len(paths)==9
 with ExitStack() as stack:
  sources=[stack.enter_context(rasterio.open(x)) for x in paths];assert all(x.crs.to_epsg()==4326 for x in sources);a,t=merge(sources,nodata=np.nan,dtype='float32')
 a=a[0];report={};grids={}
 for k in (129,257,513):
  g=np.fromfile(folder/f'{k}.f32',dtype='<f4').reshape(k,k);assert np.isfinite(g).all();grids[k]=g
  lon,lat=np.meshgrid(np.linspace(w,e,k),np.linspace(n,s,k));col,row=(~t)*(lon,lat);ref=a[np.floor(row).astype(int),np.floor(col).astype(int)];assert np.isfinite(ref).all();err=g-ref
  def stats(v):return dict(min=float(v.min()),max=float(v.max()),mean=float(v.mean()))
  def compare(v):return dict(mae=float(np.abs(v-ref).mean()),rmse=float(np.sqrt(np.mean((v-ref)**2))))
  markers=[]
  for name,x,y in region['markers']:
   i=round((n-y)/(n-s)*(k-1));j=round((x-w)/(e-w)*(k-1));markers.append(dict(name=name,grid=float(g[i,j]),native_at_grid=float(ref[i,j]),difference=float(err[i,j]),grid_lon=float(lon[i,j]),grid_lat=float(lat[i,j])))
  report[str(k)]=dict(grid=stats(g),native_at_grid=stats(ref),normal=compare(g),north_south_reversed=compare(g[::-1]),east_west_reversed=compare(g[:,::-1]),markers=markers)
 report['shared_nodes']={str(k):float(np.abs(grids[513][::512//(k-1),::512//(k-1)]-grids[k]).max()) for k in (129,257)}
 pathlib.Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
