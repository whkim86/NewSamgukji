import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {decode} from '../../src/terrain/dem-loader.js';
import {tileSamples} from '../../src/core/tile-cache.js';
import {chunkRanges} from '../../src/terrain/chunks.js';
const root='public/assets/terrain/henan-central';
const manifest={version:1,source:'Copernicus GLO-90',resolutions:{}};
for(const n of [129,257,513]){
 const bytes=await readFile(`${root}/${n}.f32`),a=decode(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),n);
 await mkdir(`${root}/tiles/${n}`,{recursive:true});
 manifest.resolutions[n]=[];
 for(const [id,{x,z,step}] of chunkRanges(n).entries()){
  const values=tileSamples(a,n,x,z,step),buffer=Buffer.alloc(values.length*4);
  values.forEach((v,i)=>buffer.writeFloatLE(v,i*4));
  const path=`tiles/${n}/${id}.f32`;await writeFile(`${root}/${path}`,buffer);
  manifest.resolutions[n].push({id,x,z,step,size:step+1,path,bytes:buffer.length,sha256:createHash('sha256').update(buffer).digest('hex')});
 }
}
await writeFile(`${root}/tiles.json`,JSON.stringify(manifest,null,2));
console.log('48 detail tiles generated; original DEM unchanged');
