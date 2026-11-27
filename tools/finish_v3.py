from pathlib import Path
r=Path(__file__).resolve().parents[1]
p=r/'src/terrain/overlays.js';s=p.read_text(encoding='utf-8');s="import {applyCover} from './cover-render.js';\n"+s
s=s.replace('const layers={};','const layers={};const coverGroup=new T.Group();layers.cover=coverGroup;group.add(coverGroup);')
s=s.replace('validateCover(d);active.coverType=(x,z)=>coverType(coverAt(d,...inverseProjection(active.bounds,active.projection,x,z)));output("cover",`${d.source} · 현대 토지피복`)', 'const count=applyCover(d,active,coverGroup,layers.cost);output("cover",`${d.source} · 현대 토지피복 · 숲 기호 ${count}개(절차적 배치)`);')
p.write_text(s,encoding='utf-8')
p=r/'src/main.js';s=p.read_text(encoding='utf-8').replace("['river','road','cost']","['river','road','cost','cover']");p.write_text(s,encoding='utf-8')
p=r/'index.html';s=p.read_text(encoding='utf-8').replace('<div id="cellInfo">','<label><input id="cover" type="checkbox" checked> 현대 토지피복 / 숲 기호</label><div id="cellInfo">');s=s.replace('v0.5.0-dev.2','v0.5.0-dev.3');s=s.replace('<div id="terrainInfo">','<small>현대 수계·도로: Natural Earth (public domain). 토지피복: © ESA WorldCover project 2021 / Contains modified Copernicus Sentinel data (2021) processed by ESA WorldCover consortium · CC BY 4.0. 삼국시대 지리 복원 아님.</small><div id="terrainInfo">');p.write_text(s,encoding='utf-8')
p=r/'src/core/models.js';s=p.read_text(encoding='utf-8');s=s.replace('return {group,update','return {group,stats(){return {loaded,failed,instances:count,visible:group.visible,renderedModels:group.visible?loaded+mixers.length+count:0,mixers:mixers.length,cache:cache.size,cacheLimit:8}},update');p.write_text(s,encoding='utf-8')
p=r/'package.json';import json;d=json.loads(p.read_text());d['version']='0.5.0-dev.3';d['scripts']['test:browser']='node tools/browser/check.mjs';d['scripts']['test:benchmark']='node tools/browser/benchmark.mjs';p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
p=r/'.gitignore';p.write_text(p.read_text()+'\n.tooling/\ndem-cache/\ncover-cache/\nverification/\n',encoding='utf-8')
