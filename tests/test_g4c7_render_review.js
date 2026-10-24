'use strict';
const assert=require('assert');
const {create,validate}=require('../tools/g4c7_urban_layout_lab');
const {svg,toObj,mtl,assess,primitives,cameras}=require('../tools/g4c7_render_review');
validate();
const plan=create(),report=assess(plan);
assert.equal(plan.buildingCount,22);
assert.equal(Object.keys(cameras).length,4);
for(const cam of Object.keys(cameras)){
 const rendered=svg(plan,cam);
 assert(rendered.startsWith('<?xml version="1.0" encoding="UTF-8"?>'),'SVG header '+cam);
 assert(rendered.includes('<svg')&&rendered.includes('</svg>'),'Complete SVG '+cam);
 assert(rendered.includes('CONCEPT ONLY'),'No hardware build claim '+cam);
 assert(rendered.includes('REVIEW STATUS: '+report.verdict),'Unambiguous quality status '+cam);
 assert((rendered.match(/<polygon /g)||[]).length>150,'Visible faces missing '+cam);
 const faces=primitives(plan,cameras[cam]);
 assert(faces.length>150);
 assert(faces.every(f=>f.points.length===4&&f.points.every(p=>p.every(Number.isFinite))));
}
const obj=toObj(plan);
assert.equal((obj.match(/^o /gm)||[]).length,plan.boxes.length);
assert.equal((obj.match(/^v /gm)||[]).length,plan.boxes.length*8);
assert.equal((obj.match(/^f /gm)||[]).length,plan.boxes.length*6);
assert(obj.includes('mtllib g4c7_review.mtl'));
assert(mtl().includes('newmtl B_stone'));
assert.equal(report.kind,'OFFLINE_ART_REPETITION_METRIC_NOT_HUMAN_VISUAL_QA');
assert.equal(Object.keys(report.distribution).length,4);
for(const r of Object.values(report.distribution)){
 assert(r.buildings>=5);
 assert(r.distinctFootprintFamilies>=1);
}
assert.equal(report.verdict,'REJECT_REPEATED_FOOTPRINT_FAMILIES',
 'The current 22-block mass concept MUST NOT be called visually approved');
assert(report.distribution.B.repeatingClusters.some(a=>a.length>=3),'Culture repeated slabs not detected');
assert(report.distribution.C.repeatingClusters.some(a=>a.length>=3),'Residential repeated U blocks not detected');
assert(report.distribution.D.repeatingClusters.some(a=>a.length>=3),'Research repeated H blocks not detected');
console.log('PASS 4 view SVGs and OBJ/MTL export for '+plan.boxes.length+' cuboids');
console.log('PASS aesthetic regression detection: repetitive 22-building layout remains REJECT and must be redesigned before Minecraft');
console.log(JSON.stringify(report.distribution));
