import test from 'node:test';
import assert from 'node:assert/strict';
import {NetworkTiles} from '../src/core/network-tiles.js';
const tick=()=>new Promise(r=>setImmediate(r));
test('network tiles prioritize, deduplicate and bound resident data',async()=>{
 const calls=[],finish=new Map(),ready=[];
 const s=new NetworkTiles(id=>{calls.push(id);return new Promise(r=>finish.set(id,r))},id=>ready.push(id),{limit:2,concurrency:1});
 s.select([4,2,1]);s.select([4,2]);await tick();assert.deepEqual(calls,[4]);
 finish.get(4)(new Float32Array([4]));await tick();assert.deepEqual(calls,[4,2]);finish.get(2)(2);await tick();
 assert.deepEqual(ready,[4,2]);assert.equal(s.cache.size,2);s.select([9]);await tick();assert.equal(s.cache.size,0);finish.get(9)(9);await tick();assert.equal(s.cache.size,1);s.stop();assert.equal(s.cache.size,0);
});
test('camera jump aborts stale requests and late results cannot be applied',async()=>{
 const finish=new Map(),signals=new Map(),ready=[];
 const s=new NetworkTiles((id,signal)=>{signals.set(id,signal);return new Promise(r=>finish.set(id,r))},id=>ready.push(id),{concurrency:1});
 s.select([0]);await tick();s.select([1]);assert.equal(signals.get(0).aborted,true);finish.get(0)(0);await tick();finish.get(1)(1);await tick();assert.deepEqual(ready,[1]);assert.equal(s.stats().aborted,1);s.stop();
});
test('failed tile keeps fallback without retry storm and can retry after leaving',async()=>{
 let requests=0;const s=new NetworkTiles(async()=>{requests++;throw Error('404')},()=>{});
 s.select([0]);await tick();s.select([0]);await tick();assert.equal(requests,1);assert.equal(s.stats().failed,1);
 s.select([]);s.select([0]);await tick();assert.equal(requests,2);s.stop();
});
