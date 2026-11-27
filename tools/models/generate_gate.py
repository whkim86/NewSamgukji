# Original primitive model; meters, Y-up glTF.
import trimesh
from pathlib import Path
s=trimesh.Scene()
for name,ext,pos in [('left',(2,5,2),(-3,2.5,0)),('right',(2,5,2),(3,2.5,0)),('beam',(8,1,3),(0,5.5,0)),('roof',(9,.5,4),(0,6.25,0))]:
 m=trimesh.creation.box(extents=ext);m.apply_translation(pos);s.add_geometry(m,node_name=name)
p=Path(__file__).resolve().parents[2]/'public/assets/models/test-gate.glb';p.write_bytes(s.export(file_type='glb'))
