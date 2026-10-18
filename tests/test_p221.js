// P2.2.1 offline voxel oracle and fault injection; NOT Minecraft hardware evidence.
const assert=require('assert'),fs=require('fs'),vm=require('vm'),path=require('path');
const compiled=fs.readFileSync(path.join(__dirname,'../build/limitlab_p2_2_1.js'),'utf8');
const ROOT='__P221_ROOT__/', LATCH=ROOT+'logs/P221_ONCE.txt';
function material(x,y,z,W,H,D,patch) {
 if(patch&&x>=16&&x<32&&y>=16&&y<32&&z>=16&&z<32)return 2;
 const a=Math.floor(x/8)*8,b=Math.floor(y/8)*8,c=Math.floor(z/8)*8;
 if(a%24===0&&c%24===0)return 2;
 if(a===0||c===0||a+8>=W||c+8>=D||b%16===0||b+8>=H)return 1;
 return 0;
}
function scenario(o={}) {
 const W=o.large?82:35,H=o.large?49:33,D=o.large?77:34,dst=W+16;
 const code=compiled.replace(/var P221_W = 82;/,'var P221_W = '+W+';')
 .replace(/var P221_H = 49;/,'var P221_H = '+H+';')
 .replace(/var P221_D = 77;/,'var P221_D = '+D+';');
 assert(code.includes('var P221_W = '+W+';'));
 const files=o.files||new Map(o.noLatch?[]:[[LATCH,'READY_P221']]);
 const cells=new Map(),handlers={},messages=[],calls=[];
 let fillCalls=0,cloneCalls=0,csvWrites=0,checks=0,pauses=0,maxFill=0,maxClone=0;
 const cloneSizes=[];
 const key=p=>p.x+','+p.y+','+p.z;
 const get=p=>cells.get(key(p))??0;
 const put=(p,v)=>{if(v===0)cells.delete(key(p));else cells.set(key(p),v);};
 const each=(a,b,f)=>{for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)f({x,y,z});};
 const volume=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 const origin={x:16,y:16,z:24};
 if(o.occupiedSample)put(origin,99);
 if(o.occupiedHalo)put({x:15,y:16,z:24},99);
 if(o.occupiedSiteGrid)put({x:16+Math.floor(W/2),y:16+Math.floor(H/2),
   z:24+Math.floor(D/2)},99);
 if(o.hiddenCorruption)put({x:36,y:40,z:44},99);
 const env={
  Math,AIR:0,STONE:1,GOLD_BLOCK:2,Axis:{X:0,Y:1,Z:2},
  FillOperation:{Replace:0},CloneMask:{Replace:0},CloneMode:{Normal:0},TestForBlocksMask:{All:0},
  world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(n,f)=>handlers[n]=f,say:s=>messages.push(s)},
  file:{readFile:p=>{if(o.badReadback&&p.endsWith('.csv'))return 'BAD';return files.get(p)||'';},
   writeFile:(p,v)=>{if(o.badLatchWrite&&p.endsWith('P221_ONCE.txt'))return;
    files.set(p,v);if(p.endsWith('.csv'))csvWrites++;}},
  loops:{runInBackground:f=>f(),pause:ms=>{assert.equal(ms,1);pauses++;
   if(o.monitorPlan && env.p221Stage==="PLAN" && env.p221Done>0 && !o._monitored){
     o._monitored=true;handlers.labstatus221();
   }
   if(o.stopAtPause===pauses)handlers.labstop221();}},
  blocks:{
   testForBlock:(id,p)=>{checks++;return get(p)===id;},
   testForBlocks:(a,b,d)=>{checks++;let same=true;each(a,b,p=>{
     if(get(p)!==get({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z}))same=false;});return same;},
   fill:(id,a,b)=>{fillCalls++;const n=volume(a,b);maxFill=Math.max(maxFill,n);
    assert(n<=32768,'oversize source fill');calls.push({kind:'fill',n,id});
    if(o.dropFill===fillCalls)return;
    each(a,b,p=>put(p,id));
    if(o.stopFill===fillCalls)handlers.labstop221();},
   clone:(a,b,d)=>{cloneCalls++;const n=volume(a,b);maxClone=Math.max(maxClone,n);
    cloneSizes.push(n);assert(n<=262144,'oversize clone');
    if(o.rejectClone===cloneCalls)return false;
    let i=0;each(a,b,p=>{if(!o.partialClone||i++<128)
      put({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p));});
    if(o.corruptClone===cloneCalls)put(d,99);
    return true;}
  }
 };
 vm.runInNewContext(code,env,{timeout:90000});
 const rows=()=>[...files.entries()].find(([p,v])=>p.endsWith('.csv')&&v.startsWith('Version,Stage,Units,Total'))?.[1]||'';
 const stats=()=>({files,cells,fillCalls,cloneCalls,csvWrites,checks,pauses,maxFill,maxClone,cloneSizes,calls});
 const assertExact=()=>{
  for(let y=0;y<H;y++)for(let z=0;z<D;z++)for(let x=0;x<W;x++){
   assert.equal(get({x:16+x,y:16+y,z:24+z}),material(x,y,z,W,H,D,false),'source '+x+','+y+','+z);
   assert.equal(get({x:16+dst+x,y:16+y,z:24+z}),material(x,y,z,W,H,D,true),'dest '+x+','+y+','+z);
  }
 };
 return {fast:()=>handlers.labfast221(),verify:()=>handlers.labverify221(),stop:()=>handlers.labstop221(),
 status:()=>handlers.labstatus221(),report:()=>handlers.labreport221(),plan:()=>handlers.labplan221(),
 area:()=>handlers.labarea221(),
 rows,stats,assertExact,messages};
}
let count=0;function test(name,fn){fn();count++;console.log('PASS',name);}
test('default 309386-block FAST uses <=90 fill and exactly two large clones',()=>{
 const s=scenario({large:true});s.fast();const h=s.stats(),r=s.rows();
 assert(r.includes('FINISHED,FAST_COMPLETED_SAMPLED_'));
 assert(h.cloneCalls===2);
 assert.deepEqual(h.cloneSizes,[82*40*77,82*9*77]);
 assert(h.fillCalls===69,'expected 68 source fills + 1 patch, got '+h.fillCalls);
 assert(r.includes('P2.2.1,PLAN,68,208010,PASS,'),'unexpected source plan ledger');
 assert(h.maxFill<=32768&&h.maxClone<=262144);
 assert(h.csvWrites<20,'too many CSV writes '+h.csvWrites);
 assert(h.checks<900,'too many FAST checks '+h.checks);
 s.assertExact();
});
test('partial-edge source and target correctly reconstructed in FAST',()=>{
 const s=scenario();s.fast();s.assertExact();assert(s.stats().cloneCalls===1);
});
test('VERIFY performs complete post-patch exact audit for small volume',()=>{
 const s=scenario();s.verify();s.assertExact();
 assert(s.rows().includes('VERIFY,2,2,PASS,source_and_patched_target_all_tiles_exact'));
 assert(s.rows().includes('FINISHED,VERIFY_PASS_EXACT_'));
});
test('full dimensions VERIFY confirms both exact volumes',()=>{
 const s=scenario({large:true});s.verify();s.assertExact();
 assert(s.rows().includes('FINISHED,VERIFY_PASS_EXACT_'));
 assert(s.stats().cloneCalls===2);
});
test('rejected clone stops without further calls',()=>{
 const s=scenario({rejectClone:1});s.fast();
 assert(s.rows().includes('STOP,CLONE_RETURN_FALSE_SLAB0'));
 assert(s.stats().cloneCalls===1);
});
test('partial clone with false return stops',()=>{
 const s=scenario({rejectClone:1,partialClone:true});s.fast();
 assert(s.stats().cloneCalls===1&&s.rows().includes('STOP,CLONE_RETURN_FALSE'));
});
test('corrupted first clone sample is detected',()=>{
 const s=scenario({corruptClone:1});s.fast();
 assert(s.rows().includes('STOP,CLONE_SENTINEL_MISMATCH'));
});
test('missing latch disallows all writes',()=>{
 const s=scenario({noLatch:true});s.fast();
 assert(s.stats().fillCalls===0);
 assert(s.messages.some(x=>x.includes('LATCH_ALREADY_USED_OR_NOT_READY')));
});
test('used latch disallows all writes',()=>{
 const s=scenario({files:new Map([[LATCH,'USED_P221']])});s.fast();
 assert(s.stats().fillCalls===0);
});
test('latch readback mismatch disallows construction',()=>{
 const s=scenario({badLatchWrite:true});s.fast();
 assert(s.stats().fillCalls===0);
 assert(s.messages.some(x=>x.includes('LATCH_READBACK_FAILED')));
});
test('occupied sample stops before first fill',()=>{
 const s=scenario({occupiedSample:true});s.fast();
 assert(s.stats().fillCalls===0&&s.rows().includes('STOP,SAMPLE_MISMATCH'));
});
test('occupied halo stops before first fill',()=>{
 const s=scenario({occupiedHalo:true});s.fast();
 assert(s.stats().fillCalls===0&&s.rows().includes('STOP,HALO_SAMPLE_NOT_AIR'));
});
test('CSV readback failure prevents construction',()=>{
 const s=scenario({badReadback:true});s.fast();
 assert(s.stats().fillCalls===0&&s.messages.some(x=>x.includes('CSV_READBACK_FAILED')));
});
test('cooperative stop during first fill prevents cloning',()=>{
 const s=scenario({stopFill:1});s.fast();
 assert(s.stats().cloneCalls===0&&s.rows().includes('STOP,USER_STOP'));
});
test('repeat and mode switch after run cannot touch world',()=>{
 const s=scenario();s.fast();const h=s.stats(),r=s.rows();
 s.verify();s.fast();assert(s.stats().fillCalls===h.fillCalls);
 assert(s.stats().cloneCalls===h.cloneCalls&&s.rows()===r);
});
test('read-only controls never write CSV or blocks',()=>{
 const s=scenario();s.plan();s.report();s.status();
 assert(s.stats().fillCalls===0&&s.stats().csvWrites===0);
});
test('FAST acknowledges a hidden error can pass sparse probes',()=>{
 const s=scenario({hiddenCorruption:true});s.fast();
 assert(s.rows().includes('FINISHED,FAST_COMPLETED_SAMPLED'));
 assert.throws(()=>s.assertExact());
});
test('VERIFY detects the same hidden error',()=>{
 const s=scenario({hiddenCorruption:true});s.verify();
 assert(s.rows().includes('STOP,FULL_MISMATCH'));
 assert(!s.rows().includes('FINISHED,VERIFY_PASS_EXACT'));
});
test('immediate ACK precedes worker latch check and CPU planning',()=>{
 const s=scenario();s.fast();
 const a=s.messages.findIndex(m=>m.includes('COMMAND RECEIVED FAST'));
 const b=s.messages.findIndex(m=>m.includes('WORKER ACTIVE'));
 const c=s.messages.findIndex(m=>m.includes('PLAN COMPLETE'));
 assert(a>=0 && b>a && c>b);
 assert(s.messages.some(m=>m.includes('PLANNING')));
});
test('planning yields and live status reports nonzero progress',()=>{
 const s=scenario({monitorPlan:true});s.fast();
 assert(s.messages.some(m=>m.includes('PLAN ') && m.includes('/125 fill')));
 assert(s.messages.some(m=>m.includes('PLAN COMPLETE')));
});
test('STOP while planning records final CSV and never writes Minecraft blocks',()=>{
 const s=scenario({stopAtPause:3});s.fast();
 assert(s.rows().includes('PLAN,0,125,BEGIN,cpu_only_no_world_writes'));
 assert(s.rows().includes('STOP,USER_STOP'));
 assert.strictEqual(s.stats().fillCalls,0);
 assert.strictEqual(s.stats().cloneCalls,0);
 assert(s.messages.some(m=>m.includes('TEST STOPPED')));
});
test('5x5x5 survey rejects hidden middle-region obstruction',()=>{
 const s=scenario({occupiedSiteGrid:true});s.fast();
 assert(s.rows().includes('STOP,SITE_NOT_AIR'));
 assert.strictEqual(s.stats().fillCalls,0);
 assert.strictEqual(s.stats().cloneCalls,0);
});
test('P221 latch is independent of USED_P22',()=>{
 const fs=new Map([[ROOT+'logs/P22_ONCE.txt','USED_P22'],[LATCH,'READY_P221']]);
 const s=scenario({files:fs});s.fast();s.assertExact();
 assert(s.rows().includes('FINISHED,FAST_COMPLETED_SAMPLED'));
 assert.strictEqual(fs.get(ROOT+'logs/P22_ONCE.txt'),'USED_P22');
 assert.strictEqual(fs.get(LATCH),'USED_P221');
});
test('site preview shows bounded coordinates but writes nothing',()=>{
 const s=scenario();s.area();
 assert(s.messages.some(m=>m.includes('SITE SOURCE x')));
 assert(s.messages.some(m=>m.includes('SITE TARGET x')));
 assert.strictEqual(s.stats().fillCalls,0);
 assert.strictEqual(s.stats().csvWrites,0);
});
console.log('P2.2.1 Minecraft simulation '+count+'/'+count+' PASS');
