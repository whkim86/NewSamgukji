import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import {writeFile} from 'node:fs/promises';
const browser=await chromium.launch({headless:false,args:['--enable-webgl']});
const results=[];const base=process.env.GAME_URL||'http://127.0.0.1:4174/';
async function check(name,fn){try{await fn();results.push({name,pass:true})}catch(e){results.push({name,pass:false,error:String(e)})}}
try{
 await check('failed detail tile retains usable terrain without retry storm',async()=>{
  const p=await browser.newPage();let requests=0;
  await p.route('**/tiles/257/0.f32',async route=>{requests++;await route.fulfill({status:503,body:'expected test failure'})});
  await p.goto(base+'?verify=1');await p.waitForFunction(()=>window.__samgukji?.snapshot().tiles?.pending===0&&window.__samgukji.snapshot().tiles?.failed===1);
  await p.waitForTimeout(1500);assert.equal(requests,1);assert.equal(await p.locator('#status').isHidden(),true);assert.ok(await p.evaluate(()=>Number.isFinite(window.__samgukji.snapshot().raw)));await p.screenshot({path:'verification/expected-tile-failure.png'});await p.close();
 });
 await check('mobile two-finger pinch and rotation, no measurement after gesture',async()=>{
  const p=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});await p.goto(base+'?verify=1');await p.waitForFunction(()=>window.__samgukji?.snapshot().tiles?.pending===0);
  const c=await p.context().newCDPSession(p),before=await p.evaluate(()=>window.__samgukji.snapshot());
  await c.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:140,y:200,id:1},{x:240,y:200,id:2}]});
  await c.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:135,y:200,id:1},{x:245,y:200,id:2}]});
  await c.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:115,y:180,id:1},{x:265,y:220,id:2}]});
  await c.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await p.waitForTimeout(500);const after=await p.evaluate(()=>window.__samgukji.snapshot());
  const distance=s=>Math.hypot(...s.camera.map((v,i)=>v-s.target[i]));assert.ok(distance(after)<distance(before));assert.notDeepEqual(after.camera,before.camera);assert.equal(await p.locator('#measureInfo').textContent(),'거리 측정 대기');await p.screenshot({path:'verification/mobile-pinch.png'});await p.close();
 });
 await check('continuous wheel zoom reaches individual model scale and stays above terrain',async()=>{
  const p=await browser.newPage({viewport:{width:1920,height:1080}});await p.goto(base+'?verify=1');await p.waitForFunction(()=>window.__samgukji?.snapshot().models?.loaded===8);
  const b=await p.locator('#viewport canvas').boundingBox();await p.mouse.move(b.x+b.width*.7,b.y+b.height*.3);
  const before=await p.evaluate(()=>window.__samgukji.snapshot());
  await p.mouse.down();await p.mouse.move(b.x+b.width*.7+40,b.y+b.height*.3+20,{steps:8});await p.mouse.up();await p.waitForTimeout(300);assert.notDeepEqual((await p.evaluate(()=>window.__samgukji.snapshot())).target,before.target);
  for(let i=0;i<240;i++){await p.mouse.wheel(0,-120);await p.waitForTimeout(15)}await p.waitForTimeout(400);
  const after=await p.evaluate(()=>window.__samgukji.snapshot());const dist=s=>Math.hypot(...s.camera.map((v,i)=>v-s.target[i]));assert.ok(dist(after)<.1);assert.ok(after.camera[1]>=after.target[1]);assert.equal(await p.locator('#status').isHidden(),true);await p.close();
 });
}finally{await browser.close();await writeFile('verification/edge-cases.json',JSON.stringify({results},null,2))}
console.log(JSON.stringify(results));if(results.some(r=>!r.pass))process.exitCode=1;
