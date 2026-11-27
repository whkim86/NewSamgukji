import {chromium} from 'playwright';
import {readFile} from 'node:fs/promises';
const browser=await chromium.launch({headless:false});
try{
 const page=await browser.newPage({viewport:{width:1920,height:1080}});
 await page.goto((process.env.GAME_URL||'http://127.0.0.1:4174/')+'?verify=1');
 await page.waitForFunction(()=>window.__samgukji?.snapshot().models?.loaded===8&&window.__samgukji.snapshot().tiles?.pending===0);
 await page.locator('#togglePanel').click();
 const region=JSON.parse(await readFile('public/data/regions.json','utf8')).regions[0];
 const river=JSON.parse(await readFile('public/data/henan-central-river.json','utf8')).features.find(f=>f.properties.name_en==='Yellow').geometry.coordinates;
 const cover=JSON.parse(await readFile('public/data/henan-central-landcover.json','utf8')),index=cover.classes.findIndex((v,i)=>v===10&&i>cover.width*100&&i<cover.width*250&&i%cover.width>60&&i%cover.width<200),[w,s,e,n]=cover.bounds;
 const views=[['city-luoyang',region.markers[0].slice(1),40],['yellow-river',river[Math.floor(river.length/2)],80],['actual-forest',[w+(index%cover.width+.5)/cover.width*(e-w),n-(Math.floor(index/cover.width)+.5)/cover.height*(n-s)],15]];
 for(const [name,geo,distance]of views){await page.evaluate(({geo,distance})=>{const[x,z]=window.__samgukji.world(...geo);window.__samgukji.view(x,z,distance)},{geo,distance});await page.waitForTimeout(1200);await page.screenshot({path:`verification/${name}.png`})}
 await page.evaluate(()=>window.__samgukji.focus('officer'));await page.waitForTimeout(600);await page.screenshot({path:'verification/officer-model.png'});
}finally{await browser.close()}
