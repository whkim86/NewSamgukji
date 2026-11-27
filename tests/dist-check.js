import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
import {resolve} from 'node:path';
const html = readFileSync('dist/index.html','utf8');
const refs = [...html.matchAll(/(?:src|href)="([^\"]+\.(?:js|css))"/g)].map(m=>m[1]);
assert.ok(refs.some(x=>x.endsWith('.js')));
assert.ok(refs.some(x=>x.endsWith('.css')));
for(const ref of refs){assert.ok(ref.startsWith('./'),ref);assert.ok(existsSync(resolve('dist',ref)),ref);}
assert.ok(existsSync('dist/data/world_config.json'));
console.log('Static build paths and world config OK');
