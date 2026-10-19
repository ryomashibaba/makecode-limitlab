// G4-C C0 offline voxel model: geometry, safe execution and pedestrian grade; not hardware.
const assert = require('assert'), fs=require('fs'), vm=require('vm'), path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../build/limitlab_g4c_a1.js'),'utf8');
const ROOT='__G4C_ROOT__/',LATCH=ROOT+'logs/G4C_ONCE.txt',CSV=ROOT+'results/USER_UPLOAD_THIS_G4C_STATUS.csv';
const M={AIR:0,WHITE_CONCRETE:1,LIGHT_GRAY_CONCRETE:2,BLACK_CONCRETE:3,
 CYAN_STAINED_GLASS:4,LIGHT_BLUE_STAINED_GLASS:5,CYAN_CONCRETE:6,
 GREEN_CONCRETE:7,BROWN_CONCRETE:8};
const familyHeight=[52,68,56], families=['slender','broad','dual_wing'];
function simulation(o={}) {
 const cells=new Map(), files=o.files||new Map(o.noLatch?[]:[[LATCH,'READY_G4C']]);
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
    if(o.stopPause===pauses)handlers.labstopg4c();
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
 const run=()=>handlers.labcityg4c();
 return {block,stats,logs,files,run,
         area:()=>handlers.labareag4c(),status:()=>handlers.labstatusg4c(),
         report:()=>handlers.labreportg4c(),stop:()=>handlers.labstopg4c(),
         csv:()=>files.get(CSV)||''};
}
let passed=0;function test(title,fn){fn();console.log('PASS',title);passed++;}
test('three real silhouettes, eight buildings, roads and monument are placed',()=>{
 const t=simulation();t.run();const p=t.stats();assert.equal(p.fill,386);
 assert.equal(p.clone,5);assert(p.checks>=118);
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
 assert.equal(t.block(138+6,5,18+4),M.CYAN_STAINED_GLASS);
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
 assert.equal(t.files.get(LATCH),'READY_G4C');
 assert(t.logs.some(x=>x.includes('PRECHECK BLOCKED SITE_NOT_AIR')));
});
test('already USED latch refuses construction without destroying prior files',()=>{
 const t=simulation({files:new Map([[LATCH,'USED_G4C']])});t.run();
 assert.equal(t.stats().fill,0);assert.equal(t.csv(),'');
 assert.equal(t.files.get(LATCH),'USED_G4C');
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
 assert.equal(t.files.get(LATCH),'READY_G4C');
 assert(t.logs.some(x=>x.includes('y96..179')));
 assert(!t.logs.some(x=>/[<>]/.test(x)),'chat parser operator text');
});
test('three roofs and five clones always stay within declared district',()=>{
 const t=simulation();t.run();
 assert.equal(t.stats().clone,5);
 assert(t.stats().maxClone<=262144);
 assert.equal(t.block(192,0,20),M.AIR);
});
test('nine plot sidewalks match the road surface at Y+1',()=>{
 const t=simulation();t.run();
 for(let row=0;row<3;row++)for(let col=0;col<3;col++){
   const x=12+60*col,z=12+60*row;
   assert.equal(t.block(x+1,1,z+10),M.WHITE_CONCRETE,'west sidewalk');
   assert.equal(t.block(x+46,1,z+10),M.WHITE_CONCRETE,'east sidewalk');
   assert.equal(t.block(x+10,1,z+1),M.WHITE_CONCRETE,'north sidewalk');
   assert.equal(t.block(x+10,1,z+46),M.WHITE_CONCRETE,'south sidewalk');
 }
});
test('zebra crosswalks visible on all 24 approaches, inside road boundary',()=>{
 const t=simulation();t.run();
 for(let road=0;road<4;road++)for(let seg=0;seg<3;seg++){
   const o=road*60,pos=22+seg*60;
   for(let bar=0;bar<3;bar++){
     assert.equal(t.block(pos+bar*3,1,o+2),M.WHITE_CONCRETE,'horizontal zebra');
     assert.equal(t.block(o+2,1,pos+bar*3),M.WHITE_CONCRETE,'vertical zebra');
   }
 }
 assert.equal(t.block(5,0,20),M.BLACK_CONCRETE,'road base preserved');
});
test('every tower has a recessed entry and an uninterrupted sidewalk connection',()=>{
 const t=simulation();t.run();
 for(let row=0;row<3;row++)for(let col=0;col<3;col++){
  if(row===1&&col===1)continue;
  const px=12+col*60,pz=12+row*60,tx=px+6,tz=pz+6;
  const front=col===0?tz+6:col===1?tz:tz+4;
  const middle=col===2?tx+9:tx+18;
  assert.equal(t.block(middle,5,front),M.AIR,'real open doorway');
  assert.equal(t.block(middle,1,pz+3),M.WHITE_CONCRETE,'walkable front path');
  assert.equal(t.block(middle,2,front),M.AIR,'ground-level doorway clearance');
  assert.equal(t.block(middle,8,front-2),M.WHITE_CONCRETE,'entry canopy');
 }
});
test('sixteen shade trees have real trunks and green crowns without covering facades',()=>{
 const t=simulation();t.run();
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){
  if(c===1&&r===1)continue;
  const px=12+60*c,pz=12+60*r;
  for(const dx of [10,36]){
   assert.equal(t.block(px+dx,4,pz+3),M.BROWN_CONCRETE,'tree trunk');
   assert.equal(t.block(px+dx,7,pz+3),M.GREEN_CONCRETE,'green crown');
   assert.equal(t.block(px+dx+2,7,pz+4),M.GREEN_CONCRETE,'crown spread');
  }
 }
});
test('civic plaza is a public destination with four planted garden courts',()=>{
 const t=simulation();t.run();const px=72,pz=72;
 for(const dx of [10,31])for(const dz of [10,31]){
   assert.equal(t.block(px+dx,3,pz+dz),M.GREEN_CONCRETE,'garden');
   assert.equal(t.block(px+dx+2,4,pz+dz+2),M.CYAN_CONCRETE,'public sculpture');
 }
 assert.equal(t.block(px+20,1,pz+4),M.WHITE_CONCRETE,'north public path');
 assert.equal(t.block(px+43,2,pz+23),M.WHITE_CONCRETE,'east public path');
 assert.equal(t.block(px+22,5,pz+22),M.CYAN_CONCRETE,'civic monument unchanged');
});
test('no planting or path destroys foundation/roof checks after clones',()=>{
 const t=simulation();t.run();const final=t.csv();
 assert(final.includes('SAMPLE,28,28,PASS'));
 assert(final.includes('G4C,RUN,1,1,FINISHED'));
 assert(t.stats().maxFill<=32768);
 assert(t.stats().clone===5);
});


