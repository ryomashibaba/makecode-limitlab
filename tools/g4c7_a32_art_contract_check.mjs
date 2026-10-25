#!/usr/bin/env node
// Validate A32 research artifacts only, never trigger Minecraft/CI by default.
// Run from repo root: node tools/g4c7_a32_art_contract_check.mjs
import fs from "node:fs";
import assert from "node:assert/strict";
const base = "artifacts/g4c7-a32-art-direction/";
const doc = fs.readFileSync("docs/G4C7_A32_ARCHITECTURAL_ART_DIRECTION_JA.md","utf8");
const meta = JSON.parse(fs.readFileSync(base+"a32_gate_manifest.json","utf8"));
assert.equal(meta.stage, "A32 / G0 visual art-direction contract");
assert.equal(meta.status.includes("NOT ART APPROVED"), true);
assert.equal(meta.preserved.art_hold,true);
assert.equal(meta.preserved.minecraft_education_construction,"FORBIDDEN");
assert.equal(meta.preserved.city_integration,"FORBIDDEN");
assert.equal(meta.preserved.body_samples,331);
assert.equal(meta.preserved.foot_samples,993);
assert.equal(meta.preserved.halfwidth,0.65);
assert.deepEqual(meta.preserved.foot_offset,[0.15,3.25]);
assert.equal(meta.preserved.historical_body_surface_interference_ceiling,45);
assert.equal(meta.preserved.unsupported_feet_ceiling,0);
assert.equal(meta.preserved.negative_control,"REQUIRED");
assert.equal(meta.gates[0].id,"G0");
assert.equal(meta.gates[1].now,"NOT RUN");
assert.equal(meta.gates[2].now,"NOT RUN");
assert.equal(meta.gates[3].now,"NOT RUN");
assert.equal(meta.design_zones.length,5);
for(const zone of meta.design_zones) assert.equal(zone.conceptual_xyz.length,3);
for(const term of ["A22","A25","A26","A27","A28","A29","A30","A31","ART HOLD","施工禁止","都市統合"]) assert(doc.includes(term), "missing "+term);
for(const path of ["a32_section_plan.svg","a32_three_view_targets.svg"]){
 const s=fs.readFileSync(base+path,"utf8");
 assert(s.startsWith("<svg "));
 assert(s.trimEnd().endsWith("</svg>"));
 assert(s.includes("2D")||s.includes("概念"));
 assert(!s.includes("<script"));
 assert(s.length>1500);
}
console.log("A32 G0 ART DIRECTION INVARIANT CHECK PASS (not art approval / not 3D QA)");
