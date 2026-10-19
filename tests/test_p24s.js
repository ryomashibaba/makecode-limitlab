// P2.4S offline voxel simulation; does NOT establish Minecraft hardware success.
const assert=require('assert'),fs=require('fs'),vm=require('vm'),path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../build/limitlab_p24s_r2.js'),'utf8');
const ROOT='__P24S_ROOT__/',LATCH=ROOT+'logs/P24S_ONCE.txt',PLOT=[18,78,138],H=[40,64,48];
function simulation(o={}) {
 const cells=new Map(),files=o.files||new Map(o.noLatch?[]:[[LATCH,'READY_P24S']]);
 const listeners={},chat=[],cloneSizes=[];
 let fillCalls=0,cloneCalls=0,checks=0,maxFill=0,maxClone=0,pauses=0;
 const key=p=>p.x+','+p.y+','+p.z;
 const get=p=>cells.get(key(p))||0;
 const put=(p,n)=>{if(n===0)cells.delete(key(p));else cells.set(key(p),n);};
 const volume=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 const each=(a,b,f)=>{for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)f({x,y,z});};
 const at=(x,y,z)=>({x:16+x,y:96+y,z:24+z});
 if(o.occupiedStart)put(at(0,0,0),99);
 if(o.occupiedMiddle)put(at(48,36,48),99);
 if(o.undetectedOld)put(at(20,12,21),99);
 const api={
  Math,AIR:0,STONE:1,GOLD_BLOCK:2,Axis:{X:0,Y:1,Z:2},
  FillOperation:{Replace:0},CloneMask:{Replace:0},CloneMode:{Normal:0},
  TestForBlocksMask:{All:0},world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(n,f)=>listeners[n]=f,say:t=>chat.push(t)},
  file:{readFile:p=>o.invalidCsv&&p.endsWith('.csv')&&files.has(p)?'WRONG':(o.missingCsvReturnsNonempty&&p.endsWith('.csv')&&!files.has(p)?'FILE_MISSING_ERROR':files.get(p)||''),
   writeFile:(p,v)=>{if(o.dropLatch&&p.endsWith('P24S_ONCE.txt'))return;files.set(p,v);}},
  loops:{runInBackground:f=>f(),pause:ms=>{
    assert.equal(ms,1);pauses++;
    if(o.stopPause===pauses)listeners.labstop24s();
    if(o.stopStage&&api.p24sStage===o.stopStage&&!o.stopped){
      o.stopped=true;listeners.labstop24s();
    }
  }},
  blocks:{
   testForBlock:(id,p)=>{checks++;return get(p)===id;},
   testForBlocks:()=>{throw Error('P2.4S FAST unexpectedly used full block checks');},
   fill:(id,a,b)=>{
    fillCalls++;const n=volume(a,b);maxFill=Math.max(maxFill,n);
    assert(n>0&&n<=32768,'unsafe fill');
    if(o.dropFill===fillCalls)return;
    each(a,b,p=>{
      assert(p.x>=16&&p.x<208&&p.y>=96&&p.y<180&&p.z>=24&&p.z<216,'fill outside district');
      put(p,id);
    });
   },
   clone:(a,b,d)=>{
    cloneCalls++;const n=volume(a,b);cloneSizes.push(n);
    maxClone=Math.max(maxClone,n);assert(n<=262144,'unsafe clone');
    if(o.rejectClone===cloneCalls)return false;
    let i=0;const changes=[];
    each(a,b,p=>{
      if(!o.partialClone||i++<128)
        changes.push([{x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p)]);
    });
    for(const [p,id] of changes){
      assert(p.x>=16&&p.x<208&&p.y>=96&&p.y<180&&p.z>=24&&p.z<216,'clone outside district');
      put(p,id);
    }
    if(o.corruptClone===cloneCalls)put({x:d.x,y:d.y+4,z:d.z},99);
    return true;
   }
  }
 };
 vm.runInNewContext(code,api,{timeout:90000});
 const rows=()=>files.get(ROOT+'results/USER_UPLOAD_THIS_P24S_STATUS.csv')||'';
 const stat=()=>({fillCalls,cloneCalls,checks,maxFill,maxClone,cloneSizes,pauses,files,cells});
 const block=(x,y,z)=>get(at(x,y,z));
 function skyline() {
  for(let r=0;r<3;r++)for(let c=0;c<3;c++){
   if(r===1&&c===1)continue;
   const x=PLOT[c],z=PLOT[r];
   assert.equal(block(x,4,z),2,'tower corner '+c+','+r);
   assert.equal(block(x+6,1,z+6),1,'foundation '+c+','+r);
   assert.equal(block(x+6,8,z+6),1,'interior floor '+c+','+r);
   assert.equal(block(x+3,4,z+3),0,'open interior '+c+','+r);
   assert.equal(block(x+3,H[c]-1,z+3),1,'roof '+c+','+r);
  }
  assert.equal(block(94,5,94),2,'plaza');
  for(const n of [5,65,125,185]){
   assert.equal(block(n,0,20),1,'x road '+n);
   assert.equal(block(20,0,n),1,'z road '+n);
   assert.equal(block(n,1,20),2,'x road marking '+n);
  }
  assert.equal(block(1,2,1),2,'gateway');
  assert.equal(block(192,0,20),0,'out-of-bounds write');
 }
 function cloneExact() {
  for(const [c,r] of [[0,1],[2,1],[0,2],[1,2],[2,2]]){
   for(let y=0;y<H[c];y++)for(let dz=0;dz<36;dz++)for(let dx=0;dx<36;dx++)
    assert.equal(block(PLOT[c]+dx,y,PLOT[r]+dz),
      block(PLOT[c]+dx,y,PLOT[0]+dz),'clone not exact '+c+','+r);
  }
 }
 return {run:()=>listeners.labcity24s(),status:()=>listeners.labstatus24s(),
  area:()=>listeners.labarea24s(),report:()=>listeners.labreport24s(),
  stop:()=>listeners.labstop24s(),rows,stat,block,skyline,cloneExact,chat,files};
}
let n=0;function test(name,fn){fn();n++;console.log('PASS',name);}
test('metro city creates 8 towers, center monument, road grid and five mixed-material clones',()=>{
 const t=simulation();t.run();const s=t.stat(),r=t.rows();
 assert(r.includes('FINISHED,FAST_COMPLETED_SAMPLED_'));
 assert(s.fillCalls>80&&s.fillCalls<180,'fill budget '+s.fillCalls);
 assert.equal(s.cloneCalls,5);assert(s.checks<180);
 assert(s.maxFill<=32768&&s.maxClone<=262144);
 t.skyline();t.cloneExact();
});
test('five prefab volume requests stay bounded and use three source families',()=>{
 const t=simulation();t.run();assert.deepEqual(t.stat().cloneSizes,
  [36*(40+13)*36,36*(48+13)*36,36*(40+13)*36,36*(64+13)*36,36*(48+13)*36]);
});
test('eight rooftops survive partial modification and plaza is open',()=>{
 const t=simulation();t.run();t.cloneExact();
 assert.equal(t.block(94,5,94),2);
 assert.equal(t.block(94,30,94),0);
});
test('occupied origin is read-only failure and leaves retry latch READY',()=>{
 const t=simulation({occupiedStart:true});t.run();
 assert.equal(t.stat().fillCalls,0);
 assert.equal(t.rows(),'');
 assert.equal(t.files.get(LATCH),'READY_P24S');
 assert(t.chat.some(x=>x.includes('PRECHECK BLOCKED SITE_NOT_AIR')));
});
test('blocked high point keeps latch unconsumed, with no CSV overwrite',()=>{
 const t=simulation({occupiedMiddle:true});t.run();
 assert.equal(t.stat().fillCalls,0);
 assert.equal(t.rows(),'');
 assert.equal(t.files.get(LATCH),'READY_P24S');
});
test('persistent latch absence blocks start without writing CSV',()=>{
 const t=simulation({noLatch:true});t.run();
 assert.equal(t.stat().fillCalls,0);assert.equal(t.rows(),'');
});
test('used latch blocks later restart',()=>{
 const t=simulation({files:new Map([[LATCH,'USED_P24S']])});t.run();
 assert.equal(t.stat().fillCalls,0);assert.equal(t.rows(),'');
});
test('latch readback failure stops before construction',()=>{
 const t=simulation({dropLatch:true});t.run();
 assert.equal(t.stat().fillCalls,0);
 assert(t.chat.some(x=>x.includes('LATCH_READBACK_FAILED')));
});
test('CSV corruption aborts before planning and construction',()=>{
 const t=simulation({invalidCsv:true});t.run();
 assert.equal(t.stat().fillCalls,0);
 assert(t.chat.some(x=>x.includes('CSV_READBACK_FAILED')));
});
test('cooperative stop before construction does not spend latch or write CSV',()=>{
 const t=simulation({stopPause:3});t.run();
 assert.equal(t.stat().fillCalls,0);
 assert.equal(t.rows(),'');
 assert.equal(t.files.get(LATCH),'READY_P24S');
});
test('cooperative stop during roads prevents prototype and clones',()=>{
 const t=simulation({stopStage:'ROADS'});t.run();
 assert.equal(t.stat().cloneCalls,0);
 assert(t.rows().includes('STOP,USER_STOP'));
 assert(!t.rows().includes('PROTOTYPES,'));
});
test('first clone return false prevents any further construction',()=>{
 const t=simulation({rejectClone:1});t.run();
 assert.equal(t.stat().cloneCalls,1);
 assert(t.rows().includes('STOP,CLONE_RETURN_FALSE_AT_0'));
 assert(!t.rows().includes('PLAZA,'));
});
test('corrupt first clone corner rejected immediately',()=>{
 const t=simulation({corruptClone:1});t.run();
 assert.equal(t.stat().cloneCalls,1);
 assert(t.rows().includes('STOP,CLONE_STRUCTURE_SAMPLE_FAILED_0'));
});
test('repeat invocation and read-only commands never rewrite completed city',()=>{
 const t=simulation();t.run();const s=t.stat(),r=t.rows();
 t.run();t.report();t.status();t.area();
 assert.equal(t.stat().fillCalls,s.fillCalls);
 assert.equal(t.stat().cloneCalls,s.cloneCalls);
 assert.equal(t.rows(),r);
});
test('site preview is read-only and does not consume latch',()=>{
 const t=simulation();t.area();t.status();t.report();
 assert.equal(t.stat().fillCalls,0);assert.equal(t.rows(),'');
 assert.equal(t.files.get(LATCH),'READY_P24S');
 assert(t.chat.some(x=>x.includes('SITE x16..207 y96..179')));
});
test('FAST result is only sampled and does not claim universal city correctness',()=>{
 const t=simulation({undetectedOld:true});t.run();
 assert(t.rows().includes('FAST_COMPLETED_SAMPLED'));
 assert(!t.rows().includes('VERIFY_PASS_EXACT'));
});
// Additional safety regressions below; final count printed last.

