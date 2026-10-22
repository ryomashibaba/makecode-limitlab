// Offline ONLY: stronger G4C5 route witnesses, not Minecraft real-player proof.
// Reads the exact frozen G4C5 A1 source through its existing voxel simulator.
'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const {createRequire}=require('module'),{createHash}=require('crypto');
const root=path.resolve(__dirname,'..');
const frozen='058fa73fe67c26c53902a4f76f6e15988606a1ad';
const input=fs.readFileSync(path.join(root,'makecode/limitlab_g4c5_a4a1.ts'),'utf8').replace(/\r\n?/g,'\n');
const blob=createHash('sha1').update('blob '+Buffer.byteLength(input)+'\0').update(input).digest('hex');
if(blob!==frozen)throw new Error('Refuse unpinned source: '+blob);
const fixture=path.join(root,'tests/test_g4c5_a4a1_access.js');
const prefix=fs.readFileSync(fixture,'utf8').split('let count=0;function test(')[0];
if(!prefix.includes('function simulate('))throw new Error('Cannot locate frozen simulator');
const context={require:createRequire(fixture),__dirname:path.dirname(fixture),module:{exports:{}}};
vm.runInNewContext(prefix+'\nmodule.exports={simulate,M};',context);
const {simulate,M}=context.module.exports;

const SPECS=[
 ['A1',0,104,25,48],['A2',0,44,145,38],
 ['B1',1,44,24,46],['B2',1,164,144,38],
 ['C1',2,44,82,46],['C2',2,164,24,38],
 ['D1',3,44,144,49],['D2',3,164,84,42]
];
function stairPath(){
 const a=[];
 for(let z=12;z>=4;z--)a.push([10,z]);
 for(let x=9;x>=2;x--)a.push([x,4]);
 for(let z=5;z<=18;z++)a.push([2,z]);
 for(let x=3;x<=10;x++)a.push([x,18]);
 if(a.length!==39)throw new Error('Unexpected stairs length '+a.length);
 return a;
}
const stairs=stairPath();
function analyze(options={}){
 const t=simulate();t.run();
 const W=372,H=84,N=W*W*H,seen=new Uint8Array(N),queue=new Int32Array(N);
 const index=(x,y,z)=>(y*W+z)*W+x;
 const get=(x,y,z)=>(options.removeTread && 
    x===options.removeTread[0]&&y===options.removeTread[1]&&z===options.removeTread[2])?
    M.AIR:t.get(x,y,z);
 const inBounds=(x,y,z)=>x>=0&&x<W&&z>=0&&z<W&&y>=0&&y<H;
 const empty=(x,y,z)=>inBounds(x,y,z)&&get(x,y,z)===M.AIR;
 const solid=(x,y,z)=>inBounds(x,y,z)&&get(x,y,z)!==M.AIR;
 const stand=(x,y,z)=>y>=2&&y<H-1&&empty(x,y,z)&&empty(x,y+1,z)&&solid(x,y-1,z);
 let tail=0;
 function add(x,y,z){if(!stand(x,y,z))return;const n=index(x,y,z);if(!seen[n]){seen[n]=1;queue[tail++]=n;}}
 for(let z=0;z<W;z++)for(let x=0;x<W;x++)if(x%60<12||z%60<12)add(x,2,z);
 for(let head=0;head<tail;head++){
  const n=queue[head],x=n%W,z=Math.floor(n/W)%W,y=Math.floor(n/(W*W));
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]])for(const dy of [0,1,-1]){
   if(dy===1&&!empty(x,y+2,z))continue;
   if(dy===-1&&!empty(x+dx,y+1,z+dz))continue;
   add(x+dx,y+dy,z+dz);
  }
 }
 const result=[];
 for(const [id,d,rx,rz,height] of SPECS){
  const x=rx+(d%2)*180,z=rz+Math.floor(d/2)*180;
  const room={at:[x+1,2,z+20],streetReachable:!!seen[index(x+1,2,z+20)]};
  const count=height>=46?39:27;
  const treads=[];
  for(let i=0;i<count;i++){
   const [sx,sz]=stairs[i],px=x+sx,pz=z+sz,blockY=i+2,feetY=i+3;
   const isSolid=solid(px,blockY,pz);
   const headroom=empty(px,feetY,pz)&&empty(px,feetY+1,pz);
   const reachable=headroom&&isSolid&&!!seen[index(px,feetY,pz)];
   treads.push({step:i+1,block:[px,blockY,pz],headroom,treadSolid:isSolid,roadReachable:reachable});
  }
  const floors=[];
  for(const slab of [14,28,...(height>=46?[40]:[])]){
   let reachable=0,standable=0;
   for(let zz=z+1;zz<z+27;zz++)for(let xx=x+1;xx<x+12;xx++){
    if(stand(xx,slab+1,zz)){standable++;if(seen[index(xx,slab+1,zz)])reachable++;}
   }
   floors.push({slab,standable,reachable});
  }
  result.push({id,district:d,height,relativeOrigin:[x,z],room,
   totalTreads:count,solidTreads:treads.filter(v=>v.treadSolid).length,
   fullHeadroomTreads:treads.filter(v=>v.headroom).length,
   roadReachableTreads:treads.filter(v=>v.roadReachable).length,
   firstBadTread:treads.find(v=>!v.roadReachable)||null,
   floors});
 }
 const roomCount=result.filter(w=>w.room.streetReachable).length;
 const floorsTotal=result.reduce((n,w)=>n+w.floors.length,0);
 const floorCount=result.reduce((n,w)=>n+w.floors.filter(f=>f.reachable>0).length,0);
 const stairTotal=result.reduce((n,w)=>n+w.totalTreads,0);
 const stairReach=result.reduce((n,w)=>n+w.roadReachableTreads,0);
 const final=roomCount===8&&floorsTotal===20&&floorCount===20&&stairTotal===264&&stairReach===stairTotal;
 return {
  kind:'OFFLINE_G4C5_DETAILED_STAIR_GRAPH_NOT_MINECRAFT_WALK',
  sourceBlob:blob,voxelStats:t.stats(),
  movementModel:'full 1-block riser / 2-block air headroom / 4-direction / +/-1 elevation; no player collision, jump physics, or aesthetic test',
  privateWorldUnmodified:true,
  streetReachableCells:tail,roomCount,floorCount,floorsTotal,stairTotal,stairReach,
  verdict:final?'OFFLINE_ALL_TREADS_AND_FLOORS_REACHABLE':'OFFLINE_ACCESS_ROUTE_DEFECT',
  wings:result
 };
}
if(require.main===module){
 const report=analyze();
 process.stdout.write(JSON.stringify(report,null,2)+'\n');
 if(report.verdict!=='OFFLINE_ALL_TREADS_AND_FLOORS_REACHABLE')process.exitCode=2;
}
module.exports={analyze,SPECS,stairPath};
