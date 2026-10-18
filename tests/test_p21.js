// Independent voxel oracle and fault injection. NOT Minecraft hardware evidence.
const assert = require('assert'), fs = require('fs'), vm = require('vm'), path = require('path');
const compiled = fs.readFileSync(path.join(__dirname, '../build/limitlab_p2_1.js'), 'utf8');
function scenario(o = {}) {
 const W=o.large?82:35,H=o.large?49:33,D=o.large?77:34, dst=W+16, ref=2*W+40;
 let script=compiled.replace(/var P21_W = 82;/,'var P21_W = '+W+';')
  .replace(/var P21_H = 49;/,'var P21_H = '+H+';').replace(/var P21_D = 77;/,'var P21_D = '+D+';');
 if(o.invalid)script=script.replace(/var P21_CX = 32;/,'var P21_CX = 33;');
 const cells=new Map(),files=o.files||new Map([['__P21_ROOT__/logs/P21_ONCE.txt','READY_P21']]);
 const handlers={},messages=[],calls=[],csvs=[];
 let fills=0,clones=0,pauses=0,checks=0,reads=0,writes=0,firstWriteChecks=0,patches=0;
 const key=p=>p.x+','+p.y+','+p.z;
 const get=p=>cells.get(key(p))||0;
 const put=(p,id)=>{cells.set(key(p),id);};
 const each=(a,b,fn)=>{for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)fn({x,y,z});};
 const vol=(a,b)=>(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
 const cx=[16,-368,16,-368,400,16],cz=[24,24,-360,-360,24,408];
 for(const c of o.occupied||[])put({x:cx[c],y:16,z:cz[c]},99);
 if(o.occupiedTarget)put({x:16+dst+W-1,y:16+H-1,z:24+D-1},99);
 if(o.occupiedHalo)put({x:16-8,y:16-8,z:24-8},99);
 if(o.occupiedRef)put({x:16+ref+23,y:23,z:31},99);
 const origin={x:16,y:16,z:24};
 const sx=ref+32,sy=H+16,sz=D+16,coverage=new Uint8Array(sx*sy*sz);
 const coverIndex=p=>{
  const x=p.x-origin.x+8,y=p.y-origin.y+8,z=p.z-origin.z+8;
  return x>=0&&x<sx&&y>=0&&y<sy&&z>=0&&z<sz?x+sx*(y+sy*z):-1;
 };
 const mark=p=>{if(fills===0){const i=coverIndex(p);if(i>=0)coverage[i]=1;}};
 const env={Math,AIR:0,STONE:1,GOLD_BLOCK:2,Axis:{X:0,Y:1,Z:2},
  FillOperation:{Replace:0},CloneMask:{Replace:0},CloneMode:{Normal:0},TestForBlocksMask:{All:0},
  world:(x,y,z)=>({x,y,z}),
  player:{position:()=>({getValue:()=>0}),say:s=>messages.push(s),onChat:(n,f)=>handlers[n]=f},
  file:{readFile:p=>{reads++;if(o.badLatchRead&&p.endsWith('P21_ONCE.txt'))return 'BAD';
    if(o.badCSVRead&&p.endsWith('.csv'))return 'BAD';return files.get(p)||'';},
   writeFile:(p,s)=>{writes++;if(o.badLatchWrite&&p.endsWith('P21_ONCE.txt'))return;
    if(o.failLogAfterClone&&clones>0&&p.endsWith('.csv'))return;
    files.set(p,s);if(p.endsWith('.csv'))csvs.push(s);
    if(o.stopOnPatchLog&&s.endsWith('PATCH,0,8,WRITE,x16_y16_z16\n'))handlers.labstop21();}},
  loops:{runInBackground:f=>f(),pause:ms=>{assert.equal(ms,1);pauses++;
    if(o.stopPause===pauses)handlers.labstop21();}},
  blocks:{testForBlock:(id,p)=>{checks++;mark(p);return get(p)===id;},
   testForBlocks:(a,b,d)=>{checks++;let same=true;
    if(o.unloaded)return false;
    each(a,b,p=>{const q={x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z};mark(p);mark(q);if(get(p)!==get(q))same=false;});return same;},
   fill:(id,a,b)=>{if(!fills)firstWriteChecks=checks;fills++;calls.push({kind:'fill',id,a,b});
    assert(vol(a,b)<=512);if(o.dropFill===fills)return;
    each(a,b,p=>put(p,id));
    if(o.stopFill===fills)handlers.labstop21();
    if(a.x>=16+dst&&a.x<16+dst+W){patches++;
     if(o.corruptPatchOutside)put({x:16+dst+W-1,y:16+H-1,z:24+D-1},99);
     if(o.corruptSourceOnPatch)put({x:16+W-1,y:16+H-1,z:24+D-1},99);
    }
   },
   clone:(a,b,d)=>{clones++;calls.push({kind:'clone',a,b,d});assert(vol(a,b)<=16384);
    if(o.rejectClone===clones)return false;
    let index=0;each(a,b,p=>{if(!o.partialClone||index++<7)put({x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},get(p));});
    if(o.corruptClone===clones)put({x:d.x+b.x-a.x,y:d.y+b.y-a.y,z:d.z+b.z-a.z},99);
    if(o.spillClone===clones)put({x:16+dst+W,y:16,z:24},99);
    if(o.corruptSourceClone===clones)put(a,99);
    if(o.corruptRefClone===clones)put({x:16+ref,y:16,z:24},99);
    if(o.stopClone===clones)handlers.labstop21();
    return !o.falseExact;
   }}
 };
 vm.runInNewContext(script,env,{timeout:120000});
 return {run:()=>handlers.labauto21(),report:()=>{handlers.labstatus21();handlers.labreport21();handlers.labplan21();},
  csv:()=>files.get('__P21_ROOT__/results/USER_UPLOAD_THIS_P21_STATUS.csv')||'',
  stats:()=>({fills,clones,patches,checks,reads,writes,firstWriteChecks}),messages,calls,cells,files,csvs,W,H,D,dst,ref,origin,get,
  covered:p=>coverage[coverIndex(p)]===1};
}
function oracle(s) {
 const {W,H,D,dst,origin:o}=s;
 const material=(x,y,z)=>{
  const tx=Math.floor(x/8)*8,ty=Math.floor(y/8)*8,tz=Math.floor(z/8)*8;
  if(tx%24===0&&tz%24===0)return 2;
  return tx===0||tz===0||tx+8>=W||tz+8>=D||ty%16===0||ty+8>=H?1:0;
 };
 for(let y=-8;y<H+8;y++)for(let z=-8;z<D+8;z++)for(let x=-8;x<W+8;x++){
  const inside=x>=0&&x<W&&y>=0&&y<H&&z>=0&&z<D;
  const expected=inside?material(x,y,z):0;
  assert.equal(s.get({x:o.x+x,y:o.y+y,z:o.z+z}),expected,'source voxel');
  assert(s.covered({x:o.x+x,y:o.y+y,z:o.z+z}),'source and halo preflight coverage');
  const patch=inside&&x>=16&&x<32&&y>=16&&y<32&&z>=16&&z<32;
  assert.equal(s.get({x:o.x+dst+x,y:o.y+y,z:o.z+z}),patch?2:expected,'target voxel');
  assert(s.covered({x:o.x+dst+x,y:o.y+y,z:o.z+z}),'target and halo preflight coverage');
 }
 for(let x=s.ref;x<s.ref+24;x++)for(let y=0;y<8;y++)for(let z=0;z<8;z++)
  assert(s.covered({x:o.x+x,y:o.y+y,z:o.z+z}),'reference preflight coverage');
 // Every destination voxel belongs to exactly one clone cuboid.
 const seen=new Set();
 for(const c of s.calls.filter(c=>c.kind==='clone')){
  for(let y=c.a.y;y<=c.b.y;y++)for(let z=c.a.z;z<=c.b.z;z++)for(let x=c.a.x;x<=c.b.x;x++){
   const k=x+','+y+','+z;assert(!seen.has(k),'overlapping clone partition');seen.add(k);
  }
 }
 assert.equal(seen.size,W*H*D,'partition gaps');
 assert(s.stats().firstWriteChecks>2*Math.ceil(W/8)*Math.ceil(H/8)*Math.ceil(D/8),'full preflight before writes');
}
let count=0;
function test(n,f){f();count++;console.log('PASS',n);}
function stopped(o,check){const s=scenario(o);s.run();assert(!s.csv().includes('FINISHED,ALL_PASS'));assert(s.messages.some(m=>m.includes('TEST STOPPED')));if(check)check(s);return s;}
test('default 309386 block build and clipped chunk coverage',()=>{const s=scenario({large:true});s.run();assert(s.csv().includes('FINISHED,ALL_PASS'));assert.equal(s.stats().clones,36);oracle(s);});
test('non-aligned small plan and independent full voxel oracle',()=>{const s=scenario();s.run();assert(s.csv().includes('FINISHED,ALL_PASS'));oracle(s);assert.equal(s.csv(),fs.readFileSync(path.join(__dirname,'fixtures/p21_synthetic.csv'),'utf8').replace(/\r\n/g,'\n'),'runtime transcript matches synthetic fixture');});
test('all occupied candidates: zero world writes',()=>stopped({occupied:[0,1,2,3,4,5]},s=>assert.equal(s.stats().fills,0)));
for(const opt of ['occupiedTarget','occupiedHalo','occupiedRef'])test(opt+' rejects candidate without destroying sentinel',()=>{const s=scenario({[opt]:true});s.run();assert(s.csv().includes('PREFLIGHT,2,6,PASS'));assert([...s.cells.values()].includes(99));});
test('unloaded comparisons fail closed',()=>stopped({unloaded:true},s=>assert.equal(s.stats().fills,0)));
test('invalid partition plan: zero world and file writes',()=>stopped({invalid:true},s=>assert.equal(s.stats().writes,0)));
test('reference fill silent failure',()=>stopped({dropFill:1},s=>assert.equal(s.stats().clones,0)));
test('construction silent failure stops at that tile',()=>stopped({dropFill:3},s=>assert.equal(s.stats().fills,3)));
test('false clone with no writes stops first call',()=>stopped({rejectClone:1},s=>assert.equal(s.stats().clones,1)));
test('false return with exact data still stops',()=>stopped({falseExact:true},s=>assert.equal(s.stats().clones,1)));
test('partial clone true return stops',()=>stopped({partialClone:true},s=>assert.equal(s.stats().clones,1)));
test('last voxel clone corruption stops before next',()=>stopped({corruptClone:1},s=>assert.equal(s.stats().clones,1)));
test('clone writes into guard: no next clone',()=>stopped({spillClone:1},s=>assert.equal(s.stats().clones,1)));
test('source corruption detected before patch',()=>stopped({corruptSourceClone:1},s=>assert.equal(s.stats().patches,0)));
test('reference corruption detected before next clone',()=>stopped({corruptRefClone:1},s=>assert.equal(s.stats().clones,1)));
test('partial update outside region detected by full final scan',()=>stopped({corruptPatchOutside:true},s=>assert(s.stats().patches>0)));
test('partial update source corruption detected',()=>stopped({corruptSourceOnPatch:true}));
test('stop during preflight: zero writes',()=>stopped({stopPause:1},s=>assert.equal(s.stats().fills,0)));
test('stop after fill: no further fill',()=>stopped({stopFill:3},s=>assert.equal(s.stats().fills,3)));
test('stop after clone: no further clone or patch',()=>stopped({stopClone:1},s=>{assert.equal(s.stats().clones,1);assert.equal(s.stats().patches,0);}));
test('stop between patch log and mutation: zero patch writes',()=>stopped({stopOnPatchLog:true},s=>assert.equal(s.stats().patches,0)));
for(const opt of ['badLatchRead','badLatchWrite','badCSVRead'])test(opt+' prevents world mutation',()=>stopped({[opt]:true},s=>assert.equal(s.stats().fills,0)));
test('CSV failure after clone prevents next world mutation',()=>stopped({failLogAfterClone:true},s=>assert.equal(s.stats().clones,1)));
test('same-session rerun cannot mutate files or world',()=>{const s=stopped({rejectClone:1});const before=s.stats();s.run();assert.deepEqual(s.stats(),before);});
test('persistent latch refuses after reload without overwriting CSV',()=>{const a=stopped({rejectClone:1});const csv=a.csv();const b=scenario({files:a.files});b.run();assert.equal(b.stats().fills,0);assert.equal(b.stats().writes,0);assert.equal(b.csv(),csv);});
test('report status plan are read-only',()=>{const s=scenario();const before=s.stats();s.report();assert.deepEqual(s.stats(),before);});
console.log('P2.1 mock '+count+'/'+count+' PASS (not hardware)');
