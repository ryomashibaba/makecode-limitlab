const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const source = fs.readFileSync(path.join(__dirname, '..', 'build', 'limitlab_p1_4.js'), 'utf8');
const STATUS_NAME = 'USER_UPLOAD_THIS_P14_STATUS.csv';

function createScenario(opts={}) {
    const worldMap = new Map();
    const logs = new Map();
    const messages = [];
    const handlers = {};
    let fills = 0, clones = 0, pauses = 0, totalBlocksWritten = 0;
    const key = p => `${p.x},${p.y},${p.z}`;
    const get = p => worldMap.get(key(p)) ?? 0;
    const set = (p, id) => { worldMap.set(key(p), id); totalBlocksWritten++; };
    const forVolume = (a, b, callback) => {
        for (let x=a.x; x<=b.x; x++) for(let y=a.y; y<=b.y; y++) for(let z=a.z; z<=b.z; z++) callback({x,y,z});
    };
    for (const candidate of opts.occupiedCandidates || []) {
        // First write lane is occupied in each requested candidate.
        worldMap.set(`12,16,${30+candidate*22}`, 99);
    }
    if(opts.referenceBlock) worldMap.set('72,16,30', 99);
    const c = {
        Math,
        Axis:{X:0,Y:1,Z:2}, AIR:0, GOLD_BLOCK:2,STONE:1,
        FillOperation:{Replace:0},CloneMask:{Replace:0},CloneMode:{Normal:0},TestForBlocksMask:{All:0},
        world:(x,y,z)=>({x,y,z}),
        player:{
            position:()=>({getValue:()=>0}),
            onChat:(name,handler)=>handlers[name]=handler,
            say:text=>messages.push(text)
        },
        blocks:{
            testForBlock:(id,p)=>get(p)===id,
            testForBlocks:(start,end,dest)=>{
                let match=true;
                forVolume(start,end,p=>{
                    const d={x:dest.x + p.x-start.x, y:dest.y + p.y-start.y,z:dest.z + p.z-start.z};
                    if(get(p)!==get(d)) match=false;
                });
                return !opts.forceMismatch || dest.x!==36 ? match : false;
            },
            fill:(id,a,b)=>{
                fills++;
                const volume=(b.x-a.x+1)*(b.y-a.y+1)*(b.z-a.z+1);
                assert(volume<=512, 'Oversized fill call');
                if(opts.skipFillNumber===fills) return;
                forVolume(a,b,p=>set(p,id));
            },
            clone:(a,b,d)=>{
                clones++;
                if(opts.cloneFalse) return false;
                const arr=[];forVolume(a,b,p=>arr.push({p:{x:d.x+p.x-a.x,y:d.y+p.y-a.y,z:d.z+p.z-a.z},id:get(p)}));
                for(const {p,id} of arr) set(p,id);
                return true;
            }
        },
        file:{
            writeFile:(name,content)=>logs.set(name,content),
            readFile:name=>opts.corruptRead&&name.includes('P14_heartbeat')?'CORRUPT':opts.corruptLargeIo&&name.includes('262144')?'CORRUPT':(logs.get(name)??'')
        },
        loops:{
            runInBackground:handler=>handler(),
            pause:()=>{
                pauses++;
                if(opts.stopAtPause===pauses) handlers.labstop14();
            }
        }
    };
    vm.runInNewContext(source,c,{timeout:20000});
    return {
        run:()=>handlers.labauto14(),
        stop:()=>handlers.labstop14(),
        statusCmd:()=>handlers.labstatus14(),
        plan:()=>handlers.labplan14(),
        getStatus:()=>[...logs.entries()].find(([name])=>name.endsWith(STATUS_NAME))?.[1]??'',
        getHistory:()=>({fills,clones,pauses,totalBlocksWritten,worldMap,logs,messages}),
        messages,worldMap,logs,handlers
    };
}
function report(name, cb){cb();console.log('PASS',name);}
report('complete all phases with 8 verified 512-block trials',()=>{
    const s=createScenario();s.run();const csv=s.getStatus(),hist=s.getHistory();
    assert(csv.includes('P1.4,BENCH,8,8,PASS,four_fill_four_clone'));
    assert(csv.includes('P1.4,PAUSE150,150,150,PASS'));
    assert(csv.includes('P1.4,MIXED150,150,150,PASS'));
    assert(csv.includes('P1.4,POSTIO60,60,60,PASS'));
    assert(csv.includes('P1.4,IO_256K,262144,262144,PASS'));
    assert(csv.includes('P1.4,RUN,1,1,PASS,ALL_P14_STAGES'));
    assert.strictEqual(hist.clones,4);
    assert.strictEqual((csv.match(/P1.4,BENCH,[1-4],4,PASS,clone_512_exact/g)||[]).length,4);
    assert.strictEqual((csv.match(/P1.4,BENCH,[1-4],4,PASS,fill_512_exact/g)||[]).length,4);
    assert(![...hist.worldMap.entries()].some(([coord,value])=>coord.startsWith('72,')&&value!==0));
    const markers=[...hist.logs.keys()].filter(k=>/P14_t[1-4]_(fill|clone)_(begin|end)\.txt$/.test(k));
    assert.strictEqual(markers.length,16);
    assert(hist.pauses>=360);
});
report('blocked candidate safely skipped and alternate selected',()=>{
    const s=createScenario({occupiedCandidates:[0]});s.run();
    assert(s.getStatus().includes('P1.4,PREFLIGHT,2,4,PASS'));
    assert(s.getStatus().includes('P1.4,RUN,1,1,PASS'));
    assert.strictEqual(s.worldMap.get('12,16,30'),99);
});
report('all candidate regions occupied no edits',()=>{
    const s=createScenario({occupiedCandidates:[0,1,2,3]});s.run();const h=s.getHistory();
    assert(h.totalBlocksWritten===0);
    assert(s.getStatus().includes('STOP,NO_EMPTY_SAFE_REGION'));
});
report('clone return false fails closed',()=>{
    const s=createScenario({cloneFalse:true});s.run();assert(s.getStatus().includes('STOP,BENCH_VERIFY_'));
    assert(!s.getStatus().includes('P1.4,PAUSE150,150,150,PASS'));
});
report('source mismatch fails closed',()=>{
    const s=createScenario({skipFillNumber:1});s.run();assert(s.getStatus().includes('STOP,SOURCE_MISMATCH'));
});
report('heartbeat corruption detected',()=>{
    const s=createScenario({corruptRead:true});s.run();assert(s.getStatus().includes('STOP,PAUSE150_HEARTBEAT_MISMATCH'));
});
report('256KiB mismatch reported with prior stages retained',()=>{
    const s=createScenario({corruptLargeIo:true});s.run();const t=s.getStatus();
    assert(t.includes('P1.4,MIXED150,150,150,PASS'));
    assert(t.includes('STOP,IO_256K_MISMATCH'));
    assert(!t.includes('P1.4,POSTIO60,60,60,PASS'));
});
report('explicit stop during PAUSE loop records checkpoint and prevents next stage',()=>{
    const s=createScenario({stopAtPause:36});s.run();const t=s.getStatus();
    assert(t.includes('STOP,USER_STOP'));
    assert(!t.includes('P1.4,MIXED150,150,150,PASS'));
});
report('one-shot guard prevents retry from overwriting existing world/logs',()=>{
    const s=createScenario();s.run();const a=s.getHistory();s.run();const b=s.getHistory();
    assert.strictEqual(a.fills,b.fills);assert.strictEqual(a.clones,b.clones);
    assert(s.messages.some(m=>m.includes('already running or used')));
});
report('read-only large construction plan never modifies blocks or files',()=>{
    const s=createScenario();s.plan();const h=s.getHistory();
    assert.strictEqual(h.totalBlocksWritten,0);assert.strictEqual(h.logs.size,0);
    assert(s.messages.some(m=>m.includes('65536 plan')));
});
