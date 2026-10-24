#!/usr/bin/env node
// G4C7 A4: OFFLINE-ONLY architectural circulation proof-of-concept.
// Four representative districts: ground room -> supported one-block stair run
// -> roof-cap landing via actually OPEN roof slit. Not 20 upper floors.
// No Minecraft, no computer-use, no old source/result/latch mutation.
'use strict';
const {buildA3,evaluateA3}=require('./g4c7_a3_hollow_access_lab.js');

const PILOTS=['A1','B1','C1','D1'];
function addPart(copy,role,x,y,z,w,h,d){
 if(w<=0||h<=0||d<=0)throw Error('Invalid circulation cuboid '+role);
 return {...copy,role:copy.role+'-'+role,x,y,z,w,h,d};
}
function buildA4(){
 const plan=buildA3();
 const flights=[];
 for(const building of PILOTS){
  const bFloor=plan.boxes.find(b=>b.id===building&&b.role.endsWith('-floor'));
  const roof=plan.boxes.find(b=>b.id===building&&b.role.endsWith('-bearing-roof'));
  if(!bFloor||!roof)throw Error('Missing hollow shell '+building);
  if(bFloor.y!==2||roof.y!==bFloor.y+roofOriginHeight(plan,building)-1)
   throw Error('Unexpected ground/roof topology '+building);
  const capY=roof.y, risers=capY-2;
  const sx=bFloor.x+8, sz=bFloor.z+1; // internal edge of unoccupied street-side shell
  if(risers<2||risers>10||sx+risers+2>=bFloor.x+bFloor.w)throw Error('Flight out of range '+building);
  const depth=3;
  if(bFloor.d<=depth+6)throw Error('Base too shallow');
  const roofNew=[
   addPart(roof,'cut-south-bearing',roof.x,capY,roof.z,roof.w,1,1),
   addPart(roof,'cut-north-bearing',roof.x,capY,roof.z+1+depth,roof.w,1,roof.d-1-depth),
   addPart(roof,'cut-west-bearing',roof.x,capY,roof.z+1,sx-roof.x,1,depth),
   addPart(roof,'cut-east-bearing',sx+risers,capY,roof.z+1,
     roof.x+roof.w-(sx+risers),1,depth)
  ];
  const idx=plan.boxes.indexOf(roof);
  plan.boxes.splice(idx,1,...roofNew);
  const steps=[];
  for(let i=0;i<risers;i++){
   const tread=addPart(bFloor,'A4-ascending-supported-tread-'+i,sx+i,3,sz,1,i+1,1);
   plan.boxes.push(tread);
   steps.push({index:i,tread:[sx+i,3+i,sz],feet:[sx+i,4+i,sz]});
  }
  flights.push({
   id:building,steps,stairLength:risers,
   fromRoom:[sx-1,3,sz],roofLanding:[sx+risers,capY+1,sz],
   roofHeight:capY,roofCutArea:risers*depth,
   headroomMin:2,routeGeometry:'supported one-block risers inside hollow podium; slab cut only on flight',
   notMinecraftStairs:'visual geometry is solid risers; angled Education stairs not yet integrated'
  });
 }
 plan.solidBoxes=plan.boxes.length;
 plan.label='G4C7_A4_FOUR_ROOF_LANDING_PILOTS_CONCEPT_ONLY';
 plan.upperPilots=flights;
 plan.notes.push('Four prototype supported rooftop access flights; entire 20-upper-floor network NOT addressed.');
 return plan;
}
function roofOriginHeight(plan,id){
 const b=plan.buildings.find(x=>x.id===id);
 if(!b)throw Error('No pilot building '+id);
 // Height of its A2 ground podium is architecturally unrelated to the
 // actual tower height. Return cap by original A3 hollow shell height.
 const f=plan.boxes.find(x=>x.id===id&&x.role.endsWith('-floor'));
 const r=plan.boxes.find(x=>x.id===id&&x.role.endsWith('-bearing-roof'));
 if(!f||!r)throw Error('Missing shell');
 return r.y-f.y+1;
}
function evaluateA4(plan=buildA4(),opts={}){
 const base=evaluateA3(plan,opts);
 const roads=plan.upperPilots.map(p=>{
  const flight=p.steps.map(s=>{
   const pos=s.feet;
   // evaluator must not infer upper walkability from bounding boxes alone.
   const ok=base.reachableAt ?base.reachableAt(pos):null;
   return {index:s.index,feet:pos,reachable:ok};
  });
  return {id:p.id,roofLanding:p.roofLanding,stairLength:p.stairLength,flight};
 });
 return {kind:'G4C7_A4_FOUR_ROOF_LANDING_OFFLINE_PROTOTYPE',
  base:base.verdict,pilots:roads,
  verdict:'TO_BE_MEASURED_WITH_EXPLICIT_CELL_WITNESSES',
  noHardware:true};
}
if(require.main===module){
 const plan=buildA4();
 console.log(JSON.stringify({label:plan.label,buildings:plan.buildingCount,
  flights:plan.upperPilots.map(x=>({id:x.id,steps:x.stairLength,roofLanding:x.roofLanding})),
  status:'GEOMETRY ONLY; NO PLAYER ROUTE APPROVAL'},null,2));
}
module.exports={buildA4,evaluateA4,PILOTS};
