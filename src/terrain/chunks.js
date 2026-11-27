export function chunkRanges(n,divisions=4){if((n-1)%divisions)throw Error('invalid chunk grid');const step=(n-1)/divisions;return Array.from({length:divisions**2},(_,i)=>({x:i%divisions*step,z:Math.floor(i/divisions)*step,step}));}
export function zoomLevel(m){return m>80000?1:m>15000?2:m>1500?3:m>100?4:5;}
