// P1.9 Minecraft mock: bounded 98304->131072 one-call clones, safe stages.
// Offline simulation only, not a Minecraft Education hardware measurement.
const assert=require('assert');
const fs=require('fs');
const vm=require('vm');
const path=require('path');
const script=fs.readFileSync(path.join(__dirname,'../build/limitlab_p1_9.js'),'utf8');
function scenario(opts={}) {
 const cells=new Map(), files=new Map(), handlers={}, messages=[];
 let fillCalls=0,cloneCalls=0,writes=0,pauses=0,highestFill=0,highestClone=0;
 const cloneSizes=[];
 const key=p=>p.x+','+p.y+','+p.z;
 const get=p=>cells.get(key(p))??0;
 const put=(p,v)=>{cells.set(key(p),v);writes++;};
 const each=(a,b,fn)=>{
  for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)fn({x,y,z});
 };
 const vol=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 const cx=[16,-176,16,-176,208,16], cz=[24,24,-176,-176,24,208];
 for (const i of opts.occupiedCandidates||[]) cells.set(cx[i]+',12,'+cz[i],99);
 if(opts.referenceOccupied)cells.set('112,12,24',99);
 if(opts.targetOccupied)cells.set('64,12,24',99);
 const env={
  Math,AIR:0,GOLD_BLOCK:2,STONE:1,
  Axis:{X:0,Y:1,Z:2},FillOperation:{Replace:0},
  CloneMask:{Replace:0},CloneMode:{Normal:0},TestForBlocksMask:{All:0},
  world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(name,fn)=>handlers[name]=fn,say:t=>messages.push(t)},
  file:{writeFile:(p,v)=>files.set(p,v),readFile:p=>files.get(p)||''},
  loops:{runInBackground:fn=>fn(),pause:ms=>{
    assert.equal(ms,1,'no long endurance wait allowed');
    pauses++;
    if(opts.stopAtPause===pauses) handlers.labstop19();
  }},
  blocks:{
    testForBlock:(id,p)=>get(p)===id,
    testForBlocks:(a,b,d)=>{
      let same=true;
      each(a,b,p=>{
        const q={x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z};
        if(get(p)!==get(q))same=false;
      });
      return same;
    },
    fill:(id,a,b)=>{
      fillCalls++;
      const n=vol(a,b);highestFill=Math.max(highestFill,n);
      assert(n<=1024,'safe segmented fill is unexpectedly large');
      if(opts.failFirstSourceFill && fillCalls===2)return;
      each(a,b,p=>put(p,id));
    },
    clone:(a,b,d)=>{
      cloneCalls++;
      const n=vol(a,b);highestClone=Math.max(highestClone,n);
      cloneSizes.push(n);
      assert([98304,131072].includes(n),'unplanned clone size');
      if(n>(opts.cloneCap===undefined?131072:opts.cloneCap)){
        if(opts.partialFailure){
          let i=0;
          each(a,b,p=>{if(i++<128)put({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p));});
        }
        return false;
      }
      const changes=[];
      each(a,b,p=>changes.push([{
        x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z
      },get(p)]));
      if(opts.corruptFirstClone&&n===98304)changes[0][1]=99;
      for(const [p,v] of changes)put(p,v);
      if(opts.spillFirstClone&&n===98304)put({x:d.x,y:d.y+48,z:d.z},2);
      if(opts.returnFalseWhenExact)return false;
      return true;
    }
  }
 };
 vm.runInNewContext(script,env,{timeout:50000});
 return {run:()=>handlers.labauto19(),stop:()=>handlers.labstop19(),status:()=>handlers.labstatus19(),
 report:()=>handlers.labreport19(),plan:()=>handlers.labplan19(),
 rows:()=>[...files.values()].find(v=>typeof v==='string'&&v.startsWith('Version,Stage,Units,Total'))||'',
 stats:()=>({fillCalls,cloneCalls,writes,pauses,highestFill,highestClone,cloneSizes,cells,files,messages}),
 messages};
}
let passed=0;
function test(name,fn){fn();passed++;console.log('PASS',name);}
test('both 98304 and 131072 clones pass full exact verification',()=>{
 const s=scenario();s.run();const r=s.rows(),st=s.stats();
 assert(r.includes('P1.9,ONE_CLONE,98304,98304,PASS,return_true_full_exact'));
 assert(r.includes('P1.9,RESET,96,96,PASS,full_target_air_source_unchanged'));
 assert(r.includes('P1.9,ONE_CLONE,131072,131072,PASS,return_true_full_exact'));
 assert(r.includes('P1.9,RUN,1,1,FINISHED,ALL_PASS_131072_single_clone_fully_verified_not_a_universal_maximum'));
 assert.deepEqual(st.cloneSizes,[98304,131072]);
 assert.strictEqual(st.highestFill,1024);
 assert.strictEqual(st.highestClone,131072);
 assert(s.messages.some(x=>x.includes('TEST FINISHED')));
 assert(s.messages.some(x=>x.includes('lower bound 131072')));
});
test('98304 reject means 131072 never attempted',()=>{
 const s=scenario({cloneCap:65536});s.run();const r=s.rows();
 assert(r.includes('P1.9,ONE_CLONE,98304,98304,LIMIT,RETURN_FALSE_NO_WRITE'));
 assert(!r.includes('ONE_CLONE,131072'));
 assert(r.includes('P1.9,RUN,1,1,FINISHED,LIMIT_OBSERVED_'));
 assert(s.messages.some(x=>x.includes('lower bound 65536')));
});
test('98304 succeeds and 131072 reject retains first success and clear progress',()=>{
 const s=scenario({cloneCap:98304});s.run();const r=s.rows();
 assert(r.includes('P1.9,ONE_CLONE,98304,98304,PASS,return_true_full_exact'));
 assert(r.includes('P1.9,ONE_CLONE,131072,131072,LIMIT,RETURN_FALSE_NO_WRITE'));
 assert(r.includes('P1.9,RUN,1,1,FINISHED,LIMIT_OBSERVED_131072'));
 assert(s.messages.some(x=>x.includes('lower bound 98304')));
});
test('partial failed clone is not mistaken for zero-write',()=>{
 const s=scenario({cloneCap:65536,partialFailure:true});s.run();
 assert(s.rows().includes('P1.9,ONE_CLONE,98304,98304,LIMIT,RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS'));
});
test('clone reports success but corrupted cell fails full verification',()=>{
 const s=scenario({corruptFirstClone:true});s.run();const r=s.rows();
 assert(r.includes('P1.9,ONE_CLONE,98304,98304,LIMIT,PARTIAL_OR_UNEXPECTED_BLOCKS'));
 assert(!r.includes('ONE_CLONE,131072'));
});
test('false clone return plus exact world output classified as anomaly',()=>{
 const s=scenario({returnFalseWhenExact:true});s.run();const r=s.rows();
 assert(r.includes('P1.9,ONE_CLONE,98304,98304,ANOMALY,RETURN_FALSE_BUT_EXACT'));
 assert(r.includes('P1.9,RUN,1,1,FINISHED,ANOMALY_'));
 assert(!r.includes('ONE_CLONE,131072'));
});
test('first clone writing beyond requested height triggers anomaly and prevents next',()=>{
 const s=scenario({spillFirstClone:true});s.run();const r=s.rows();
 assert(r.includes('P1.9,ONE_CLONE,98304,98304,ANOMALY,WRITE_OUTSIDE_REQUESTED_VOLUME'));
 assert(!r.includes('ONE_CLONE,131072'));
});
test('all 6 spatial candidates rejected, zero world changes',()=>{
 const s=scenario({occupiedCandidates:[0,1,2,3,4,5]});s.run();const st=s.stats();
 assert(rHas(s,'STOP,NO_EMPTY_SAFE_REGION'));
 assert.strictEqual(st.writes,0);
 assert(s.messages.some(x=>x.includes('TEST STOPPED')));
});
function rHas(s,needle){return s.rows().includes(needle);}
test('five occupied candidates safely fall through to sixth',()=>{
 const s=scenario({occupiedCandidates:[0,1,2,3,4]});s.run();
 assert(rHas(s,'P1.9,PREFLIGHT,6,6,PASS'));
 assert.strictEqual(s.stats().cells.get('16,12,24'),99);
});
test('occupied target candidate 1 diagnosed, candidate 2 chosen',()=>{
 const s=scenario({targetOccupied:true});s.run();
 assert(rHas(s,'P1.9,PREFLIGHT,1,6,SKIP,candidate_1_TARGET_TILE_x0_y0_z0'));
 assert(rHas(s,'P1.9,PREFLIGHT,2,6,PASS'));
});
test('occupied reference diagnosed without false safe approval',()=>{
 const s=scenario({referenceOccupied:true});s.run();
 assert(rHas(s,'P1.9,PREFLIGHT,1,6,SKIP,candidate_1_REFERENCE_REF_x0_y0_z0'));
 assert(rHas(s,'P1.9,PREFLIGHT,2,6,PASS'));
});
test('silent safe source-construction failure stops before cloning',()=>{
 const s=scenario({failFirstSourceFill:true});s.run();
 assert(rHas(s,'STOP,SOURCE_MISMATCH'));
 assert.strictEqual(s.stats().cloneCalls,0);
});
test('cooperative stop during source records STOP and never clones',()=>{
 // first references:16 pauses, source/target:8+8 = 32, then first source progress pause:33.
 const s=scenario({stopAtPause:33});s.run();
 assert(rHas(s,'STOP,USER_STOP'));
 assert.strictEqual(s.stats().cloneCalls,0);
 assert(s.messages.some(x=>x.includes('TEST STOPPED')));
});
test('one-use guard does not overwrite previous results or blocks',()=>{
 const s=scenario({cloneCap:65536});s.run();
 const before=s.stats().writes,rows=s.rows();s.run();
 assert.strictEqual(s.stats().writes,before);
 assert.strictEqual(s.rows(),rows);
 assert(s.messages.some(x=>x.includes('unsafe rerun refused')));
});
test('read-only plan/report and repeated report never write',()=>{
 const s=scenario();s.plan();s.report();
 assert.strictEqual(s.stats().writes,0);assert.strictEqual(s.stats().files.size,0);
 s.run();const w=s.stats().writes;s.report();s.status();
 assert.strictEqual(s.stats().writes,w);
 assert(s.messages.some(x=>x.includes('RESULT ALL_PASS')));
});
console.log('P1.9 mock scenarios '+passed+'/'+passed+' PASS');
