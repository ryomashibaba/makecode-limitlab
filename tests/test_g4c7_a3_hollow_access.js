'use strict';
const assert=require('assert');
const {create}=require('../tools/g4c7_urban_layout_lab');
const {buildA3,evaluateA3}=require('../tools/g4c7_a3_hollow_access_lab');
const {svg,toObj,assess}=require('../tools/g4c7_render_review');
const original=create();
const a3=buildA3();
assert.equal(a3.buildingCount,22,'historical A2 program count retained');
assert.equal(a3.entrances.length,22);
assert.equal(a3.civicConnections.length,4);
assert(a3.solidBoxes>original.solidBoxes);
assert.equal(a3.label,'G4C7_A3_HOLLOW_GROUND_CONCEPT_NOT_BUILT');
assert(!a3.boxes.some(b=>b.x%60<12||b.z%60<12),'some A3 cuboid extends to road start');
// Every room is now an actual sheltered void with support below and roof above,
// not a decorative AIR pocket or teleported upper floor.
for(const e of a3.entrances){
 const b=original.boxes.find(x=>x.id===e.building&&x.y===2);
 assert(b,'Missing base '+e.building);
 assert(a3.boxes.some(x=>x.id===b.id&&x.role.endsWith('-bearing-roof')));
 assert(a3.boxes.some(x=>x.id===b.id&&x.role.endsWith('-floor')));
 assert(!a3.boxes.some(x=>x===b),'Old solid plinth must be removed '+b.id);
 assert.equal(e.doorWidth,3);
 const [ex,ey,ez]=e.inside;
 assert(ex>b.x&&ex<b.x+b.w&&ez>b.z&&ez<b.z+b.d);
 assert.equal(ey,3);
}
const result=evaluateA3(a3);
assert.equal(result.kind,'OFFLINE_GROUND_LEVEL_ACCESS_ONLY_NO_MINECRAFT');
assert.equal(result.groundRooms.total,22);
assert.equal(result.groundRooms.passed,22,'Some street-to-main-room path is blocked: '+JSON.stringify(result.groundRooms.items.filter(x=>!x.innerRoomReachable)));
assert.equal(result.publicSquares.total,4);
assert.equal(result.publicSquares.passed,4,'Some road-to-public-square transition is blocked: '+JSON.stringify(result.publicSquares.items));
assert.equal(result.verdict,'GROUND_ONLY_OFFLINE_PASS');
assert.equal(new Set(result.groundRooms.items.map(x=>x.building)).size,22);
assert.equal(new Set(result.publicSquares.items.map(x=>x.id)).size,4);
// Don't accidentally turn an offline simple movement model into a Minecraft human QA.
assert(result.notApproved.includes('actual player walking'));
assert(result.notApproved.includes('upper floors'));
// Essential negative control: one occupied A1 doorway must be detected as failure.
const one=a3.entrances.find(x=>x.building==='A1');
const bad=evaluateA3(a3,{blockDoor:one.doorway});
assert.equal(bad.verdict,'GROUND_ACCESS_BLOCKED');
assert.equal(bad.groundRooms.passed,21);
assert.equal(bad.publicSquares.passed,4);
const audit=assess(a3);
assert.equal(audit.verdict,'REQUIRES_HUMAN_ART_REVIEW');
assert(svg(a3,'oblique').includes('CONCEPT ONLY'));
assert(svg(a3,'aerial',{district:'B'}).includes('CONCEPT ONLY'));
assert((toObj(a3).match(/^o /gm)||[]).length===a3.solidBoxes);
console.log('G4C7 A3 PASS — 22/22 street-to-hollow-room routes, 4/4 accessible civic-grade transitions');
console.log('G4C7 A3 PASS — adversarial blocked A1 entrance rejected; all previous 22 sites preserved');
console.log('G4C7 A3 HOLD — upper floors, actual Minecraft walk, materials, performance and aesthetics UNVERIFIED');
