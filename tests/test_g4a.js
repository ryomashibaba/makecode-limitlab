// G4-A offline voxel model: validates executable geometry, not Minecraft hardware.
const assert = require('assert'), fs=require('fs'), vm=require('vm'), path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../build/limitlab_g4a.js'),'utf8');
const ROOT='__G4A_ROOT__/',LATCH=ROOT+'logs/G4A_ONCE.txt',CSV=ROOT+'results/USER_UPLOAD_THIS_G4A_STATUS.csv';
const M={AIR:0,WHITE_CONCRETE:1,LIGHT_GRAY_CONCRETE:2,BLACK_CONCRETE:3,
 CYAN_STAINED_GLASS:4,LIGHT_BLUE_STAINED_GLASS:5,CYAN_CONCRETE:6};
const familyHeight=[52,68,56], families=['slender','broad','dual_wing'];
function simulation(o={}) {
 const cells=new Map(), files=o.files||new Map(o.noLatch?[]:[[LATCH,'READY_G4A']]);
 const logs=[], handlers={},boxCounts={fill:0,clone:0},cloneSizes=[];
 let checks=0,maxFill=0,maxClone=0,pauses=0;
 const at=(x,y,z)=>({x:16+x,y:96+y,z:24+z});
 const key=p=>p.x+','+p.y+','+p.z;
 const get=p=>cells.get(key(p))||0;
 const set=(p,v)=>v?cells.set(key(p),v):cells.delete(key(p));
 const every=(a,b,fn)=>{
   for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)
     fn({x,y,z});
 };
 const volume=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 if(o.occupied) set(at(0,0,0),99);
 const api={...M,Math,Axis:{X:0,Y:1,Z:2},FillOperation:{Replace:0},
  CloneMask:{Replace:0},CloneMode:{Normal:0},
  TestForBlocksMask:{All:0},world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(n,f)=>handlers[n]=f,say:t=>logs.push(t)},
  loops:{runInBackground:fn=>fn(),pause:ms=>{
    assert.equal(ms,1); pauses++;
    if(o.stopPause===pauses)handlers.labstopg4a();
  }},
  file:{readFile:p=>files.get(p)||'',
    writeFile:(p,v)=>{if(o.dropLatch&&p===LATCH)return;files.set(p,v);}},
  blocks:{
   testForBlock:(id,p)=>{checks++;return get(p)===id;},
   testForBlocks:()=>{throw Error('No costly full checks allowed')},
   fill:(id,a,b)=>{
     boxCounts.fill++;
     let n=volume(a,b);maxFill=Math.max(n,maxFill);
     assert(n>0&&n<=32768,'unsafe fill '+n);
     every(a,b,p=>{
       assert(p.x>=16&&p.x<208&&p.y>=96&&p.y<180&&p.z>=24&&p.z<216,'box escapes plot');
       set(p,id);
     });
   },
   clone:(a,b,d)=>{
     boxCounts.clone++;let n=volume(a,b);maxClone=Math.max(maxClone,n);
     cloneSizes.push(n);
     assert(n>0&&n<=262144,'unsafe clone '+n);
     if(o.rejectClone===boxCounts.clone)return false;
     const changes=[];
     every(a,b,p=>changes.push([{x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p)]));
     for(const [p,v] of changes){
       assert(p.x>=16&&p.x<208&&p.y>=96&&p.y<180&&p.z>=24&&p.z<216,'clone escapes');
       set(p,v);
     }
     return true;
   }
  }
 };
 vm.runInNewContext(code,api,{timeout:90000});
 const block=(x,y,z)=>get(at(x,y,z));
 const stats=()=>({fill:boxCounts.fill,clone:boxCounts.clone,checks,maxFill,maxClone,
                    cloneSizes,pauses,voxels:cells.size});
 const run=()=>handlers.labcityg4a();
 return {block,stats,logs,files,run,
         area:()=>handlers.labareag4a(),status:()=>handlers.labstatusg4a(),
         report:()=>handlers.labreportg4a(),stop:()=>handlers.labstopg4a(),
         csv:()=>files.get(CSV)||''};
}
let passed=0;function test(title,fn){fn();console.log('PASS',title);passed++;}
test('three real silhouettes, eight buildings, roads and monument are placed',()=>{
 const t=simulation();t.run();const p=t.stats();assert(p.fill>100&&p.fill<500);
 assert.equal(p.clone,5);assert(p.checks>=98);
 assert(p.maxFill<=32768&&p.maxClone<=262144);
 assert(t.csv().includes('FINISHED,FAST_COMPLETED_SAMPLED_'));
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){
   if(r===1&&c===1)continue;
   const x=18+60*c,z=18+60*r,h=familyHeight[c];
   assert.equal(t.block(x+6,1,z+6),M.WHITE_CONCRETE);
   assert.equal(t.block(x+6,h-1,z+6),M.WHITE_CONCRETE);
 }
 assert.equal(t.block(5,0,20),M.BLACK_CONCRETE);
 assert.equal(t.block(94,5,94),M.CYAN_CONCRETE);
});
test('slender, curtain-wall and twin-wing bodies have truly distinct profiles',()=>{
 const t=simulation();t.run();
 assert.equal(t.block(18,12,18),M.AIR,'set-back narrow silhouette');
 assert.equal(t.block(78,12,18),M.WHITE_CONCRETE,'broad facade corner');
 assert.equal(t.block(138+18,12,18+12),M.AIR,'open center between twin slabs');
 assert.equal(t.block(18+12,5,18+6),M.CYAN_STAINED_GLASS);
 assert.equal(t.block(78+11,5,18),M.LIGHT_BLUE_STAINED_GLASS);
 assert.equal(t.block(138+7,5,18+4),M.CYAN_STAINED_GLASS);
});
test('five customized clones have varying facade colors at unique positions',()=>{
 const t=simulation();t.run();const dest=[[0,1],[2,1],[0,2],[1,2],[2,2]];
 dest.forEach(([c,r],i)=>{
   const x=18+60*c,z=18+60*r;
   assert.equal(t.block(x+16,5,z+3),i%2===0?M.CYAN_CONCRETE:M.WHITE_CONCRETE);
 });
 assert.deepEqual(t.stats().cloneSizes,[36*65*36,36*69*36,36*65*36,36*81*36,36*69*36]);
});
test('survey of occupied air prevents writing/consuming one-shot latch',()=>{
 const t=simulation({occupied:true});t.run();
 assert.equal(t.stats().fill,0);
 assert.equal(t.csv(),'');
 assert.equal(t.files.get(LATCH),'READY_G4A');
 assert(t.logs.some(x=>x.includes('PRECHECK BLOCKED SITE_NOT_AIR')));
});
test('already USED latch refuses construction without destroying prior files',()=>{
 const t=simulation({files:new Map([[LATCH,'USED_G4A']])});t.run();
 assert.equal(t.stats().fill,0);assert.equal(t.csv(),'');
 assert.equal(t.files.get(LATCH),'USED_G4A');
});
test('latch write readback failure refuses all construction',()=>{
 const t=simulation({dropLatch:true});t.run();
 assert.equal(t.stats().fill,0);
 assert(t.logs.some(x=>x.includes('LATCH_READBACK_FAILED')));
});
test('failed clone is terminal; no plaza or later detail writes',()=>{
 const t=simulation({rejectClone:1});t.run();
 assert.equal(t.stats().clone,1);
 assert(t.csv().includes('STOP,CLONE_RETURN_FALSE_AT_0'));
 assert(!t.csv().includes('PLAZA,'));
});
test('repeat command never modifies completed city or logged CSV',()=>{
 const t=simulation();t.run();const a=t.stats(),csv=t.csv();
 t.run();t.area();t.status();t.report();
 assert.equal(t.stats().fill,a.fill);assert.equal(t.stats().clone,a.clone);assert.equal(t.csv(),csv);
});
test('read-only preview reports safe height with no output files',()=>{
 const t=simulation();t.area();
 assert.equal(t.csv(),'');assert.equal(t.stats().fill,0);
 assert.equal(t.files.get(LATCH),'READY_G4A');
 assert(t.logs.some(x=>x.includes('y96..179')));
 assert(!t.logs.some(x=>/[<>]/.test(x)),'chat parser operator text');
});
test('three roofs and five clones always stay within declared district',()=>{
 const t=simulation();t.run();
 assert.equal(t.stats().clone,5);
 assert(t.stats().maxClone<=262144);
 assert.equal(t.block(192,0,20),M.AIR);
});
console.log('G4A voxel simulations '+passed+'/'+passed+' PASS');
