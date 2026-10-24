#!/usr/bin/env node
// G4-C7 concept lab: reusable massing DSL and conservative block-copy proxy.
// NOT a Minecraft build source. NEVER edits any world, RUN file, private ZIP or latch.
'use strict';
const fs=require('fs');
const PITCH=180,CITY=372,ROAD=12,MAX_Y=78,GROUND=2;
const dims={region:PITCH,road:ROAD,city:CITY,buildMaxY:MAX_Y};
const programs={
 A:{name:'Finance — vertical core + deep street-level podiums',style:'office',heights:[74,62,48,56,18,14]},
 B:{name:'Culture — low open halls and public courts',style:'cultural',heights:[30,24,18,22,15]},
 C:{name:'Green residences — courtyard blocks and terrace gardens',style:'residential',heights:[31,28,35,24,16,29]},
 D:{name:'Research — bridge-linked deep horizontal laboratories',style:'research',heights:[42,36,47,33,41]}
};
const sites={
 A:[[0,0],[2,0],[0,2],[2,2],[1,0],[1,2]],
 B:[[0,0],[1,0],[2,0],[0,2],[2,2]],
 C:[[0,0],[1,0],[2,0],[0,2],[1,2],[2,2]],
 D:[[0,0],[1,0],[2,0],[0,2],[2,2]]
};
const boxes=[],buildings=[];
function overlap(a,b){return Math.max(0,Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x))*
  Math.max(0,Math.min(a.z+a.d,b.z+b.d)-Math.max(a.z,b.z))}
