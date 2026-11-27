"""Reproduce original bilinear grids in memory; never modify published DEM."""
import pathlib,json,hashlib
import numpy as np,rasterio
from rasterio.merge import merge
from rasterio.warp import reproject,Resampling
from rasterio.transform import from_bounds
from contextlib import ExitStack
r=pathlib.Path(__file__).resolve().parents[2];folder=r/'public/assets/terrain/henan-central'
m=json.loads((folder/'metadata.json').read_text(encoding='utf-8'));w,s,e,north=m['bounds'];report={}
with ExitStack() as stack:
 sources=[stack.enter_context(rasterio.open(p)) for p in sorted((r/'dem-cache').glob('*.tif'))]
 assert len(sources)==9
 mosaic,transform=merge(sources,nodata=np.nan,dtype='float32')
for n in [129,257,513]:
 dx=(e-w)/(n-1);dy=(north-s)/(n-1);target=from_bounds(w-dx/2,s-dy/2,e+dx/2,north+dy/2,n,n)
 a=np.full((n,n),np.nan,dtype=np.float32)
 reproject(mosaic[0],a,src_transform=transform,src_crs='EPSG:4326',src_nodata=np.nan,dst_transform=target,dst_crs='EPSG:4326',dst_nodata=np.nan,resampling=Resampling.bilinear)
 old=np.fromfile(folder/f'{n}.f32',dtype='<f4').reshape(n,n);assert np.isfinite(a).all()
 report[n]={'maxAbsoluteDifferenceMetres':float(np.abs(a-old).max()),'meanAbsoluteDifferenceMetres':float(np.abs(a-old).mean())}
(r/'verification/dem-reproduction.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report,indent=2))
