// G4-C1 A1 offline 372x372x84 typed-array voxel simulator (NOT hardware).
const assert=require('assert'), fs=require('fs'),vm=require('vm'),path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../build/limitlab_g4c1_a1.js'),'utf8');
const M={AIR:0,WHITE_CONCRETE:1,LIGHT_GRAY_CONCRETE:2,BLACK_CONCRETE:3,
 CYAN_STAINED_GLASS:4,LIGHT_BLUE_STAINED_GLASS:5,CYAN_CONCRETE:6,
 GREEN_CONCRETE:7,BROWN_CONCRETE:8};
const ROOT='__G4C1_ROOT__/',LATCH=ROOT+'logs/G4C1_ONCE.txt',CSV=ROOT+'results/USER_UPLOAD_THIS_G4C1_STATUS.csv';
function simulate(o={}){
 const SIZE=372, H=84,vox=new Uint8Array(SIZE*SIZE*H);
 const files=o.files||new Map([[LATCH,'READY_G4C1']]), handlers={},msgs=[];
 let fills=0,clones=0,checks=0, maxFill=0,maxClone=0;
 const idx=(x,y,z)=>{assert(x>=0&&x<SIZE&&z>=0&&z<SIZE&&y>=0&&y<H,
    'out of world: '+x+','+y+','+z);return (y*SIZE+z)*SIZE+x};
 const pos=p=>[p.x-16,p.y-96,p.z-24];
 const get=(x,y,z)=>vox[idx(x,y,z)];
 const put=(x,y,z,v)=>vox[idx(x,y,z)]=v;
 if(o.occupied)put(180,0,0,99);
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
 const run=()=>handlers.labcityg4c1();
 return {run,files,msgs,get,stats:()=>({fills,clones,checks,maxFill,maxClone}),csv:()=>files.get(CSV)||'',preview:()=>handlers.labareag4c1()};
}
let count=0;function test(name,fn){fn();console.log('PASS',name);count++}
test('real 2x2 MakeCode plan completes with 32 buildings, 4 parks and 52 clones',()=>{
 const t=simulate();t.run(),s=t.stats();
 assert.equal(s.fills,386);assert.equal(s.clones,52);assert.equal(s.checks,361);
 assert(s.maxFill<=32768&&s.maxClone<=262144);
 assert(t.csv().includes('G4C1,RUN,1,1,FINISHED,FAST_COMPLETED_SAMPLED_fill386_clone52_checks361_towers32'));
 assert(t.csv().includes('G4C1,DISTRICT_SAMPLE,18,18,PASS'));
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
 assert.equal(t.stats().clones,0);assert.equal(t.files.get(LATCH),'READY_G4C1');
 assert.equal(t.csv(),'');
 assert(t.msgs.some(x=>x.includes('SITE_NOT_AIR')));
});
test('one-shot USED latch refuses construction',()=>{
 const f=new Map([[LATCH,'USED_G4C1']]),t=simulate({files:f});
 t.run();assert.equal(t.stats().fills,0);assert.equal(t.stats().clones,0);
 assert.equal(t.files.get(LATCH),'USED_G4C1');
});
test('failed first tile never finishes or retries; records STOP',()=>{
 const t=simulate({failClone:6});t.run();
 assert.equal(t.stats().clones,6);assert.equal(t.files.get(LATCH),'USED_G4C1');
 assert(t.csv().includes('G4C1,RUN,'));
 assert(t.csv().includes('STOP,TILE_CLONE_FAILED_0'));
 assert(!t.csv().includes('FINISHED'));
});
test('repeat command cannot restart the spent construction',()=>{
 const t=simulate();t.run();const s=t.stats(),csv=t.csv();
 t.run();const after=t.stats();
 assert.deepEqual(after,s);assert.equal(t.csv(),csv);
});
console.log('G4C1 A1 simulated integration '+count+'/'+count+' PASS');
