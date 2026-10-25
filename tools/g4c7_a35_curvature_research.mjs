#!/usr/bin/env node
// A35 reproducible curvature study; ART HOLD, does not access Minecraft.
import fs from "node:fs";import path from "node:path";
const improve=function improve(a34Obj){
const root="artifacts/g4c7-a35-integrated-form-scout/",cam={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},target=[0,78,0],s=1.03,W=1500,H=880;
const materials=[["limestone","#d9e7eb",[.850,.906,.922,1]],["support","#476579",[.278,.396,.475,1]],["plaza","#edc391",[.929,.765,.569,1]],["facade","#5ebec9",[.369,.745,.788,1]],["garden","#80b59e",[.502,.710,.620,1]],["north","#b1c3cd",[.694,.765,.804,1]]];
const matToNum=Object.fromEntries(materials.map((x,i)=>[x[0],i]));
let V=[],F=[],cur=0;
for(let line of a34Obj.split("\n")){
if(line.startsWith("v "))V.push(line.slice(2).trim().split(/\s+/).map(Number));
else if(line.startsWith("usemtl "))cur=matToNum[line.slice(7).trim()]??0;
else if(line.startsWith("f ")){let t=line.slice(2).trim().split(/\s+/).map(x=>Number(x.split("/")[0])-1);if(t.length===3)F.push([...t,cur]);}}
if(V.length!==6860||F.length!==13720)throw Error("reference A34 unexpectedly changed "+V.length+" "+F.length);
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((p,x,i)=>p+x*b[i],0),len=a=>Math.hypot(...a),unit=a=>a.map(x=>x/len(a));
let neighbors=Array.from({length:V.length},()=>new Set()),undirected=new Map();
for(let t of F)for(let i=0;i<3;i++){let a=t[i],b=t[(i+1)%3];neighbors[a].add(b);neighbors[b].add(a);let k=Math.min(a,b)+":"+Math.max(a,b);undirected.set(k,(undirected.get(k)||0)+1);}
if([...undirected.values()].some(x=>x!==2))throw Error("A34 source edges are not closed");
let adj=neighbors.map(set=>[...set]);
const rough=P=>P.reduce((acc,p,i)=>{let n=adj[i];if(!n.length)return acc;let avg=[0,0,0];for(let j of n)for(let k=0;k<3;k++)avg[k]+=P[j][k]/n.length;return acc+len(sub(p,avg));},0)/P.length;
const bbox=P=>{let low=[Infinity,Infinity,Infinity],high=[-Infinity,-Infinity,-Infinity];for(let p of P)for(let k=0;k<3;k++){low[k]=Math.min(low[k],p[k]);high[k]=Math.max(high[k],p[k]);}return[low,high];};
const vol=P=>F.reduce((acc,t)=>{let a=P[t[0]],b=P[t[1]],c=P[t[2]];return acc+dot(a,cross(b,c))/6;},0);
const origRough=rough(V),origVol=vol(V),base=V.map(p=>[...p]);
let P=V.map(p=>[...p]);
function smooth(P,lam){let next=P.map(p=>p.slice());for(let i=0;i<P.length;i++){let ns=adj[i],q=P[i],height=Math.max(0,Math.min(1,(q[1]-2)/22));
let mean=[0,0,0];for(let j of ns)for(let k=0;k<3;k++)mean[k]+=P[j][k]/ns.length;
for(let k=0;k<3;k++)next[i][k]+=lam*height*(mean[k]-q[k]);}return next;}
for(let i=0;i<17;i++){P=smooth(P,.48);P=smooth(P,-.51);}
// Domain-specific macro-form sweep; deform existing single mesh, DO NOT add boxes, windows or roads.
for(let i=0;i<P.length;i++){
let p=P[i],t=Math.max(0,Math.min(1,p[1]/200)),smoothK=Math.sin(Math.PI*t);
let x=p[0],z=p[2];let dx=10*Math.sin((z+68)/100)*smoothK, dz=7*Math.sin((x-34)/85)*smoothK;
// Deform supporting landform as a whole rather than stamping identical terraces.
p[0]+=dx; p[2]+=dz;
p[1]+=2.8*smoothK*Math.sin((x+0.36*z)/63);
}
// Re-check topology and inversion against original face orientation.
let angleFlip=0,areaNearZero=0,smallMin=Infinity;
for(let t of F){
let a=base[t[0]],b=base[t[1]],c=base[t[2]],nn=cross(sub(b,a),sub(c,a));
let A=P[t[0]],B=P[t[1]],C=P[t[2]],q=cross(sub(B,A),sub(C,A)),area=len(q)/2;
smallMin=Math.min(smallMin,area);
if(area<1e-5)areaNearZero++;
if(dot(nn,q)<=0)angleFlip++;
}
let resultVol=vol(P),newRough=rough(P);
if(angleFlip!==0||areaNearZero!==0||resultVol*origVol<=0||resultVol/origVol<.8||resultVol/origVol>1.20)throw Error("A35 geometry deform check "+JSON.stringify({angleFlip,areaNearZero,ratio:resultVol/origVol,newRough,origRough}));
function obj(){
let out="# A35 single connected void topology; architecturally curved, ART HOLD\nmtllib materials.mtl\n";for(let p of P)out+=`v ${p.map(x=>x.toFixed(5)).join(" ")}\n`;
let m=-1;for(let t of F){if(t[3]!==m){m=t[3];out+=`usemtl ${materials[m][0]}\n`;}out+=`f ${t[0]+1} ${t[1]+1} ${t[2]+1}\n`;}return out;
}
function b64(bytes){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",a=[];for(let i=0;i<bytes.length;i+=3){let x=bytes[i],y=bytes[i+1]??0,z=bytes[i+2]??0;a.push(abc[x>>2],abc[((x&3)<<4)|(y>>4)],i+1<bytes.length?abc[((y&15)<<2)|(z>>6)]:"=",i+2<bytes.length?abc[z&63]:"=");}return a.join("");}
function glb(){
let positions=new Uint8Array(P.length*12),pv=new DataView(positions.buffer);
for(let i=0;i<P.length;i++)for(let k=0;k<3;k++)pv.setFloat32(i*12+k*4,P[i][k],true);
let normals=P.map(()=>[0,0,0]);
for(let t of F){let a=P[t[0]],b=P[t[1]],c=P[t[2]],n=cross(sub(b,a),sub(c,a));for(let q of t.slice(0,3))for(let k=0;k<3;k++)normals[q][k]+=n[k];}
normals=normals.map(n=>len(n)>0?unit(n):[0,1,0]);
let normBytes=new Uint8Array(normals.length*12),nv=new DataView(normBytes.buffer);
for(let i=0;i<normals.length;i++)for(let k=0;k<3;k++)nv.setFloat32(i*12+4*k,normals[i][k],true);
let bin=[...positions,...normBytes],BV=[{buffer:0,byteOffset:0,byteLength:positions.length,target:34962},{buffer:0,byteOffset:positions.length,byteLength:normBytes.length,target:34962}],AC=[{bufferView:0,componentType:5126,count:P.length,type:"VEC3",min:bbox(P)[0],max:bbox(P)[1]},{bufferView:1,componentType:5126,count:P.length,type:"VEC3"}],pr=[];
for(let k=0;k<materials.length;k++){let ids=F.filter(t=>t[3]===k).flatMap(t=>t.slice(0,3));if(!ids.length)continue;
let data=new Uint8Array(ids.length*4),iv=new DataView(data.buffer);ids.forEach((q,i)=>iv.setUint32(i*4,q,true));
let offset=bin.length;bin.push(...data);BV.push({buffer:0,byteOffset:offset,byteLength:data.length,target:34963});AC.push({bufferView:BV.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0,NORMAL:1},indices:AC.length-1,material:k,mode:4});}
while(bin.length%4)bin.push(0);
const j={asset:{version:"2.0",generator:"G4-C7 A35 Taubin-smooth void-preserving city G1"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:"A35 Curvature Study -- ART HOLD"}],meshes:[{primitives:pr}],materials:materials.map(m=>({name:m[0],pbrMetallicRoughness:{baseColorFactor:m[2],metallicFactor:.16,roughnessFactor:.67},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:BV,accessors:AC};
let json=Array.from(JSON.stringify(j),x=>x.charCodeAt(0));while(json.length%4)json.push(32);
const bytes=new Uint8Array(28+json.length+bin.length),h=new DataView(bytes.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,bytes.length,true);h.setUint32(12,json.length,true);h.setUint32(16,0x4e4f534a,true);bytes.set(json,20);
const off=20+json.length;h.setUint32(off,bin.length,true);h.setUint32(off+4,0x004e4942,true);bytes.set(bin,off+8);return{encoded:b64(bytes),bytes:bytes.length};
}
const audits={},screens=[],interiors={};
function orthographic(name){
const eye=cam[name],front=unit(sub(target,eye)),right=unit(cross([0,1,0],front)),up=unit(cross(front,right));
const models=[{v:base,id:"A34"},{v:P,id:"A35"}];
let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#132c40"/><defs><clipPath id="a0"><rect x="10" y="55" width="725" height="770"/></clipPath><clipPath id="a1"><rect x="760" y="55" width="725" height="770"/></clipPath></defs>`;
audits[name]=[];
for(let m=0;m<2;m++){let source=models[m],pts=source.v.map(p=>{let q=sub(p,target);return[m*750+375+s*dot(q,right),438-s*dot(q,up)]});
let bounds=[Math.min(...pts.map(v=>v[0])),Math.min(...pts.map(v=>v[1])),Math.max(...pts.map(v=>v[0])),Math.max(...pts.map(v=>v[1]))];let fits=bounds[0]>=m*750+13&&bounds[2]<=(m+1)*750-13&&bounds[1]>=58&&bounds[3]<=824;
if(!fits)throw Error("A35 shot clipped "+name+" "+source.id+" "+bounds.join(","));
audits[name].push({model:source.id,bounds,fits});
let tris=[];
for(let t of F){let A=source.v[t[0]],B=source.v[t[1]],C=source.v[t[2]],n=unit(cross(sub(B,A),sub(C,A))),mid=A.map((x,k)=>(x+B[k]+C[k])/3);if(dot(n,sub(eye,mid))<=0)continue;
let hex=materials[t[3]][1].slice(1),shade=Math.max(.37,Math.min(1.22,.76+.38*dot(n,unit([-.45,.83,-.32])))),color="#"+[0,2,4].map(i=>Math.min(255,Math.round(parseInt(hex.slice(i,i+2),16)*shade)).toString(16).padStart(2,"0")).join("");
tris.push({depth:dot(sub(mid,eye),front),points:t.slice(0,3).map(i=>pts[i].map(x=>x.toFixed(2)).join(",")).join(" "),color});
}
tris.sort((a,b)=>b.depth-a.depth);
svg+=`<rect x="${m*750+10}" y="55" width="725" height="770" fill="#233e51"/><g clip-path="url(#a${m})">`;
for(let t of tris)svg+=`<polygon points="${t.points}" fill="${t.color}" stroke="#203949" stroke-width=".10"/>`;
svg+=`</g><text x="${m*750+18}" y="34" fill="#f6fcff" font-size="21" font-family="sans-serif">${m?"A35 CURVATURE EXPERIMENT":"A34 ARCHIVED ART REJECT"}</text>`;
}
svg+=`<text x="18" y="857" fill="#bad3de" font-size="13" font-family="sans-serif">${name.toUpperCase()} / identical historic camera, target, orthographic scale 1.03 / actual mesh triangles / ART HOLD</text></svg>`;
return svg;
}
function perspective(name,eye,look){
let forward=unit(sub(look,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),near=4,faces=[],omitted=0;
for(let t of F){let A=P[t[0]],B=P[t[1]],C=P[t[2]],n=unit(cross(sub(B,A),sub(C,A))),mid=A.map((x,k)=>(x+B[k]+C[k])/3);if(dot(n,sub(eye,mid))<=0)continue;
let d=t.slice(0,3).map(q=>sub(P[q],eye)),z=d.map(x=>dot(x,forward));if(z.some(x=>x<=near)){omitted++;continue;}
let xy=d.map((p,i)=>(480+480*dot(p,right)/z[i]).toFixed(2)+","+(367-480*dot(p,up)/z[i]).toFixed(2)).join(" ");
let col=materials[t[3]][1].slice(1),shade=Math.max(.38,Math.min(1.20,.77+.37*dot(n,unit([-.43,.82,-.32])))),fill="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(col.slice(k,k+2),16)*shade)).toString(16).padStart(2,"0")).join("");
faces.push({z:z.reduce((a,b)=>a+b,0)/3,xy,fill});}
faces.sort((a,b)=>b.z-a.z);
let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="960" height="750" viewBox="0 0 960 750"><rect width="960" height="750" fill="#183249"/><text x="18" y="32" font-family="sans-serif" font-size="20" fill="#f4fbfe">${name} (A35 ACTUAL MESH / HUMAN ACCESS NOT VERIFIED)</text>`;
for(let f of faces)svg+=`<polygon points="${f.xy}" fill="${f.fill}" stroke="#223b50" stroke-width=".10"/>`;
svg+=`<text x="18" y="727" font-family="sans-serif" font-size="13" fill="#b2cedd">Camera [${eye}] target [${look}]. Near faces omitted ${omitted}; not a third-party engine.</text></svg>`;
interiors[name]={camera:eye,target:look,triangles_rendered:faces.length,triangles_omitted_near:omitted};return svg;
}
const assets=[],add=(name,text,encoding="utf-8")=>assets.push({path:root+name,content:text,encoding}),g=glb();
add("a35_curved_integral_city.obj",obj());add("a35_curved_integral_city.glb",g.encoded,"base64");add("materials.mtl",materials.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let k of Object.keys(cam))add(`fourview/${k}_a34_vs_a35.svg`,orthographic(k));
add("interior/a35_south_civic.svg",perspective("SOUTH_CIVIC",[0,35,-120],[0,95,130]));
add("interior/a35_west_carved_hall.svg",perspective("WEST_CARVED_HALL",[-102,45,-75],[-23,78,-7]));
const report={stage:"G4C7 A35 single experimental curvature-and-civic-void form",date_jst:"2026-10-25",input:"A34 canonical OBJ actual 6860 vertices,13720 triangles",geometry:{vertices:P.length,triangles:F.length,edge_count:undirected.size,unmatched_edges:0,original_signed_volume:origVol,result_signed_volume:resultVol,volume_ratio:resultVol/origVol,old_mean_laplacian_distance:origRough,new_mean_laplacian_distance:newRough,roughness_reduction_percent:100*(1-newRough/origRough),flipped_triangle_normals:angleFlip,degenerate_triangle_count:areaNearZero,minimum_triangle_area:smallMin,bounds:bbox(P),actual_glb_bytes:g.bytes,algorithm:"17 Taubin lambda=.48 mu=-.51 iterations with ground anchor, macro x-z warping + subtle topographic y bending; no added floor or box geometry"},reference_camera:cam,target,scale:s,matched_projection_frames:audits,interior_diagnostics:interiors,art_status:"PENDING G1 HUMAN REVIEW, NOT AN ADOPTION",technical_limitations:["topology preserved by identical faces; geometry self intersections not comprehensively tested","no new walking/structural QA","no third party GLB renderer","area/roughness proxy != beauty"],protections:{ART_HOLD:true,Minecraft_Education_construction:"FORBIDDEN",city_integration:"FORBIDDEN",old_project_assets:"PROTECTED",legacy_bodies:331,legacy_feet:993,body_halfwidth:.65,foot_vertical:[.15,3.25],historical_body_collisions_ceiling:45,unsupported_feet_max:0,negative_blocker:"REQUIRED"}};
add("a35_initial_manifest.json",JSON.stringify(report,null,2));return{assets,report};
};
const src=fs.readFileSync("artifacts/g4c7-a34-carved-single-body/a34_city.obj","utf8");
const result=improve(src);for(let f of result.assets){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.report.geometry,null,2));
