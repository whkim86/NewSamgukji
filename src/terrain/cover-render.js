import * as T from 'three';
import {validateCover,coverAt,coverType} from '../geo/landcover.js';
import {inverseProjection} from '../geo/coordinates.js';
import {classify,terrainSlope,speeds} from './cost.js';
const palette={10:0x245b31,20:0x78934a,30:0xa2b967,40:0xc5b168,50:0xa38c87,60:0xb6a68a,70:0xf0f2ed,80:0x387fa8,90:0x599b8c,95:0x467868,100:0xa9af77};
export function applyCover(d,active,group,cost){
 validateCover(d);const p=active.projection;
 active.coverType=(x,z)=>coverType(coverAt(d,...inverseProjection(active.bounds,p,x,z)));
 const pos=cost.geometry.attributes.position,colors=[];
 for(let i=0;i<pos.count;i++){const x=pos.getX(i),z=pos.getZ(i),type=classify({elevation:active.raw(x,z),slope:terrainSlope(active.raw,p,x,z,p.width/256,p.depth/256),verifiedType:active.coverType(x,z)}),c=new T.Color(speeds[type]===0?0xb83030:type==='wetland'?0x397bb9:type==='forest'?0x205c32:type==='mountain'?0xd69b35:0x46a95d);colors.push(c.r,c.g,c.b)}
 cost.geometry.setAttribute('color',new T.Float32BufferAttribute(colors,3));
 const canvas=document.createElement('canvas');canvas.width=d.width;canvas.height=d.height;
 const ctx=canvas.getContext('2d'),pixels=ctx.createImageData(d.width,d.height);
 d.classes.forEach((code,i)=>{const c=palette[code]??0x888888;pixels.data.set([c>>16,(c>>8)&255,c&255,255],i*4)});ctx.putImageData(pixels,0,0);
 const texture=new T.CanvasTexture(canvas);texture.colorSpace=T.SRGBColorSpace;texture.magFilter=T.NearestFilter;texture.minFilter=T.NearestFilter;
 const geometry=new T.PlaneGeometry(p.width,p.depth,128,128);geometry.rotateX(-Math.PI/2);const points=geometry.attributes.position;
 for(let i=0;i<points.count;i++)points.setY(i,active.height(points.getX(i),points.getZ(i))+p.scale*.05);
 group.add(new T.Mesh(geometry,new T.MeshBasicMaterial({map:texture,transparent:true,opacity:.65,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-1})));
 const cells=[];for(let row=0;row<d.height;row+=4)for(let col=0;col<d.width;col+=4)if(d.classes[row*d.width+col]===10&&cells.length<800){const[w,s,e,n]=d.bounds;cells.push(p.toWorld(w+(col+.5)/d.width*(e-w),n-(row+.5)/d.height*(n-s)))}
 const tree=new T.InstancedMesh(new T.ConeGeometry(1,3,5),new T.MeshStandardMaterial({color:0x2c683b}),cells.length),m=new T.Matrix4();
 for(const[i,[x,z]]of cells.entries()){m.makeScale(p.scale*12,p.scale*12,p.scale*12);m.setPosition(x,active.height(x,z)+p.scale*18,z);tree.setMatrixAt(i,m)}tree.castShadow=tree.receiveShadow=true;group.add(tree);
 return cells.length;
}
