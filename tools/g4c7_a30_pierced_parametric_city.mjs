#!/usr/bin/env node
// A30 genuinely perforated parametric city surface. ART HOLD: no Minecraft world access.
import fs from "node:fs";import path from "node:path";
const buildA30=function buildA30(oldOBJ){
const ROOT="artifacts/g4c7-a30-perforated-cityland/", CAM={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]}, TARGET=[0,78,0], SCALE=1.03;
const MAT=[["ceramic_land","#dae6eb",[.855,.902,.922,1]],["deep_struct","#3e5b70",[.243,.357,.439,1]],["public_city","#e8c18f",[.910,.757,.561,1]],["inhabited_glass","#59c0ca",[.349,.753,.792,1]],["planted_court","#79ad97",[.475,.678,.592,1]],["metallic_rib","#b69a82",[.714,.604,.510,1]]];
const M={name:"A30 / PUNCTURED CIVIC LANDSCAPE",v:[],f:[],solids:[],names:[],holes:[],metadata:[]};
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function cubic(c,t){
let u=1-t;return [0,1].map(k=>u*u*u*c[0][k]+3*u*u*t*c[1][k]+3*u*t*t*c[2][k]+t*t*t*c[3][k]);
}
function tangent(c,t){let a=cubic(c,Math.max(0,t-.003)),b=cubic(c,Math.min(1,t+.003)),dx=b[0]-a[0],dz=b[1]-a[1],d=Math.hypot(dx,dz);return [-dz/d,dx/d];}
function gridSolid(name,ns,nt,surfaces,keep,materialFn){
let nv=(ns+1)*(nt+1),V=[],F=[],boundary=new Map(),absent=0,kept=0;
for(let layer=0;layer<2;layer++)for(let i=0;i<=ns;i++)for(let j=0;j<=nt;j++){
  const p=surfaces(i/ns,j/nt,layer);if(p.some(x=>!Number.isFinite(x)))throw Error("nonfinite "+name);V.push(p);
}
const id=(i,j)=>i*(nt+1)+j,edge=(a,b)=>{let key=Math.min(a,b)+":"+Math.max(a,b),q=boundary.get(key);if(q){q.count++;}else boundary.set(key,{a,b,count:1});};
for(let i=0;i<ns;i++)for(let j=0;j<nt;j++){
 if(!keep(i,j)){absent++;continue;}kept++;
 let a=id(i,j),b=id(i+1,j),c=id(i+1,j+1),d=id(i,j+1),mat=materialFn(i,j);
 F.push([a,b,c,mat],[a,c,d,mat],[a+nv,c+nv,b+nv,1],[a+nv,d+nv,c+nv,1]);
 for(let [x,y] of [[a,b],[b,c],[c,d],[d,a]])edge(x,y);
}
for(let q of boundary.values()){if(q.count!==1)continue;let {a,b}=q;F.push([b,a,a+nv,1],[b,a+nv,b+nv,1]);}
let dir=new Map(),counts=new Map(),volume=0,badArea=0;
for(let f of F){
let a=V[f[0]],b=V[f[1]],c=V[f[2]],N=cross(sub(b,a),sub(c,a));if(Math.hypot(...N)<1e-7)badArea++;
volume+=dot(a,cross(b,c))/6;
for(let k=0;k<3;k++){let A=f[k],B=f[(k+1)%3],key=Math.min(A,B)+":"+Math.max(A,B);counts.set(key,(counts.get(key)||0)+1);let ordered=A+":"+B;dir.set(ordered,(dir.get(ordered)||0)+1);}
}
let topoBad=0;for(let [e,n]of counts){let [a,b]=e.split(":");if(n!==2||(dir.get(a+":"+b)||0)!==1||(dir.get(b+":"+a)||0)!==1)topoBad++;}
if(topoBad||badArea||Math.abs(volume)<1e-4)throw Error("grid manifold failure "+name+" "+JSON.stringify({topoBad,badArea,volume}));
if(volume<0){F=F.map(f=>[f[0],f[2],f[1],f[3]]);volume=-volume;}
let off=M.v.length;M.v.push(...V);M.f.push(...F.map(f=>[f[0]+off,f[1]+off,f[2]+off,f[3]]));M.solids.push({name,vertices:V.length,triangles:F.length,grid_cells_kept:kept,removed_cells:absent,nontrivial_holes:absent>0,signed_volume:+volume.toFixed(2)});M.names.push(name);
}
function terra(name,ctrl,w0,w1,y0,y1,thick,holes,color=0){
const ns=17,nt=8,profile=(s,t)=>{
let [x,z]=cubic(ctrl,s),[nx,nz]=tangent(ctrl,s),u=2*t-1,w=w0+(w1-w0)*s+6*Math.sin(Math.PI*s*1.3),height=y0+(y1-y0)*(3*s*s-2*s*s*s)+9*Math.sin(Math.PI*t)+6*Math.sin(2.6*Math.PI*s)*Math.sin(Math.PI*t);
return {x:x+nx*w*u/2,z:z+nz*w*u/2,y:height};};
const removed=(i,j)=>holes.some(h=>i>=h[0]&&i<h[1]&&j>=h[2]&&j<h[3]);
gridSolid(name,ns,nt,(s,t,layer)=>{let p=profile(s,t);return[p.x,p.y-(layer?thick:0),p.z]},(i,j)=>!removed(i,j),(i,j)=>i%5===0?2:color);
M.holes.push({name,grid_removed_cells:holes.map(h=>(h[1]-h[0])*(h[3]-h[2])).reduce((a,b)=>a+b,0),hole_ranges:holes});
return profile;
}
function inhabitedScreen(name,ctrl,w,streetProfile,side,lo,hi,holes){
 const ns=17,nt=6,occ=(i,j)=>holes.some(h=>i>=h[0]&&i<h[1]&&j>=h[2]&&j<h[3]);
 gridSolid(name,ns,nt,(s,t,layer)=>{let [x,z]=cubic(ctrl,s),[nx,nz]=tangent(ctrl,s),street=streetProfile(s,side>0?.85:.15),lateral=side*w*.43+(layer?.95:-.95),y=street.y+lo+hi*t+3*Math.sin(Math.PI*s);return[x+nx*lateral,y,z+nz*lateral]},(i,j)=>!occ(i,j),(i,j)=>(j===0||j===5)?5:3);
 M.holes.push({name,facade_actual_void_cells:holes.map(h=>(h[1]-h[0])*(h[3]-h[2])).reduce((a,b)=>a+b,0),hole_ranges:holes});
}
const A=[[-148,-99],[-126,-16],[-105,91],[17,130]];
const B=[[126,-119],[120,-66],[78,14],[110,100]];
const C=[[-86,70],[-34,104],[28,118],[84,94]];
const pa=terra("WEST sculptural inhabited land-section",A,66,72,13,131,15,[[4,7,2,5],[11,14,2,4]],0);
const pb=terra("EAST descending civic metropolis",B,58,54,12,124,13,[[4,7,2,5],[10,13,4,6]],0);
const pc=terra("NORTH skyline landscape gallery",C,58,37,95,158,10,[[6,9,2,5]],2);
inhabitedScreen("WEST truly perforated occupied facade",A,66,pa,-1,5,33,[[4,7,2,4],[10,13,2,5]]);
inhabitedScreen("EAST truly perforated occupied facade",B,58,pb,1,5,31,[[5,8,1,3],[12,15,3,5]]);
// broad central public address, not a ring or roof, a concave twisted civic bowl as two low-level sloping galleries with an open main court
const D=[[-61,-100],[-39,-35],[9,24],[35,81]];
terra("Grand public ascending civic hall",D,47,40,3,56,7,[[6,8,3,5]],2);
// Use a curved civic piazza which joins the entry side; no little box dwellings.
terra("Central landscaped urban welcome plaza",[[-90,-100],[-57,-101],[22,-92],[76,-46]],73,72,1,10,5,[],4);
// A real internal camera: inside conceptual public court looking back towards the taller landscape.
const ref={id:"A29",v:[],f:[]},lookup={chalk_limestone:0,basalt:1,civic_floor:2,inhabited_glass:3,garden:4,bronze:5,habitat:0};let current=0;
for(let line of oldOBJ.split("\n")){if(line.startsWith("v ")){ref.v.push(line.trim().split(/\s+/).slice(1,4).map(Number));}else if(line.startsWith("usemtl ")){current=lookup[line.slice(7).trim()]??0;}else if(line.startsWith("f ")){let f=line.trim().split(/\s+/).slice(1).map(k=>Number(k.split("/")[0])-1);if(f.length===3)ref.f.push([...f,current]);}}
if(ref.v.length!==822||ref.f.length!==1260)throw Error("Reference A29 archive parsed incorrectly");
function bounds(v){let lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let p of v)for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],p[j]);hi[j]=Math.max(hi[j],p[j]);}return [lo,hi];}
function OBJ(){let str="# A30 TRUE PERFORATED CURVED CITYLAND, ART HOLD only\nmtllib materials.mtl\n";for(let p of M.v)str+=`v ${p.map(x=>x.toFixed(5)).join(" ")}\n`;let mat=-1;for(let f of M.f){if(f[3]!==mat){mat=f[3];str+=`usemtl ${MAT[mat][0]}\n`;}str+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return str;}
function base64(u){let a="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<u.length;i+=3){let x=u[i],y=u[i+1]??0,z=u[i+2]??0;out.push(a[x>>2],a[((x&3)<<4)|(y>>4)],i+1<u.length?a[((y&15)<<2)|(z>>6)]:"=",i+2<u.length?a[z&63]:"=");}return out.join("");}
function GLB(){let positions=new Uint8Array(M.v.length*12),p=new DataView(positions.buffer);for(let i=0;i<M.v.length;i++)for(let j=0;j<3;j++)p.setFloat32(12*i+4*j,M.v[i][j],true);
let bin=[...positions],BV=[{buffer:0,byteOffset:0,byteLength:positions.length,target:34962}],AC=[{bufferView:0,componentType:5126,count:M.v.length,type:"VEC3",min:bounds(M.v)[0],max:bounds(M.v)[1]}],pr=[];
for(let mat=0;mat<MAT.length;mat++){let ix=M.f.filter(f=>f[3]===mat).flatMap(f=>f.slice(0,3));if(!ix.length)continue;let b=new Uint8Array(ix.length*4),q=new DataView(b.buffer);ix.forEach((x,i)=>q.setUint32(i*4,x,true));let off=bin.length;bin.push(...b);BV.push({buffer:0,byteOffset:off,byteLength:b.length,target:34963});AC.push({bufferView:BV.length-1,componentType:5125,count:ix.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:AC.length-1,material:mat,mode:4});}
while(bin.length%4)bin.push(0);
let doc={asset:{version:"2.0",generator:"G4-C7 A30 parametric pierced cityland"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:M.name}],meshes:[{primitives:pr}],materials:MAT.map(v=>({name:v[0],pbrMetallicRoughness:{baseColorFactor:v[2],roughnessFactor:.67,metallicFactor:.11},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:BV,accessors:AC};
let json=Array.from(JSON.stringify(doc),x=>x.charCodeAt(0));while(json.length%4)json.push(32);
let buf=new Uint8Array(28+json.length+bin.length),h=new DataView(buf.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,buf.length,true);h.setUint32(12,json.length,true);h.setUint32(16,0x4e4f534a,true);buf.set(json,20);let off=20+json.length;h.setUint32(off,bin.length,true);h.setUint32(off+4,0x004e4942,true);buf.set(bin,off+8);
return{content:base64(buf),bytes:buf.length};
}
const viewMeta={};
function view(name){
const eye=CAM[name],look=unit(sub(TARGET,eye)),right=unit(cross([0,1,0],look)),up=unit(cross(look,right)),sets=[ref,{id:"A30",v:M.v,f:M.f}],W=1500,H=580,cell=750,cy=291;
let xml=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#11283b"/><defs>`;
for(let j=0;j<2;j++)xml+=`<clipPath id="p${j}"><rect x="${j*cell+10}" y="45" width="730" height="485"/></clipPath>`;xml+="</defs>";viewMeta[name]=[];
for(let j=0;j<2;j++){
let m=sets[j],cx=cell*j+cell/2,pts=m.v.map(p=>{let d=sub(p,TARGET);return[cx+SCALE*dot(d,right),cy-SCALE*dot(d,up)]});
let xx=pts.map(p=>p[0]),yy=pts.map(p=>p[1]),min=[Math.min(...xx),Math.min(...yy)],max=[Math.max(...xx),Math.max(...yy)],fitted=min[0]>=cell*j+15&&max[0]<=(j+1)*cell-15&&min[1]>=52&&max[1]<=523;
if(!fitted)throw Error("Clipped comparison "+name+" "+j+" "+JSON.stringify({min,max}));
viewMeta[name].push({id:j?"A30":"A29",min,max,all_vertices_inside:true});
let fs=[];for(let f of m.f){let a=m.v[f[0]],b=m.v[f[1]],c=m.v[f[2]],n=unit(cross(sub(b,a),sub(c,a))),mid=a.map((x,k)=>(x+b[k]+c[k])/3);
if(dot(n,sub(eye,mid))<=0)continue;let colorBase=MAT[f[3]][1].slice(1),light=Math.max(.4,Math.min(1.22,.75+.37*dot(n,unit([-.4,.84,-.3])))),col="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(colorBase.slice(k,k+2),16)*light)).toString(16).padStart(2,"0")).join("");
fs.push({depth:dot(sub(mid,eye),look),xy:f.slice(0,3).map(k=>pts[k].map(x=>x.toFixed(2)).join(",")).join(" "),col});}
fs.sort((a,b)=>b.depth-a.depth);
xml+=`<rect x="${j*cell+10}" y="45" width="730" height="485" fill="#233b4c" stroke="#668ba1"/><g clip-path="url(#p${j})">`;
for(let f of fs)xml+=`<polygon points="${f.xy}" fill="${f.col}" stroke="#203749" stroke-width=".2"/>`;
xml+=`</g><text x="${cell*j+22}" y="30" font-family="sans-serif" font-size="23" fill="#f4f8fc">${j?"A30 PIERCED CITYLAND":"A29 ARCHIVED ART REJECT"}</text>`;}
xml+=`<text x="20" y="564" font-family="sans-serif" font-size="14" fill="#b5cede">${name.toUpperCase()} | EXACT SAME A29 CAMERA TARGET AND SCALE 1.03 | ACTUAL 3D TRIANGLES | ART HOLD</text></svg>`;
return xml;
}
function inner(){
 const eye=[0,45,-28],target=[0,87,75],fw=unit(sub(target,eye)),right=unit(cross([0,1,0],fw)),up=unit(cross(fw,right)),focal=390,W=1000,H=760,fs=[];
 for(let f of M.f){let a=M.v[f[0]],b=M.v[f[1]],c=M.v[f[2]],md=a.map((x,k)=>(x+b[k]+c[k])/3);
 let ds=f.slice(0,3).map(k=>sub(M.v[k],eye)); // discarded, corrected below
 ds=f.slice(0,3).map(k=>sub(M.v[k],eye));
 let depth=ds.map(d=>dot(d,fw));if(depth.some(d=>d<3))continue;
 let n=unit(cross(sub(b,a),sub(c,a)));if(dot(n,sub(eye,md))<=0)continue;
 let base=MAT[f[3]][1].slice(1),light=Math.max(.42,Math.min(1.2,.75+.4*dot(n,unit([-.42,.83,-.31])))),col="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(base.slice(k,k+2),16)*light)).toString(16).padStart(2,"0")).join("");
 let points=ds.map((d,j)=>[(500+focal*dot(d,right)/depth[j]).toFixed(2),(385-focal*dot(d,up)/depth[j]).toFixed(2)].join(",")).join(" ");
 fs.push({z:depth.reduce((a,b)=>a+b,0)/3,points,col});
 }
 fs.sort((a,b)=>b.z-a.z);
 let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#162c42"/><text x="22" y="33" font-size="23" fill="#eff7fa" font-family="sans-serif">A30 PUBLIC-COURT CONCEPT VIEW / CAMERA (0,45,-28)</text>`;
 for(let t of fs)svg+=`<polygon points="${t.points}" fill="${t.col}" stroke="#20384c" stroke-width=".32"/>`;
 svg+=`<text x="22" y="739" fill="#b6c9d9" font-size="14" font-family="sans-serif">Target (0,87,75) | Perspective F=390 | Near-plane triangles omitted, not a validated pedestrian position</text></svg>`;
 return {svg,camera:eye,target,triangles_drawn:fs.length};
}
const files=[],add=(path,content,encoding="utf-8")=>files.push({path:ROOT+path,content,encoding}),g=GLB();
add("a30_pierced_cityland.obj",OBJ());add("a30_pierced_cityland.glb",g.content,"base64");
add("materials.mtl",MAT.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let name of Object.keys(CAM))add(`fourview/${name}_a29_vs_a30.svg`,view(name));
const iv=inner();add("interior/a30_court_perspective.svg",iv.svg);
const report={stage:"A30 parametric lattice with actual through-holes and curved inhabited cityland",base_head:"dfe3998c2290af524b2475c8e36cbdae34120202",objective:"change modelling algorithm from box/loft to smooth subdivided warped surfaces with physical holes and sidewalls",mesh:{vertices:M.v.length,triangles:M.f.length,closed_components:M.solids.length,curve_components:M.solids,bounds:bounds(M.v),glb_bytes:g.bytes,through_hole_masks:M.holes},comparison:{reference:"archived A29 OBJ",same_CAM_target_scale:true,cameras:CAM,target:TARGET,scale:SCALE,frame_audit:viewMeta},court_perspective:{camera:iv.camera,target:iv.target,visible_triangles:iv.triangles_drawn,note:"perspective reference from inside conceptual area; do not claim collision-free safe access"},verified:["actual curved tessellated mesh surfaces","omitted grid cells make topologically real through-openings with generated sidewalls","every individually connected grid volume has paired oriented edges, nonzero triangles, positive oriented signed volume","no clipping in four-view comparison at unchanged A29 camera/scale","GLB 2 and OBJ generated from same model"],not_verified:["real Boolean union of intersecting sheets","independent third party 3D readback","pedestrian occupancy safety or visual aesthetics","331 bodies/993 feet incl negative blocker","actual km-scale proof"],project:"ART HOLD",construction:"PROHIBITED",city_integration:"PROHIBITED",legacy:{bodies:331,feet:993,halfwidth:.65,feet_elevation:[.15,3.25],old_interference_limit:45,unsupported_feet_max:0}};
add("a30_manifest.json",JSON.stringify(report,null,2));
return{files,report};
};
const old=fs.readFileSync("artifacts/g4c7-a29-open-city-section/a29_civic_strata.obj","utf8");
const result=buildA30(old);
for(let f of result.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.report.mesh,null,2));
