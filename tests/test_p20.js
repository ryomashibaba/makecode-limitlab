// P2.0 Minecraft mock: safety, success, failures, side-effects, completion.
// Offline simulator, NOT Minecraft Education hardware evidence.
const assert=require('assert'),fs=require('fs'),vm=require('vm'),path=require('path');
const script=fs.readFileSync(path.join(__dirname,'../build/limitlab_p2_0.js'),'utf8');

function scenario(opts={}) {
 const cells=new Map(), files=new Map(), handlers={}, messages=[];
 let fills=0,clones=0,writes=0,pauses=0,maxFill=0,maxClone=0;
 const cloneSizes=[];
 const key=p=>p.x+','+p.y+','+p.z;
 const get=p=>cells.get(key(p))??0;
 const put=(p,v)=>{cells.set(key(p),v);writes++;};
 const each=(a,b,fn)=>{
  for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)fn({x,y,z});
 };
 const vol=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 const cx=[16,-240,16,-240,272,16], cz=[24,24,-240,-240,24,272];
 for(const i of opts.occupiedCandidates||[])cells.set(cx[i]+',12,'+cz[i],99);
 if(opts.referenceOccupied)cells.set('176,12,24',99);
 if(opts.targetOccupied)cells.set('96,12,24',99);
 const env={
  Math,AIR:0,GOLD_BLOCK:2,STONE:1,Axis:{X:0,Y:1,Z:2},
  FillOperation:{Replace:0},CloneMask:{Replace:0},CloneMode:{Normal:0},
  TestForBlocksMask:{All:0},world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(name,fn)=>handlers[name]=fn,
          say:message=>messages.push(message)},
  file:{writeFile:(name,value)=>files.set(name,value),readFile:name=>files.get(name)||''},
  loops:{runInBackground:fn=>fn(),pause:ms=>{
    assert.equal(ms,1,'no endurance delay allowed');
    pauses++;
    if(opts.stopAtPause===pauses)handlers.labstop20();
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
    fills++;const n=vol(a,b);
    maxFill=Math.max(maxFill,n);
    assert(n<=4096,'oversize source/clear fill');
    if(opts.silentSourceFailure&&fills===2)return;
    each(a,b,p=>put(p,id));
   },
   clone:(a,b,d)=>{
    clones++;const n=vol(a,b);
    maxClone=Math.max(maxClone,n);
    cloneSizes.push(n);
    assert([196608,262144].includes(n),'unexpected one-call clone size');
    if(n>(opts.cloneCap??262144)){
      if(opts.partialFailure){
        let i=0;each(a,b,p=>{
          if(i++<128)put({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p));
        });
      }
      return false;
    }
    // Source and target do not overlap. Test deliberately models the result
    // without requiring Minecraft's native copy semantics to execute.
    each(a,b,p=>{
      const q={x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z};
      put(q,get(p));
    });
    if(opts.corruptFirstClone&&n===196608) put({x:d.x,y:d.y,z:d.z},99);
    if(opts.spillFirstClone&&n===196608)put({x:d.x,y:d.y+48,z:d.z},2);
    if(opts.returnFalseWhenExact)return false;
    return true;
   }
  }
 };
 vm.runInNewContext(script,env,{timeout:60000});
 return {run:()=>handlers.labauto20(),stop:()=>handlers.labstop20(),
         status:()=>handlers.labstatus20(),report:()=>handlers.labreport20(),
         plan:()=>handlers.labplan20(),
         rows:()=>[...files.values()].find(v=>typeof v==='string'&&v.startsWith('Version,Stage,Units,Total'))||'',
         stats:()=>({fills,clones,writes,pauses,maxFill,maxClone,cloneSizes,cells,files,messages}),
         messages};
}
let passed=0;
function test(name,fn){fn();passed++;console.log('PASS',name);}
test('196608 then 262144 single clone both exact, without huge fill',()=>{
 const s=scenario();s.run();const r=s.rows(),h=s.stats();
 assert(r.includes('P2.0,ONE_CLONE,196608,196608,PASS,return_true_full_exact'));
 assert(r.includes('P2.0,RESET,48,48,PASS,entire_target_air_and_source_unchanged'));
 assert(r.includes('P2.0,ONE_CLONE,262144,262144,PASS,return_true_full_exact'));
 assert(r.includes('P2.0,RUN,1,1,FINISHED,ALL_PASS_262144_single_clone_verified_not_universal_maximum'));
 assert.deepEqual(h.cloneSizes,[196608,262144]);
 assert.equal(h.maxFill,4096);assert.equal(h.maxClone,262144);
 assert(s.messages.some(x=>x.includes('TEST FINISHED')));
 assert(s.messages.some(x=>x.includes('at least 262144')));
});
test('first clone limit stops second test and retains P1.9 baseline',()=>{
 const s=scenario({cloneCap:131072});s.run();const r=s.rows();
 assert(r.includes('P2.0,ONE_CLONE,196608,196608,LIMIT,RETURN_FALSE_NO_WRITE'));
 assert(!r.includes('ONE_CLONE,262144'));
 assert(r.includes('P2.0,RUN,1,1,FINISHED,LIMIT_OBSERVED_196608_'));
 assert(s.messages.some(x=>x.includes('at least 131072')));
});
test('second clone limit retains 196608 verified as lower bound',()=>{
 const s=scenario({cloneCap:196608});s.run();const r=s.rows();
 assert(r.includes('P2.0,ONE_CLONE,196608,196608,PASS,return_true_full_exact'));
 assert(r.includes('P2.0,ONE_CLONE,262144,262144,LIMIT,RETURN_FALSE_NO_WRITE'));
 assert(r.includes('FINISHED,LIMIT_OBSERVED_262144_'));
 assert(s.messages.some(x=>x.includes('at least 196608')));
});
test('partial write by rejected clone is detected, no second call',()=>{
 const s=scenario({cloneCap:131072,partialFailure:true});s.run();
 assert(s.rows().includes('P2.0,ONE_CLONE,196608,196608,LIMIT,RETURN_FALSE_PARTIAL_OR_UNEXPECTED_BLOCKS'));
 assert.equal(s.stats().clones,1);
});
test('silent corruption despite return true causes LIMIT and no next',()=>{
 const s=scenario({corruptFirstClone:true});s.run();
 assert(s.rows().includes('P2.0,ONE_CLONE,196608,196608,LIMIT,PARTIAL_OR_UNEXPECTED_BLOCKS'));
 assert.equal(s.stats().clones,1);
});
test('return false but exact is an anomaly, no second call',()=>{
 const s=scenario({returnFalseWhenExact:true});s.run();
 assert(s.rows().includes('P2.0,ONE_CLONE,196608,196608,ANOMALY,RETURN_FALSE_BUT_EXACT'));
 assert(s.rows().includes('FINISHED,ANOMALY_'));
 assert.equal(s.stats().clones,1);
});
test('writes outside first 196608 target classified as anomaly',()=>{
 const s=scenario({spillFirstClone:true});s.run();
 assert(s.rows().includes('P2.0,ONE_CLONE,196608,196608,ANOMALY,WRITE_OUTSIDE_REQUESTED_VOLUME'));
 assert.equal(s.stats().clones,1);
});
test('all six candidate sites occupied causes stop with no writes',()=>{
 const s=scenario({occupiedCandidates:[0,1,2,3,4,5]});s.run();
 assert(s.rows().includes('STOP,NO_EMPTY_SAFE_REGION'));
 assert.equal(s.stats().writes,0);
 assert(s.messages.some(x=>x.includes('TEST STOPPED')));
});
test('five candidate sites occupied allow sixth only',()=>{
 const s=scenario({occupiedCandidates:[0,1,2,3,4]});s.run();
 assert(s.rows().includes('P2.0,PREFLIGHT,6,6,PASS'));
 assert.equal(s.stats().cells.get('16,12,24'),99);
});
test('occupied clone target rejects first candidate with diagnostic',()=>{
 const s=scenario({targetOccupied:true});s.run();
 assert(s.rows().includes('P2.0,PREFLIGHT,1,6,SKIP,candidate_1_TARGET_TILE_x0_y0_z0'));
 assert(s.rows().includes('P2.0,PREFLIGHT,2,6,PASS'));
});
test('occupied air reference rejected before source writes',()=>{
 const s=scenario({referenceOccupied:true});s.run();
 assert(s.rows().includes('P2.0,PREFLIGHT,1,6,SKIP,candidate_1_REFERENCE_REF_x0_y0_z0'));
 assert(s.rows().includes('P2.0,PREFLIGHT,2,6,PASS'));
});
test('source silent failure detected before huge single clone',()=>{
 const s=scenario({silentSourceFailure:true});s.run();
 assert(s.rows().includes('STOP,SOURCE_VERIFY_MISMATCH'));
 assert.equal(s.stats().clones,0);
});
test('user stop during source stops before any clone',()=>{
 // 16 reference pauses, 8+8 preflight tile pauses = 32;
 // 1 source layer progress pause makes 33.
 const s=scenario({stopAtPause:33});s.run();
 assert(s.rows().includes('STOP,USER_STOP'));
 assert.equal(s.stats().clones,0);
 assert(s.messages.some(x=>x.includes('TEST STOPPED')));
});
test('second invocation is rejected and CSV does not get erased',()=>{
 const s=scenario({cloneCap:131072});s.run();const w=s.stats().writes,r=s.rows();s.run();
 assert.equal(s.stats().writes,w);assert.equal(s.rows(),r);
 assert(s.messages.some(x=>x.includes('unsafe repeat refused')));
});
test('status/report/plan never write or reexecute world',()=>{
 const s=scenario();s.plan();s.report();
 assert.equal(s.stats().writes,0);assert.equal(s.stats().files.size,0);
 s.run();const w=s.stats().writes;
 s.report();s.status();
 assert.equal(s.stats().writes,w);
 assert(s.messages.some(x=>x.includes('RESULT ALL_PASS')));
});
console.log('P2.0 Minecraft mock scenarios '+passed+'/'+passed+' PASS');
