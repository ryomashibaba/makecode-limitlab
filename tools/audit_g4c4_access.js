// Offline diagnostic only. This does not connect to Minecraft or touch run files.
// Reuse the frozen construction simulator without running its assertion suite.
const fs = require('fs'), path = require('path'), vm = require('vm');
const {createRequire} = require('module');
const {createHash} = require('crypto');
const source=fs.readFileSync(path.join(__dirname,'../makecode/limitlab_g4c4_a3.ts'),'utf8').replace(/\r\n?/g,'\n');
const sourceBlob=createHash('sha1').update('blob '+Buffer.byteLength(source)+'\0').update(source).digest('hex');
if(sourceBlob!=='417fc20aedec61deb99e70e0b8c6b70751314453')
 throw new Error('Diagnostic is pinned to the original G4C4 source; review the audit before changing its baseline');
const fixture = path.join(__dirname, '../tests/test_g4c4_a3.js');
const prefix = fs.readFileSync(fixture, 'utf8').split('let count=0;function test(')[0];
const context = {require:createRequire(fixture), __dirname:path.dirname(fixture), module:{exports:{}}};
vm.runInNewContext(prefix + '\nmodule.exports={simulate,M};', context);
const {simulate,M} = context.module.exports;
const t=simulate(); t.run();
const W=372,H=84,N=W*W*H,seen=new Uint8Array(N),queue=new Int32Array(N);
const index=(x,y,z)=>(y*W+z)*W+x;
const empty=(x,y,z)=>x>=0&&x<W&&z>=0&&z<W&&y>=0&&y<H&&t.get(x,y,z)===M.AIR;
const stand=(x,y,z)=>y>=2&&y<H-1&&empty(x,y,z)&&empty(x,y+1,z)&&!empty(x,y-1,z);
let tail=0;
function add(x,y,z){if(!stand(x,y,z))return;const n=index(x,y,z);if(!seen[n]){seen[n]=1;queue[tail++]=n;}}
// All street cells are seeds. Consequently an isolated exterior courtyard is
// never mistaken for an accessible room merely because it contains AIR.
for(let z=0;z<W;z++)for(let x=0;x<W;x++)
  if(x%60<12||z%60<12)add(x,2,z);
for(let head=0;head<tail;head++){
  const n=queue[head],x=n%W,z=Math.floor(n/W)%W,y=Math.floor(n/(W*W));
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]])for(const dy of [0,1,-1]){
    if(dy===1&&!empty(x,y+2,z))continue;
    if(dy===-1&&!empty(x+dx,y+1,z+dz))continue;
    add(x+dx,y+dy,z+dz);
  }
}
const specs=[['A1',0,104,25,48],['A2',0,44,145,38],['B1',1,44,24,46],['B2',1,164,144,38],
 ['C1',2,44,82,46],['C2',2,164,24,38],['D1',3,44,144,49],['D2',3,164,84,42]];
const wings=specs.map(([id,d,x,z,h])=>{
 x+=(d%2)*180;z+=Math.floor(d/2)*180;
 const floors=[14,28,...(h>=46?[40]:[])].map(slab=>{
   let standable=0,streetReachable=0;
   for(let zz=z+1;zz<z+27;zz++)for(let xx=x+1;xx<x+12;xx++){
     if(stand(xx,slab+1,zz)){standable++;if(seen[index(xx,slab+1,zz)])streetReachable++;}
   }
   return {slabY:slab,standable,streetReachable};
 });
 const cut={x:x+10,y:2,z:z+13};
 return {id,relativeOrigin:[x,z],height:h,cutAir:empty(cut.x,cut.y,cut.z),
   cutStreetReachable:!!seen[index(cut.x,cut.y,cut.z)],floors};
});
// Witness for the east leg of the finance crown. A continuous-looking crown
// must not be inferred merely from a non-AIR sample on its top.
const financeCrownWitness={x:118,z:26,legStartsY:69,
 airBelowLeg:[]};
for(let y=50;y<69;y++)if(empty(118,y,26))financeCrownWitness.airBelowLeg.push(y);
const researchCivicWitness={x:264,z:265,legStartsY:29,consecutiveAirBelowLeg:[]};
for(let y=28;y>=1&&empty(264,y,265);y--)researchCivicWitness.consecutiveAirBelowLeg.push(y);
const report={kind:'OFFLINE_VOXEL_DIAGNOSTIC_NOT_HARDWARE',
 movementModel:'2 AIR cells above solid support; four horizontal directions; at most one block ascent/descent with head clearance; no flight, teleport, ladders or Minecraft physics validation',
 sourceHead:'db410635108fce3805ddaac5b9392f111d3b216f',sourceBlob,stats:t.stats(),reachableCells:tail,wings,financeCrownWitness,researchCivicWitness,
 verdict:wings.every(w=>w.floors.every(f=>f.streetReachable>0))?'MODEL_ACCESSIBLE':'MODEL_UPPER_FLOORS_UNREACHABLE'};
process.stdout.write(JSON.stringify(report,null,2)+'\n');
// A successful diagnostic process is deliberately NOT a city quality PASS.
