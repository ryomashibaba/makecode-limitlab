#!/usr/bin/env node
// G4-C7 A34 interior views from REAL OBJ, no Minecraft; diagnostic only.
import fs from "node:fs";import path from "node:path";
const capture=function capture(textOBJ){
const palette={limestone:"#d9e7eb",support:"#476579",plaza:"#edc391",facade:"#5ebec9",garden:"#80b59e",north:"#b1c3cd"},V=[],F=[];let color="limestone";
for(let ln of textOBJ.split("\n")){if(ln.startsWith("v "))V.push(ln.split(/\s+/).slice(1,4).map(Number));else if(ln.startsWith("usemtl "))color=ln.slice(7).trim();else if(ln.startsWith("f ")){let ids=ln.split(/\s+/).slice(1).map(s=>Number(s.split("/")[0])-1);if(ids.length===3)F.push({idx:ids,color});}}
if(V.length!==6860||F.length!==13720)throw Error("A34 reference file wrong "+V.length+" "+F.length);
const sub=(a,b)=>a.map((v,i)=>v-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function render(eye,look,name){
const forward=unit(sub(look,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),P=[],width=1100,height=790,near=3,focal=490;
let omitted=0;for(let f of F){let a=V[f.idx[0]],b=V[f.idx[1]],c=V[f.idx[2]],mid=a.map((x,i)=>(x+b[i]+c[i])/3),n=unit(cross(sub(b,a),sub(c,a)));if(dot(n,sub(eye,mid))<=0)continue;
let p=f.idx.map(i=>sub(V[i],eye)),z=p.map(x=>dot(x,forward));if(z.some(d=>d<=near)){omitted++;continue;}
let xy=p.map((x,i)=>(width/2+focal*dot(x,right)/z[i]).toFixed(2)+","+(height/2-focal*dot(x,up)/z[i]).toFixed(2)).join(" ");
let col=(palette[f.color]??palette.limestone).slice(1),shade=Math.max(.39,Math.min(1.2,.75+.37*dot(n,unit([-.45,.84,-.33])))),fill="#"+[0,2,4].map(i=>Math.min(255,Math.round(parseInt(col.slice(i,i+2),16)*shade)).toString(16).padStart(2,"0")).join("");
P.push({z:z.reduce((a,b)=>a+b,0)/3,xy,fill});
}
P.sort((a,b)=>b.z-a.z);let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><rect width="${width}" height="${height}" fill="#172d41"/><text x="24" y="36" fill="#eff8fc" font-family="sans-serif" font-size="24">A34 ${name} | REAL CARVED MESH - CONCEPT VIEW</text>`;
for(let p of P)svg+=`<polygon points="${p.xy}" fill="${p.fill}" stroke="#253e52" stroke-width=".12"/>`;
svg+=`<text x="24" y="760" fill="#bed3df" font-family="sans-serif" font-size="14">eye (${eye.join(", ")}) look (${look.join(", ")}) | ${omitted} near triangles skipped | NOT human access verified</text></svg>`;
return{svg,meta:{name,camera:eye,look,visible_triangles:P.length,near_skipped:omitted,scope:"G1 failure diagnostic, not formal G2 / not walkable claim"}};
}
const results=[render([0,35,-120],[0,95,130],"SOUTH CIVIC ENTRY"),render([-102,45,-75],[-23,78,-7],"WEST CARVED HALL"),render([0,80,145],[0,95,175],"NORTH PUBLIC ROOM")];
return results;
};
const mesh=fs.readFileSync("artifacts/g4c7-a34-carved-single-body/a34_city.obj","utf8");
const views=capture(mesh);for(const v of views){let p="artifacts/g4c7-a34-carved-single-body/interior/"+v.meta.name.toLowerCase().replace(/ /g,"_")+".svg";fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,v.svg);}
