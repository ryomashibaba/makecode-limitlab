#!/usr/bin/env node
/* A70 verifies truthful registration and abstract route contract only.
 * It DOES NOT verify image attractiveness, actual room mesh, physical support, daylight, or human walkability.
 * Execute: node tools/g4c7_a70_authorial_contract.mjs [--negative]
 */
import fs from 'node:fs';
const data=JSON.parse(fs.readFileSync(new URL('../artifacts/g4c7-a70-registered-urban-form/design_contract.json',import.meta.url),'utf8'));
const validate=function validate(d){
 let errors=[];
 if(d.stage!=="A70"||d.medium!=="AUTHOR_DRAWN_2D_COMPOSITION_AND_SPATIAL_CONTRACT_NOT_TRUE_3D"||d.renderer!=="NONE")errors.push("EVIDENCE_TRUTH");
 if(d.visual_status!=="ART_HOLD_UNPROVEN"||d.art_adoptions!==0)errors.push("ART_PREMATURE");
 if(["S1","G1","G2","G3"].some(k=>d.formal_gates?.[k]!=="NOT_RUN"))errors.push("FORMAL_GATE_PREMATURE");
 if(d.minecraft_construction!=="FORBIDDEN"||d.city_integration!=="FORBIDDEN")errors.push("CONSTRUCTION_LOCK");
 const ids=new Set(d.nodes?.map(n=>n.id));const pos=new Map(d.nodes?.map(n=>[n.id,n.xyz]));
 if(ids.size!==d.nodes?.length||!ids.has("PUBLIC_EYE"))errors.push("DUPLICATE_OR_MISSING_NODE");
 const programNames=new Set(d.programs?.map(p=>p.id));
 if(["MARKET","MAKING","LEARNING","HOUSING","COMMONS"].some(x=>!programNames.has(x)||!ids.has(d.programs.find(p=>p.id===x)?.node)))errors.push("PROGRAM_REALITY");
 for(let e of d.edges||[]){
  const a=pos.get(e.from), b=pos.get(e.to);
  if(!a||!b){errors.push("MISSING_PATH_NODE");continue;}
  if(e.kind==="level"){if(Math.abs(b[2]-a[2])>1e-6)errors.push("VERTICAL_TELEPORT");}
  else if(e.kind==="stair"){
   const z=b[2]-a[2], run=Math.hypot(b[0]-a[0],b[1]-a[1]);
   if(e.steps!==20||Math.abs(z-e.steps*e.rise_m)>1e-6||Math.abs(run-e.steps*e.going_m)>0.001)errors.push("STAIR_DISCONTINUITY");
  }else errors.push("UNKNOWN_EDGE");
  if(!(e.intent_width_m>=2.5))errors.push("NARROW_INTENT");
 }
 let found=new Set(["PUBLIC_EYE"]),change=true;
 while(change){change=false;for(const e of d.edges||[])if(found.has(e.from)&&!found.has(e.to)){found.add(e.to);change=true}}
 if([...programNames].some(id=>!found.has(d.programs.find(p=>p.id===id)?.node)))errors.push("DISCONNECTED_PROGRAM");
 if(d.civic_anchor?.zone!=="CIVIC_ANCHOR"||d.civic_anchor.eye_node!=="PUBLIC_EYE"||d.civic_anchor.eye_height_above_floor_m!==1.7)errors.push("LOST_NEAR_FAR_ANCHOR");
 if(d.zones?.length!==4||!d.zones.some(z=>z.id==="CIVIC_ANCHOR"&&z.micro_node==="PUBLIC_EYE"))errors.push("LOST_MACRO_URBAN_WITNESS");
 return [...new Set(errors)];
};
const failures=validate(data);
if(process.argv.includes('--negative')){
 const mutations=[
  d=>d.art_adoptions=1,d=>d.formal_gates.G2="PASS",
  d=>d.nodes.find(n=>n.id==="STAIR_2_END").xyz[2]=7.1,
  d=>d.edges=d.edges.filter(e=>e.to!=="READING_ENTRY"),
  d=>d.zones.find(z=>z.id==="CIVIC_ANCHOR").micro_node="missing",
  d=>d.renderer="Cycles",d=>d.minecraft_construction="ALLOWED"
 ];
 if(failures.length)throw Error('Canonical contract invalid: '+failures.join(','));
 mutations.forEach((m,i)=>{
  const x=JSON.parse(JSON.stringify(data));m(x);
  if(!validate(x).length)throw Error('Mutation '+i+' was not caught');
 });
 console.log('A70 seven contract negative controls detected. NOT visual or physical tests.');
}
console.log(JSON.stringify({stage:'A70',pass:!failures.length,medium:data.medium,formal_gates:data.formal_gates,art:data.visual_status,errors:failures},null,2));
if(failures.length)process.exitCode=1;
