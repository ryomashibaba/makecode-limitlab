const fs = require('fs');
const vm = require('vm');
const assert = require('assert');
const path = require('path');
const source = fs.readFileSync(path.join(__dirname,'..','build','endurance_p1_3.js'),'utf8');
function scenario({occupied=false,stopAfter=0,corruptHeartbeat=false,fillFailure=false}={}) {
  const worldBlocks = new Map();
  const logs = new Map();
  const handlers = {};
  const messages=[];
  let pauses=0, writes=0, fills=0;
  if(occupied)worldBlocks.set('12,16,28',99);
  const key=(p)=>`${p.x},${p.y},${p.z}`;
  const context = {
    Math,
    Axis:{X:0,Y:1,Z:2}, AIR:0, STONE:1,GOLD_BLOCK:2,FillOperation:{Replace:0},
    world:(x,y,z)=>({x,y,z}),
    player:{say:s=>messages.push(s),position:()=>({getValue:a=>0}),onChat:(name,cb)=>handlers[name]=cb},
    blocks:{testForBlock:(mat,p)=>(worldBlocks.get(key(p))||0)===mat,fill:(mat,a,b)=>{
      fills++;
      if (fillFailure && fills===2) return;
      for(let x=a.x;x<=b.x;x++)for(let y=a.y;y<=b.y;y++)for(let z=a.z;z<=b.z;z++) worldBlocks.set(`${x},${y},${z}`,mat);
    }},
    file:{writeFile:(p,s)=>{writes++;logs.set(p,s);},readFile:(p)=>corruptHeartbeat&&p.includes('heartbeat')?'CORRUPT':logs.get(p)||''},
    loops:{runInBackground:cb=>cb(),pause:()=>{pauses++;if(stopAfter && pauses===stopAfter)handlers.labstop13();}}
  };
  vm.runInNewContext(source,context);
  const result=()=>({logs,messages,handlers,worldBlocks,pauses,writes,fills,status:logs.get([...logs.keys()].find(s=>s.includes('USER_UPLOAD_THIS_P13_STATUS.csv'))) || ''});
  return {...result(),run:()=>{handlers.labrun13();return result();}};
}
let r=scenario().run();
assert(r.status.includes('QUICK,24,24,PASS')); assert(r.status.includes('RUN,24,24,PASS')); assert(r.messages.some(s=>s.includes('QUICK PASS')));assert(r.pauses===24);console.log('PASS basic quick');
let a=scenario({occupied:true}).run();assert(a.status.includes('STOP,SCRATCH_OCCUPIED'));assert(a.fills===0);console.log('PASS occupied has zero edits');
let b=scenario({stopAfter:3}).run();assert(b.status.includes('STOP,USER_STOP'));assert(!b.status.includes('QUICK,24,24,PASS')); console.log('PASS early stop recorded');
let c=scenario({corruptHeartbeat:true}).run();assert(c.status.includes('STOP,HEARTBEAT_MISMATCH'));console.log('PASS I/O mismatch');
let d=scenario({fillFailure:true}).run();assert(d.status.includes('STOP,PATCH_MISMATCH'));console.log('PASS block mismatch');
let e=scenario();e.handlers.labsoak13();assert(e.messages.some(s=>s.includes('quick PASS required')));e.handlers.labrun13();e.handlers.labsoak13();let z=e.logs.get([...e.logs.keys()].find(s=>s.includes('USER_UPLOAD_THIS_P13_STATUS.csv')));assert(z.includes('SOAK30,300,300,PASS'));console.log('PASS gated long test');
let f=scenario();f.handlers.labrun13();let prior=f.logs.size;f.handlers.labrun13();assert(f.logs.size===prior);console.log('PASS one-shot protection');
