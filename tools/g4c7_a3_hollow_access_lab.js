#!/usr/bin/env node
// G4-C7 A3: architectural ground-floor hollow shell & street access prototype.
// Geometric-only, deterministic, read-only, no MakeCode / Minecraft operations.
// DO NOT treat this as a build file or proof of in-game player collision.
'use strict';
const {create}=require('./g4c7_urban_layout_lab.js');
const W=372, H=78;
const ROAD=12, ROADSIDE_Y=2;
function occupancy(boxes){
 const solid=new Uint8Array(W*W*H);
 const idx=(x,y,z)=>(y*W+z)*W+x;
 for(const b of boxes){
  for(let y=b.y;y<b.y+b.h;y++)for(let z=b.z;z<b.z+b.d;z++){
   const base=idx(b.x,y,z);
   solid.fill(1,base,base+b.w);
  }
 }
 return {solid,idx};
}
function addBox(parts,template,suffix,x,y,z,w,h,d){
 if(w<=0||h<=0||d<=0)throw Error('Invalid A3 shell '+suffix);
 parts.push({...template,role:template.role+'-'+suffix,x,y,z,w,h,d});
}
function hollowMainPlinth(b){
 if(b.y!==2||b.w<12||b.d<12||b.h<4)throw Error('Unsupported base shell '+b.id);
 const pieces=[];
 const cap=b.y+b.h-1, inner=b.h-2;
 const dz=Math.floor(b.d/2),doorZ=b.z+dz-1,doorW=3;
 addBox(pieces,b,'floor',b.x,b.y,b.z,b.w,1,b.d);
 addBox(pieces,b,'bearing-roof',b.x,cap,b.z,b.w,1,b.d);
 addBox(pieces,b,'east-bearing-wall',b.x+b.w-1,b.y+1,b.z,1,inner,b.d);
 addBox(pieces,b,'south-bearing-wall',b.x+1,b.y+1,b.z,b.w-2,inner,1);
 addBox(pieces,b,'north-bearing-wall',b.x+1,b.y+1,b.z+b.d-1,b.w-2,inner,1);
 const left=doorZ-b.z, right=b.z+b.d-(doorZ+doorW);
 if(left<3||right<3)throw Error('Doorway too close to corner '+b.id);
 addBox(pieces,b,'entry-west-left',b.x,b.y+1,b.z,1,inner,left);
 addBox(pieces,b,'entry-west-right',b.x,b.y+1,doorZ+doorW,1,inner,right);
 // Keep two blocks of AIR over the interior floor. For a tall base a third
 // clearance block is useful; for h=4 roof begins at y+3, so use 2.
 if(inner>2)addBox(pieces,b,'entry-load-bearing-header',b.x,b.y+3,doorZ,1,inner-2,doorW);
 return {parts:pieces,entry:{
  building:b.id,outer:[b.x-1,2,doorZ+1],
  doorway:[b.x,b.y+1,doorZ+1],
  inside:[b.x+2,b.y+1,doorZ+1],
  footY:b.y+1,clearanceCells:2,doorWidth:doorW,
  sourceRole:b.role
 }};
}
function civicApproach(box,id){
 // Four actual ramps: road Y+1 -> level Y+2 step -> civic top Y+3.
 // Civic region B has stage in the south; enter from its north instead.
 const d=id[0],north=d==='B',x=box.x+Math.floor(box.w/2);
 const z=north?box.z+box.d:box.z-1;
 const approach={id,kind:'civic-grade-transition',role:'accessible-public-approach',
  x:x-2,y:2,z,w:5,h:1,d:1,material:'stone'};
 const portal={building:id,outer:[x,2,north?z+1:z-1],
  step:[x,3,z],inside:[x,4,north?box.z+box.d-1:box.z],
  entrySide:north?'north':'south',clearanceCells:2};
 return {approach,portal};
}
function buildA3(){
 const input=create();
 const bases=new Map();
 for(const b of input.buildings){
  const options=input.boxes.filter(p=>p.id===b.id&&p.y===2);
  if(options.length!==1)throw Error('Expected exactly 1 ground plinth '+b.id);
  bases.set(b.id,options[0]);
 }
 const pieces=[],doors=[],entries=[];
 for(const b of input.boxes){
  if(bases.get(b.id)===b){
   const shell=hollowMainPlinth(b);pieces.push(...shell.parts);
   doors.push(shell.entry);
  }else pieces.push(b);
 }
 for(const reg of ['A','B','C','D']){
  const box=pieces.find(p=>p.id===reg+'0'&&p.y===2);
  if(!box)throw Error('Missing civic '+reg);
  const {approach,portal}=civicApproach(box,reg+'0');
  pieces.push(approach);entries.push(portal);
 }
 const plan={...input,label:'G4C7_A3_HOLLOW_GROUND_CONCEPT_NOT_BUILT',
  boxes:pieces,solidBoxes:pieces.length,
  entrances:doors,civicConnections:entries,
  notes:[
   '22 plinths converted to actual floored hollow shells with 3-wide entrances',
   'Four civic squares gain grade transition into different public cores',
   'Ground-only simplified access model; upper-floor and real walking unverified',
   'No MakeCode construction, clone optimization timings or private data used'
  ]};
 return plan;
}
function safe(box){return box.x>=0&&box.z>=0&&box.y>=2&&box.x+box.w<=W&&box.z+box.d<=W&&box.y+box.h<=H}
function evaluateA3(plan=buildA3(),opts={}){
 if(plan.buildingCount!==22||plan.entrances.length!==22||plan.civicConnections.length!==4)throw Error('Unexpected A3 plan');
 if(plan.boxes.some(b=>!safe(b)))throw Error('Box out of city boundaries');
 for(const b of plan.boxes){
  for(let x=b.x;x<b.x+b.w;x++)for(let z=b.z;z<b.z+b.d;z++){
   if(x%60<ROAD||z%60<ROAD)throw Error('Street occupied by '+b.id+' '+b.role);
  }
 }
 const {solid,idx}=occupancy(plan.boxes);
 const block=(x,y,z)=>{
  if(x<0||z<0||y<0||x>=W||z>=W||y>=H)return 1;
  if(opts.blockDoor && x===opts.blockDoor[0]&&y===opts.blockDoor[1]&&z===opts.blockDoor[2])return 1;
  return solid[idx(x,y,z)];
 };
 // Y=1 is the previously established solid grade throughout the planned
 // street grid. This is a testing assumption, not a generated Minecraft floor.
 const isSolid=(x,y,z)=>y===1||block(x,y,z)===1;
 const stand=(x,y,z)=>y>=2&&y<H-1&&!block(x,y,z)&&!block(x,y+1,z)&&isSolid(x,y-1,z);
 const seen=new Uint8Array(solid.length),queue=new Int32Array(solid.length);
 let tail=0;
 function visit(x,y,z){
  if(x<0||z<0||x>=W||z>=W||!stand(x,y,z))return;
  const k=idx(x,y,z);
  if(!seen[k]){seen[k]=1;queue[tail++]=k;}
 }
 // Every street position is a valid starting point, but we do not invent
 // a 3D walk path through walls or skip head collisions.
 for(let z=0;z<W;z++)for(let x=0;x<W;x++){
  if(x%60<ROAD||z%60<ROAD)visit(x,ROADSIDE_Y,z);
 }
 for(let p=0;p<tail;p++){
  const n=queue[p],x=n%W,z=Math.floor(n/W)%W,y=Math.floor(n/(W*W));
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
   for(const dy of [0,1,-1]){
    const nx=x+dx,nz=z+dz,ny=y+dy;
    if(dy===1 && block(x,y+2,z))continue;
    if(dy===-1 && block(nx,y+1,nz))continue;
    visit(nx,ny,nz);
   }
  }
 }
 const reachable=pos=>pos&&!!seen[idx(pos[0],pos[1],pos[2])];
 const rooms=plan.entrances.map(e=>({
  building:e.building,doorFree:!block(...e.doorway)&&!block(e.doorway[0],e.doorway[1]+1,e.doorway[2]),
  outerRoadReachable:reachable(e.outer),
  innerRoomReachable:reachable(e.inside),
  insideFootSupported:stand(...e.inside)
 }));
 const commons=plan.civicConnections.map(e=>({
  id:e.building,entrySide:e.entrySide,
  stepReachable:reachable(e.step),mainSquareReachable:reachable(e.inside)
 }));
 const roomCount=rooms.filter(x=>x.innerRoomReachable&&x.doorFree&&x.insideFootSupported).length;
 const commonsCount=commons.filter(x=>x.stepReachable&&x.mainSquareReachable).length;
 return {kind:'OFFLINE_GROUND_LEVEL_ACCESS_ONLY_NO_MINECRAFT',
  buildingCount:plan.buildingCount,cityExtent:[W,W,H],
  groundRooms:{passed:roomCount,total:22,items:rooms},
  publicSquares:{passed:commonsCount,total:4,items:commons},
  visitedWalkCells:tail,approximateMovement:'2 AIR head, 1 block rise, four-direction; no Minecraft collision simulation',
  verdict:roomCount===22&&commonsCount===4?'GROUND_ONLY_OFFLINE_PASS':'GROUND_ACCESS_BLOCKED',
  notApproved:['upper floors','actual player walking','city aesthetics','speed','Minecraft construction']};
}
if(require.main===module){
 const report=evaluateA3();
 process.stdout.write(JSON.stringify(report,null,2)+'\n');
 if(report.verdict!=='GROUND_ONLY_OFFLINE_PASS')process.exitCode=2;
}
module.exports={buildA3,evaluateA3,hollowMainPlinth,civicApproach};
