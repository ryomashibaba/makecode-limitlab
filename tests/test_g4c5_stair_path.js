// Exact source-pinned route audit: a green result is ONLY offline voxel geometry.
'use strict';
const assert=require('assert'),{analyze,SPECS,stairPath}=require('../tools/audit_g4c5_stair_path.js');
const base=analyze();
assert.equal(base.kind,'OFFLINE_G4C5_DETAILED_STAIR_GRAPH_NOT_MINECRAFT_WALK');
assert.equal(base.sourceBlob,'058fa73fe67c26c53902a4f76f6e15988606a1ad');
assert.equal(base.roomCount,8);
assert.equal(base.floorsTotal,20);
assert.equal(base.floorCount,20);
assert.equal(base.stairTotal,264);
assert.equal(base.stairReach,264,
 'Blocked individual stair tread(s): '+JSON.stringify(base.wings.filter(x=>x.firstBadTread).map(x=>({id:x.id,step:x.firstBadTread}))));
assert.equal(base.verdict,'OFFLINE_ALL_TREADS_AND_FLOORS_REACHABLE');
assert.equal(base.voxelStats.fills,871);
assert.equal(base.voxelStats.clones,49);
assert.equal(base.voxelStats.checks,431);
assert.equal(stairPath().length,39);
assert.equal(SPECS.length,8);
console.log('PASS 8 inner rooms + 20 upper floors + 264/264 individual stair treads, offline only');
// Negative control: one missing stair block must be detected even if another
// unrelated route still exists; removes ONLY from simulated readout, never world.
const p=stairPath()[15];
const broken=analyze({removeTread:[104+p[0],17,25+p[1]]});
assert.notEqual(broken.verdict,'OFFLINE_ALL_TREADS_AND_FLOORS_REACHABLE',
 'A broken A1 tread must never qualify');
const a1=broken.wings.find(x=>x.id==='A1');
assert.equal(a1.solidTreads,38);
assert(a1.firstBadTread && a1.firstBadTread.step<=16,
 'Mutated riser did not register as broken');
console.log('PASS missing step negative control (offline only)');
