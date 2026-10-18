// Offline Minecraft API simulator for LimitLab P1.6.
// Verifies geometry, fail-closed safety, CSV, and bounded one-call probes.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const path = require('path');
const script = fs.readFileSync(path.join(__dirname, '../build/limitlab_p1_6.js'), 'utf8');

function scenario(opts = {}) {
  const cells = new Map(), files = new Map(), handlers = {}, messages = [];
  let fills = 0, clones = 0, writes = 0, pauses = 0, largestFill = 0, largestClone = 0;
  let writesOutside = 0;
  const key = p => `${p.x},${p.y},${p.z}`;
  const get = p => cells.get(key(p)) ?? 0;
  const put = (p, id) => {
    if ((p.x >= 8 && p.x <= 23) || (p.x >= 32 && p.x <= 47) ||
      (p.x >= 56 && p.x <= 71) || (p.x >= 88 && p.x <= 103)) {
      // Expected write positions, see below for reference block ranges.
    } else { writesOutside++; }
    cells.set(key(p), id); writes++;
  };
  const each = (a, b, cb) => {
    for (let y = a.y; y <= b.y; y++)
      for (let z = a.z; z <= b.z; z++)
        for (let x = a.x; x <= b.x; x++) cb({x,y,z});
  };
  const volume = (a,b) => (b.x-a.x+1) * (b.y-a.y+1) * (b.z-a.z+1);
  // P1.6 candidate #1 origin 8,12,16; #2 at Z=104; #3 at Z=192.
  for (const candidate of opts.occupiedCandidates || []) {
    cells.set(key({x:8,y:12,z:16+88*candidate}), 99);
  }
  if (opts.referenceBlocked) cells.set(key({x:88,y:12,z:16}), 99);
  if (opts.occupiedCloneDestination) cells.set(key({x:56,y:12,z:16}),99);
  const c = {
    Math, AIR:0, STONE:1, GOLD_BLOCK:2, Axis:{X:0,Y:1,Z:2},
    FillOperation:{Replace:0}, CloneMask:{Replace:0}, CloneMode:{Normal:0}, TestForBlocksMask:{All:0},
    world:(x,y,z)=>({x,y,z}),
    player:{
      position:()=>({getValue:()=>0}),
      onChat:(name,fn)=>{handlers[name]=fn;},
      say:s=>messages.push(s)
    },
    file:{writeFile:(n,v)=>files.set(n,v),readFile:n=>files.get(n)||''},
    loops:{
      pause:ms=>{
        if(ms !== 1)throw Error('Unexpected long wait '+ms);
        pauses++;
        if(opts.stopAtPause===pauses) handlers.labstop16();
      },
      runInBackground:fn=>fn()
    },
    blocks:{
      testForBlock:(id,p)=>get(p)===id,
      testForBlocks:(a,b,d)=>{
        if(opts.forceTargetMismatch && d.x===32 && a.x===8 && b.x===15) return false;
        let same=true;
        each(a,b,p=>{
          if(get(p)!==get({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z}))same=false;
        });
        return same;
      },
      fill:(id,a,b)=>{
        fills++;
        const count=volume(a,b);largestFill=Math.max(count,largestFill);
        assert(count<=32768, 'single fill exceeds guarded cap');
        if(opts.failFillAt===fills)return;
        each(a,b,p=>put(p,id));
      },
      clone:(a,b,d)=>{
        clones++;
        const count=volume(a,b);largestClone=Math.max(count,largestClone);
        assert(count<=32768, 'single clone exceeds guarded cap');
        if(opts.cloneFalseAt===clones)return false;
        const changes=[];
        each(a,b,p=>changes.push([{
          x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p)]));
        changes.forEach(([p,v])=>put(p,v));
        return true;
      }
    }
  };
  vm.runInNewContext(script,c,{timeout:10000});
  const status=()=>[...files.values()].find(v=>typeof v==='string'&&v.startsWith('Version,Stage,Completed'))||'';
  const stats=()=>({fills,clones,writes,pauses,largestFill,largestClone,writesOutside,messages,cells,files});
  return {
    run:()=>handlers.labauto16(), probe:()=>handlers.labprobe16(),
    status:()=>handlers.labstatus16(), stop:()=>handlers.labstop16(),
    plan:()=>handlers.labplan16(), rows:status, stats, handlers, messages
  };
}
let checks=0;
function test(name,fn){fn(); checks++; console.log('PASS',name);}

