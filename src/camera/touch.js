export function gesture(a,b){return {x:(a.x+b.x)/2,y:(a.y+b.y)/2,d:Math.hypot(b.x-a.x,b.y-a.y),angle:Math.atan2(b.y-a.y,b.x-a.x)}}
export function delta(a,b){return {x:b.x-a.x,y:b.y-a.y,zoom:a.d>0&&b.d>0?a.d/b.d:1,angle:Math.atan2(Math.sin(b.angle-a.angle),Math.cos(b.angle-a.angle))}}
