// Offline Minecraft Education API simulator: P1.8.
// These checks do NOT replace an actual in-game test.
const assert=require('assert'),fs=require('fs'),path=require('path'),vm=require('vm');
const script=fs.readFileSync(path.join(__dirname,'../build/limitlab_p1_8.js'),'utf8');
function scenario(opts={}) {
 const cells=new Map(), logs=new Map(), handlers={}, messages=[];
 let fills=0,clones=0,writes=0,pauses=0,maxFill=0,maxClone=0, cloneSizes=[],fillSizes=[];
 const key=p=>[p.x,p.y,p.z].join(',');
 const get=p=>cells.get(key(p))??0;
 const put=(p,v)=>{cells.set(key(p),v);writes++;};
 const volume=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 const each=(a,b,fn)=>{for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)fn({x,y,z});};
 const candidateX=[16,-152,16,-152,192,16];
 const candidateZ=[20,20,-152,-152,20,192];
 for(const i of opts.occupiedCandidates||[]) cells.set([candidateX[i],12,candidateZ[i]].join(','),99);
 if(opts.cloneOccupied)cells.set('88,12,20',99);
 if(opts.referenceOccupied)cells.set('128,12,20',99);
 const c={
  Math,AIR:0,GOLD_BLOCK:2,STONE:1,Axis:{X:0,Y:1,Z:2},
  FillOperation:{Replace:0},CloneMask:{Replace:0},
  CloneMode:{Normal:0},TestForBlocksMask:{All:0},
  world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(n,f)=>handlers[n]=f,say:s=>messages.push(s)},
  file:{writeFile:(n,v)=>logs.set(n,v),readFile:n=>logs.get(n)||''},
  loops:{runInBackground:f=>f(),pause:ms=>{
    if(ms!==1)throw Error('unexpected long pause');
    pauses++;
    if(opts.stopPause===pauses)handlers.labstop18();
  }},
  blocks:{
   testForBlock:(id,p)=>get(p)===id,
   testForBlocks:(a,b,d)=>{
     let same=true;each(a,b,p=>{
       const q={x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z};
       if(get(p)!==get(q))same=false;
     });
     return same;
   },
   fill:(id,a,b)=>{
     fills++;const n=volume(a,b);fillSizes.push(n);maxFill=Math.max(maxFill,n);
     assert(n<=32775,'unplanned large fill call');
     if(opts.failSourceFill&&fills===2)return;
     if(n>(opts.fillLimit??32768)){
       if(opts.partialFill){let i=0;each(a,b,p=>{if(i++<192)put(p,id);});}
       return;
     }
     each(a,b,p=>put(p,id));
   },
   clone:(a,b,d)=>{
     clones++;const n=volume(a,b);cloneSizes.push(n);maxClone=Math.max(maxClone,n);
     assert([33024,40960,65536].includes(n),'wrong clone size');
     const over=n>(opts.cloneLimit??65536);
     if(over) {
       if(opts.partialClone){let i=0;each(a,b,p=>{if(i++<192)put({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p));});}
       return false;
     }
     let v=[];each(a,b,p=>v.push([{x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p)]));
     if(opts.cloneWriteCorrupt&&n===33024)v[0][1]=99;
     v.forEach(([p,id])=>put(p,id));
     return !opts.cloneReturnsFalseWhenWrites;
   }
  }
 };
 vm.runInNewContext(script,c,{timeout:30000});
 return {run:()=>handlers.labauto18(),stop:()=>handlers.labstop18(),status:()=>handlers.labstatus18(),
  report:()=>handlers.labreport18(),plan:()=>handlers.labplan18(),
  rows:()=>[...logs.values()].find(v=>typeof v==='string'&&v.startsWith('Version,Stage,Units,Total'))||'',
  stats:()=>({fills,clones,writes,pauses,maxFill,maxClone,cloneSizes,fillSizes,cells,logs,messages}),messages
 };
}
let passed=0;
function test(name,fn){fn();passed++;console.log('PASS',name);}
test('fill32775 and clones33024/40960/65536 all pass in API simulator',()=>{
 const s=scenario({fillLimit:32775});s.run();const r=s.rows(),h=s.stats();
 assert(r.includes('P1.8,ONE_FILL,32775,32775,PASS,PASS'));
 for(const size of [33024,40960,65536])assert(r.includes('P1.8,ONE_CLONE,'+size+','+size+',PASS,return_true_and_full_exact'));
 assert(r.includes('P1.8,RUN,1,1,FINISHED,ALL_PASS_'));
 assert.deepEqual(h.cloneSizes,[33024,40960,65536]);
 assert(h.maxFill===32775&&h.maxClone===65536);
 assert(s.messages.some(x=>x.includes('TEST FINISHED')));
 assert(s.messages.some(x=>x.includes('CloneBest 65536')));
});
test('historically likely silent fill rejection still runs independent clone trials',()=>{
 const s=scenario();s.run();const r=s.rows();
 assert(r.includes('P1.8,ONE_FILL,32775,32775,LIMIT,NO_WRITE'));
 assert(r.includes('P1.8,ONE_CLONE,65536,65536,PASS'));
 assert(r.includes('P1.8,RUN,1,1,FINISHED,LIMIT_OBSERVED_'));
 assert(s.messages.some(x=>x.includes('Fill32775 NO_WRITE')));
});
test('fill partial-write detected and never mistaken for no-write',()=>{
 const s=scenario({partialFill:true});s.run();
 assert(s.rows().includes('P1.8,ONE_FILL,32775,32775,LIMIT,PARTIAL_OR_UNEXPECTED_BLOCKS'));
});
test('33024 clone rejection stops escalation but saves fill outcome',()=>{
 const s=scenario({cloneLimit:32800});s.run();const r=s.rows();
 assert(r.includes('P1.8,ONE_CLONE,33024,33024,LIMIT,RETURN_FALSE_NO_WRITE'));
 assert(!r.includes('P1.8,ONE_CLONE,40960'));
 assert(r.includes('FINISHED,LIMIT_OBSERVED_'));
 assert(s.messages.some(x=>x.includes('TEST FINISHED')));
});
test('40960 clone rejection retains preceding 33024 PASS',()=>{
 const s=scenario({cloneLimit:33024});s.run();const r=s.rows();
 assert(r.includes('P1.8,ONE_CLONE,33024,33024,PASS'));
 assert(r.includes('P1.8,ONE_CLONE,40960,40960,LIMIT,RETURN_FALSE_NO_WRITE'));
 assert(!r.includes('P1.8,ONE_CLONE,65536'));
 assert(s.messages.some(x=>x.includes('CloneBest 33024')));
});
test('partial clone response classified distinctly from zero write',()=>{
 const s=scenario({cloneLimit:32800,partialClone:true});s.run();
 assert(s.rows().includes('P1.8,ONE_CLONE,33024,33024,LIMIT,RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS'));
});
test('return false despite exact clone is an anomaly, no escalation',()=>{
 const s=scenario({cloneReturnsFalseWhenWrites:true});s.run();const r=s.rows();
 assert(r.includes('P1.8,ONE_CLONE,33024,33024,ANOMALY,RETURN_FALSE_BUT_EXACT'));
 assert(r.includes('P1.8,RUN,1,1,FINISHED,ANOMALY_'));
 assert(!r.includes('P1.8,ONE_CLONE,40960'));
});
test('clone wrong content detected by full-tile check even if return true',()=>{
 const s=scenario({cloneWriteCorrupt:true});s.run();
 assert(s.rows().includes('P1.8,ONE_CLONE,33024,33024,LIMIT,PARTIAL_OR_UNEXPECTED_BLOCKS'));
 assert(!s.rows().includes('P1.8,ONE_CLONE,40960'));
});
test('all six candidates occupied -> STOP with zero writes',()=>{
 const s=scenario({occupiedCandidates:[0,1,2,3,4,5]});s.run();
 assert(s.rows().includes('STOP,NO_EMPTY_SAFE_REGION'));
 assert(s.stats().writes===0);
 assert(s.messages.some(x=>x.includes('TEST STOPPED')));
});
test('five blocked candidate cells -> sixth candidate selected without edits to occupied cells',()=>{
 const s=scenario({occupiedCandidates:[0,1,2,3,4]});s.run();const r=s.rows();
 assert(r.includes('P1.8,PREFLIGHT,6,6,PASS'));
 assert(s.stats().cells.get('16,12,20')===99);
 assert(s.messages.some(x=>x.includes('safe candidate 6/6 selected')));
});
test('occupied clone target at first candidate yields SKIP with region reason',()=>{
 const s=scenario({cloneOccupied:true});s.run();
 assert(s.rows().includes('P1.8,PREFLIGHT,1,6,SKIP,candidate_1_CLONE_MISMATCH_x0_y0_z0'));
 assert(s.rows().includes('P1.8,PREFLIGHT,2,6,PASS'));
});
test('occupied reference at first candidate yields SKIP with cell reason',()=>{
 const s=scenario({referenceOccupied:true});s.run();
 assert(s.rows().includes('P1.8,PREFLIGHT,1,6,SKIP,candidate_1_REF_REFERENCE_x0_y0_z0'));
 assert(s.rows().includes('P1.8,PREFLIGHT,2,6,PASS'));
});
test('source build failure prevents dangerous probe calls',()=>{
 const s=scenario({failSourceFill:true});s.run();
 assert(s.rows().includes('STOP,SOURCE_VERIFY_MISMATCH'));
 assert(s.stats().clones===0);
});
test('manual cooperative stop during source does not run probes',()=>{
 // AIR ref pause 16, SOURCE 4, FILL 4, CLONE 4 = 28; first source pause is #29.
 const s=scenario({stopPause:29});s.run();
 assert(s.rows().includes('STOP,USER_STOP'));
 assert(s.stats().clones===0);
 assert(s.messages.some(x=>x.includes('TEST STOPPED')));
});
test('single-use guard refuses replay or overwriting previous result',()=>{
 const s=scenario();s.run();const w=s.stats().writes,r=s.rows();s.run();
 assert(s.stats().writes===w);assert(s.rows()===r);
 assert(s.messages.some(x=>x.includes('unsafe rerun refused')));
});
test('read-only planning and repeatable final report never modify world',()=>{
 const s=scenario();s.plan();s.report();
 assert(s.stats().writes===0&&s.stats().logs.size===0);
 assert(s.messages.some(x=>x.includes('not retesting historical')));
 s.run();const w=s.stats().writes;s.report();s.status();
 assert(s.stats().writes===w&&s.messages.some(x=>x.includes('final')));
});
console.log('P1.8 Minecraft mock scenarios '+passed+'/'+passed+' PASS');
