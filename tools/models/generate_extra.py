import trimesh as t
from pathlib import Path
root=Path(__file__).resolve().parents[2]/'public/assets/models'
models={'tree':[((.5,4,.5),(0,2,0)),((3,3,3),(0,4,0))],'rock':[((2,1,1.5),(0,.5,0))],'house':[((6,3,5),(0,1.5,0)),((7,.5,6),(0,3.25,0))],'wall':[((8,5,2),(0,2.5,0))],'soldier':[((.5,.8,.3),(0,1.05,0)),((.25,.25,.25),(0,1.625,0)),((.35,.65,.3),(0,.325,0))],'officer':[((.6,.85,.35),(0,1.075,0)),((.3,.3,.3),(0,1.65,0)),((.4,.65,.3),(0,.325,0))],'horse':[((.7,.8,1.8),(0,1.15,0)),((.4,.7,.5),(0,1.65,.85))]+[((.15,.8,.15),(x,.4,z)) for x in [-.25,.25] for z in [-.65,.65]]}
for name,parts in models.items():
 s=t.Scene()
 for ext,pos in parts:
  m=t.creation.box(extents=ext);m.apply_translation(pos);s.add_geometry(m)
 (root/f'test-{name}.glb').write_bytes(s.export(file_type='glb'))
