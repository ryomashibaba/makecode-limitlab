// G4-C1 A1 offline 372x372x84 typed-array voxel simulator (NOT hardware).
const assert=require('assert'), fs=require('fs'),vm=require('vm'),path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../build/limitlab_g4c4_a3.js'),'utf8');
const M={AIR:0,WHITE_CONCRETE:1,LIGHT_GRAY_CONCRETE:2,BLACK_CONCRETE:3,
 CYAN_STAINED_GLASS:4,LIGHT_BLUE_STAINED_GLASS:5,CYAN_CONCRETE:6,
 GREEN_CONCRETE:7,BROWN_CONCRETE:8};
const ROOT='__G4C4_ROOT__/',LATCH=ROOT+'logs/G4C4_ONCE.txt',CSV=ROOT+'results/USER_UPLOAD_THIS_G4C4_STATUS.csv';
function simulate(o={}){
 const SIZE=372, H=84,vox=new Uint8Array(SIZE*SIZE*H);
 const files=o.files||new Map([[LATCH,'READY_G4C4']]), handlers={},msgs=[];
 let fills=0,clones=0,checks=0, maxFill=0,maxClone=0;
 const idx=(x,y,z)=>{assert(x>=0&&x<SIZE&&z>=0&&z<SIZE&&y>=0&&y<H,
    'out of world: '+x+','+y+','+z);return (y*SIZE+z)*SIZE+x};
 const pos=p=>[p.x-16,p.y-96,p.z-24];
 const get=(x,y,z)=>vox[idx(x,y,z)];
 const put=(x,y,z,v)=>vox[idx(x,y,z)]=v;
 if(o.occupied)put(180,0,0,99);
 if(o.farOccupied)put(371,0,371,99);
 const blocks={
  testForBlock:(id,p)=>{checks++;const [x,y,z]=pos(p);return get(x,y,z)==id},
  fill:(id,a,b)=>{
   fills++;const [x,y,z]=pos(a),[X,Y,Z]=pos(b),n=(X-x+1)*(Y-y+1)*(Z-z+1);
   assert(n>0&&n<=32768,'unsafe fill '+n);maxFill=Math.max(maxFill,n);
   for(let j=y;j<=Y;j++)for(let k=z;k<=Z;k++)for(let i=x;i<=X;i++)put(i,j,k,id);
  },
  clone:(a,b,d)=>{
   clones++;if(clones===o.failClone)return false;
   const [x,y,z]=pos(a),[X,Y,Z]=pos(b),[dx,dy,dz]=pos(d);
   const w=X-x+1,h=Y-y+1,dw=Z-z+1,n=w*h*dw;
   assert(n>0&&n<=262144,'unsafe clone '+n);maxClone=Math.max(maxClone,n);
   // All source/dest boxes are disjoint in this construction plan.
   for(let yy=0;yy<h;yy++)for(let zz=0;zz<dw;zz++)for(let xx=0;xx<w;xx++)
     put(dx+xx,dy+yy,dz+zz,get(x+xx,y+yy,z+zz));
   return true;
  }
 };
 const sandbox={...M,Math,Axis:{X:0,Y:1,Z:2},
  FillOperation:{Replace:0},CloneMask:{Replace:0},CloneMode:{Normal:0},
  world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),onChat:(n,f)=>handlers[n]=f,say:t=>msgs.push(t)},
  file:{readFile:p=>files.get(p)||'',writeFile:(p,v)=>files.set(p,v)},
  blocks,
  loops:{runInBackground:fn=>fn(),pause:n=>assert.equal(n,1)}
 };
 vm.runInNewContext(code,sandbox,{timeout:120000});
 const run=()=>handlers.labcityg4c4();
 return {run,files,msgs,get,stats:()=>({fills,clones,checks,maxFill,maxClone}),csv:()=>files.get(CSV)||'',preview:()=>handlers.labareag4c4()};
}
let count=0;function test(name,fn){fn();console.log('PASS',name);count++}
test('real 2x2 MakeCode plan completes with 32 buildings, 4 parks and 49 clones',()=>{
 const t=simulate();t.run(),s=t.stats();
 assert.equal(s.fills,563);assert.equal(s.clones,49);assert.equal(s.checks,395);
 assert(s.maxFill<=32768&&s.maxClone<=262144);
 assert(t.csv().includes('G4C4,RUN,1,1,FINISHED,FAST_COMPLETED_SAMPLED_fill563_clone49_checks395_towers32'));
 assert(t.csv().includes('G4C4,DISTRICT_SAMPLE,18,18,PASS'));
 for(const [xx,zz] of [[0,0],[180,0],[0,180],[180,180]]){
  assert.equal(t.get(xx+94,5,zz+94),M.CYAN_CONCRETE,'missing civic center');
  assert.equal(t.get(xx+24,1,zz+24),M.WHITE_CONCRETE,'missing building core');
  assert.equal(t.get(xx+22,1,zz+62),M.WHITE_CONCRETE,'missing pedestrian crossing');
 }
 // The only tall perimeter markers are the four far outside city corners.
 for(const x of [2,368])for(const z of [2,368])
   assert.equal(t.get(x,3,z),M.WHITE_CONCRETE,'missing outer marker');
 for(const [x,z] of [[181,1],[1,181],[181,181]])
   assert.equal(t.get(x,3,z),M.AIR,'pillar obstructs shared road junction');
 for(const z of [34,214,363])assert.equal(t.get(363,1,z),M.BLACK_CONCRETE);
 assert.equal(t.get(34,1,363),M.BLACK_CONCRETE);
});
test('site occupancy in distant district prevents all writes and leaves latch READY',()=>{
 const t=simulate({occupied:true});t.run();assert.equal(t.stats().fills,0);
 assert.equal(t.stats().clones,0);assert.equal(t.files.get(LATCH),'READY_G4C4');
 assert.equal(t.csv(),'');
 assert(t.msgs.some(x=>x.includes('SITE_NOT_AIR')));
});
test('far outer-edge road occupancy also blocks before spending latch',()=>{
 const t=simulate({farOccupied:true});t.run();
 assert.equal(t.stats().fills,0);assert.equal(t.stats().clones,0);
 assert.equal(t.files.get(LATCH),'READY_G4C4');
});
test('one-shot USED latch refuses construction',()=>{
 const f=new Map([[LATCH,'USED_G4C4']]),t=simulate({files:f});
 t.run();assert.equal(t.stats().fills,0);assert.equal(t.stats().clones,0);
 assert.equal(t.files.get(LATCH),'USED_G4C4');
});
test('failed first tile never finishes or retries; records STOP',()=>{
 const t=simulate({failClone:6});t.run();
 assert.equal(t.stats().clones,6);assert.equal(t.files.get(LATCH),'USED_G4C4');
 assert(t.csv().includes('G4C4,RUN,'));
 assert(t.csv().includes('STOP,TILE_CLONE_FAILED_0'));
 assert(!t.csv().includes('FINISHED'));
});
test('repeat command cannot restart the spent construction',()=>{
 const t=simulate();t.run();const s=t.stats(),csv=t.csv();
 t.run();const after=t.stats();
 assert.deepEqual(after,s);assert.equal(t.csv(),csv);
});


