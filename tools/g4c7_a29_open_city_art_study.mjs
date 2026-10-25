#!/usr/bin/env node
// A29 ART-FIRST public civic city study; only isolated artifact output. No Education world usage.
import fs from "node:fs";import path from "node:path";
const makeA29=function makeA29(oldOBJ){
const ROOT="artifacts/g4c7-a29-open-city-section/",CAM={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270],civic:[60,125,-370]},TARGET=[0,78,0],SCALE=1.03;
const MAT=[["chalk_limestone","#d6e2e6",[.839,.886,.902,1]],["basalt","#45657a",[.271,.396,.478,1]],["civic_floor","#eabf89",[.918,.749,.537,1]],["inhabited_glass","#54bbc3",[.329,.733,.765,1]],["garden","#7daf96",[.49,.686,.588,1]],["bronze","#bc9472",[.737,.58,.447,1]],["habitat","#8198ae",[.506,.596,.682,1]]];
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
const model={id:"A29",name:"CIVIC STRATA / OPEN INHABITED DELTA",v:[],f:[],solids:[],tags:{city_quarters:0,inhabited_large_sections:0,civic_roofgardens:0,substantial_public_levels:0,district_bridges:0}};
function solid(V,F,mat,label){
let vol=0,deg=0,edges=new Map(),dir=new Map();for(let t of F){let A=V[t[0]],B=V[t[1]],C=V[t[2]],N=cross(sub(B,A),sub(C,A));if(Math.hypot(...N)<1e-7)deg++;vol+=dot(A,cross(B,C))/6;}
if(vol<0){F=F.map(f=>[f[0],f[2],f[1]]);vol=-vol;}
for(let t of F)for(let j=0;j<3;j++){let a=t[j],b=t[(j+1)%3],k=Math.min(a,b)+":"+Math.max(a,b),d=a+":"+b;edges.set(k,(edges.get(k)||0)+1);dir.set(d,(dir.get(d)||0)+1);}
let bad=0;for(let [k,n] of edges){let [a,b]=k.split(":");if(n!==2||(dir.get(a+":"+b)||0)!==1||(dir.get(b+":"+a)||0)!==1)bad++;}
if(deg||bad||vol<1e-5)throw Error("FAILED geometric component "+label+" "+JSON.stringify({deg,bad,vol}));
const base=model.v.length;model.v.push(...V);model.f.push(...F.map(t=>[t[0]+base,t[1]+base,t[2]+base,mat]));model.solids.push({label,triangles:F.length,positive_volume:Math.round(vol*100)/100});
}
function extrude(P,lo,hi,mat,label){
if(hi<=lo)throw Error("bad elevation "+label);
const n=P.length,area=P.reduce((z,a,i)=>{let b=P[(i+1)%n];return z+a[0]*b[1]-b[0]*a[1]},0),p=area>0?P:P.slice().reverse();
if(Math.abs(area)<1e-7)throw Error("bad polygon "+label);
let V=[],F=[];for(let y of [lo,hi])for(let q of p)V.push([q[0],y,q[1]]);
for(let i=1;i<n-1;i++)F.push([0,i+1,i],[n,n+i,n+i+1]);
for(let i=0;i<n;i++){let j=(i+1)%n;F.push([i,j,n+j],[i,n+j,n+i]);}
solid(V,F,mat,label);
}
function box(x,z,w,d,lo,hi,mat,label,angle=0){
let c=Math.cos(angle),s=Math.sin(angle);
extrude([[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([a,b])=>[x+a*c-b*s,z+a*s+b*c]),lo,hi,mat,label);
}
function loft(P,W,L,H,mat,label){
let V=[],F=[];for(let i=0;i<P.length;i++){
let a=P[Math.max(0,i-1)],b=P[Math.min(P.length-1,i+1)],dx=b[0]-a[0],dz=b[1]-a[1],d=Math.hypot(dx,dz),nx=-dz/d,nz=dx/d,p=P[i],w=Array.isArray(W)?W[i]:W,lo=Array.isArray(L)?L[i]:L,hi=Array.isArray(H)?H[i]:H;
if(d<=.01||w<=0||hi<=lo)throw Error("bad loft "+label);
V.push([p[0]+nx*w/2,lo,p[1]+nz*w/2],[p[0]-nx*w/2,lo,p[1]-nz*w/2],[p[0]-nx*w/2,hi,p[1]-nz*w/2],[p[0]+nx*w/2,hi,p[1]+nz*w/2]);}
for(let i=0;i<P.length-1;i++)for(let j=0;j<4;j++){let a=4*i+j,b=4*i+(j+1)%4,c=4*(i+1)+(j+1)%4,d=4*(i+1)+j;F.push([a,b,c],[a,c,d]);}
F.push([0,2,1],[0,3,2]);let e=(P.length-1)*4;F.push([e,e+1,e+2],[e,e+2,e+3]);solid(V,F,mat,label);
}
function bridge(A,B,w,lo,hi,mat,label){let dx=B[0]-A[0],dz=B[1]-A[1],len=Math.hypot(dx,dz),px=-dz/len*w/2,pz=dx/len*w/2;extrude([[A[0]+px,A[1]+pz],[B[0]+px,B[1]+pz],[B[0]-px,B[1]-pz],[A[0]-px,A[1]-pz]],lo,hi,mat,label);}
function stratum(name,baseX,baseZ,angle,levels,levelGap,sizes,offset){
const c=Math.cos(angle),s=Math.sin(angle),local=(x,z)=>[baseX+x*c-z*s,baseZ+x*s+z*c];
let width=sizes[0],length=sizes[1];
for(let i=0;i<levels;i++){
let y=18+offset+i*levelGap,shift=Math.sin(i*.92+offset)*8,w=width-i*2.7,d=length-i*1.3;
let ctr=local(shift,0);
box(ctr[0],ctr[1],w,d,y,y+5,2,name+"_public_civic_terrace_"+i,angle);model.tags.substantial_public_levels++;
// one mid-scale room on one street edge and one asymmetric larger Hall; not repeated little boxes
for(let side of [-1,1]){
 let x=shift+side*(w*.25),z=-d*.04+side*i*2,q=local(x,z),ww=w*.30,dd=d*.64-(i%2)*5,rise=18+(i%3)*4+side*2;
 box(q[0],q[1],ww,dd,y+5,y+5+rise,6,name+"_inhabited_hall_"+i+"_"+side,angle);model.tags.inhabited_large_sections++;
 let gg=local(x,-d*.04+side*(dd*.36)),gY=y+8;
 box(gg[0],gg[1],ww*.72,1.4,gY,gY+Math.min(rise-5,12),3,name+"_atrium_facing_glazing_"+i+"_"+side,angle);
}
if(i%2===0){
 let g=local(shift+(i%3)*6,d*.33);
 box(g[0],g[1],w*.30,d*.22,y+5,y+7.2,4,name+"_inhabited_terrace_green_"+i,angle);model.tags.civic_roofgardens++;
}
}
model.tags.city_quarters++;
}
// grounded city is a terraced district rather than one huge roof over the city
extrude([[-166,-139],[-90,-160],[59,-141],[162,-83],[158,30],[75,143],[-46,150],[-161,66]],-4,9,1,"linked_civic_landscape_footprint");
// central monumental open-air civic void; actual terrace in footprint, open towards near camera -Z
extrude([[-91,-84],[1,-111],[84,-53],[77,43],[18,94],[-69,55]],9,14,2,"grand_open_civic_exchange_court");
extrude([[-42,-44],[22,-52],[49,1],[8,57],[-33,31]],14,17,4,"lower_green_public_room");model.tags.civic_roofgardens++;
// three nonparallel inhabited quarter plateaus: each top tier open and visible, significantly different heights
stratum("west_urban_terrace",-105,-2,-.18,4,29,[68,93],1);
stratum("north_ascending_civic",10,111,.3,5,27,[83,76],20);
stratum("east_city_fin",108,-27,-.5,3,34,[65,90],12);
// shift skyline via big public inhabited terraces, not big external dead walls
loft([[-143,-73],[-144,-18],[-127,42],[-101,98],[-59,128]],[38,44,41,28,14],[-4,13,27,48,60],[37,58,95,117,101],0,"WEST_URBAN_BUTTRESS_ANCHORED_TO_INHABITED_FRONTAGE");
loft([[138,-112],[137,-60],[132,-5],[111,59],[74,101]],[36,38,30,24,13],[-4,6,34,59,75],[43,69,101,143,119],0,"EAST_TECTONIC_BACKBONE_OPEN_FACE_TO_CIVIC_SPACE");
// prominent urban exchange terraces: no isolated bridge-shaped building
for(let [i,x,z,w,d,y,ang] of [[0,-42,7,42,31,35,.18],[1,39,35,53,35,67,-.22],[2,-26,80,38,39,103,.18]]){
 box(x,z,w,d,y,y+6,2,"civic_district_assembly_"+i,ang);model.tags.substantial_public_levels++;
 box(x,z,w*.72,d*.62,y+6,y+26+(i%2)*5,6,"active_inhabited_civic_hall_"+i,ang);model.tags.inhabited_large_sections++;
 let gp=x+8,gz=z-10;box(gp,gz,w*.34,d*.4,y+6,y+8.5,4,"civic_hanging_garden_"+i,ang);model.tags.civic_roofgardens++;
}
// urban processional concourses: broad and short, not a single highway dominating composition
for(let [i,A,B,width,level] of [
 [0,[-64,-79],[-32,-37],29,16],
 [1,[-32,-37],[4,-5],33,28],
 [2,[4,-5],[22,39],37,41],
 [3,[22,39],[8,82],29,59]
]){loft([A,[(A[0]+B[0])/2,(A[1]+B[1])/2],B],[width,width+3,width],[level-4,level+3,level+9],[level,level+7,level+13],2,"inhabited_rising_public_terrace_"+i);model.tags.district_bridges++;}
bridge([-72,-9],[-31,11],24,52,58,2,"western_to_exchange_gallery");model.tags.district_bridges++;
bridge([43,16],[89,-13],27,69,75,2,"eastern_to_exchange_gallery");model.tags.district_bridges++;
bridge([-36,75],[44,83],31,117,124,2,"urban_skyline_public_boulevard");model.tags.district_bridges++;
// readable urban silhouette derived from sky courts and occupied groups, not random thin spires
for(let [i,x,z,low,top,w,d]of [[0,-110,38,95,142,25,28],[1,-50,105,109,168,21,31],[2,20,125,137,191,29,34],[3,101,51,118,168,23,37]]){
 box(x,z,w,d,low,top,6,"inhabited_skyline_landmark_"+i,(i-1)*.19);model.tags.inhabited_large_sections++;
 box(x,z-12,w*.66,1.5,low+9,low+22,3,"visible_city_high_gallery_"+i,(i-1)*.19);
}
// A28 comparison model from saved real OBJ
let ref={id:"A28-A",name:"A28-A REJECTED",v:[],f:[]},oldMap={stone:0,graphite:1,glass:3,public:2,garden:4,bronze:5,city:6},active=0;
for(let ln of oldOBJ.split("\n")){if(ln.startsWith("v ")){ref.v.push(ln.trim().split(/\s+/).slice(1,4).map(Number));}else if(ln.startsWith("usemtl ")){active=oldMap[ln.slice(7).trim()]??0;}else if(ln.startsWith("f ")){let p=ln.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(p.length===3)ref.f.push([...p,active]);}}
if(ref.v.length!==194||ref.f.length!==316)throw Error("reference mismatch");
function bounds(V){let min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];for(let p of V)for(let j=0;j<3;j++){min[j]=Math.min(min[j],p[j]);max[j]=Math.max(max[j],p[j]);}return[min,max];}
function OBJ(){let s=`# G4-C7 A29 real 3D conceptual mass with populated public tiers ART HOLD\nmtllib materials.mtl\n`;for(let p of model.v)s+=`v ${p.map(x=>x.toFixed(4)).join(" ")}\n`;let prev=-1;for(let f of model.f){if(f[3]!==prev){s+=`usemtl ${MAT[f[3]][0]}\n`;prev=f[3];}s+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return s;}
function base64(u){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<u.length;i+=3){let a=u[i],b=u[i+1]??0,c=u[i+2]??0;out.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<u.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<u.length?abc[c&63]:"=");}return out.join("");}
function GLB(){
let v=new Uint8Array(model.v.length*12),dv=new DataView(v.buffer);for(let i=0;i<model.v.length;i++)for(let j=0;j<3;j++)dv.setFloat32(i*12+j*4,model.v[i][j],true);
let binary=[...v],views=[{buffer:0,byteOffset:0,byteLength:v.length,target:34962}],acc=[{bufferView:0,componentType:5126,count:model.v.length,type:"VEC3",min:bounds(model.v)[0],max:bounds(model.v)[1]}],prim=[];
for(let m=0;m<MAT.length;m++){let f=model.f.filter(x=>x[3]===m).flatMap(x=>x.slice(0,3));if(!f.length)continue;let bytes=new Uint8Array(4*f.length),view=new DataView(bytes.buffer);f.forEach((x,i)=>view.setUint32(i*4,x,true));let at=binary.length;binary.push(...bytes);views.push({buffer:0,byteOffset:at,byteLength:bytes.length,target:34963});acc.push({bufferView:views.length-1,componentType:5125,count:f.length,type:"SCALAR"});prim.push({attributes:{POSITION:0},indices:acc.length-1,material:m,mode:4});}
while(binary.length%4)binary.push(0);
let gltf={asset:{version:"2.0",generator:"G4C7 A29 OPEN CITY research"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:model.name}],meshes:[{primitives:prim}],materials:MAT.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],metallicFactor:.12,roughnessFactor:.70},doubleSided:true})),buffers:[{byteLength:binary.length}],bufferViews:views,accessors:acc};
let J=[...JSON.stringify(gltf)].map(x=>x.charCodeAt(0));while(J.length%4)J.push(32);let bytes=new Uint8Array(28+J.length+binary.length),h=new DataView(bytes.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,bytes.length,true);h.setUint32(12,J.length,true);h.setUint32(16,0x4e4f534a,true);bytes.set(J,20);let pos=20+J.length;h.setUint32(pos,binary.length,true);h.setUint32(pos+4,0x004e4942,true);bytes.set(binary,pos+8);
return {data:base64(bytes),length:bytes.length};
}
let QA={};
function render(view){
let eye=CAM[view],front=unit(sub(TARGET,eye)),right=unit(cross([0,1,0],front)),up=unit(cross(front,right));
let sets=view==="civic"?[model]:[ref,model],width=sets.length===1?850:1400,height=540,cell=sets.length===1?850:700,cy=264;
let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}"><rect width="${width}" height="${height}" fill="#101f31"/><defs>`;
for(let j=0;j<sets.length;j++)s+=`<clipPath id="p${j}"><rect x="${j*cell+10}" y="48" width="${cell-20}" height="443"/></clipPath>`;
s+="</defs>";QA[view]=[];
for(let j=0;j<sets.length;j++){
let m=sets[j],cx=j*cell+cell/2,P=m.v.map(p=>{let d=sub(p,TARGET);return[cx+dot(d,right)*SCALE,cy-dot(d,up)*SCALE]});
let min=[Math.min(...P.map(p=>p[0])),Math.min(...P.map(p=>p[1]))],max=[Math.max(...P.map(p=>p[0])),Math.max(...P.map(p=>p[1]))],fit=min[0]>=cell*j+16&&max[0]<=(j+1)*cell-16&&min[1]>=54&&max[1]<=485;
QA[view].push({id:m.id,min,max,in_frame:fit});if(!fit)throw Error("clipped "+view+" "+m.id);
s+=`<rect x="${cell*j+10}" y="48" width="${cell-20}" height="443" fill="#1a3348" stroke="#4c6c87"/><g clip-path="url(#p${j})">`;
let list=[];for(let f of m.f){let A=m.v[f[0]],B=m.v[f[1]],C=m.v[f[2]],normal=unit(cross(sub(B,A),sub(C,A))),mid=A.map((x,k)=>(x+B[k]+C[k])/3);
if(dot(normal,sub(eye,mid))<=0)continue;
let base=MAT[f[3]][1].slice(1),light=Math.max(.41,Math.min(1.22,.77+.38*dot(normal,unit([-.4,.82,-.36])))),color="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(base.slice(k,k+2),16)*light)).toString(16).padStart(2,"0")).join("");
list.push({z:dot(sub(mid,eye),front),p:f.slice(0,3).map(k=>P[k].map(n=>n.toFixed(2)).join(",")).join(" "),color});}
list.sort((a,b)=>b.z-a.z);for(let t of list)s+=`<polygon points="${t.p}" fill="${t.color}" stroke="#294457" stroke-width=".28"/>`;
s+=`</g><text x="${cell*j+25}" y="32" font-size="20" font-family="sans-serif" fill="#eff8fc">${m.id==="A29"?"A29 CIVIC STRATA - OPEN CITY":"A28-A REJECTED BENCHMARK"}</text>`;}
s+=`<text x="20" y="526" fill="#b6cddf" font-size="12" font-family="sans-serif">REAL TRIANGLE PROJECTION · ${view.toUpperCase()} · SAME CAMERA / TARGET / SCALE 1.03 · ART HOLD · NO CONSTRUCTION</text></svg>`;
return s;
}
let files=[],add=(path,content,encoding="utf-8")=>files.push({path:ROOT+path,content,encoding}),g=GLB();
add("a29_civic_strata.obj",OBJ());add("a29_civic_strata.glb",g.data,"base64");
add("materials.mtl",MAT.map(m=>`newmtl ${m[0]}\nKd ${m[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let view of Object.keys(CAM))add((view==="civic"?"interior/":"fourview/")+view+"_a28a_vs_a29.svg",render(view));
let report={stage:"G4-C7 A29 simultaneous urban/public/main structure initial art candidate",parent:"cc486aa8e2dcf537831bcda402992e1d851a8433",reference:"archived A28-A genuine OBJ",concept:"Three asymmetric occupied urban districts visibly opening on inhabited city-scale public basin. Fragmentary main buttresses remain secondary.",model:{vertices:model.v.length,triangles:model.f.length,closed_component_count:model.solids.length,bounds:bounds(model.v),program:model.tags,glb_file_bytes:g.length},scale_hypothesis:{unit:"conceptual unit",hypothetical_real_world_factor:10,intended_bbox_in_meters:bounds(model.v).map(p=>p.map(x=>x*10)),warning:"A scale assumption, not demonstrated physical km scale or Minecraft capacity"},cameras:CAM,target:TARGET,ortho_scale:SCALE,view_frame_audit:QA,checks_done:["individual positive-volume closed solids","degenerate face count 0","undirected paired edges and opposite directed half edges","real OBJ GLB binary generated from actual same triangular mesh","same four historical A26-28 cameras and scale; A28A actual stored model reprojected","all projected silhouettes inside frames"],unverified:["external independent GLB loader","all-solid Boolean union/intersection","structural load, useable urban space and egress","candidate 331-body/993-feet including negative control","independent human acceptance"],status:"ART HOLD / NOT YET HUMAN-APPROVED",construction:"PROHIBITED",city_integration:"PROHIBITED",old_assets:"UNMODIFIED",legacy:{body:331,feet:993,halfwidth:.65,foot_relative:[.15,3.25],old_collision_cap:45,unsupported_feet_max:0}};
add("a29_initial_manifest.json",JSON.stringify(report,null,2));
return{files,report};
};
const src=fs.readFileSync("artifacts/g4c7-a28-macro-gate/a28_a.obj","utf8");
const result=makeA29(src);
for(const f of result.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.report.model,null,2));
