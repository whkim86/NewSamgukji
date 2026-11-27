import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
await mkdir('verification', {recursive:true});
const browser = await chromium.launch({headless:false,args:['--enable-webgl']});
try {
 const page = await browser.newPage({viewport:{width:1920,height:1080}});
 const errors=[]; page.on('pageerror',e=>errors.push(String(e)));
 await page.goto('http://127.0.0.1:4173/');
 await page.waitForTimeout(8000);
 const state=await page.evaluate(()=>{
  const gl=document.querySelector('canvas')?.getContext('webgl2');
  const ext=gl?.getExtension('WEBGL_debug_renderer_info');
  return {text:document.body.innerText,renderer:ext?gl.getParameter(ext.UNMASKED_RENDERER_WEBGL):null,vendor:ext?gl.getParameter(ext.UNMASKED_VENDOR_WEBGL):null};
 });
 await page.screenshot({path:'verification/gpu-probe.png'});
 await writeFile('verification/gpu-probe.json',JSON.stringify({state,errors},null,2));
 console.log(JSON.stringify({state,errors}));
} finally { await browser.close(); }