test('main 65536x3 segmented construction and exact tiles PASS',()=>{
  const s=scenario();s.run();const r=s.rows(),h=s.stats();
  assert(r.includes('P1.6,SOURCE,65536,65536,PASS'));
  assert(r.includes('P1.6,FILL65536,65536,65536,PASS'));
  assert(r.includes('P1.6,CLONE65536,65536,65536,PASS'));
  assert(r.includes('P1.6,RUN,1,1,PASS,65536_SOURCE_FILL_CLONE_EXACT'));
  assert.equal(h.fills,128);assert.equal(h.clones,16);
  assert.equal(h.largestFill,1024);assert.equal(h.largestClone,4096);
  assert.equal(h.writes,196608);assert.equal(h.writesOutside,0);
});

test('occupied first candidate safely moves to second candidate',()=>{
  const s=scenario({occupiedCandidates:[0]});s.run();
  assert(s.rows().includes('P1.6,PREFLIGHT,2,3,PASS'));
  assert.equal(s.stats().cells.get('8,12,16'),99);
});

test('all candidate locations occupied: no blocks changed',()=>{
  const s=scenario({occupiedCandidates:[0,1,2]});s.run();
  assert(s.rows().includes('STOP,NO_EMPTY_SAFE_REGION'));
  assert.equal(s.stats().writes,0);assert.equal(s.stats().clones,0);
});

test('AIR reference occupied: switch candidates without overwriting',()=>{
  const s=scenario({referenceBlocked:true});s.run();
  assert(s.rows().includes('P1.6,PREFLIGHT,2,3,PASS'));
  assert.equal(s.stats().cells.get('88,12,16'),99);
});

test('partially occupied clone volume: use alternate candidate',()=>{
  const s=scenario({occupiedCloneDestination:true});s.run();
  assert(s.rows().includes('P1.6,PREFLIGHT,2,3,PASS'));
  assert.equal(s.stats().cells.get('56,12,16'),99);
});

test('first source fill does not write: stop before fill target',()=>{
  const s=scenario({failFillAt:1});s.run();
  assert(s.rows().includes('STOP,SOURCE_SEED_MISMATCH'));
  assert.equal(s.stats().clones,0);
});

test('segmented clone reject: stop and never mark main PASS',()=>{
  const s=scenario({cloneFalseAt:1});s.run();
  assert(s.rows().includes('STOP,CLONE_RETURN_FALSE'));
  assert(!s.rows().includes('65536_SOURCE_FILL_CLONE_EXACT'));
});

test('user STOP during source build retains partial journal and does not clone',()=>{
  // 24 initial AIR volume pauses; the next pause is after first source fill.
  const s=scenario({stopAtPause:25});s.run();
  assert(s.rows().includes('STOP,USER_STOP'));
  assert(s.stats().writes>0);assert.equal(s.stats().clones,0);
});

test('main cannot be re-run into occupied regions in same MakeCode session',()=>{
  const s=scenario();s.run();const first=s.stats().writes;const rows=s.rows();s.run();
  assert.equal(s.stats().writes,first);assert.equal(s.rows(),rows);
});

test('probe is blocked without verified main run',()=>{
  const s=scenario();s.probe();
  assert.equal(s.stats().writes,0);
  assert.equal(s.stats().files.size,0);
});

test('single-operation probes 4k/8k/16k/32k each PASS and never 65536',()=>{
  const s=scenario();s.run();s.probe();const r=s.rows(),h=s.stats();
  for(const n of [4096,8192,16384,32768]) {
    assert(r.includes(`P1.6,ONE_FILL,${n},${n},PASS,single_call_exact`));
    assert(r.includes(`P1.6,ONE_CLONE,${n},${n},PASS,single_call_exact`));
  }
  assert(r.includes('P1.6,PROBE,8,8,PASS'));
  assert.equal(h.largestFill,32768);assert.equal(h.largestClone,32768);
  const before=h.writes;s.probe();assert.equal(s.stats().writes,before);
});

test('one-call clone rejection is reported and prior main PASS preserved',()=>{
  const s=scenario({cloneFalseAt:17});s.run();s.probe();const r=s.rows();
  assert(r.includes('65536_SOURCE_FILL_CLONE_EXACT'));
  assert(r.includes('STOP,ONE_CLONE_RETURN_FALSE_4096'));
  assert(!r.includes('P1.6,PROBE,8,8,PASS'));
});

test('single-call fill silent failure detected via GOLD comparison',()=>{
  // 128 segmented fills in main + 2 reference + 64 reset = first ONE_FILL #195.
  const s=scenario({failFillAt:195});s.run();s.probe();
  assert(s.rows().includes('STOP,ONE_FILL_VERIFY_4096'));
  assert(!s.rows().includes('P1.6,PROBE,8,8,PASS'));
});

test('read-only plan leaves world and output untouched',()=>{
  const s=scenario();s.plan();assert.equal(s.stats().writes,0);
  assert.equal(s.stats().files.size,0);
  assert(s.messages.some(m=>m.includes('65536')));
});

console.log(`P1.6 mock tests ${checks}/${checks} PASS`);