test('all twelve internal crosswalks are flush paths with two blocks of headroom',()=>{
 const t=simulation();t.run();
 function continuous(cells) {
  for(const [x,z] of cells) {
   assert.notEqual(t.block(x,1,z),M.AIR,'missing ground at '+x+','+z);
   assert.equal(t.block(x,2,z),M.AIR,'1st obstructed at '+x+','+z);
   assert.equal(t.block(x,3,z),M.AIR,'2nd obstructed at '+x+','+z);
  }
 }
 for(const road of [60,120])for(const pos of [22,82,142]) {
  continuous(Array.from({length:14},(_,i)=>[pos,road-1+i]));
  continuous(Array.from({length:14},(_,i)=>[road-1+i,pos]));
 }
 assert.equal(t.block(3,1,34),M.BLACK_CONCRETE,'asphalt shares zebra grade');
});
test('all tower entries have a continuous Y+1 approach, no two-block doorstep',()=>{
 const t=simulation();t.run();
 for(let row=0;row<3;row++)for(let col=0;col<3;col++){
  if(row===1&&col===1)continue;
  const px=12+col*60,pz=12+row*60;
  const tx=px+6,tz=pz+6;
  const front=col===0?tz+6:col===1?tz:tz+4;
  const middle=col===2?tx+9:tx+18;
  for(let z=pz+2;z<=front;z++) {
   assert.notEqual(t.block(middle,1,z),M.AIR,'approach is not solid');
   assert.equal(t.block(middle,2,z),M.AIR,'approach head blocked at '+z);
   assert.equal(t.block(middle,3,z),M.AIR,'approach head blocked above '+z);
  }
 }
});
test('pedestrian graph connects central plaza to all eight actual doorways',()=>{
 const t=simulation();t.run(),size=192;
 const seen=new Uint8Array(size*size),queue=[94+76*size];
 seen[queue[0]]=1;
 let head=0;
 while(head<queue.length){
  const k=queue[head++],x=k%size,z=Math.floor(k/size);
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]]){
   const xx=x+dx,zz=z+dz;
   if(xx<0||xx>=size||zz<0||zz>=size)continue;
   const nk=xx+zz*size;
   if(seen[nk])continue;
   if(t.block(xx,1,zz)===M.AIR||t.block(xx,2,zz)!==M.AIR||t.block(xx,3,zz)!==M.AIR)continue;
   seen[nk]=1;queue.push(nk);
  }
 }
 for(let row=0;row<3;row++)for(let col=0;col<3;col++){
  if(row===1&&col===1)continue;
  const px=12+col*60,pz=12+row*60,tx=px+6,tz=pz+6;
  const front=col===0?tz+6:col===1?tz:tz+4;
  const middle=col===2?tx+9:tx+18;
  assert.equal(seen[middle+front*size],1,'unreachable doorway at '+middle+','+front);
 }
});

console.log('G4C voxel simulations '+passed+'/'+passed+' PASS');
