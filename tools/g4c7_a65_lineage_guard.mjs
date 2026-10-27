#!/usr/bin/env node
/**
 * A65 fail-closed lineage/evidence guard. NOT an aesthetic classifier.
 * Protects against stale historical sources and unjustified ART/G2/G3 claims.
 * Run: node tools/g4c7_a65_lineage_guard.mjs [--self-test]
 */
import fs from "node:fs";
import crypto from "node:crypto";
import path from "node:path";
const root=path.resolve(path.dirname(new URL(import.meta.url).pathname),"..");
const manifestPath=path.join(root,"artifacts/g4c7-a65-lineage-gate/lineage.json");
const input=JSON.parse(fs.readFileSync(manifestPath,"utf8"));
const verify=function verify(d){
 const bad=[];
 if(d.overall_art!=="HOLD"||d.formal_art_adoptions!==0)bad.push("UNAUTHORIZED_ART_PROMOTION");
 if(d.construction!=="FORBIDDEN"||d.city_integration!=="FORBIDDEN")bad.push("CONSTRUCTION_LOCK");
 if(["S1","G1","G2","G3"].some(k=>d[k]!=="NOT_RUN"))bad.push("MISLEADING_FORMAL_GATE");
 const known=new Set((d.precedents||[]).map(p=>p.id));
 if(!["A16","A34","A35","A63","A64"].every(k=>known.has(k)))bad.push("MISSING_HISTORICAL_PRECEDENT");
 for(const p of d.precedents||[]){
  if(!p.source||!/^[a-f0-9]{40}$/.test(p.source_git_blob)||!p.audit||!p.finding)bad.push("UNTRACEABLE_SOURCE_"+p.id);
 }
 for(const c of d.candidates||[]){
  if(!c.id||!c.precedent_refs?.length||!c.precedent_refs.every(k=>known.has(k)))bad.push("UNREVIEWED_FORM_LINEAGE");
  if(c.go_ahead_3d){
   if(!c.evidence?.human_eye_render||!c.evidence?.distant_render||!c.evidence?.same_scene_geometry)bad.push("UNFOUNDED_3D_PROMOTION");
   if(c.art_acceptance!=="NOT_APPROVED")bad.push("ART_RESULT_NOT_AUTHORIZED");
  }
 }
 return bad;
};
const assert=(condition,label)=>{if(!condition)throw new Error("A65 "+label);};
if(process.argv.includes("--self-test")){
 assert(verify(input).length===0,"canonical contract invalid");
 const cases=[
  ["fake-art",d=>d.formal_art_adoptions=1],
  ["construction",d=>d.construction="ALLOWED"],
  ["formal-gate",d=>d.G2="PASS"],
  ["missing-precedent",d=>d.precedents=d.precedents.filter(p=>p.id!=="A34")],
  ["unfounded-3d",d=>d.candidates[0].go_ahead_3d=true]
 ];
 for(const [label,mutation] of cases){const d=structuredClone(input);mutation(d);assert(verify(d).length>0,label+" not rejected");}
}
const failures=verify(input);
for(const precedent of input.precedents){
 const file=path.join(root,precedent.source);
 if(!fs.existsSync(file)){failures.push("FILE_MISSING_"+precedent.id);continue;}
 const bytes=fs.readFileSync(file);
 const actual=crypto.createHash("sha1").update("blob "+bytes.length+"\0").update(bytes).digest("hex");
 if(actual!==precedent.source_git_blob)failures.push("SOURCE_CHANGED_"+precedent.id);
}
const result={stage:"A65",meaning:"EVIDENCE_PROVENANCE_AND_HOLD_ONLY_NOT_ART_PASS",
 valid:failures.length===0, source_count:input.precedents.length,
 art:"HOLD",construction:"FORBIDDEN",S1:"NOT_RUN",G1:"NOT_RUN",G2:"NOT_RUN",G3:"NOT_RUN",
 errors:failures};
process.stdout.write(JSON.stringify(result,null,2)+"\n");
if(failures.length)process.exitCode=1;