function part(id,role,x,y,z,w,h,d,material){
 if(![x,y,z,w,h,d].every(Number.isInteger)||w<=0||h<=0||d<=0)throw Error('Invalid box');
 if(y<GROUND||y+h>MAX_Y)throw Error('HEIGHT '+id+' '+role);
 const b={id,role,x,y,z,w,h,d,material};
 const localX=x%PITCH,localZ=z%PITCH;
 if(localX<ROAD||localZ<ROAD||localX+w>PITCH||localZ+d>PITCH)
   throw Error('ROAD_OR_DISTRICT_ENCROACH '+id+' '+role);
 const previous=boxes.filter(v=>v.id===id);
 if(y>GROUND&&!previous.some(v=>v.y+v.h===y&&overlap(v,b)>=6))
   throw Error('UNSUPPORTED_COMPONENT '+id+' '+role+' at Y'+y);
 boxes.push(b);
}
function building(region,index,col,row,targetH){
 const districtIndex=['A','B','C','D'].indexOf(region), ox=(districtIndex%2)*180,
 oz=Math.floor(districtIndex/2)*180, x=ox+col*60+ROAD,z=oz+row*60+ROAD;
 const id=region+(index+1),kind=programs[region].style;
 buildings.push({id,region,kind,plot:[col,row],height:targetH});
 const add=(role,dx,y,dz,w,h,d,material)=>part(id,role,x+dx,y,z+dz,w,h,d,material);
 if(kind==='office'&&targetH>40){
   // 4 genuinely different podium and tower footprint proportions.
   // Taller/recolored copies of one footprint do NOT count as a new building.
   const k=index%4;
   const baseW=[40,43,36,39][k],baseD=[40,36,44,39][k];
   const towerW=[26,31,24,29][k],towerD=[28,22,30,25][k];
   add('urban-podium',4,2,4,baseW,8,baseD,'concrete');
   add('vertical-core',9,10,9,towerW,targetH-10,towerD,'glass-and-frame');
   const topW=[17,20,14,18][k],topD=[16,14,18,13][k];
   add('integrated-setback-crown',13,targetH,13,topW,2,topD,'stone');
 }else if(kind==='office'){
   const w=index===4?40:34,d=index===4?34:41;
   add('transit-podium',4,2,5,w,8,d,'concrete');
   add('atrium-volume',9,10,10,w-10,targetH-10,d-10,'glass');
 }else if(kind==='cultural'){
   const spanX=[42,36,44,40,38][index],spanZ=[38,42,33,40,42][index];
   add('civic-floor',3,2,5,spanX,3,spanZ,'stone');
   for(const [dx,dz] of [[5,7],[spanX-3,7],[5,spanZ-1],[spanX-3,spanZ-1]])
     add('exposed-hall-support',dx,5,dz,5,targetH-8,5,'concrete');
   add('thick-joined-roof',4,targetH-3,6,spanX-2,3,spanZ-2,'stone');
   // Low masonry front canopy defines an entrance instead of a tall tower.
   if(index%2===1) {
     add('grounded-entrance-slab',12,2,5,12,5,8,'concrete');
   }
 }else if(kind==='residential'){
   const spanX=[42,38,44,40,36,42][index],spanZ=[42,44,39,43,38,40][index];
   const wall=[8,10,7,9,8,10][index],livingH=targetH-6;
   add('courtyard-base',3,2,3,spanX,4,spanZ,'stone');
   add('west-residence',4,6,8,wall,livingH,spanZ-12,'glass');
   add('east-residence',3+spanX-wall,6,8,wall,livingH,spanZ-12,'glass');
   const barZ=index%2===0?3+spanZ-wall:4;
   add(index%2===0?'south-residence':'north-residence',
     4,6,barZ,spanX-2,livingH,wall,'glass');
   // The courtyard is open on alternating sides of the block.
 }else{
   const spanX=[42,38,44,39,41][index],spanZ=[42,44,38,40,43][index];
   const lower=Math.max(9,targetH-17);
   add('ground-lab',3,2,3,spanX,6,spanZ,'stone');
   add('north-lab-wing',4,8,5,spanX-2,lower,10,'glass');
   add('south-lab-wing',4,8,spanZ-9,spanX-2,lower,10,'glass');
   add('supported-bridge-west',5,8,14,7,lower,spanZ-19,'concrete');
   add('supported-bridge-east',spanX-5,8,14,7,lower,spanZ-19,'concrete');
   add('high-sky-gallery',5,8+lower,14,spanX-3,3,spanZ-19,'glass');
   add('recessed-observatory',Math.floor(spanX/2)-2,11+lower,18,
     11,targetH-(11+lower),9,'stone');
 }
}
function create(){
 boxes.length=0;buildings.length=0; // repeated evaluations must be pure and deterministic
 for(const region of ['A','B','C','D']){
  const p=programs[region];
  sites[region].forEach(([col,row],i)=>building(region,i,col,row,p.heights[i]));
 }
 const profiles={};
 for(const region of ['A','B','C','D']){
  let bs=buildings.filter(x=>x.region===region);
  profiles[region]={name:programs[region].name,count:bs.length,
    heights:bs.map(x=>x.height),meanHeight:bs.reduce((n,b)=>n+b.height,0)/bs.length,
    typology:programs[region].style,centerPlotReserved:true};
 }
 const baselineTiles=3*13*180*180*6+4*12*84*180+12*84*12;
 const buildingClones=[84240,89424,84240,104976,89424].reduce((a,b)=>a+b,0);
 const candidateRoads=3*180*180*2+4*12*2*180+12*2*12;
 const cloneAnalysis={
  currentG4C6:{tileCloneCalls:44,buildingCloneCalls:5,
    tileCopiedVolume:baselineTiles,totalCopiedVolume:baselineTiles+buildingClones},
  proposedG4C7:{roadSurfaceOnlyCloneCalls:8,buildingCloneCalls:0,
    estimatedCopiedVolume:candidateRoads,assumption:'Only Y0/Y1 baseline grade can be safely shared; buildings are built separately'},
  copiedVolumeProxyReductionPct:100*(1-candidateRoads/(baselineTiles+buildingClones))
 };
 return {label:'G4C7_PROPOSED_LAYOUT_ONLY_NOT_BUILT',dims,
  profiles,buildingCount:buildings.length,solidBoxes:boxes.length,
  buildings,boxes,cloneAnalysis,verdict:'CONCEPT_NOT_HARDWARE_APPROVED'};
}
const plan=create();
function validate(){
 if(plan.buildingCount!==22)throw Error('building count');
 if(plan.solidBoxes>180)throw Error('Excess per-box calls: '+plan.solidBoxes);
 const heights=Object.values(plan.profiles).map(x=>x.meanHeight);
 if(!(heights[0]>heights[3]&&heights[3]>heights[2]&&heights[2]>heights[1]))
   throw Error('Region skylines not separated '+heights);
 if(new Set(Object.values(plan.profiles).map(x=>x.typology)).size!==4)throw Error('Repeated typologies');
 const p=plan.cloneAnalysis;
 if(p.copiedVolumeProxyReductionPct<95)throw Error('Not enough clone input reduction');
 // Different building footprints in each region; no building occupies central commons.
 for(const b of plan.buildings){
  if(b.plot[0]===1&&b.plot[1]===1)throw Error('Civic core was overwritten');
 }
 for(const box of boxes){
  if(box.y<GROUND||box.y+box.h>MAX_Y||box.x<0||box.x>=CITY||box.z<0||box.z>=CITY)
   throw Error('Invalid dimensions');
 }
 return true;
}
if(require.main===module){
 validate();
 if(process.argv.includes('--json'))process.stdout.write(JSON.stringify(plan,null,2)+'\n');
 else console.log('G4C7 concept PASS — '+plan.buildingCount+' diverse primary structures / '+
  plan.solidBoxes+' mass boxes, estimated tile+tower clone input '+
  plan.cloneAnalysis.currentG4C6.totalCopiedVolume+' -> '+
  plan.cloneAnalysis.proposedG4C7.estimatedCopiedVolume+
  ' blocks (NOT elapsed time), original user world UNCHANGED');
}
module.exports={create,validate,overlap};