test('P2.4S preview at player y0 floats safely at fixed floor y96',()=>{
 const t=simulation();t.area();
 assert(t.chat.some(x=>x.includes('y96..179')));
 assert.equal(t.files.get(LATCH),'READY_P24S');
});
test('valid survey followed by already USED latch refuses any construction',()=>{
 const t=simulation({files:new Map([[LATCH,'USED_P24S']])});t.run();
 assert.equal(t.stat().fillCalls,0);
 assert.equal(t.rows(),'');
});
test('a missing-CSV read is not used to decide whether to spend the latch',()=>{
 // The actual File extension may return a nonempty error for a missing file.
 // Exclusive private folder creation is validated by the Windows preparer.
 const t=simulation({missingCsvReturnsNonempty:true});t.run();
 assert(t.rows().includes('FINISHED,FAST_COMPLETED_SAMPLED_'));
 assert.equal(t.files.get(LATCH),'USED_P24S');
 assert(t.stat().fillCalls>80);
});

test('preview chat text avoids operator tokens that Minecraft parses as invalid syntax',()=>{
 const t=simulation();t.area();
 assert(t.chat.some(x=>x.includes('sky deck starts at Y96')));
 assert(!t.chat.some(x=>/[<>]/.test(x)), 'raw angle bracket in world chat');
 assert.equal(t.files.get(LATCH),'READY_P24S');
 assert.equal(t.rows(),'');
});

console.log('P2.4S Minecraft offline simulations '+n+'/'+n+' PASS');
