// Camera-prioritized network detail tiles. Authoritative elevations remain separate.
export class NetworkTiles {
 constructor(load,ready,{limit=16,concurrency=3}={}){
  this.load=load;this.ready=ready;this.limit=limit;this.concurrency=concurrency;
  this.cache=new Map();this.pending=new Map();this.failed=new Set();this.wanted=[];this.closed=false;
  this.requests=0;this.aborted=0;
 }
 select(ids){
  if(this.closed)return;
  this.wanted=[...new Set(ids)].slice(0,this.limit);
  const wanted=new Set(this.wanted);
  for(const [id,job] of this.pending)if(!wanted.has(id)){job.controller.abort();this.aborted++}
  for(const id of this.cache.keys())if(!wanted.has(id))this.cache.delete(id);
  for(const id of this.failed)if(!wanted.has(id))this.failed.delete(id);
  this.pump();
 }
 pump(){
  if(this.closed)return;
  for(const id of this.wanted){
   if(this.pending.size>=this.concurrency)break;
   if(this.cache.has(id)||this.pending.has(id)||this.failed.has(id))continue;
   const controller=new AbortController(),job={controller};this.pending.set(id,job);this.requests++;
   Promise.resolve().then(()=>this.load(id,controller.signal)).then(data=>{
    if(!this.closed&&!controller.signal.aborted&&this.wanted.includes(id)){
     this.cache.set(id,data);this.ready(id,data);
    }
   }).catch(e=>{if(!controller.signal.aborted&&!this.closed)this.failed.add(id)}).finally(()=>{
    if(this.pending.get(id)===job)this.pending.delete(id);this.pump();
   });
  }
 }
 stats(){return {cached:this.cache.size,pending:this.pending.size,failed:this.failed.size,requests:this.requests,aborted:this.aborted,limit:this.limit}}
 stop(){this.closed=true;for(const job of this.pending.values())job.controller.abort();this.cache.clear();this.failed.clear();this.wanted=[]}
}
