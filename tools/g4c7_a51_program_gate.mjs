// G4-C7 A51 — evidence-first "public room" preflight, not a beauty score.
// Reuses the independent A49 depth-tested semantic visibility engine.
// Usage: node tools/g4c7_a51_program_gate.mjs --report
//        node tools/g4c7_a51_program_gate.mjs --write  (create only; will not overwrite)
// Strict scope: A50 baseline. G0 diagnostics are not S1/G1/G2/G3 certification.
import fs from "node:fs";
import vm from "node:vm";
import {createHash} from "node:crypto";
import path from "node:path";
import {analyze,testOcclusion} from "./g4c7_a49_visibility_gate.mjs";
const contractPath="tools/g4c7_a51_program_contract.json";
const codePath="tools/g4c7_a50_three_deep_rooms.mjs";
const outputPath="artifacts/g4c7-a51-evidence-first/a50_preflight.json";
const sub=(a,b)=>a.map((x,i)=>x-b[i]);
const dot=(a,b)=>a.reduce((n,x,i)=>n+x*b[i],0);
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
function hit(o,dir,mesh,f){
 const [a,b,c]=f.slice(0,3).map(i=>mesh.V[i]),u=sub(b,a),v=sub(c,a),p=cross(dir,v),det=dot(u,p);
 if(Math.abs(det)<1e-8)return false;
 const r=sub(o,a),s=dot(r,p)/det;if(s<0||s>1)return false;
 const q=cross(r,u),t=dot(dir,q)/det;if(t<0||s+t>1)return false;
 const distance=dot(v,q)/det;return distance>=0&&distance<9;
}
function portalEvidence(mesh,rooms){
 let cursor=0,ranges={};
 for(const [name,count] of Object.entries(mesh.tags)){ranges[name]=[cursor,cursor+count];cursor+=count;}
 if(cursor!==mesh.F.length)throw Error("Mesh semantic grouping mismatch");
 const result=[];
 for(const room of rooms){
  const {name,cx,cz,theta,depth}=room;
  const c=Math.cos(theta),s=Math.sin(theta),transform=(x,y,z)=>[cx+x*c+z*s,y,cz-x*s+z*c],dir=[s,0,c];
  const range=ranges["room-envelope-"+name];if(!range)throw Error("Missing evidence group for "+name);
  const faces=mesh.F.slice(...range);
  for(const point of room.probes){
   const p=transform(point.x,point.y,-depth/2-3.6);
   const hits=faces.reduce((n,f)=>n+(hit(p,dir,mesh,f)?1:0),0);
   result.push({room:name,probe:point.label,expected:point.expected,rayHits:hits,pass:point.expected==="open"?hits===0:hits>0});
  }
 }
 return {sampledRayPass:result.every(r=>r.pass),samples:result,scope:"Front envelope triangle ray intersections only; no full navigable volume or door/structural QA"};
}
function reportScene(mesh,contract){
 const rows={};
 const semanticTags=new Set(Object.keys(mesh.tags));
 for(const [label,tag] of Object.entries(contract.programGroups)){
   if(!semanticTags.has(tag))throw Error("A51 contract program '"+label+"' references nonexistent mesh group '"+tag+"'");
 }
 for(const [view,config] of Object.entries(contract.cameras)){
  const measurement=analyze(mesh,config.pose);
  const model=measurement.modelPixels;
  const program=Object.fromEntries(Object.entries(contract.programGroups).map(([name,tag])=>{
    const count=measurement.groupPixels[tag]??0;
    const percent=model?100*count/model:0;
    return [name,{pixels:count,ofModelPercent:Math.round(percent*1000)/1000,inspectionTrigger:percent<contract.minMeaningfulVisiblePercent?"BELOW_VISIBILITY_INSPECTION_THRESHOLD":"PRESENT_FOR_HUMAN_REVIEW"}];
  }));
  const missed=contract.requiredSimultaneousPrograms.filter(name=>program[name].inspectionTrigger!=="PRESENT_FOR_HUMAN_REVIEW");
  rows[view]={modelPixels:model,program,simultaneousProgramInspection:{reviewRequired:missed.length>0,belowThresholdPrograms:missed,
   interpretation:"This is a *review trigger*, never automatic art acceptance or rejection."}};
 }
 const control=testOcclusion(),portals=portalEvidence(mesh,contract.rooms);
 return {stage:"A51",sourceScene:"A50 real mesh from existing source",contractVersion:1,purpose:"Pre-model urban architecture review: align apparent public activity with true room entrances; stop blind detailing",
  pixelVisibility:{reviewTriggerThresholdPercent:contract.minMeaningfulVisiblePercent,denominator:"nearest foreground model pixels",meaning:"geometry tag visibility, NOT user comprehension or quality",cameras:rows},
  selectedPortalRays:portals,rendererNegativeControls:control,
  gate:{result:"REDESIGN_REQUIRED_BEFORE_ANY_NEW_MODEL",reason:"A50 S1 rejected and central public room fails 3-program visibility inspection; external megacity aesthetic is not achieved",
     noNewModelCommitted:true,artStatus:"ART HOLD",newS1:"NOT RUN",g1:"NOT RUN",g2:"NOT RUN",g3:"NOT RUN"},
  exclusions:["Not a visual art score","Not a minimum legal accessible doorway check","Not a structural load or G2 walking check","Not G3 331 human / 993 feet safety check","Not approval to integrate or build in Minecraft"]};
}
function loadScene(src){
 // Operates only on this repo's pinned A50 first-party JS file. Never run arbitrary CLI paths.
 const pre=src.indexOf("import fs from");if(pre<0||!src.includes("function build(){"))throw Error("Unexpected A50 code");
 return vm.runInNewContext(src.slice(0,pre)+"\n({build});",{}, {timeout:20000}).build();
}
function gitBlobSha(text){
 const content=Buffer.from(text,"utf8");
 return createHash("sha1").update(Buffer.from("blob "+content.length+"\0")).update(content).digest("hex");
}
function selfTest(mesh,contract){
 const good=portalEvidence(mesh,contract.rooms);
 const altered=JSON.parse(JSON.stringify(contract.rooms));
 altered[0].probes[0].expected="blocked";
 const bad=portalEvidence(mesh,altered);
 const missing=JSON.parse(JSON.stringify(contract));
 missing.programGroups.market="nonexistent-group-test";
 let rejectedMissing=false;
 try{reportScene(mesh,missing)}catch(e){rejectedMissing=String(e).includes("nonexistent mesh group");}
 let rejectedCorrupt=false;
 try{reportScene({...mesh,F:mesh.F.slice(0,-1)},contract)}catch(e){rejectedCorrupt=String(e).includes("mismatch");}
 const passed=good.sampledRayPass&&!bad.sampledRayPass&&rejectedMissing&&rejectedCorrupt;
 if(!passed)throw Error("A51 self-test failed");
 return {passed,goodRayCount:good.samples.length,invertedExpectedRejected:!bad.sampledRayPass,missingSemanticGroupRejected:rejectedMissing,damagedFaceTaxonomyRejected:rejectedCorrupt};
}
function main(){
 const contract=JSON.parse(fs.readFileSync(contractPath,"utf8"));
 const sceneText=fs.readFileSync(codePath,"utf8");
 if(gitBlobSha(sceneText)!==contract.expectedGitBlobs.scene)throw Error("A50 source changed; cannot compare against pinned A50 baseline");
 const semanticSource=fs.readFileSync("tools/g4c7_a49_visibility_gate.mjs","utf8");
 if(gitBlobSha(semanticSource)!==contract.expectedGitBlobs.visibilityEngine)throw Error("A49 pixel engine changed; require baseline review");
 const mesh=loadScene(sceneText);
 const tests=selfTest(mesh,contract);
 const report=reportScene(mesh,contract);
 report.selfTests=tests;
 if(!report.selectedPortalRays.sampledRayPass||!report.rendererNegativeControls.frontBlocksFar||!report.rendererNegativeControls.behindCameraHidden)throw Error("A51 baseline technical evidence failed");
 if(process.argv.includes("--write")){
   if(fs.existsSync(outputPath))throw Error("Refusing to replace existing A51 evidence");
   fs.mkdirSync(path.dirname(outputPath),{recursive:true});
   fs.writeFileSync(outputPath,JSON.stringify(report,null,2)+"\n");
 }
 console.log(JSON.stringify(report,null,2));
}
if(process.argv.includes("--report")||process.argv.includes("--write")||process.argv.includes("--self-test"))main();
export {reportScene,portalEvidence,hit,loadScene,selfTest,gitBlobSha};