test('post-tile overlays produce genuinely distinct large district signatures',()=>{
 const t=simulate();t.run();
 assert(t.csv().includes('G4C4,A2_OVERLAY,61,61,PASS'));
 assert(t.csv().includes('G4C4,A2_SAMPLE,22,22,PASS'));
 assert.equal(t.get(90,82,30),M.LIGHT_GRAY_CONCRETE,'finance long crown missing');
 assert.equal(t.get(260,16,80),M.WHITE_CONCRETE,'cultural civic hall posts missing');
 assert.equal(t.get(90,81,210),M.GREEN_CONCRETE,'garden roof missing');
 assert.equal(t.get(242,39,218),M.CYAN_STAINED_GLASS,'research skybridge glazing missing');
 // Base grade and road surfaces must remain byte identical across 4 core districts.
 for(let z=0;z<180;z++)for(let x=0;x<180;x++){
  const baseline=t.get(x,1,z);
  assert.equal(t.get(x+180,1,z),baseline,'cultural pedestrian grade changed');
  assert.equal(t.get(x,1,z+180),baseline,'green pedestrian grade changed');
  assert.equal(t.get(x+180,1,z+180),baseline,'tech pedestrian grade changed');
 }
 // R1 empty-top guard applied BEFORE overlay: selected rooftop y76 remains
 // intact on every cloned district. A2 may then occupy previously empty y78+.
 for(const [dx,dz] of [[0,0],[180,0],[0,180],[180,180]]){
    assert.equal(t.get(dx+91,76,dz+31),M.WHITE_CONCRETE);
 }
});
test('all four districts have independent architectural massing above base roofs',()=>{
 const t=simulate();t.run();
 const signatures=[];
 for(const [dx,dz] of [[0,0],[180,0],[0,180],[180,180]]){
   let count=0, green=0,cyan=0,glass=0;
   for(let z=12;z<172;z++)for(let x=12;x<172;x++)
      for(let y=30;y<=83;y++){
        let v=t.get(dx+x,y,dz+z);
        if(v!==M.AIR)count++;
        if(v===M.GREEN_CONCRETE)green++;
        if(v===M.CYAN_CONCRETE)cyan++;
        if(v===M.CYAN_STAINED_GLASS)glass++;
      }
   signatures.push([count,green,cyan,glass]);
 }
 assert(signatures.every(v=>v[0]>0),'each district must have an observable skyline');
 assert.equal(new Set(signatures.map(v=>v.join(','))).size,4,'identical massing across districts');
 assert(signatures[2][1]>500,'residential large-scale greenery insufficient');
});

