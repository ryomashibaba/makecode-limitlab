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
assert.equal(report.verdict,'REQUIRES_HUMAN_ART_REVIEW',
 'Footprint family uniqueness is not a substitute for human 4-view quality review');
for(const [region,metric] of Object.entries(report.distribution)){
 assert(metric.distinctFootprintFamilies>=3,
   region+' still clones near-identical architectural footprints');
 assert.equal(metric.repeatingClusters.length,0,
   region+' has at least three repeated identical building plans');
}
console.log('PASS 4 view SVGs and OBJ/MTL export for '+plan.boxes.length+' cuboids');
console.log('PASS quantitative repetition guard: 4 regions no triple-duplicate footprint; HUMAN aesthetics still HOLD');
// Adversarial art QA: deliberately convert six varied C buildings to the same
// U-footprint, keeping their original heights. Must fail despite height differences.
const synthetic=JSON.parse(JSON.stringify(plan));
const original=synthetic.boxes.filter(b=>b.id==='C1');
const c1base=[Math.min(...original.map(b=>b.x)),Math.min(...original.map(b=>b.z))];
const bad=[];
for(let n=1;n<=6;n++){
 const id='C'+n;
 const before=synthetic.boxes.filter(b=>b.id===id);
 const base=[Math.min(...before.map(b=>b.x)),Math.min(...before.map(b=>b.z))];
 for(const q of original){
  bad.push({...q,id,x:q.x-c1base[0]+base[0],z:q.z-c1base[1]+base[1],
    y:q.y+(n%2),material:n%2?'glass':'stone'});
 }
}
synthetic.boxes=synthetic.boxes.filter(b=>b.id[0]!=='C').concat(bad);
const syntheticResult=assess(synthetic);
assert.equal(syntheticResult.verdict,'REJECT_REPEATED_FOOTPRINT_FAMILIES',
 'Painting or raising identical U-blocks must not satisfy variety gate');
console.log('PASS adversarial cloned C courtyard blocks are rejected despite new colors/heights');
console.log(JSON.stringify(report.distribution));
