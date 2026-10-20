// G4-C1 A1 offline 372x372x84 typed-array voxel simulator (NOT hardware).
const assert=require('assert'), fs=require('fs'),vm=require('vm'),path=require('path');
const code=fs.readFileSync(path.join(__dirname,'../build/limitlab_g4c5_a4a1.js'),'utf8');
const M={AIR:0,WHITE_CONCRETE:1,LIGHT_GRAY_CONCRETE:2,BLACK_CONCRETE:3,
 CYAN_STAINED_GLASS:4,LIGHT_BLUE_STAINED_GLASS:5,CYAN_CONCRETE:6,
 GREEN_CONCRETE:7,BROWN_CONCRETE:8};
const ROOT='__G4C5_ROOT__/',LATCH=ROOT+'logs/G4C5_ONCE.txt',CSV=ROOT+'results/USER_UPLOAD_THIS_G4C5_STATUS.csv';
function simulate(o={}){
 const SIZE=372, H=84,vox=new Uint8Array(SIZE*SIZE*H);
 const files=o.files||new Map([[LATCH,'READY_G4C5']]), handlers={},msgs=[];
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
 const run=()=>handlers.labcityg4c5();
 return {run,files,msgs,get,stats:()=>({fills,clones,checks,maxFill,maxClone}),csv:()=>files.get(CSV)||'',preview:()=>handlers.labareag4c5()};
}

// Tests below are a simplified voxel mobility model, NOT an actual Minecraft
// walking/step-height collision run; no GUI or player physics is involved.
const specs=[['A1',0,104,25,48],['A2',0,44,145,38],
 ['B1',1,44,24,46],['B2',1,164,144,38],
 ['C1',2,44,82,46],['C2',2,164,24,38],
 ['D1',3,44,144,49],['D2',3,164,84,42]];
let count=0;function test(name,fn){fn();console.log('PASS',name);count++}
test('all 8 wings: G4C5 one-shot construction & bounded 49 clones',()=>{
 const t=simulate();t.run();const a=t.stats();
 assert.equal(a.fills,871);assert.equal(a.clones,49);
 assert.equal(a.checks,431,'G4C5 checked '+a.checks+' samples; recent log='+t.csv().slice(-1100));
 assert(a.maxFill<=32768&&a.maxClone<=262144);
 assert(t.csv().includes('G4C5,A4_ACCESS,308,308,PASS'));
 assert(t.csv().includes('G4C5,A4_SAMPLE,36,36,PASS'));
 assert(t.csv().includes('G4C5,RUN,1,1,FINISHED,FAST_COMPLETED_SAMPLED_fill871_clone49_checks431_towers32'));
});
test('8 pockets, each new inner foyer, stair supports and 20 intermediate floors',()=>{
 const t=simulate();t.run();
 let total=0;
 for(const [label,d,rx,rz,h] of specs){
  const x=rx+(d%2)*180,z=rz+Math.floor(d/2)*180;
  assert.equal(t.get(x+10,2,z+13),M.AIR,label+' old street-accessible pocket blocked');
  assert.equal(t.get(x+1,2,z+20),M.AIR,label+' host foyer blocked');
  for(const [i,y] of [[0,2],[12,14],[26,28],...(h>=46?[[38,40]]:[])]){
   const xx=i<=8?10:i<=16?10-(i-8):i<=30?2:2+(i-30);
   const zz=i<=8?12-i:i<=16?4:i<=30?4+(i-16):18;
   assert.equal(t.get(x+xx,y,z+zz),M.WHITE_CONCRETE,
    label+' stair tread missing at '+i+' x'+xx+' z'+zz);
  }
  for(const y of [14,28,...(h>=46?[40]:[])]){
   total++;
   const px=y===14?x+6:y===28?x+1:x+10;
   const pz=y===14?z+3:y===28?z+14:z+19;
   assert.equal(t.get(px,y+1,pz),M.AIR,label+' landing headroom invalid at slab '+y);
   assert.notEqual(t.get(px,y,pz),M.AIR,label+' landing lacks solid floor at slab '+y);
  }
 }
 assert.equal(total,20);
});
test('existing 300-point AIR preflight and USED latch protect zero-write scenarios',()=>{
 for(const input of [{occupied:true},{farOccupied:true},{files:new Map([['__G4C5_ROOT__/logs/G4C5_ONCE.txt','USED_G4C5']])}]){
  const t=simulate(input);t.run();assert.equal(t.stats().fills,0);
  assert.equal(t.stats().clones,0);assert(!t.csv().includes('FINISHED'));
 }
});
test('all 4 regions Y+1 floor remains byte-identical',()=>{
 const t=simulate();t.run();
 for(let z=0;z<180;z++)for(let x=0;x<180;x++){
  const b=t.get(x,1,z);
  assert.equal(t.get(x+180,1,z),b);
  assert.equal(t.get(x,1,z+180),b);
  assert.equal(t.get(x+180,1,z+180),b);
 }
});
test('offline 2-cell standing and 1-step traversal reaches 8 true foyers and 20 floors',()=>{
 const t=simulate();t.run(), W=372,H=84,N=W*W*H,seen=new Uint8Array(N),queue=new Int32Array(N);
 const ix=(x,y,z)=>(y*W+z)*W+x;
 const empty=(x,y,z)=>x>=0&&x<W&&z>=0&&z<W&&y>=0&&y<H&&t.get(x,y,z)===M.AIR;
 const stand=(x,y,z)=>y>=2&&y<H-1&&empty(x,y,z)&&empty(x,y+1,z)&&!empty(x,y-1,z);
 let tail=0;
 const add=(x,y,z)=>{if(!stand(x,y,z))return;let n=ix(x,y,z);if(!seen[n]){seen[n]=1;queue[tail++]=n;}};
 for(let z=0;z<W;z++)for(let x=0;x<W;x++)if(x%60<12||z%60<12)add(x,2,z);
 for(let head=0;head<tail;head++){
  let n=queue[head],x=n%W,z=Math.floor(n/W)%W,y=Math.floor(n/(W*W));
  for(const [dx,dz] of [[1,0],[-1,0],[0,1],[0,-1]])for(const dy of [0,1,-1]){
   if(dy===1&&!empty(x,y+2,z))continue;
   if(dy===-1&&!empty(x+dx,y+1,z+dz))continue;
   add(x+dx,y+dy,z+dz);
  }
 }
 let roadFoyers=0,upper=0;
 const witness=[];
 for(const [label,d,rx,rz,h] of specs){
  let x=rx+(d%2)*180,z=rz+Math.floor(d/2)*180;
  let foyer=seen[ix(x+1,2,z+20)]!==0;
  roadFoyers+=foyer?1:0;
  for(const slab of [14,28,...(h>=46?[40]:[])]){
   let accessible=0,standable=0;
   for(let xx=x+1;xx<=x+11;xx++)for(let zz=z+1;zz<=z+26;zz++)
    if(stand(xx,slab+1,zz)){standable++;if(seen[ix(xx,slab+1,zz)])accessible++;}
   upper+=accessible>0?1:0;
   witness.push({label,slab,standable,accessible});
  }
  assert(foyer,label+' road -> actual inner room is blocked');
 }
 assert.equal(roadFoyers,8,'not all 8 wing foyers road-accessible');
 assert.equal(upper,20,'not all 20 storeys road-reachable: '+JSON.stringify(witness));
});
console.log('G4C5 offline accessibility '+count+'/'+count+' PASS — NOT HARDWARE WALKING');