test('A2-A2 finances civic gateway legs truly meet civic Y+1 floor',()=>{
 const t=simulate();t.run();
 for(const x of [86,104]){
   assert.notEqual(t.get(x,1,86),M.AIR,'plaza under gateway is absent');
   for(let y=2;y<=50;y++)
     assert.equal(t.get(x,y,86),M.WHITE_CONCRETE,'air gap in civic support at '+x+','+y);
   assert.equal(t.get(x,51,86),M.CYAN_CONCRETE,'gate crossbeam not attached at '+x);
 }
});
test('culture canopy and garden roof supports have continuous facade connections',()=>{
 const t=simulate();t.run();
 const supports=[
   [204,25,14,60,61],[224,44,14,60,61],
   [324,25,14,64,65],[345,44,14,64,65],
   [24,205,18,58,59],[46,226,18,58,59],
   [85,205,30,77,78],[106,226,30,77,78],
   [144,325,20,62,63],[165,345,20,62,63],
 ];
 for(const [x,z,y1,y2,roofY] of supports){
   for(let y=y1;y<=y2;y++)
     assert.notEqual(t.get(x,y,z),M.AIR,'broken facade rib (including attached floor contact) at '+x+','+y+','+z);
   assert.notEqual(t.get(x,roofY,z),M.AIR,'roof slab missing above facade support');
 }
});


test('all eight attached wings contain real storeys, side entrances and roof supports',()=>{
 const t=simulate();t.run(), wings=[
  [0,104,25,48,M.CYAN_CONCRETE],[0,44,145,38,M.LIGHT_GRAY_CONCRETE],
  [1,44,24,46,M.LIGHT_GRAY_CONCRETE],[1,164,144,38,M.CYAN_CONCRETE],
  [2,44,82,46,M.GREEN_CONCRETE],[2,164,24,38,M.GREEN_CONCRETE],
  [3,44,144,49,M.CYAN_CONCRETE],[3,164,84,42,M.LIGHT_GRAY_CONCRETE]
 ];
 assert(t.csv().includes('G4C4,A3_MASSING,116,116,PASS'));
 assert(t.csv().includes('G4C4,A3_SAMPLE,12,12,PASS'));
 for(const [d,x,z,h,accent] of wings){
  const wx=x+(d%2)*180,wz=z+Math.floor(d/2)*180;
  assert.equal(t.get(wx+10,3,wz+13),M.AIR,'side-entry cut missing '+d);
  assert.equal(t.get(wx+13,7,wz+7),M.LIGHT_BLUE_STAINED_GLASS,
    'glazed facade missing'); // interior facade not identical to external post
  for(const [px,pz] of [[0,0],[13,0],[0,26],[13,26]])
   for(const y of [3,12,Math.min(h-2,30)])
     assert.equal(t.get(wx+px,y,wz+pz),M.WHITE_CONCRETE,'unsupported wing pillar');
  for(const y of [14,28])assert.equal(t.get(wx+7,y,wz+7),M.LIGHT_GRAY_CONCRETE,
       'multi-level floor missing '+d);
  if(h>=46)assert.equal(t.get(wx+7,40,wz+7),M.LIGHT_GRAY_CONCRETE,
       'upper occupied floor missing '+d);
  assert.equal(t.get(wx+7,h+5,wz+10),accent,'stepped thick roof missing '+d);
 }
});
test('A3 massing never rewrites Y+1 walking surfaces or shared twelve-wide roads',()=>{
 const t=simulate();t.run();
 for(let z=0;z<180;z++)for(let x=0;x<180;x++){
   const base=t.get(x,1,z);
   assert.equal(t.get(x+180,1,z),base);
   assert.equal(t.get(x,1,z+180),base);
   assert.equal(t.get(x+180,1,z+180),base);
 }
 for(const road of [60,120,180,240,300,360]){
   for(const coord of [5,15,55,75,115,135,175,195,235,255,295,315,355,365]){
     assert.equal(t.get(road+5,2,coord),M.AIR,'arterial blocked along Z');
     assert.equal(t.get(coord,2,road+5),M.AIR,'arterial blocked along X');
   }
 }
});
test('A3 remains a truly bounded append-only post-clone overlay, not new Clone',()=>{
 const t=simulate();t.run();const v=t.stats();
 assert.equal(v.clones,49);assert.equal(v.fills,563);assert.equal(v.checks,395);
 assert(v.maxFill<=32768&&v.maxClone<=262144);
});

console.log('G4C4 A3 simulated integration '+count+'/'+count+' PASS');
