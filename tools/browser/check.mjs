import { chromium } from 'playwright';
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
const out='verification'; await mkdir(out,{recursive:true});
const browser=await chromium.launch({args:['--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const results=[],errors=[],network=[];
const base=process.env.GAME_URL||'http://127.0.0.1:4173/';
async function check(name,fn){try{await fn();results.push({name,pass:true})}catch(e){results.push({name,pass:false,error:String(e)})}}
try{
for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1920,height:1080},hasTouch:mobile,isMobile:mobile});
 page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('requestfailed',r=>network.push({url:r.url(),error:r.failure()}));page.on('response',r=>{if(r.status()>=400)network.push({url:r.url(),status:r.status()})});
 await check(`${mobile?'mobile':'desktop'} renderer`,async()=>{await page.goto(base);await page.waitForFunction(()=>/^FPS [0-9]/.test(document.querySelector('#fps').textContent),{},{timeout:60000});assert.equal(await page.locator('#viewport canvas').count(),1);assert.ok(await page.locator('#viewport canvas').evaluate(c=>!!c.getContext('webgl2')));});
 if(mobile)await page.locator('#togglePanel').click();
 await check('actual DEM and GLB',async()=>{await page.waitForFunction(()=>document.querySelector('#modeLabel').textContent.includes('실제 DEM'),{},{timeout:30000});await page.waitForFunction(()=>document.querySelector('#modelStatus').textContent.includes('GLB 8/8'),{},{timeout:30000});});
 await check('quality and fallback',async()=>{for(const q of ['LOW','HIGH','MEDIUM']){await page.selectOption('#quality',q);await page.waitForTimeout(1000);assert.ok(await page.locator('#status').isHidden());}await page.selectOption('#mode','virtual');await page.waitForFunction(()=>document.querySelector('#modeLabel').textContent==='가상 지형');});
 await check('camera and layer interactions',async()=>{await page.selectOption('#mode','real');await page.waitForFunction(()=>document.querySelector('#modelStatus').textContent.includes('GLB 8/8'));const c=page.locator('#viewport canvas');const b=await c.boundingBox();const x=b.x+b.width*.75,y=b.y+b.height*.7;await page.mouse.move(x,y);await page.mouse.wheel(0,-400);await page.waitForTimeout(700);await page.mouse.down({button:'right'});await page.mouse.move(x+40,y+20,{steps:5});await page.mouse.up({button:'right'});for(const id of ['river','road','cost','measure']){await page.locator('#'+id).setChecked(true);assert.ok(await page.locator('#'+id).isChecked())}await page.mouse.click(x,y);await page.mouse.click(x+25,y+20);await page.locator('#clearMeasure').click();for(const mode of ['0','1','2'])await page.selectOption('#animation',mode);await page.locator('#reset').click();assert.ok(await page.locator('#status').isHidden());});
 await page.screenshot({path:`${out}/${mobile?'mobile':'desktop'}.png`});await page.close();
}
}finally{await browser.close();await writeFile(`${out}/browser.json`,JSON.stringify({renderer:'requested SwiftShader software',results,errors,network},null,2));}
if(results.some(r=>!r.pass)||errors.length||network.length)process.exitCode=1;
