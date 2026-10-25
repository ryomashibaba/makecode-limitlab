#!/usr/bin/env node
// A28 S0 early art beauty gate, no Minecraft world modification
import fs from "node:fs";import path from "node:path";
const buildA28=function buildA28(referenceOBJ){
const ROOT="artifacts/g4c7-a28-macro-gate/",CAM={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},TARGET=[0,78,0],SCALE=1.03;
const MAT=[["stone","#cbdce5",[.796,.863,.898,1]],["graphite","#476477",[.278,.392,.467,1]],["glass","#60bdc8",[.376,.741,.784,1]],["public","#efc493",[.937,.769,.576,1]],["garden","#7db99f",[.49,.725,.624,1]],["bronze","#b99377",[.725,.576,.467,1]],["city","#7b97a8",[.482,.592,.659,1]]];
const ds=(a,b)=>a.map((x,i)=>x-b[i]),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],unit=a=>a.map(x=>x/Math.hypot(...a));
function make(id,name){return{id,name,v:[],f:[],solids:[],intent:[]};}
function mesh(m,v,f,mat,label){
 let vol=0,deg=0,e=new Map(),direct=new Map();
 for(let t of f){let [a,b,c]=t,A=v[a],B=v[b],C=v[c];if(Math.hypot(...cross(ds(B,A),ds(C,A)))<1e-7)deg++;vol+=dot(A,cross(B,C))/6;}
 if(vol<0){f=f.map(t=>[t[0],t[2],t[1]]);vol=-vol;}
 for(let t of f)for(let j=0;j<3;j++){let a=t[j],b=t[(j+1)%3],k=Math.min(a,b)+":"+Math.max(a,b),d=a+":"+b;e.set(k,(e.get(k)||0)+1);direct.set(d,(direct.get(d)||0)+1);}
 let bad=0;for(let [k,n]of e){let [a,b]=k.split(":");if(n!==2||(direct.get(a+":"+b)||0)!==1||(direct.get(b+":"+a)||0)!==1)bad++;}
 if(vol<=.00001||bad||deg)throw Error("topology failure "+label+" "+JSON.stringify({vol,bad,deg}));
 let off=m.v.length;m.v.push(...v);m.f.push(...f.map(t=>[t[0]+off,t[1]+off,t[2]+off,mat]));m.solids.push({label,triangle_count:f.length,volume:+vol.toFixed(2)});
}
function solid(m,p,lo,hi,mat,label){
 let n=p.length,signed=p.reduce((z,q,i)=>{let t=p[(i+1)%n];return z+q[0]*t[1]-t[0]*q[1]},0);if(hi<=lo||Math.abs(signed)<1e-6)throw Error("invalid solid "+label);
 let P=signed>0?p:[...p].reverse(),v=[],f=[];for(let y of [lo,hi])for(let q of P)v.push([q[0],y,q[1]]);
 for(let i=1;i<n-1;i++)f.push([0,i+1,i],[n,n+i,n+i+1]);
 for(let i=0;i<n;i++){let j=(i+1)%n;f.push([i,j,n+j],[i,n+j,n+i]);}mesh(m,v,f,mat,label);
}
function box(m,x,z,w,d,lo,hi,mat,key,angle=0){let c=Math.cos(angle),s=Math.sin(angle);solid(m,[[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([a,b])=>[x+a*c-b*s,z+a*s+b*c]),lo,hi,mat,key);}
function loft(m,P,width,low,high,mat,label){
 let v=[],f=[];for(let i=0;i<P.length;i++){let A=P[Math.max(0,i-1)],B=P[Math.min(P.length-1,i+1)],d=ds(B,A),len=Math.hypot(...d),n=[-d[1]/len,d[0]/len],p=P[i],w=Array.isArray(width)?width[i]:width,lo=Array.isArray(low)?low[i]:low,hi=Array.isArray(high)?high[i]:high;if(hi<=lo||w<=0||len<.1)throw Error(label+" loft invalid");
 v.push([p[0]+n[0]*w/2,lo,p[1]+n[1]*w/2],[p[0]-n[0]*w/2,lo,p[1]-n[1]*w/2],[p[0]-n[0]*w/2,hi,p[1]-n[1]*w/2],[p[0]+n[0]*w/2,hi,p[1]+n[1]*w/2]);}
 for(let i=0;i<P.length-1;i++)for(let k=0;k<4;k++){let a=i*4+k,b=i*4+(k+1)%4,c=(i+1)*4+(k+1)%4,d=(i+1)*4+k;f.push([a,b,c],[a,c,d]);}
 f.push([0,2,1],[0,3,2]);let q=(P.length-1)*4;f.push([q,q+1,q+2],[q,q+2,q+3]);mesh(m,v,f,mat,label);
}
const footprint=[[-160,-141],[-93,-158],[48,-148],[151,-89],[156,14],[80,138],[-40,146],[-154,58]];
const A=make("A","LIVING ESCARPMENT");solid(A,footprint,-4,7,1,"megaurban_foundation");
loft(A,[[-128,-91],[-122,-27],[-108,40],[-55,96],[28,119],[103,92]],[79,84,74,65,55,29],[-4,10,22,35,58,38],[56,96,139,176,194,133],0,"WEST_NORTH_ACTIVELY_INHABITED_LANDFORM");
loft(A,[[137,-109],[112,-59],[77,-26],[74,25],[91,69]],[63,68,70,60,27],[-4,6,27,39,45],[46,86,121,158,108],6,"EAST_INHABITED_LANDSCAPE");
solid(A,[[-90,-80],[-5,-100],[53,-35],[50,46],[-2,81],[-87,29]],7,13,3,"GRAND_PUBLIC_CIVIC_VOID_DESTINATION");
for(let k=0;k<3;k++){let y=[35,72,110][k],z=[-64,-14,41][k],x=[-84,-92,-73][k];
box(A,x,z,49-k*6,42,y,y+7,3,"WEST_PUBLIC_LEVEL_"+k,-.18);box(A,x-15,z+4,24,33,y+7,y+24,2,"WEST_CITY_FACE_"+k,-.18);
let X=[94,92,86][k],Z=[-77,-27,19][k],Y=[22,53,90][k];
box(A,X,Z,43-k*4,40,Y,Y+7,3,"EAST_PUBLIC_LEVEL_"+k,.20);box(A,X+12,Z,22,32,Y+7,Y+23,2,"EAST_CITY_FACE_"+k,.20);}
loft(A,[[-13,-89],[-5,-37],[14,11],[2,63]],[32,36,42,26],[10,18,27,49],[15,25,36,57],3,"CENTRAL_PROCESSIONAL_CIVIC_SPATIAL_SECTION");
solid(A,[[-32,4],[12,-10],[34,11],[3,44],[-29,37]],13,17,4,"CENTRAL_GREEN_COURT");
A.intent=["asymmetric uneven inhabited escarpments","large public court with definite procession rather than leftover gap","inhabited facades form the two urban cliffs"];
const B=make("B","TRIANGULATED CIVIC FABRIC");solid(B,footprint,-4,10,1,"CONNECTED_CITY_GROUND");
loft(B,[[-141,-72],[-93,-46],[-30,-7],[33,23],[114,58]],[75,84,79,66,38],[-4,15,34,48,29],[65,112,158,187,108],0,"SW_NE_LIVING_STRATUM");
loft(B,[[113,-132],[73,-90],[22,-35],[-37,11],[-115,43]],[63,77,86,70,41],[-4,19,47,50,18],[53,103,142,176,115],6,"SE_NW_INHABITED_URBAN_STRATUM");
loft(B,[[-82,115],[-38,94],[13,75],[65,53],[123,4]],[57,70,76,55,33],[18,28,48,43,13],[99,149,176,153,90],1,"THIRD_CITY_URBAN_STRATUM");
for(let [k,x,z,w,d,y] of [[0,-50,-27,48,43,59],[1,44,39,56,46,92],[2,-43,70,57,49,80]]){box(B,x,z,w,d,y,y+6,3,"MAJOR_SKY_COURT_"+k,.23*(k-1));box(B,x-9,z-7,w*.55,d*.58,y+6,y+26,2,"INHABITED_VISIBLE_FRONTAGE_"+k,.23*(k-1));}
solid(B,[[-55,-89],[21,-94],[79,-52],[84,16],[34,55],[-35,34],[-82,-18]],10,15,3,"CIVIC_AGORA_CROSS_CITY");
loft(B,[[-36,-109],[-15,-47],[19,14],[55,83]],[32,39,40,31],[10,27,53,92],[15,34,60,99],3,"INHABITED_GRAND_PROCESSION");
solid(B,[[-47,-23],[-3,-44],[30,-10],[2,28],[-30,13]],15,19,4,"CENTRAL_GREEN_PUBLIC_ROOM");
B.intent=["three mutually intersecting mega-inhabited routes","off-axis inhabited crossing is the urban spatial program","not a standalone flying bridge or circular building"];
// A27 reference: accurate OBJ stored vertices and material use patterns
let oldMat={"white_urban":0,"basalt_support":1,"city_glazing":2,"open_civic":3,"gardens":4,"bronze_brace":5,"inhabited_cladding":6},O={id:"REF",name:"A27 REJECTED",v:[],f:[]},material=0;
for(let line of referenceOBJ.split("\n")){if(line.startsWith("v ")){O.v.push(line.trim().split(/\s+/).slice(1,4).map(Number));}else if(line.startsWith("usemtl ")){material=oldMat[line.slice(7).trim()]??0;}else if(line.startsWith("f ")){let f=line.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(f.length===3)O.f.push([...f,material]);}}
if(O.v.length!==1158||O.f.length!==1780)throw Error("REFERENCE MISMATCH "+O.v.length+" "+O.f.length);
const models=[A,B];
function OBJ(m){let t=`# A28 ${m.name} stage 0 massing; ART HOLD conceptual not construction\nmtllib materials.mtl\n`;for(let p of m.v)t+=`v ${p.map(x=>x.toFixed(5)).join(" ")}\n`;let last=-1;for(let f of m.f){if(last!==f[3]){last=f[3];t+=`usemtl ${MAT[last][0]}\n`;}t+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return t;}
function base64(u){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",t=[];for(let i=0;i<u.length;i+=3){let a=u[i],b=u[i+1]??0,c=u[i+2]??0;t.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<u.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<u.length?abc[c&63]:"=");}return t.join("");}
function GLB(m){
let pos=new Uint8Array(m.v.length*12),dv=new DataView(pos.buffer);for(let i=0;i<m.v.length;i++)for(let k=0;k<3;k++)dv.setFloat32(i*12+k*4,m.v[i][k],true);
let bin=[...pos],BV=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],AC=[{bufferView:0,componentType:5126,count:m.v.length,type:"VEC3",min:[0,1,2].map(k=>Math.min(...m.v.map(p=>p[k]))),max:[0,1,2].map(k=>Math.max(...m.v.map(p=>p[k])))}],pr=[];
for(let c=0;c<MAT.length;c++){let ids=m.f.filter(f=>f[3]===c).flatMap(f=>f.slice(0,3));if(!ids.length)continue;let buf=new Uint8Array(ids.length*4),dv=new DataView(buf.buffer);ids.forEach((id,i)=>dv.setUint32(i*4,id,true));let at=bin.length;bin.push(...buf);BV.push({buffer:0,byteOffset:at,byteLength:buf.length,target:34963});AC.push({bufferView:BV.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:AC.length-1,material:c,mode:4});}
while(bin.length%4)bin.push(0);
const gltf={asset:{version:"2.0",generator:"G4C7 A28 early art gate"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:MAT.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],metallicFactor:.12,roughnessFactor:.70},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:BV,accessors:AC};
let json=[...JSON.stringify(gltf)].map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
let out=new Uint8Array(28+json.length+bin.length),dv2=new DataView(out.buffer);dv2.setUint32(0,0x46546c67,true);dv2.setUint32(4,2,true);dv2.setUint32(8,out.length,true);dv2.setUint32(12,json.length,true);dv2.setUint32(16,0x4e4f534a,true);out.set(json,20);let off=20+json.length;dv2.setUint32(off,bin.length,true);dv2.setUint32(off+4,0x004e4942,true);out.set(bin,off+8);return{data:base64(out),bytes:out.length};
}
let fitReport={};
function view(name){
let W=1560,H=500,cy=244,P=520,eye=CAM[name],forward=unit(ds(TARGET,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),sets=[O,A,B],txt=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#112438"/><defs>`;
for(let i=0;i<3;i++)txt+=`<clipPath id="p${i}"><rect x="${i*P+6}" y="47" width="508" height="410"/></clipPath>`;
txt+="</defs>";fitReport[name]=[];
for(let i=0;i<3;i++){let m=sets[i],cx=i*P+260,coords=m.v.map(p=>{let q=ds(p,TARGET);return[cx+SCALE*dot(q,right),cy-SCALE*dot(q,up)]});
let box=[Math.min(...coords.map(p=>p[0])),Math.min(...coords.map(p=>p[1])),Math.max(...coords.map(p=>p[0])),Math.max(...coords.map(p=>p[1]))],fit=box[0]>=i*P+9&&box[2]<=i*P+P-9&&box[1]>=50&&box[3]<=456;fitReport[name].push({name:m.id,bbox:box,fit});if(!fit)throw Error("CROPPED "+name+" "+m.id+" "+box);
let draw=[];for(let f of m.f){let a=m.v[f[0]],b=m.v[f[1]],c=m.v[f[2]],N=unit(cross(ds(b,a),ds(c,a))),mid=a.map((q,j)=>(q+b[j]+c[j])/3);if(dot(N,ds(eye,mid))<=0)continue;
let hex=MAT[f[3]][1].slice(1),lit=Math.max(.42,Math.min(1.19,.75+.36*dot(N,unit([-.44,.82,-.36])))),color="#"+[0,2,4].map(j=>Math.min(255,Math.round(parseInt(hex.slice(j,j+2),16)*lit)).toString(16).padStart(2,"0")).join("");
draw.push({depth:dot(ds(mid,eye),forward),xy:f.slice(0,3).map(j=>coords[j].map(x=>x.toFixed(2)).join(",")).join(" "),color});}
draw.sort((a,b)=>b.depth-a.depth);
txt+=`<rect x="${i*P+6}" y="47" width="508" height="410" fill="#213b50" stroke="#6b8498"/><g clip-path="url(#p${i})">`;
for(let t of draw)txt+=`<polygon points="${t.xy}" fill="${t.color}" stroke="#273e51" stroke-width=".42"/>`;
txt+=`</g><text x="${i*P+16}" y="32" font-size="17" font-family="sans-serif" fill="#f4f8fb">${i===0?"A27 REJECTED":i===1?"A28-A LIVING ESCARPMENT":"A28-B TRIANGULATED CIVIC"}</text>`;}
txt+=`<text x="14" y="486" font-family="sans-serif" font-size="11" fill="#bccddd">TRUE TRIANGLES · SAME A26/A27 CAMERA, TARGET AND ORTHOGRAPHIC SCALE 1.03 · EARLY GATE · NOT A KM-SCALE PROOF</text></svg>`;return txt;
}
let files=[],put=(f,content,encoding="utf-8")=>files.push({path:ROOT+f,content,encoding}),stats=[];
for(let m of models){put(`a28_${m.id.toLowerCase()}.obj`,OBJ(m));let glb=GLB(m);put(`a28_${m.id.toLowerCase()}.glb`,glb.data,"base64");
stats.push({id:m.id,title:m.name,vertices:m.v.length,triangles:m.f.length,isolated_closed_solids:m.solids.length,glb_bytes:glb.bytes,intent:m.intent});}
put("materials.mtl",MAT.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let name of Object.keys(CAM))put("fourview/"+name+"_a27_vs_a28.svg",view(name));
let manifest={phase:"A28 S0 early architecture gate",base_sha:"6d88405c34b83d1f20f403fcd52307d159118639",reference:"A27 archived real OBJ",candidate_count:2,scale_hypothesis:"320 conceptual units-wide study; hypothetical 10-12 meters per unit only for intended design scale. NOT physically verified, no Minecraft limitations imposed in initial art.",projection:{same_camera_as_A27:true,eye:CAM,target:TARGET,scale:SCALE,framing:fitReport},stats,verified:["real OBJ/GLB geometric triangles","per-individual-solid closed manifold oriented edges and positive volume","framing of all 3 compared meshes in four views","original A27 OBJ reused for comparison"],not_verified:["independent GLB readback","global Boolean, self-intersections and structural connections","physical accessibility, evacuation","331-body 993-feet legacy QA and negative control","art acceptance"],status:"ART HOLD, aesthetic gate pending",minecraft:"CONSTRUCTION PROHIBITED",integration:"PROHIBITED",previous_qa:{body_samples:331,foot_samples:993,halfwidth:.65,foot_height:[.15,3.25],historic_interferences:45,unsupported_feet:0}};
put("a28_s0_manifest.json",JSON.stringify(manifest,null,2));
return {files,stats,fitReport};
};
const reference=fs.readFileSync("artifacts/g4c7-a27-delta-civic-city/a27_delta_civic_city.obj","utf8");
const result=buildA28(reference);
for(let f of result.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.stats,null,2));
