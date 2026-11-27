// Bounded async cache: pending requests are deduplicated and never evicted mid-flight.
export class TileCache {
 constructor(limit=8){if(!Number.isInteger(limit)||limit<1)throw Error('invalid limit');this.limit=limit;this.entries=new Map()}
 get(key,load){if(this.entries.has(key)){const e=this.entries.get(key);this.entries.delete(key);this.entries.set(key,e);return e.promise}if(this.entries.size>=this.limit){const victim=[...this.entries].find(([,e])=>e.ready);if(!victim)return Promise.reject(Error('cache busy'));this.entries.delete(victim[0])}const e={ready:false};e.promise=Promise.resolve().then(load).then(v=>{e.ready=true;return v},err=>{if(this.entries.get(key)===e)this.entries.delete(key);throw err});this.entries.set(key,e);return e.promise}
}
export function tileSamples(a,n,x,z,step){if(a.length!==n*n||x<0||z<0||x+step>=n||z+step>=n)throw Error('tile bounds');const out=new Float32Array((step+1)**2);for(let j=0;j<=step;j++)out.set(a.subarray((z+j)*n+x,(z+j)*n+x+step+1),j*(step+1));return out}
