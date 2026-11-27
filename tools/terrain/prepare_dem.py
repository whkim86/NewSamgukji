"""Acquire GLO-90 tiles and generate north-to-south little-endian float32 grids."""
import json, math, urllib.request, pathlib, datetime, argparse
import numpy as np
import rasterio
from rasterio.merge import merge
from rasterio.warp import reproject, Resampling
from rasterio.transform import from_bounds
ROOT=pathlib.Path(__file__).resolve().parents[2]
BOUNDS=[112,33.5,114.5,35.2]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cache',default='dem-cache');parser.add_argument('--download-only',action='store_true');args=parser.parse_args()
    cache=pathlib.Path(args.cache);cache.mkdir(exist_ok=True);paths=[];urls=[]
    for lat in range(33,36):
        for lon in range(112,115):
            name=f'Copernicus_DSM_COG_30_N{lat:02}_00_E{lon:03}_00_DEM';url=f'https://copernicus-dem-90m.s3.eu-central-1.amazonaws.com/{name}/{name}.tif';p=cache/(name+'.tif')
            if not p.exists():
                tmp=p.with_suffix('.part');urllib.request.urlretrieve(url,tmp);tmp.replace(p)
            paths.append(p);urls.append(url)
    if args.download_only:return
    from contextlib import ExitStack
    with ExitStack() as stack:
        src=[stack.enter_context(rasterio.open(p)) for p in paths]
        assert all(x.crs.to_epsg()==4326 for x in src)
        mosaic,transform=merge(src,nodata=np.nan,dtype='float32')
    out=ROOT/'public/assets/terrain/henan-central';out.mkdir(parents=True,exist_ok=True);stats={}
    for n in [129,257,513]:
        w,s,e,north=BOUNDS;dx=(e-w)/(n-1);dy=(north-s)/(n-1);target=from_bounds(w-dx/2,s-dy/2,e+dx/2,north+dy/2,n,n)
        a=np.full((n,n),np.nan,dtype=np.float32);reproject(mosaic[0],a,src_transform=transform,src_crs='EPSG:4326',src_nodata=np.nan,dst_transform=target,dst_crs='EPSG:4326',dst_nodata=np.nan,resampling=Resampling.bilinear)
        if not np.isfinite(a).all():raise ValueError('Missing DEM samples; refusing publication')
        a.astype('<f4').tofile(out/f'{n}.f32');stats[str(n)]={'min':float(a.min()),'max':float(a.max()),'bytes':a.nbytes}
    (out/'metadata.json').write_text(json.dumps(dict(source='Copernicus GLO-90',bounds=BOUNDS,resolutions=[129,257,513],crs='EPSG:4326',vertical='EGM2008 metres',date=datetime.date.today().isoformat(),urls=urls,rawBytes=sum(p.stat().st_size for p in paths),stats=stats),indent=2))
if __name__=='__main__':main()
