'use strict';
// Simulates API invocation only. Does NOT prove in-game stair orientation/collision.
const assert=require('assert'), fs=require('fs'),path=require('path'),vm=require('vm');
const compiled=fs.readFileSync(path.resolve(__dirname,'../build/limitlab_stair_bench_a1c.js'),'utf8');
function runBench(options={}){
 const blocksByCoord=new Map(),commands={},messages=[],places=[],fills=[];
 const key=(p)=>[p.x,p.y,p.z].join(',');
 const at=(p)=>blocksByCoord.has(key(p))?blocksByCoord.get(key(p)):(p.y<100?1:0);
 const sandbox={
  Math, AIR:0, STONE:1,FillOperation:{Replace:0},Axis:{X:0,Y:1,Z:2},
  world:(x,y,z)=>({x,y,z}),
  player:{
   position:()=>({getValue:(axis)=>[400,100,600][axis]}),
   say:(message)=>messages.push(message),
   onChat:(command,callback)=>commands[command]=callback
  },
  blocks:{
   testForBlock:(block,p)=>at(p)===block,
   blockWithData:(id,data)=>{assert.equal(id,109);assert(Number.isInteger(data)&&data>=0&&data<4);return id*16+data;},
   fill:(id,a,b,op)=>{
    assert.equal(id,1); assert.equal(op,0);
    fills.push({id,a,b});
    for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++)for(let x=a.x;x<=b.x;x++)
       blocksByCoord.set(key({x,y,z}),id);
   },
   place:(id,p)=>{
    places.push({id,p});
    if(options.failAtPlace===places.length)return false;
    blocksByCoord.set(key(p),id);return true;
   }
  },loops:{pause:(ms)=>assert.equal(ms,1)}
 };
 if(options.occupied)blocksByCoord.set(key(options.occupied),1);
 if(options.noGround)blocksByCoord.set(key(options.noGround),0);
 vm.runInNewContext(compiled,sandbox,{timeout:30000});
 return {commands,places,fills,messages,blocksByCoord};
}
let count=0;function test(name,fn){fn();console.log('PASS '+name);count++}
test('4 directions × 6 separate stair runs with correctly encoded legacy state IDs',()=>{
 const t=runBench();t.commands.labstbonce();
 assert.equal(t.places.length,24);
 assert.equal(t.fills.length,20);
 const origins=[[420,620],[444,620],[420,644],[444,644]];
 const steps=[[1,0],[-1,0],[0,1],[0,-1]];
 for(let d=0;d<4;d++)for(let i=0;i<6;i++){
  const v=t.places[d*6+i],o=origins[d],s=steps[d];
  assert.equal(v.id,109*16+d);
  assert.deepEqual([v.p.x,v.p.y,v.p.z],[o[0]+s[0]*i,100+i,o[1]+s[1]*i]);
 }
 assert(t.messages.some(x=>x.includes('24 stairs issued')));
});
test('full-column preflight prevents construction over any occupied space',()=>{
 const t=runBench({occupied:{x:423,y:104,z:620}});
 t.commands.labstbonce();
 assert.equal(t.places.length,0);assert.equal(t.fills.length,0);
 assert(t.messages.some(x=>x.includes('BLOCKED_OCCUPIED_COLUMN')));
});
test('missing support ground blocks preflight before writes',()=>{
 const t=runBench({noGround:{x:420,y:99,z:620}});
 t.commands.labstbonce();
 assert.equal(t.places.length,0);assert.equal(t.fills.length,0);
 assert(t.messages.some(x=>x.includes('BLOCKED_MISSING_FLAT_GROUND')));
});
test('single-session one-shot refuses repeated build, no overwrites',()=>{
 const t=runBench();t.commands.labstbonce();
 const before=[t.places.length,t.fills.length];
 t.commands.labstbonce();assert.deepEqual([t.places.length,t.fills.length],before);
 assert(t.messages.some(x=>x.includes('ONE-SHOT LOCKED')));
});
test('placement failure stops and never retries on same run',()=>{
 const t=runBench({failAtPlace:7});
 t.commands.labstbonce();
 assert.equal(t.places.length,7);assert.equal(t.fills.length,6);
 t.commands.labstbonce();
 assert.equal(t.places.length,7);
 assert(t.messages.some(x=>x.includes('partial isolated bench, DO NOT repeat')));
});
console.log('STB A1C '+count+'/'+count+' offline API-mock tests PASS (no game interaction)');
