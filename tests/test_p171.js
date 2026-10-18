// P1.7.1 mock Minecraft test: fail-closed preflight, boundary probes, final chat.
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const script = fs.readFileSync(path.join(__dirname, '../build/limitlab_p1_7_1.js'), 'utf8');

function scenario(opts = {}) {
  const cells = new Map(), files = new Map(), messages = [], handlers = {};
  let fills = 0, clones = 0, pauses = 0, writes = 0, maxFill = 0, maxClone = 0;
  const key = p => p.x + ',' + p.y + ',' + p.z;
  const get = p => cells.get(key(p)) || 0;
  const put = (p, v) => { cells.set(key(p), v); writes++; };
  const each = (a, b, fn) => {
    for (let y=a.y;y<=b.y;y++) for(let z=a.z;z<=b.z;z++)
      for(let x=a.x;x<=b.x;x++) fn({x,y,z});
  };
  const vol = (a,b) => (b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
  const candidateX=[12,-140,12,-140,176,12];
  const candidateZ=[24,24,-140,-140,24,176];
  for(const candidate of opts.occupiedCandidates || []) {
    cells.set(candidateX[candidate]+',12,'+candidateZ[candidate], 99);
  }
  if(opts.airReferenceBlocked)cells.set('108,12,24',99);
  if(opts.cloneDestOccupied)cells.set('76,12,24',99);
  const c = {
    Math,AIR:0,GOLD_BLOCK:2,STONE:1,Axis:{X:0,Y:1,Z:2},
    FillOperation:{Replace:0},CloneMask:{Replace:0},
    CloneMode:{Normal:0},TestForBlocksMask:{All:0},
    world:(x,y,z)=>({x,y,z}),
    player:{
      position:()=>({getValue:()=>0}),
      onChat:(name,fn)=>handlers[name]=fn,
      say:s=>messages.push(s)
    },
    file:{writeFile:(name,txt)=>files.set(name,txt),readFile:name=>files.get(name)||''},
    loops:{
      pause:ms=>{
        assert.equal(ms,1,'P1.7.1 must not contain long endurance pauses');
        pauses++;
        if(opts.stopAtPause===pauses)handlers.labstop171();
      },
      runInBackground:fn=>fn()
    },
    blocks:{
      testForBlock:(id,p)=>get(p)===id,
      testForBlocks:(a,b,d)=>{
        let eq=true;
        each(a,b,p=>{if(get(p)!==get({
          x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z
        }))eq=false;});
        return eq;
      },
      fill:(v,a,b)=>{
        fills++;const n=vol(a,b);maxFill=Math.max(maxFill,n);
        assert(n<=33024,'exceeded allowed one-call size');
        const over=n>(opts.fillCap===undefined?33024:opts.fillCap);
        if(over && !opts.partialOversize)return;
        if(over && opts.partialOversize){
          let count=0;
          each(a,b,p=>{if(count++<128)put(p,v);});
          return;
        }
        if(opts.failSourceFill && fills===2)return;
        each(a,b,p=>put(p,v));
      },
      clone:(a,b,d)=>{
        clones++;const n=vol(a,b);maxClone=Math.max(maxClone,n);
        assert(n<=33024,'exceeded allowed clone size');
        const over=n>(opts.cloneCap===undefined?33024:opts.cloneCap);
        if(over && !opts.partialOversize)return false;
        if(over && opts.partialOversize){
          let count=0;
          each(a,b,p=>{
            if(count++<128)put({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p));
          });
          return false;
        }
        if(opts.cloneAlwaysFalse)return false;
        const changes=[];
        each(a,b,p=>changes.push([{
          x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z
        },get(p)]));
        changes.forEach(([p,v])=>put(p,v));
        return true;
      }
    }
  };
  vm.runInNewContext(script,c,{timeout:25000});
  const rows = () => [...files.values()].find(v=>typeof v==='string'&&v.startsWith('Version,Stage,Units')) || '';
  const stats=()=>({fills,clones,pauses,writes,maxFill,maxClone,cells,files,messages});
  return {
    run:()=>handlers.labauto171(),stop:()=>handlers.labstop171(),
    status:()=>handlers.labstatus171(),plan:()=>handlers.labplan171(),
    rows,stats,messages
  };
}
let count=0;
function test(name, fn) { fn(); count++; console.log('PASS',name); }

test('both single fill and clone succeed at 32800 and 33024',()=>{
  const s=scenario();s.run();const r=s.rows(),h=s.stats();
  for(const n of [32800,33024]){
    assert(r.includes('P1.7.1,ONE_FILL,'+n+','+n+',PASS,PASS'));
    assert(r.includes('P1.7.1,ONE_CLONE,'+n+','+n+',PASS,PASS'));
  }
  assert(r.includes('P1.7.1,RUN,2,2,PASS,BOTH_SINGLE_33024_EXACT_NOT_TRUE_MAX'));
  assert.equal(h.maxFill,33024);assert.equal(h.maxClone,33024);
  assert(s.messages.some(m=>m.includes('TEST FINISHED')));
  assert(s.messages.some(m=>m.includes('USER_UPLOAD_THIS_P171_STATUS.csv')));
});
test('fill and clone reject 32800 cleanly without retrying',()=>{
  const s=scenario({fillCap:32768,cloneCap:32768});s.run();const r=s.rows();
  assert(r.includes('P1.7.1,ONE_FILL,32800,32800,LIMIT,NO_WRITE'));
  assert(r.includes('P1.7.1,ONE_CLONE,32800,32800,LIMIT,RETURN_FALSE_NO_WRITE'));
  assert(r.includes('P1.7.1,RUN,1,2,LIMIT,32800'));
  assert(!r.includes('P1.7.1,ONE_FILL,33024'));
  assert(s.messages.some(m=>m.includes('TEST FINISHED')));
});
test('32800 passes but 33024 fails and completes visibly',()=>{
  const s=scenario({fillCap:32800,cloneCap:32800});s.run();const r=s.rows();
  assert(r.includes('P1.7.1,ONE_FILL,32800,32800,PASS'));
  assert(r.includes('P1.7.1,ONE_CLONE,32800,32800,PASS'));
  assert(r.includes('P1.7.1,ONE_FILL,33024,33024,LIMIT,NO_WRITE'));
  assert(r.includes('P1.7.1,ONE_CLONE,33024,33024,LIMIT,RETURN_FALSE_NO_WRITE'));
  assert(r.includes('P1.7.1,RUN,2,2,LIMIT,33024'));
  assert(s.messages.some(m=>m.includes('TEST FINISHED')));
});
test('partial oversized fill and clone are not mistaken for zero writes',()=>{
  const s=scenario({fillCap:32768,cloneCap:32768,partialOversize:true});s.run();const r=s.rows();
  assert(r.includes('P1.7.1,ONE_FILL,32800,32800,LIMIT,PARTIAL_OR_WRONG_BLOCKS'));
  assert(r.includes('P1.7.1,ONE_CLONE,32800,32800,LIMIT,RETURN_FALSE_PARTIAL_OR_WRONG_BLOCKS'));
});
test('fill pass and clone reject at same size are recorded independently',()=>{
  const s=scenario({fillCap:33024,cloneCap:32768});s.run();const r=s.rows();
  assert(r.includes('P1.7.1,ONE_FILL,32800,32800,PASS,PASS'));
  assert(r.includes('P1.7.1,ONE_CLONE,32800,32800,LIMIT,RETURN_FALSE_NO_WRITE'));
  assert(!r.includes('P1.7.1,ONE_FILL,33024'));
});
test('all three candidate regions occupied cause zero block writes',()=>{
  const s=scenario({occupiedCandidates:[0,1,2,3,4,5]});s.run();const h=s.stats();
  assert(s.rows().includes('STOP,NO_EMPTY_SAFE_REGION'));
  assert.equal(h.writes,0);
  assert(s.messages.some(m=>m.includes('TEST STOPPED')));
});
test('occupied candidate #1 skipped; no old block overwritten',()=>{
  const s=scenario({occupiedCandidates:[0]});s.run();
  assert(s.rows().includes('P1.7.1,PREFLIGHT,2,6,PASS'));
  assert.equal(s.stats().cells.get('12,12,24'),99);
});
test('occupied reference cube safely triggers alternate candidate',()=>{
  const s=scenario({airReferenceBlocked:true});s.run();
  assert(s.rows().includes('P1.7.1,PREFLIGHT,2,6,PASS'));
  assert.equal(s.stats().cells.get('108,12,24'),99);
});
test('occupied clone destination safely triggers alternate candidate',()=>{
  const s=scenario({cloneDestOccupied:true});s.run();
  assert(s.rows().includes('P1.7.1,PREFLIGHT,2,6,PASS'));
  assert.equal(s.stats().cells.get('76,12,24'),99);
});
test('source mismatch stops before dangerous one-call probes',()=>{
  const s=scenario({failSourceFill:true});s.run();
  assert(s.rows().includes('STOP,SOURCE_VERIFY_FAILED'));
  assert.equal(s.stats().clones,0);
  assert(!s.rows().includes('P1.7.1,ONE_FILL,32800'));
});
test('stop during source halts with definitive chat message',()=>{
  // 2 reference yields plus 5x3 preflight yields => next pause is source layer 1.
  const s=scenario({stopAtPause:18});s.run();
  assert(s.rows().includes('STOP,USER_STOP'));
  assert(s.messages.some(m=>m.includes('TEST STOPPED')));
  assert(!s.rows().includes('P1.7.1,ONE_FILL,32800'));
});
test('single-use guard prevents new writes, logs or rerun',()=>{
  const s=scenario();s.run();const w=s.stats().writes,r=s.rows();s.run();
  assert.equal(s.stats().writes,w);assert.equal(s.rows(),r);
  assert(s.messages.some(m=>m.includes('no unsafe rerun')));
});
test('read-only plan leaves world, logs and CSV untouched',()=>{
  const s=scenario();s.plan();const h=s.stats();
  assert.equal(h.writes,0);assert.equal(h.files.size,0);
  assert(s.messages.some(m=>m.includes('32769 exact not tested')));
});
test('final status stays PASS and reports final state to user',()=>{
  const s=scenario();s.run();s.status();
  assert(s.messages.some(m=>m.includes('final PASS')));
});

test('five blocked candidates fall through to sixth safe site',()=>{
  const s=scenario({occupiedCandidates:[0,1,2,3,4]});s.run();
  const text=s.rows();
  assert(text.includes('P1.7.1,PREFLIGHT,6,6,PASS'));
  for(let i=1;i<=5;i++) assert(text.includes('P1.7.1,PREFLIGHT,'+i+',6,SKIP,'));
  assert(s.messages.some(m=>m.includes('safe empty candidate 6/6')));
  assert.equal(s.stats().cells.get('12,12,24'),99);
});
test('CSV identifies SOURCE rejection and first mismatching tile',()=>{
  const s=scenario({occupiedCandidates:[0]});s.run();
  const r=s.rows();
  assert(r.includes('P1.7.1,PREFLIGHT,1,6,SKIP,candidate_1_SOURCE_TILE_NOT_MATCHED_OR_UNAVAILABLE_x0_y0_z0'));
  assert(r.includes('P1.7.1,PREFLIGHT,2,6,PASS'));
});
test('CSV identifies occupied clone destination separately',()=>{
  const s=scenario({cloneDestOccupied:true});s.run();
  const r=s.rows();
  assert(r.includes('P1.7.1,PREFLIGHT,1,6,SKIP,candidate_1_CLONE_TILE_NOT_MATCHED_OR_UNAVAILABLE_x0_y0_z0'));
  assert(r.includes('P1.7.1,PREFLIGHT,2,6,PASS'));
});
test('reference rejection contains exact relative reference-cell position',()=>{
  const s=scenario({airReferenceBlocked:true});s.run();
  const r=s.rows();
  assert(r.includes('P1.7.1,PREFLIGHT,1,6,SKIP,candidate_1_REFERENCE_REF_NOT_AIR_OR_UNAVAILABLE_x0_y0_z0'));
  assert(r.includes('P1.7.1,PREFLIGHT,2,6,PASS'));
});
console.log('P1.7.1 simulated tests '+count+'/'+count+' PASS');
