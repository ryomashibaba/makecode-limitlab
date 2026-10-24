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
assert(p.boxes.some(x=>x.role==='thick-joined-roof'));
assert(p.boxes.some(x=>x.role==='south-residence'));
assert(p.boxes.some(x=>x.role==='north-residence'));
assert(p.boxes.some(x=>x.role==='high-sky-gallery'));
assert(p.boxes.some(x=>x.role==='vertical-core'));
assert(p.buildings.every(b=>byId.has(b.id)));
console.log('PASS G4C7 urban-concept: 22 buildings, 4 unlike typologies, civic voids, ground support, no road overwrite');
console.log('PASS block-copy proxy: 8,771,760 historical candidate -> 211,968 proposed road-only copy; this is NOT time');
console.log('PASS concept-only gate: no Minecraft or previous CSV/ZIP/USED-latch writes');
