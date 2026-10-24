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
 // A2 architectural design: distinguish actual spatial organization, NOT
 // color, height or scale changes to one repeated building archetype.
 if(kind==='office'){
  if(index===0){ // twin vertical cores on a connected downtown plinth
   add('wide-mixed-podium',3,2,3,44,8,42,'concrete');
   add('west-vertical-core',7,10,8,15,targetH-10,29,'glass-and-frame');
   add('east-vertical-core',28,10,9,14,targetH-10,25,'glass');
   add('west-skyline-fin',7,targetH,8,13,2,12,'stone');
  }else if(index===1){ // one offset tower with an integrated broad middle ledge
   add('deep-transit-concourse',3,2,5,44,8,41,'concrete');
   add('setback-main-shaft',10,10,10,30,targetH-26,29,'glass-and-frame');
   add('recessed-upper-office',15,targetH-16,14,21,16,21,'glass');
   add('solid-inset-roof',16,targetH,15,18,2,18,'stone');
  }else if(index===2){ // pair of asymmetric bars and ground atrium
   add('gallery-retail-ground',4,2,4,43,8,42,'concrete');
   add('street-atrium-west',5,10,11,14,targetH-10,30,'glass');
   add('vertical-office-east',27,10,7,14,targetH-10,25,'glass-and-frame');
   add('atrium-sky-join',15,targetH,12,16,2,13,'stone');
  }else if(index===3){ // stepping terrace buildings, not a simple tower
   add('ground-transport-deck',3,2,4,44,8,42,'concrete');
   add('first-offset-terrace',5,10,6,38,targetH-29,36,'glass');
   add('upper-offset-terrace',12,targetH-19,12,24,19,25,'glass-and-frame');
   add('enclosed-top-lantern',17,targetH,15,13,2,17,'stone');
  }else if(index===4){ // deliberately low urban interchange
   add('long-bus-market-arcade',3,2,6,45,6,35,'concrete');
   add('station-glazed-spine',17,8,10,17,targetH-8,24,'glass');
  }else{ // porous municipal market
   add('market-footprint',5,2,4,40,6,42,'stone');
   add('covered-north-hall',7,8,6,33,targetH-8,15,'glass');
   add('covered-south-stalls',7,8,29,27,targetH-8,14,'concrete');
  }
 }else if(kind==='cultural'){
  if(index===0){ // deep civic auditorium: strong grounded shell, no thin crown
   add('theatre-foundation',3,2,4,43,6,41,'stone');
   add('sloped-grand-auditorium-volume',9,8,8,31,targetH-11,33,'concrete');
   add('acoustic-thick-roof',7,targetH-3,7,35,3,35,'stone');
  }else if(index===1){ // enclosed gallery wings around large atrium
   add('museum-entry-plaza',4,2,4,43,5,43,'stone');
   add('museum-west-gallery',6,7,7,13,targetH-9,35,'glass');
   add('museum-east-gallery',31,7,7,14,targetH-9,35,'glass');
   add('sculpture-bridge',11,targetH-2,11,27,2,13,'concrete');
  }else if(index===2){ // stepped solid exhibition pavilions
   add('sculpture-terrace',3,2,5,43,5,41,'stone');
   add('north-exhibition-block',5,7,7,38,targetH-10,16,'glass');
   add('south-sculpture-room',10,7,26,29,targetH-10,15,'concrete');
   add('clerestory-lightwell',13,targetH-3,10,16,3,12,'glass');
  }else if(index===3){ // long reading-hall and smaller lateral studio
   add('library-public-base',4,2,5,43,5,39,'stone');
   add('low-archive-spine',5,7,7,13,targetH-10,34,'concrete');
   add('long-reading-room',20,7,14,22,targetH-10,20,'glass');
   add('reading-room-lantern',22,targetH-3,16,18,3,15,'glass');
  }else{ // open-air small stepped event stage
   add('outdoor-stage-plinth',3,2,6,44,4,37,'stone');
   add('backstage-shell',5,6,8,15,targetH-6,32,'concrete');
   add('tiered-bleachers',24,6,15,18,4,24,'stone');
   add('open-pavilion-column',28,10,19,8,targetH-10,10,'glass');
  }
 }else if(kind==='residential'){
  if(index===0){ // U-courtyard open toward south
   add('courtyard-U-ground',3,2,3,44,4,44,'stone');
   add('courtyard-west-home',5,6,8,9,targetH-6,33,'glass');
   add('courtyard-east-home',35,6,8,9,targetH-6,33,'glass');
   add('courtyard-north-home',6,6,33,37,targetH-6,9,'glass');
  }else if(index===1){ // L-house terraces, not U
   add('L-neighborhood-base',3,2,3,44,4,44,'stone');
   add('north-L-residence',5,6,8,39,targetH-12,12,'glass');
   add('east-L-residence',31,6,14,13,targetH-12,27,'glass');
   add('sloped-terrace-mass',30,targetH-6,17,13,6,18,'stone');
  }else if(index===2){ // detached linear slabs with a garden street
   add('garden-street-base',4,2,4,42,4,42,'stone');
   add('north-flat-row',6,6,7,39,targetH-6,10,'glass');
   add('south-flat-row',6,6,30,38,targetH-6,10,'glass');
  }else if(index===3){ // 3-step terraced hill-style housing
   add('hillside-residence-ground',3,2,3,44,4,44,'stone');
   add('south-deep-terrace',5,6,6,38,8,38,'concrete');
   add('middle-terrace-home',9,14,10,31,8,29,'glass');
   add('upper-roof-garden',13,22,14,23,targetH-22,20,'stone');
  }else if(index===4){ // deliberately low greenhouse commons
   add('garden-cooperative-base',3,2,5,44,4,42,'stone');
   add('glass-greenhouse-pavilion',12,6,12,25,targetH-6,25,'glass');
  }else{ // split two small residential buildings & courtyard
   add('paired-homes-common-plaza',4,2,4,43,4,43,'stone');
   add('west-garden-apartments',6,6,9,15,targetH-6,33,'glass');
   add('east-garden-apartments',28,6,12,13,targetH-6,29,'glass');
   add('courtyard-community-hall',21,6,29,7,5,12,'concrete');
  }
 }else{
  if(index===0){ // broad horizontal research lab and one supported sky gallery
   add('research-ground-platform',3,2,3,44,6,44,'stone');
   add('south-biotech-laboratory',5,8,5,42,targetH-12,12,'glass');
   add('north-fabrication-laboratory',5,8,29,42,targetH-12,15,'glass');
   add('connected-gallery-west-spine',7,8,16,9,targetH-12,18,'concrete');
   add('supported-research-skybridge',9,targetH-4,16,31,4,15,'glass');
  }else if(index===1){ // single observatory tower with attached low lab
   add('observatory-solid-core-foundation',4,2,4,42,6,42,'stone');
   add('observatory-south-lab',6,8,8,31,12,19,'glass');
   add('grounded-observation-tower',17,8,16,15,targetH-8,16,'concrete');
   add('inset-dome-equivalent-volume',19,targetH,19,11,2,11,'glass');
  }else if(index===2){ // stacked three laboratory plates of decreasing size
   add('science-research-base',3,2,3,44,6,44,'stone');
   add('long-waveguide-facility',5,8,6,42,15,28,'glass');
   add('upper-instrument-floor',10,23,9,33,12,22,'concrete');
   add('raised-observation-well',17,35,13,18,targetH-35,16,'glass');
  }else if(index===3){ // one low clean room and transparent atrium
   add('cleanroom-foundation',3,2,3,44,6,44,'stone');
   add('cleanroom-deep-west-block',6,8,7,19,targetH-11,36,'concrete');
   add('large-glazed-science-atrium',26,8,12,16,targetH-11,28,'glass');
   add('research-sawtooth-lightwell',8,targetH-3,11,17,3,18,'glass');
  }else{ // asymmetrically split two labs with supported connecting gantry
   add('instrument-campus-ground',4,2,4,43,6,43,'stone');
   add('tall-analytical-research-lab',6,8,9,15,targetH-8,31,'glass');
   add('short-hardware-workshop',28,8,8,15,17,30,'concrete');
   add('workshop-observation-platform',29,25,10,13,3,23,'stone');
   add('joint-low-transition-bridge',19,8,20,11,7,13,'glass');
  }
 }
}
function civicCore(region){
 // Civic 48x48 core of the district: perimeter venues and open air middle.
 // Architectural placeholders, not entrances or player-walkable floors yet.
 const d=['A','B','C','D'].indexOf(region);
 const x=(d%2)*180+72,z=Math.floor(d/2)*180+72,id=region+'0';
 const add=(role,dx,y,dz,w,h,dep,material)=>
   part(id,role,x+dx,y,z+dz,w,h,dep,material);
 if(region==='A'){
   add('financial-public-square-floor',2,2,2,44,2,44,'stone');
   add('transit-hall-west-front',3,4,7,9,7,26,'concrete');
   add('transit-hall-east-front',36,4,7,9,7,26,'glass');
   add('pedestrian-east-gallery-roof',36,11,9,8,2,22,'stone');
 }else if(region==='B'){
   add('outdoor-cultural-court',2,2,2,44,2,44,'stone');
   add('main-open-stage',8,4,4,32,4,11,'concrete');
   add('rehearsal-backstage',10,8,5,28,5,9,'stone');
   add('tiered-civic-seats-west',3,4,22,12,3,18,'stone');
   add('tiered-civic-seats-east',33,4,22,12,3,18,'stone');
 }else if(region==='C'){
   add('community-park-base',2,2,2,44,2,44,'stone');
   add('park-greenhouse-west',4,4,8,11,8,27,'glass');
   add('park-woodland-terrace-east',33,4,8,11,4,27,'stone');
   add('small-garden-pavilion',33,8,15,10,5,14,'glass');
 }else{
   add('research-community-square',2,2,2,44,2,44,'stone');
   add('science-demo-west',4,4,8,13,9,32,'concrete');
   add('science-exhibit-east',31,4,10,13,9,25,'glass');
   add('grounded-community-gallery',5,13,13,11,3,20,'stone');
 }
}

function create(){
 boxes.length=0;buildings.length=0; // repeated evaluations must be pure and deterministic
 for(const region of ['A','B','C','D']){
  const p=programs[region];
  sites[region].forEach(([col,row],i)=>building(region,i,col,row,p.heights[i]));
  civicCore(region);
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
