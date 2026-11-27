from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'src/terrain/terrain-mesh.js';s=p.read_text(encoding='utf-8').replace('material.map=map;material.needsUpdate=true','material.map=map;material.vertexColors=!map;material.needsUpdate=true');p.write_text(s,encoding='utf-8')
p=r/'src/terrain/cover-render.js';s=p.read_text(encoding='utf-8').replace('===10&&cells.length<800','===10');s=s.replace(' const tree=new T.InstancedMesh', ' const count=Math.min(800,cells.length),chosen=Array.from({length:count},(_,i)=>cells[Math.floor(i*cells.length/count)]);cells.splice(0,cells.length,...chosen);\n const tree=new T.InstancedMesh');p.write_text(s,encoding='utf-8')
