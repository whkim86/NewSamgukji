from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'src/terrain/terrain-mesh.js';s=p.read_text(encoding='utf-8')
s=s.replace('cp.setXYZ(k,pos.getX(idx)', 'cg.attributes.uv.setXY(k,(x+i)/(n-1),1-(z+j)/(n-1));cp.setXYZ(k,pos.getX(idx)')
s=s.replace(' const markers=[];', ''' let coverTexture=null,costTexture=null,coverVisible=true,costVisible=false;
 function refreshMap(){const map=costVisible?costTexture:coverVisible?coverTexture:null;for(const material of [mesh.material,background.material,...meshes.map(m=>m.material)]){if(material.map!==map){material.map=map;material.needsUpdate=true}}}
 function setCover(texture,visible=coverVisible){coverTexture=texture;coverVisible=visible;refreshMap()}
 function setCost(texture,visible=costVisible){if(costTexture&&texture!==costTexture)costTexture.dispose();costTexture=texture;costVisible=visible;refreshMap()}
 const markers=[];''')
s=s.replace('stream,releaseSource(){stream?.stop();','stream,setCover,setCost,get coverTexture(){return coverTexture},get costTexture(){return costTexture},releaseSource(){stream?.stop();coverTexture?.dispose();costTexture?.dispose();')
p.write_text(s,encoding='utf-8')
p=r/'src/terrain/overlays.js';s=p.read_text(encoding='utf-8').replace("import {applyCover}","import {applyCover,updateCostTexture}")
s=s.replace('group.add(layers.cost);return', 'group.add(layers.cost);layers.cost.visible=false;updateCostTexture(active,layers.cost);return')
s=s.replace('set(kind,value){layers[kind].visible=value}', 'set(kind,value){if(kind==="cost"){active.setCost(active.costTexture,value);return}if(kind==="cover")active.setCover(active.coverTexture,value);layers[kind].visible=value}')
p.write_text(s,encoding='utf-8')
p=r/'tools/browser/capture-views.mjs';s=p.read_text(encoding='utf-8').replace('index=cover.classes.findIndex(v=>v===10)', 'index=cover.classes.findIndex((v,i)=>v===10&&i>cover.width*100&&i<cover.width*250&&i%cover.width>60&&i%cover.width<200)');p.write_text(s,encoding='utf-8')
