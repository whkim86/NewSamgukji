import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
await mkdir('verification',{recursive:true});
const browser=await chromium.launch({headless:false,args:['--enable-webgl','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']});
const results=[],errors=[];let environment;
const counts=(process.env.BENCHMARK_COUNTS||'100,500,1000,5000').split(',');
if(counts.some(n=>!['100','500','1000','5000'].includes(n)))throw Error('unsupported benchmark count');
const output=process.env.BENCHMARK_OUTPUT||'benchmark-v3.json';
if(!/^[a-z0-9-]+\.json$/.test(output))throw Error('invalid output filename');
try{
 const page=await browser.newPage({viewport:{width:1920,height:1080}});
 page.on('pageerror',e=>errors.push(String(e)));
 const loading=Date.now();await page.goto((process.env.GAME_URL||'http://127.0.0.1:4174/')+'?verify=1');
 await page.waitForFunction(()=>window.__samgukji?.snapshot().models?.loaded===8&&window.__samgukji.snapshot().tiles?.pending===0);
 environment=await page.evaluate(()=>{const gl=document.querySelector('canvas').getContext('webgl2'),ext=gl.getExtension('WEBGL_debug_renderer_info');return{renderer:gl.getParameter(ext.UNMASKED_RENDERER_WEBGL),vendor:gl.getParameter(ext.UNMASKED_VENDOR_WEBGL),userAgent:navigator.userAgent,viewport:[innerWidth,innerHeight],devicePixelRatio}});environment.initialLoadMs=Date.now()-loading;
 for(const quality of ['LOW','MEDIUM','HIGH'])for(const count of counts){
  await page.selectOption('#quality',quality);await page.selectOption('#stress',count);
  await page.waitForFunction(n=>window.__samgukji.snapshot().models?.instances===Number(n)&&window.__samgukji.snapshot().models?.loaded===8,count);
  for(const moving of [false,true]){
   await page.evaluate(()=>window.__samgukji.view(0,0,2));await page.waitForTimeout(2000);
   const result=await page.evaluate(async moving=>{
    const samples=[],metrics=[],start=performance.now();let prev=start,second=-1;
    return new Promise(resolve=>{function frame(now){const elapsed=now-start;samples.push(now-prev);prev=now;
     if(moving){const angle=elapsed/20000*Math.PI*2;window.__samgukji.view(Math.sin(angle)*.7,(Math.cos(angle)-1)*.7,2)}
     if(Math.floor(elapsed/1000)!==second){second=Math.floor(elapsed/1000);metrics.push(window.__samgukji.snapshot())}
     if(elapsed<60000)requestAnimationFrame(frame);else{const sorted=samples.slice().sort((a,b)=>a-b);resolve({durationMs:elapsed,frames:samples.length,averageFps:1000*samples.length/elapsed,minFps:1000/sorted.at(-1),meanMs:elapsed/samples.length,p95Ms:sorted[Math.ceil(sorted.length*.95)-1],metrics})}}
     requestAnimationFrame(frame)})
   },moving);
   results.push({quality,count:Number(count),moving,...result});
   await writeFile(`verification/${output}`,JSON.stringify({environment,errors,results},null,2));
   console.log(`${results.length}/${counts.length*6} ${quality} ${count} ${moving?'moving':'static'}: ${result.averageFps.toFixed(1)} FPS, P95 ${result.p95Ms.toFixed(1)}ms`);
  }
 }
 await page.screenshot({path:'verification/benchmark-final.png'});
}finally{await browser.close();await writeFile(`verification/${output}`,JSON.stringify({environment,errors,results},null,2))}
if(errors.length)process.exitCode=1;
