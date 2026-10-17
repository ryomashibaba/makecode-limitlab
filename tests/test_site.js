'use strict';
const fs=require('fs');const vm=require('vm');const assert=require('assert');const path=require('path');
const root=path.resolve(__dirname,'..');const handlers={};
function elem(){return {textContent:'',className:'',style:{},innerHTML:'',addEventListener:(n,fn)=>{handlers[n]=fn;}};}
const ctx={document:{getElementById:()=>elem()},module:{exports:{}},console};
vm.runInNewContext(fs.readFileSync(path.join(root,'docs/app.js'),'utf8'),ctx);
const {parseCSV,analyze}=ctx.module.exports;
for(const [name,version] of [['fixture_p06.csv','P0.6'],['fixture_p07.csv','P0.7'],['fixture_p08.csv','P0.8']]){
 const raw=fs.readFileSync(path.join(__dirname,name),'utf8');const r=analyze(parseCSV(raw));
 assert.equal(r.version,version);assert.equal(r.state,'PASS');
}
const partial='Stage,Method,Blocks,Trial,Status,Detail\nB4096,fill,4096,1,PASS,ok\n';
assert.equal(analyze(parseCSV(partial)).state,'INCOMPLETE');
assert.equal(analyze(parseCSV(partial+'RUN,final,0,0,STOP,REGION_OCCUPIED\n')).state,'STOP');
const requirements=[['B4096','fill',4096,2],['B4096','clone',4096,2],['B16384','fill',16384,1],['B16384','clone',16384,1],['UPDATE','full',1728,1],['UPDATE','delta',384,1],['UPDATE','clone',1536,1],['IO','roundtrip',1024,1],['IO','roundtrip',65536,1],['IO','roundtrip',262144,1],['ENDURANCE','QUICK',150,1],['RUN','final',0,1]];
const full=['Stage,Method,Blocks,Trial,Status,Detail'];
for(const [s,m,b,n] of requirements)for(let i=1;i<=n;i++)full.push(s+','+m+','+b+','+i+',PASS,ok');
assert.equal(analyze(parseCSV(full.join('\n'))).state,'PASS');
const quoted='Stage,Method,Blocks,Trial,Status,Detail\nRUN,final,0,0,STOP,"some, comma"';
assert.equal(parseCSV(quoted)[0].Detail,'some, comma');
console.log('JS site parser: PASS (7 scenarios)');
