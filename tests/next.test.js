import {test} from 'node:test';import assert from 'node:assert/strict';import {chunkRanges,zoomLevel} from '../src/terrain/chunks.js';import {cellInfo} from '../src/terrain/cost.js';import {readFileSync} from 'node:fs';
test('chunk coverage and shared boundaries',()=>{for(const n of [129,257,513]){const a=chunkRanges(n);assert.equal(a.length,16);assert.equal(a.reduce((s,c)=>s+c.step**2,0),(n-1)**2);assert.equal(a[0].x+a[0].step,a[1].x)}});
test('zoom levels monotonic',()=>assert.deepEqual([90000,20000,2000,200,10].map(zoomLevel),[1,2,3,4,5]));
test('cell cost independent of visual height',()=>{const a={raw:()=>100,projection:{width:1200,depth:1000,scale:.005}};assert.equal(cellInfo(a,0,0).speed,24)});
test('GLB header and length',()=>{const b=readFileSync(new URL('../public/assets/models/test-gate.glb',import.meta.url));assert.equal(b.toString('ascii',0,4),'glTF');assert.equal(b.readUInt32LE(4),2);assert.equal(b.readUInt32LE(8),b.length)});
