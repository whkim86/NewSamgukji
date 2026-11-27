import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import assert from 'node:assert/strict';
import {decode} from '../../src/terrain/dem-loader.js';
import {validateCover} from '../../src/geo/landcover.js';
import {validateLayer} from '../../src/geo/layers.js';
const root='public/assets/terrain/henan-central',hash=b=>createHash('sha256').update(b).digest('hex');
const report={dem:{},tiles:[],layers:{},sources:[]};
const metadata=JSON.parse(await readFile(`${root}/metadata.json`,'utf8'));
const manifest=JSON.parse(await readFile(`${root}/tiles.json`,'utf8'));
for(const n of [129,257,513]){
 const bytes=await readFile(`${root}/${n}.f32`),a=decode(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),n);
 let min=Infinity,max=-Infinity,sum=0;for(const v of a){min=Math.min(min,v);max=Math.max(max,v);sum+=v}
 assert.equal(min,metadata.stats[n].min);assert.equal(max,metadata.stats[n].max);
 report.dem[n]={bytes:bytes.length,sha256:hash(bytes),min,max,mean:sum/a.length};
 for(const tile of manifest.resolutions[n]){
  const b=await readFile(`${root}/${tile.path}`);assert.equal(hash(b),tile.sha256);assert.equal(b.length,tile.bytes);
  const values=decode(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),tile.size);
  for(let j=0;j<tile.size;j++)for(let i=0;i<tile.size;i++)assert.equal(values[j*tile.size+i],a[(tile.z+j)*n+tile.x+i]);
  report.tiles.push({resolution:n,id:tile.id,sha256:tile.sha256,exactSourceMatch:true});
 }
}
const cover=validateCover(JSON.parse(await readFile('public/data/henan-central-landcover.json','utf8'))),counts={};for(const code of cover.classes)counts[code]=(counts[code]??0)+1;
assert.deepEqual(cover.bounds,metadata.bounds);report.cover={source:cover.source,license:cover.license,width:cover.width,height:cover.height,classes:counts,sources:cover.sources};
for(const kind of ['river','road']){
 const bytes=await readFile(`public/data/henan-central-${kind}.json`),layer=JSON.parse(bytes);
 assert.equal(validateLayer(layer,metadata.bounds).length,layer.features.length);assert.ok(layer.features.length>0);
 report.layers[kind]={features:layer.features.length,sha256:hash(bytes),provenance:layer.provenance};
}
await mkdir('verification',{recursive:true});await writeFile('verification/data-audit.json',JSON.stringify(report,null,2));
console.log(`DEM 3/3, exact source tiles ${report.tiles.length}/48, cover ${cover.classes.length} cells, rivers/roads OK`);
