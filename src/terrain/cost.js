export const speeds=Object.freeze({road:36,general:30,plain:24,forest:18,mountain:12,wetland:6,cliff:0,deepRiver:0});
export function classify({slope,elevation,verifiedType}){if(!Number.isFinite(slope)||!Number.isFinite(elevation))throw Error('고도/경사 오류');if(slope>=.75)return 'cliff';if(verifiedType&&Object.hasOwn(speeds,verifiedType))return verifiedType;return slope>=.2||elevation>=650?'mountain':slope<.05&&elevation<200?'plain':'general'}
export function movementCost(km,type){if(!Number.isFinite(km)||km<0||!Object.hasOwn(speeds,type))throw Error('이동 비용 입력 오류');return speeds[type]?km/speeds[type]:Infinity}
export function terrainSlope(raw,p,x,z,dx,dz){return Math.hypot((raw(x+dx,z)-raw(x-dx,z))*p.scale/(2*dx),(raw(x,z+dz)-raw(x,z-dz))*p.scale/(2*dz))}

export function cellInfo(active,x,z){const elevation=active.raw(x,z),p=active.projection,slope=terrainSlope(active.raw,p,x,z,p.width/256,p.depth/256),type=classify({elevation,slope,verifiedType:active.coverType?.(x,z)});return {elevation,slope,type,passable:speeds[type]>0,speed:speeds[type],costPerKm:movementCost(1,type)}}
