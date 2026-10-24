'use strict';
const assert=require('assert');
const {create,validate,overlap}=require('../tools/g4c7_urban_layout_lab.js');
assert.equal(validate(),true);
const p=create();
assert.equal(p.label,'G4C7_PROPOSED_LAYOUT_ONLY_NOT_BUILT');
assert.equal(p.verdict,'CONCEPT_NOT_HARDWARE_APPROVED');
assert.equal(p.buildingCount,22,'Diverse district design should not copy 32 generic towers');
assert(p.solidBoxes<=180,'Too many individual Fill candidates for proposed architecture');
assert.deepEqual(Object.fromEntries(Object.entries(p.profiles).map(([k,v])=>[k,v.count])),
 {A:6,B:5,C:6,D:5});
const averages=Object.values(p.profiles).map(x=>x.meanHeight);
assert(averages[0]>averages[3]&&averages[3]>averages[2]&&averages[2]>averages[1]);
assert.equal(new Set(Object.values(p.profiles).map(x=>x.typology)).size,4);
const x=p.cloneAnalysis;
assert.equal(x.currentG4C6.tileCloneCalls,44);
assert.equal(x.currentG4C6.buildingCloneCalls,5);
assert.equal(x.currentG4C6.tileCopiedVolume,8319456);
assert.equal(x.currentG4C6.totalCopiedVolume,8771760);
assert.equal(x.proposedG4C7.roadSurfaceOnlyCloneCalls,8);
assert.equal(x.proposedG4C7.estimatedCopiedVolume,211968);
assert(x.copiedVolumeProxyReductionPct>97.5);
assert(x.copiedVolumeProxyReductionPct<100);
const byId=new Map();
for(const b of p.boxes){
 assert(b.w>0&&b.h>0&&b.d>0);
 assert(b.y>=2&&b.y+b.h<=78);
 const lx=b.x%180,lz=b.z%180;
 assert(lx>=12&&lz>=12&&lx+b.w<=180&&lz+b.d<=180,'road intrusion '+b.id+' '+b.role);
 const prev=byId.get(b.id)||[];
 if(b.y>2)assert(prev.some(v=>v.y+v.h===b.y&&overlap(b,v)>=6),
  'unsupported suspended primary volume '+b.id+':'+b.role);
 prev.push(b);byId.set(b.id,prev);
}
for(const b of p.buildings){
 assert(!(b.plot[0]===1&&b.plot[1]===1),'Must keep a district-specific open civic site');
}
// Region archetypes must have different purpose-built structural elements.
for(const [region,roles] of Object.entries({
 A:['wide-mixed-podium','recessed-upper-office','atrium-sky-join','upper-offset-terrace','long-bus-market-arcade','covered-south-stalls'],
 B:['acoustic-thick-roof','museum-west-gallery','clerestory-lightwell','long-reading-room','tiered-bleachers'],
 C:['courtyard-U-ground','north-L-residence','garden-street-base','middle-terrace-home','glass-greenhouse-pavilion','courtyard-community-hall'],
 D:['supported-research-skybridge','grounded-observation-tower','raised-observation-well','research-sawtooth-lightwell','workshop-observation-platform']
})){
 const present=new Set(p.boxes.filter(v=>v.id[0]===region).map(v=>v.role));
 for(const role of roles)assert(present.has(role),region+' lost structural program '+role);
}
const civicRoles={
 A:['financial-public-square-floor','transit-hall-west-front'],
 B:['outdoor-cultural-court','main-open-stage','tiered-civic-seats-west'],
 C:['community-park-base','park-greenhouse-west','park-woodland-terrace-east'],
 D:['research-community-square','science-demo-west','science-exhibit-east']
};
for(const [region,roles] of Object.entries(civicRoles)){
 const present=p.boxes.filter(b=>b.id===region+'0').map(b=>b.role);
 for(const role of roles)assert(present.includes(role),'Missing '+region+' civic role '+role);
 assert(present.length>=4,'No public center in '+region);
 const di=['A','B','C','D'].indexOf(region),cx=(di%2)*180+96,cz=Math.floor(di/2)*180+96;
 assert(!p.boxes.some(b=>b.x<=cx&&cx<b.x+b.w&&b.z<=cz&&cz<b.z+b.d&&
   b.y<=5&&5<b.y+b.h),region+' civic breathing space blocked at pedestrian head height');
}
assert(p.buildings.every(b=>byId.has(b.id)));
console.log('PASS G4C7 A2: 22 individually programmed buildings + 4 differentiated public civic hearts, structural supports and road buffers');
console.log('PASS block-copy proxy: 8,771,760 historical candidate -> 211,968 proposed road-only copy; this is NOT time');
console.log('PASS concept-only gate: no Minecraft or previous CSV/ZIP/USED-latch writes');
