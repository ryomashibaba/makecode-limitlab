// G4-C7 A20 strict same-frame review re-renderer, no dependencies beyond node:fs.
// Usage: node tools/g4c7_a20_matched_review.mjs
import fs from 'node:fs';
import path from 'node:path';
const COLORS={"porcelain":"#c7d6dc","slate":"#5c788a","cobaltGlass":"#54b7bb","terrace":"#e5b67e","planting":"#739f86","structure":"#83949d","limestone":"#d1d9d6","obsidian":"#526e7d","glass":"#40adb8","gardens":"#709c7d","civic":"#e6b276","foundation":"#758791"};
const CAMERAS={"front":[0,156,-370],"oblique":[275,218,-270],"side":[385,180,0],"aerial":[180,455,-195]};
const TARGET=[0,71,0],SCALE=1.27;
function parseObj(source){const verts=[],faces=[];let mat="porcelain";for(const line of source.split("\n")){if(line.startsWith("v ")){verts.push(line.trim().split(/\s+/).slice(1).map(Number))}else if(line.startsWith("usemtl ")){mat=line.trim().slice(7)}else if(line.startsWith("f ")){let ids=line.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(ids.length!==3||ids.some(i=>i<0||i>=verts.length))throw Error("invalid face");faces.push([...ids,mat])}}return{verts,faces}}
function vsub(a,b){return a.map((v,i)=>v-b[i])}
function vdot(a,b){return a.reduce((r,v,i)=>r+v*b[i],0)}
function vcross(a,b){return[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]]}
function vunit(v){return v.map(x=>x/Math.hypot(...v))}
function shade(hex,n){let light=Math.max(.52,Math.min(1.18,.78+.3*vdot(n,vunit([-.4,.86,-.3]))));return"#"+[1,3,5].map(i=>Math.max(0,Math.min(255,Math.round(parseInt(hex.slice(i,i+2),16)*light))).toString(16).padStart(2,"0")).join("")}
function renderPair(models,camId){
 const W=1050,H=475,P=525,eye=CAMERAS[camId],fw=vunit(vsub(TARGET,eye)),right=vunit(vcross([0,1,0],fw)),up=vunit(vcross(fw,right));
 let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#0c1827"/><defs>`;
 for(let i=0;i<2;i++)s+=`<clipPath id="p${i}"><rect x="${i*P+5}" y="46" width="${P-10}" height="391"/></clipPath>`;
 s+="</defs>";
 for(let k=0;k<2;k++){
  const {verts,faces}=models[k],cx=k*P+P/2,cy=245;
  s+=`<rect x="${k*P+5}" y="46" width="${P-10}" height="391" fill="#182a3a" stroke="#384c5f"/><g clip-path="url(#p${k})">`;
  const polys=[];
  for(let f of faces){
   const pp=f.slice(0,3).map(i=>verts[i]),n=vunit(vcross(vsub(pp[1],pp[0]),vsub(pp[2],pp[0]))),centroid=[0,1,2].map(i=>(pp[0][i]+pp[1][i]+pp[2][i])/3);
   if(vdot(n,vsub(eye,centroid))<=0)continue;
   const points=pp.map(p=>{const d=vsub(p,TARGET);return `${(cx+vdot(d,right)*SCALE).toFixed(2)},${(cy-vdot(d,up)*SCALE).toFixed(2)}`}).join(" ");
   polys.push({depth:vdot(vsub(centroid,eye),fw),points,fill:shade(COLORS[f[3]],n)});
  }
  polys.sort((a,b)=>b.depth-a.depth);
  s+=polys.map(p=>`<polygon points="${p.points}" fill="${p.fill}" stroke="#263447" stroke-width=".28"/>`).join("");
  s+=`</g><text x="${k*P+18}" y="31" fill="#dce9f0" font-size="18" font-family="sans-serif" font-weight="bold">${k===0?"A19-A / REJECT":"A20 / REJECT"}</text>`;
  s+=`<text x="${k*P+18}" y="461" fill="#b0c0d0" font-size="13" font-family="sans-serif">${faces.length} actual triangles / Y-up / NO MINECRAFT</text>`;
 }
 return s+`<text x="1034" y="24" text-anchor="end" fill="#a3bac7" font-size="12" font-family="sans-serif">MATCHED FRONT/OBLIQUE/SIDE/AERIAL CAMERA — ${camId.toUpperCase()} — ART HOLD</text></svg>`;
}
const models=[
 parseObj(fs.readFileSync('artifacts/g4c7-a19-scout/a19_a_civic_caldera.obj','utf8')),
 parseObj(fs.readFileSync('artifacts/g4c7-a20-scout/a20_faulted_civic_strata.obj','utf8'))
];
const out='build/g4c7_a20_matched_review';
fs.mkdirSync(out,{recursive:true});
for(const v of Object.keys(CAMERAS)){
 fs.writeFileSync(path.join(out,v+'_a19a_a20_matched.svg'),renderPair(models,v));
}
console.log('A19-A vs A20 same-camera same-scale visual ART REJECT comparison generated');
