#!/usr/bin/env node
// A31 genuine 3D civic valley / ART HOLD. No Minecraft commands.
import fs from "node:fs";import path from "node:path";
const build=function build(src){
const DIR="artifacts/g4c7-a31-civic-valley-scout/",eye={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},center=[0,78,0],factor=1.03;
const mats=[["shell","#dae6e9",[.85,.90,.915,1]],["base","#405a70",[.25,.353,.439,1]],["civic","#eac18e",[.918,.757,.557,1]],["window","#59bbc8",[.349,.733,.784,1]],["garden","#80b69c",[.5,.714,.612,1]],["warm","#b99074",[.725,.565,.455,1]],["inhabited","#8aa0b3",[.541,.627,.702,1]]];
let m={v:[],f:[],parts:[]},program={grand_court:0,urban_levels:0,occupied_galleries:0,green_courts:0,civic_connections:0};
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function put(V,F,c,name){
let volume=0,bad=0,edges=new Map(),directions=new Map();
for(let t of F){let A=V[t[0]],Q=V[t[1]],C=V[t[2]],n=cross(sub(Q,A),sub(C,A));if(Math.hypot(...n)<1e-6)bad++;volume+=dot(A,cross(Q,C))/6;}
if(volume<0){F=F.map(t=>[t[0],t[2],t[1]]);volume=-volume;}
for(let t of F)for(let i=0;i<3;i++){let a=t[i],b=t[(i+1)%3],k=Math.min(a,b)+":"+Math.max(a,b),d=a+":"+b;edges.set(k,(edges.get(k)||0)+1);directions.set(d,(directions.get(d)||0)+1);}
for(let [key,n] of edges){let [a,b]=key.split(":");if(n!==2||(directions.get(a+":"+b)||0)!==1||(directions.get(b+":"+a)||0)!==1)bad++;}
if(bad||volume<.00001)throw Error("solid broken "+name+" "+JSON.stringify({bad,volume}));
let offset=m.v.length;m.v.push(...V);m.f.push(...F.map(t=>[t[0]+offset,t[1]+offset,t[2]+offset,c]));m.parts.push({name,triangles:F.length,volume:+volume.toFixed(2)});
}
function polygon(P,lo,hi,col,label){
let n=P.length,area=P.reduce((s,p,i)=>{let q=P[(i+1)%n];return s+p[0]*q[1]-p[1]*q[0]},0);
if(Math.abs(area)<.001||hi<=lo)throw Error("footprint error "+label);
let poly=area>0?P:P.slice().reverse(),V=[],F=[];for(let y of [lo,hi])for(let p of poly)V.push([p[0],y,p[1]]);
for(let k=1;k<n-1;k++)F.push([0,k+1,k],[n,n+k,n+k+1]);
for(let k=0;k<n;k++){let j=(k+1)%n;F.push([k,j,n+j],[k,n+j,n+k]);}put(V,F,col,label);
}
function box(x,z,w,d,y,h,c,label,angle=0){let C=Math.cos(angle),S=Math.sin(angle);polygon([[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(p=>[x+p[0]*C-p[1]*S,z+p[0]*S+p[1]*C]),y,y+h,c,label);}
function loft(name,path,widths,low,high,col){
let V=[],F=[],N=path.length;
for(let i=0;i<N;i++){let p=path[i],a=path[Math.max(0,i-1)],b=path[Math.min(N-1,i+1)],dx=b[0]-a[0],dz=b[1]-a[1],length=Math.hypot(dx,dz),nx=-dz/length,nz=dx/length,w=widths[i];
if(w<=0||high[i]<=low[i])throw Error("bad loft "+name);
V.push([p[0]+nx*w/2,low[i],p[1]+nz*w/2],[p[0]-nx*w/2,low[i],p[1]-nz*w/2],[p[0]-nx*w/2,high[i],p[1]-nz*w/2],[p[0]+nx*w/2,high[i],p[1]+nz*w/2]);}
for(let i=0;i<N-1;i++)for(let j=0;j<4;j++){let a=i*4+j,b=i*4+(j+1)%4,c=(i+1)*4+(j+1)%4,d=(i+1)*4+j;F.push([a,b,c],[a,c,d]);}
F.push([0,2,1],[0,3,2]);let k=(N-1)*4;F.push([k,k+1,k+2],[k,k+2,k+3]);put(V,F,col,name);
}
function quarter(name,x,z,angle,levels,w,d,base,step,retreat){
let ca=Math.cos(angle),sa=Math.sin(angle),point=(u,v)=>[x+u*ca-v*sa,z+u*sa+v*ca];
for(let k=0;k<levels;k++){
let y=base+step*k,r=retreat*k,WW=w-3*k,DD=d-2*k;
let corners=[[-WW/2,-DD/2],[WW*.15,-DD/2-5],[WW/2,-DD/2+4],[WW/2,DD/2],[-WW*.3,DD/2+4],[-WW/2,DD/2]].map(p=>point(p[0],p[1]+r));
polygon(corners,y,y+5,2,name+"_real_city_floor_"+k);program.urban_levels++;
let hh=20+((k+1)%3)*4,q=point(-WW*.08,DD*.20+r),front=point(-WW*.08,-DD*.05+r);
box(q[0],q[1],WW*.75,DD*.45,y+5,hh,6,name+"_wide_occupied_gallery_"+k,angle);program.occupied_galleries++;
box(front[0],front[1],WW*.65,1.8,y+9,Math.min(hh-7,13),3,name+"_atrium_facing_occupied_windows_"+k,angle);
if(k%2===0){let g=point(WW*.27,-DD*.30+r);box(g[0],g[1],WW*.27,DD*.20,y+5,2.5,4,name+"_sky_garden_"+k,angle);program.green_courts++;}
}
}
polygon([[-162,-143],[-98,-159],[-56,-146],[-18,-128],[18,-138],[53,-153],[161,-105],[165,44],[89,138],[-61,147],[-162,51]],-5,5,1,"city_foundation_with_southern_public_gateway");
polygon([[-78,-106],[-13,-109],[57,-80],[86,-22],[56,63],[-20,71],[-88,8]],5,11,2,"monumental_sky_open_public_forum");program.grand_court++;
polygon([[-37,-50],[19,-55],[40,2],[8,42],[-28,27]],11,15,4,"public_civic_botanical_court");program.green_courts++;
quarter("WEST_ASYMMETRIC_INHABITED_CLIFF",-112,-18,-.19,4,77,72,14,28,17);
quarter("NORTH_METROPOLITAN_BALCONIES",3,90,.18,5,105,81,28,28,14);
quarter("EAST_OPEN_URBAN_STRATA",113,-20,.25,3,72,75,12,33,17);
// Massive ridgelines are fragmented, grounded and not roof structures
loft("west_grounded_tectonic_city", [[-160,-109],[-149,-64],[-150,-15],[-145,32],[-119,80],[-74,121]],[25,26,27,30,25,15],[-5,9,23,40,60,71],[40,64,92,122,153,142],0);
loft("east_grounded_tectonic_city", [[158,-118],[150,-60],[150,-11],[136,49],[93,99]],[27,29,27,23,14],[-5,10,31,55,69],[47,81,112,153,120],0);
// Processional route with explicit destinations, subordinate to occupied districts
let P=[[-23,-128],[-21,-86],[-12,-44],[1,4],[3,49],[24,88]],H=[10,23,36,53,69,84],W=[46,43,40,39,33,26];
for(let k=0;k<P.length-1;k++){
let A=P[k],Q=P[k+1],mid=[(A[0]+Q[0])/2,(A[1]+Q[1])/2],yy=(H[k]+H[k+1])/2;
loft("public_climbing_civic_terrace_"+k,[A,mid,Q],[W[k],(W[k]+W[k+1])/2,W[k+1]],[H[k]-4,yy-4,H[k+1]-4],[H[k],yy,H[k+1]],2);program.civic_connections++;
}
function bridge(A,B,w,y,label){let dx=B[0]-A[0],dz=B[1]-A[1],L=Math.hypot(dx,dz),nx=-dz/L*w/2,nz=dx/L*w/2;polygon([[A[0]+nx,A[1]+nz],[B[0]+nx,B[1]+nz],[B[0]-nx,B[1]-nz],[A[0]-nx,A[1]-nz]],y,y+5,2,label);}
bridge([-80,-8],[-38,14],25,48,"west_into_forum_gallery");bridge([33,59],[75,26],26,91,"east_upper_civic_exchange");bridge([-23,71],[58,91],27,124,"high_city_crossing");program.civic_connections+=3;
// Skyline from populated city, asymmetrical in the distant north
for(let [k,x,z,y,h,w,d] of [[0,-51,111,109,62,30,32],[1,-16,117,140,55,34,33],[2,53,116,132,51,34,29]]){
box(x,z,w,d,y,h,6,"north_occupied_crown_"+k,.1*k);
for(let n=0;n<2;n++){let yy=y+9+n*20;if(yy+12<y+h)box(x,z-d*.5,w*.83,1.3,yy,12,3,"inhabited_skyline_glazing_"+k+"_"+n);}
}
let old={v:[],f:[],id:"A30"},mat=0,map={ceramic_land:0,deep_struct:1,public_city:2,inhabited_glass:3,planted_court:4,metallic_rib:5};
for(let line of src.split("\n")){if(line.startsWith("v "))old.v.push(line.trim().split(/\s+/).slice(1,4).map(Number));else if(line.startsWith("usemtl "))mat=map[line.slice(7).trim()]??0;else if(line.startsWith("f ")){let f=line.trim().split(/\s+/).slice(1).map(t=>+t.split("/")[0]-1);if(f.length===3)old.f.push([...f,mat]);}}
if(old.v.length!==2124||old.f.length!==4152)throw Error("bad A30 OBJ baseline");
function bounds(V){let low=[Infinity,Infinity,Infinity],high=[-Infinity,-Infinity,-Infinity];for(let p of V)for(let j=0;j<3;j++){low[j]=Math.min(low[j],p[j]);high[j]=Math.max(high[j],p[j]);}return[low,high];}
function obj(){let out="# G4C7 A31 Actual conceptual 3D model; ART HOLD\nmtllib materials.mtl\n";for(let v of m.v)out+=`v ${v.map(x=>x.toFixed(4)).join(" ")}\n`;let prior=-1;for(let f of m.f){if(f[3]!==prior){prior=f[3];out+=`usemtl ${mats[prior][0]}\n`;}out+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return out;}
function b64(u){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<u.length;i+=3){let a=u[i],b=u[i+1]??0,c=u[i+2]??0;out.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<u.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<u.length?abc[c&63]:"=");}return out.join("");}
function glb(){
let POS=new Uint8Array(m.v.length*12),d=new DataView(POS.buffer);for(let i=0;i<m.v.length;i++)for(let k=0;k<3;k++)d.setFloat32(i*12+k*4,m.v[i][k],true);
let bin=[...POS],views=[{buffer:0,byteOffset:0,byteLength:POS.length,target:34962}],acc=[{bufferView:0,componentType:5126,count:m.v.length,type:"VEC3",min:bounds(m.v)[0],max:bounds(m.v)[1]}],pr=[];
for(let c=0;c<mats.length;c++){let ids=m.f.filter(f=>f[3]===c).flatMap(f=>f.slice(0,3));if(!ids.length)continue;let arr=new Uint8Array(ids.length*4),view=new DataView(arr.buffer);ids.forEach((x,k)=>view.setUint32(k*4,x,true));let offset=bin.length;bin.push(...arr);views.push({buffer:0,byteOffset:offset,byteLength:arr.length,target:34963});acc.push({bufferView:views.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:acc.length-1,material:c,mode:4});}
while(bin.length%4)bin.push(0);
let doc={asset:{version:"2.0",generator:"G4C7 A31 civic valley"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:mats.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],metallicFactor:.12,roughnessFactor:.67},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:views,accessors:acc};
let J=[...JSON.stringify(doc)].map(c=>c.charCodeAt(0));while(J.length%4)J.push(32);let bytes=new Uint8Array(28+J.length+bin.length),q=new DataView(bytes.buffer);q.setUint32(0,0x46546c67,true);q.setUint32(4,2,true);q.setUint32(8,bytes.length,true);q.setUint32(12,J.length,true);q.setUint32(16,0x4e4f534a,true);bytes.set(J,20);let off=20+J.length;q.setUint32(off,bin.length,true);q.setUint32(off+4,0x004e4942,true);bytes.set(bin,off+8);return{base64:b64(bytes),bytes:bytes.length};
}
let viewQA={};
function svg(view){
let origin=eye[view],forward=unit(sub(center,origin)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),M=[old,{v:m.v,f:m.f,id:"A31"}],W=1480,H=570,cell=740,cy=284;
let xml=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#112a3d"/><defs><clipPath id="p0"><rect x="8" y="52" width="724" height="475"/></clipPath><clipPath id="p1"><rect x="748" y="52" width="724" height="475"/></clipPath></defs>`;viewQA[view]=[];
for(let k=0;k<2;k++){
let mod=M[k],cx=k*cell+cell/2,P=mod.v.map(v=>{let q=sub(v,center);return[cx+factor*dot(q,right),cy-factor*dot(q,up)]});
let lo=[Math.min(...P.map(x=>x[0])),Math.min(...P.map(x=>x[1]))],hi=[Math.max(...P.map(x=>x[0])),Math.max(...P.map(x=>x[1]))],fitted=lo[0]>=k*cell+13&&hi[0]<=(k+1)*cell-13&&lo[1]>=54&&hi[1]<=524;
if(!fitted)throw Error("crop "+view+" "+mod.id);viewQA[view].push({model:mod.id,within_frame:fitted,min:lo,max:hi});
let tris=[];for(let f of mod.f){let A=mod.v[f[0]],B=mod.v[f[1]],C=mod.v[f[2]],n=unit(cross(sub(B,A),sub(C,A))),mid=A.map((v,j)=>(v+B[j]+C[j])/3);if(dot(n,sub(origin,mid))<=0)continue;
let h=mats[f[3]][1].slice(1),shade=Math.max(.41,Math.min(1.2,.76+.36*dot(n,unit([-.45,.84,-.33])))),c="#"+[0,2,4].map(j=>Math.min(255,Math.round(parseInt(h.slice(j,j+2),16)*shade)).toString(16).padStart(2,"0")).join("");
tris.push({depth:dot(sub(mid,origin),forward),c,points:f.slice(0,3).map(j=>P[j].map(v=>v.toFixed(2)).join(",")).join(" ")});}
tris.sort((a,b)=>b.depth-a.depth);xml+=`<rect x="${cell*k+8}" y="52" width="724" height="475" fill="#20394e"/><g clip-path="url(#p${k})">`;
for(let t of tris)xml+=`<polygon points="${t.points}" fill="${t.c}" stroke="#294256" stroke-width=".26"/>`;
xml+=`</g><text x="${cell*k+19}" y="37" font-size="21" font-family="sans-serif" fill="#f6fbff">${k?"A31 Civic Valley":"A30 Previous REJECT"}</text>`;}
xml+=`<text x="12" y="559" font-family="sans-serif" font-size="12" fill="#c3d4e1">REAL OBJ geometry: same camera, target [0,78,0], scale 1.03 | ${view.toUpperCase()} | ART HOLD</text></svg>`;return xml;
}
function interior(){
let origin=[-10,27,-36],look=[3,106,97],fw=unit(sub(look,origin)),right=unit(cross([0,1,0],fw)),up=unit(cross(fw,right)),faces=[],W=1050,H=780;
for(let f of m.f){let A=m.v[f[0]],B=m.v[f[1]],C=m.v[f[2]],n=unit(cross(sub(B,A),sub(C,A))),mid=A.map((v,j)=>(v+B[j]+C[j])/3);
if(dot(n,sub(origin,mid))<=0)continue;let pts=f.slice(0,3).map(i=>sub(m.v[i],origin)),z=pts.map(v=>dot(v,fw));if(z.some(x=>x<=3))continue;
let color=mats[f[3]][1].slice(1),shade=Math.max(.41,Math.min(1.21,.77+.36*dot(n,unit([-.43,.85,-.30])))),hex="#"+[0,2,4].map(j=>Math.min(255,Math.round(parseInt(color.slice(j,j+2),16)*shade)).toString(16).padStart(2,"0")).join("");
let xy=pts.map((v,i)=>(525+470*dot(v,right)/z[i]).toFixed(2)+","+(389-470*dot(v,up)/z[i]).toFixed(2)).join(" ");
faces.push({z:z.reduce((a,b)=>a+b,0)/3,xy,hex});}
faces.sort((a,b)=>b.z-a.z);let text=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#172e44"/><text x="21" y="33" fill="#edf7fa" font-size="23" font-family="sans-serif">A31 CIVIC COURT INTERNAL CONCEPT CAMERA (-10,27,-36)</text>`;
for(let t of faces)text+=`<polygon points="${t.xy}" fill="${t.hex}" stroke="#294558" stroke-width=".34"/>`;
text+=`<text x="21" y="757" fill="#b8cbda" font-size="14" font-family="sans-serif">Look target (3,106,97); no collision testing; near plane skipped; NOT a certified walking viewpoint</text></svg>`;
return{text,faces:faces.length,camera:origin,target:look};
}
let assets=[],add=(path,content,encoding="utf-8")=>assets.push({path:DIR+path,content,encoding}),G=glb();
add("a31_civic_valley.obj",obj());add("a31_civic_valley.glb",G.base64,"base64");add("materials.mtl",mats.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let k of Object.keys(eye))add(`fourview/${k}_a30_vs_a31.svg`,svg(k));
let inside=interior();add("interior/a31_internal_civic_court.svg",inside.text);
let manifest={stage:"A31 sculpted inhabited civic valley early real 3D",base_head:"4e95c9c63d947c8901083b2f004a4a82e6e2573f",mesh:{vertices:m.v.length,triangles:m.f.length,individual_closed_solids:m.parts.length,glb_bytes:G.bytes,bounds:bounds(m.v),program,solids:m.parts},comparison:{baseline:"A30 archived OBJ",cameras:eye,target:center,scale:factor,actual_same_camera:true,frame_audit:viewQA},interior:{camera:inside.camera,target:inside.target,visible_triangles:inside.faces,collisions:"NOT VERIFIED"},passed:["isolated solids closed manifold oriented edges","individual volumes positive","no degenerate triangles","actual OBJ GLB mesh exported from same face list","fourview fully fits"],not_proven:["whole assembly joint union or cross solid intersection","load and supports","actual urban walk, egress","third party GLB display","legacy 331 body 993 feet incl negative control","visual art approval","km scale"],safety:"ART HOLD, NO EDUCATION CONSTRUCTION, NO CITY INTEGRATION",legacy:{bodies:331,feet:993,halfwidth:.65,foot_relative:[.15,3.25],old_collisions_max:45,unsupported_feet:0}};
add("a31_manifest.json",JSON.stringify(manifest,null,2));return{assets,manifest};
};
const old=fs.readFileSync("artifacts/g4c7-a30-perforated-cityland/a30_pierced_cityland.obj","utf8");
const result=build(old);for(const f of result.assets){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.manifest.mesh,null,2));
