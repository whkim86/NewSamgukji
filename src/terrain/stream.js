// Select nearby tiles, with a hard resident budget and retention hysteresis.
export function selectTiles(tiles,x,z,radius,previous=new Set(),limit=16){return tiles.map(t=>({id:t.id,d:Math.hypot(Math.max(0,Math.abs(x-t.x)-t.halfX),Math.max(0,Math.abs(z-t.z)-t.halfZ))})).filter(t=>t.d<=radius*(previous.has(t.id)?1.15:1)).sort((a,b)=>a.d-b.d||a.id-b.id).slice(0,limit).map(t=>t.id)}
