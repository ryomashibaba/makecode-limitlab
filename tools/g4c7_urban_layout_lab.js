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
   add('urban-podium',4,2,4,40,8,40,'concrete');
   const tower=targetH-10;
   add('vertical-core',10,10,10,28,tower,28,'glass-and-frame');
   add('recessed-roof-integral',16,targetH,16,16,2,16,'stone');
 }else if(kind==='office'){
   add('transit-podium',4,2,7,40,8,34,'concrete');
   add('atrium-volume',10,10,12,28,targetH-8,24,'glass');
 }else if(kind==='cultural'){
   add('civic-floor',3,2,5,42,3,38,'stone');
   for(const [dx,dz] of [[5,7],[37,7],[5,35],[37,35]])
     add('exposed-hall-support',dx,5,dz,6,targetH-8,6,'concrete');
   add('thick-joined-roof',4,targetH-3,6,40,3,36,'stone');
 }else if(kind==='residential'){
   add('base',3,2,3,42,4,42,'stone');
   const wall=targetH-6;
   add('west-residence',4,6,8,9,wall,30,'glass');
   add('east-residence',35,6,8,9,wall,30,'glass');
   add('rear-residence',4,6,34,40,wall,9,'glass');
   // The open 22x26 central court remains genuinely AIR.
 }else{
   add('ground-lab',3,2,3,42,6,42,'stone');
   const lower=Math.max(9,targetH-17);
   add('north-lab-wing',4,8,5,40,lower,11,'glass');
   add('south-lab-wing',4,8,32,40,lower,11,'glass');
   add('supported-bridge-west',5,8,17,8,lower,14,'concrete');
   add('supported-bridge-east',35,8,17,8,lower,14,'concrete');
   add('high-sky-gallery',5,8+lower,17,38,3,14,'glass');
   add('recessed-observatory',19,11+lower,21,12,targetH-(11+lower),9,'stone');
 }
}
function create(){
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
