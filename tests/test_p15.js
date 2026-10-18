// Minecraft Education API mock regression checks for P1.5 bounded volume study.
const assert = require('assert');
const vm = require('vm');
const fs = require('fs');
const path = require('path');
const source = fs.readFileSync(path.resolve(__dirname, '../build/limitlab_p1_5.js'), 'utf8');
function mock(options={}) {
  const cells=new Map(), files=new Map(), handlers={}, messages=[];
  let fills=0, clones=0, pauses=0, writes=0, maxFill=0, maxClone=0;
  const key=p=>p.x+','+p.y+','+p.z;
  const get=p=>cells.get(key(p)) || 0;
  const put=(p,v)=>{cells.set(key(p),v);writes++;};
  const each=(a,b,fn)=>{
    for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)
      for(let x=a.x;x<=b.x;x++)fn({x,y,z});
  };
  const volume=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
  // Candidate #1 anchor = 8,12,12; next starts at z=92,172.
  for(const i of (options.blockCandidates||[])) cells.set(key({x:8,y:12,z:12+i*80}),99);
  const context={
    Math, AIR:0, STONE:1, GOLD_BLOCK:2,
    Axis:{X:0,Y:1,Z:2},FillOperation:{Replace:0},
    CloneMask:{Replace:0},CloneMode:{Normal:0},TestForBlocksMask:{All:0},
    world:(x,y,z)=>({x,y,z}),
    player:{
      position:()=>({getValue:()=>0}),
      onChat:(name,fn)=>{handlers[name]=fn;},
      say:(text)=>messages.push(text)
    },
    file:{
      writeFile:(n,v)=>files.set(n,v),
      readFile:n=>files.get(n)||''
    },
    loops:{pause:()=>{pauses++;if(options.stopOnPause===pauses)handlers.labstop15();},runInBackground:fn=>fn()},
    blocks:{
      testForBlock:(v,p)=>get(p)===v,
      testForBlocks:(a,b,d)=>{
        if(options.corruptDestination && d.x>=56 && a.x<40) return false;
        let matches=true;
        each(a,b,p=>{
          let target={x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z};
          if(get(p)!==get(target)) matches=false;
        });
        return matches;
      },
      fill:(v,a,b)=>{
        fills++; let size=volume(a,b); maxFill=Math.max(size,maxFill);
        assert(size<=1024,'fill upper bound violated');
        if(options.failFillAt===fills)return;
        each(a,b,p=>put(p,v));
      },
      clone:(a,b,d)=>{
        clones++;let size=volume(a,b);maxClone=Math.max(size,maxClone);
        assert(size<=4096,'clone upper bound violated');
        if(options.cloneReturnsFalse)return false;
        const values=[];each(a,b,p=>values.push([{
          x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p)]));
        values.forEach(([p,v])=>put(p,v));return true;
      }
    }
  };
  vm.runInNewContext(source,context,{timeout:30000});
  return {
    run:()=>handlers.labauto15(), plan:()=>handlers.labplan15(),
    stop:()=>handlers.labstop15(),status:()=>handlers.labstatus15(),
    rows:()=>[...files.values()].find(v=>typeof v==='string'&&v.startsWith('Version,Stage,Completed,Total'))||'',
    stats:()=>({fills,clones,writes,pauses,maxFill,maxClone,files,cells,messages}),
    messages,handlers
  };
}
function test(label,fn){fn();console.log('PASS',label);}
test('32768 segmented source/fill/clone fully verified',()=>{
  const s=mock();s.run();const r=s.rows(),st=s.stats();
  assert(r.includes('P1.5,SOURCE,32768,32768,PASS'));
  assert(r.includes('P1.5,FILL32768,32768,32768,PASS'));
  assert(r.includes('P1.5,CLONE32768,32768,32768,PASS'));
  assert(r.includes('P1.5,RUN,1,1,PASS,32768_SOURCE_FILL_CLONE_EXACT'));
  assert.equal(st.clones,8);assert.equal(st.fills,64);
  assert.equal(st.maxFill,1024);assert.equal(st.maxClone,4096);
  assert.equal(st.writes,98304);
});
test('candidate occupied finds alternative and preserves occupied block',()=>{
  const s=mock({blockCandidates:[0]});s.run();
  assert(s.rows().includes('P1.5,PREFLIGHT,2,3,PASS'));
  assert.equal(s.stats().cells.get('8,12,12'),99);
  assert(s.rows().includes('32768_SOURCE_FILL_CLONE_EXACT'));
});
test('no safe region refuses all changes',()=>{
  const s=mock({blockCandidates:[0,1,2]});s.run();
  assert(s.rows().includes('STOP,NO_EMPTY_SAFE_REGION'));
  assert.equal(s.stats().writes,0);
  assert.equal(s.stats().fills,0);
});
test('failed fill verification fails closed before clone',()=>{
  const s=mock({failFillAt:1});s.run();
  assert(s.rows().includes('STOP,SOURCE_SEED_MISMATCH'));
  assert.equal(s.stats().clones,0);
});
test('clone false stops and prevents final PASS',()=>{
  const s=mock({cloneReturnsFalse:true});s.run();
  assert(s.rows().includes('STOP,CLONE_RETURN_FALSE'));
  assert(!s.rows().includes('32768_SOURCE_FILL_CLONE_EXACT'));
});
test('full-volume comparison detects clone corruption',()=>{
  const s=mock({corruptDestination:true});s.run();
  assert(s.rows().includes('STOP,EXACT_TILE_MISMATCH'));
  assert(!s.rows().includes('32768_SOURCE_FILL_CLONE_EXACT'));
});
test('second command cannot overwrite test volume or CSV',()=>{
  const s=mock();s.run();const w=s.stats().writes,txt=s.rows();s.run();
  assert.equal(s.stats().writes,w);assert.equal(s.rows(),txt);
});
test('read-only 65536 plan does not write or build',()=>{
  const s=mock();s.plan();
  assert.equal(s.stats().writes,0);assert.equal(s.stats().files.size,0);
  assert(s.messages.some(x=>x.includes('65536')));
});
test('user stop during source build prevents later construction',()=>{
  // 8 air-reference and 12 preflight pauses, then first source heartbeat.
  const s=mock({stopOnPause:21});s.run();
  assert(s.rows().includes('STOP,USER_STOP'));
  assert(s.stats().writes>0);
  assert.equal(s.stats().clones,0);
  assert(!s.rows().includes('32768_SOURCE_FILL_CLONE_EXACT'));
});
