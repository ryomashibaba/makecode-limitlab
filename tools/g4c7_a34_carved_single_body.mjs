#!/usr/bin/env node
// A34 ART HOLD, single connected carved city research only. Never invokes Minecraft.
import fs from "node:fs";import path from "node:path";
const model=function model(reference){
const root="artifacts/g4c7-a34-carved-single-mass/",nx=42,ny=24,nz=40,N=nx*ny*nz,S=10,low=[-210,-10,-200],vox=new Uint8Array(N);
const cams={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},target=[0,78,0],scale=1.03;
const materials=[["limestone","#d9e7eb",[.85,.906,.922,1]],["support","#476579",[.278,.396,.475,1]],["plaza","#edc391",[.929,.765,.569,1]],["facade","#5ebec9",[.369,.745,.788,1]],["garden","#80b59e",[.502,.71,.62,1]],["north","#b1c3cd",[.694,.765,.804,1]]];
const D=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],valid=(i,j,k)=>i>=0&&j>=0&&k>=0&&i<nx&&j<ny&&k<nz,I=(i,j,k)=>(k*ny+j)*nx+i,get=(i,j,k)=>valid(i,j,k)?vox[I(i,j,k)]:0;
function carve(x,y,z){
if(y<0||y>225)return false;
if(y<=10&&Math.abs(x)<185+13*Math.sin(z/44)&&Math.abs(z)<183+8*Math.sin(x/70))return true;
const wi=-39+12*Math.sin(z/59),ei=47+13*Math.sin((z-22)/57);
let solid=z>-164&&z<170&&((x>-194+8*Math.sin((z+25)/55)&&x<wi&&y<96+.26*(z+130)+.14*(-x-50)+11*Math.sin(z/39)+7*Math.cos(x/27))||(x>ei&&x<192-12*Math.cos((z+6)/64)&&y<61+.21*(z+130)+.11*(x-50)+9*Math.sin(z/44)));
if(z>78&&z<185&&x>-118&&x<111&&y<151+.25*(z-88)+16*Math.sin((x+50)/52))solid=true;
if(!solid)return false;
if(z>-178&&z<112&&y>=10&&x>wi-3&&x<ei+3)return false;
if(z>88&&z<181&&x>-76&&x<79&&y>36&&y<133)return false;
if(z>131&&z<179&&x>-43&&x<47&&y>=133)return false;
for(let r of [[27,62,-130,-35,-142,-24],[84,121,-18,86,-149,-30],[139,168,98,161,-138,-28],[30,73,-125,23,27,150],[91,136,15,128,30,143]])if(y>r[0]&&y<r[1]&&z>r[2]&&z<r[3]&&x>r[4]&&x<r[5])return false;
return true;
}
for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)vox[I(i,j,k)]=carve(low[0]+(i+.5)*S,low[1]+(j+.5)*S,low[2]+(k+.5)*S)?1:0;
let repairs=0;for(let t=0;t<9;t++){
let todo=new Set();for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)for(let [a,b] of [[0,1],[0,2],[1,2]]){
let p=[i,j,k],q=p.slice(),r=p.slice(),s=p.slice();q[a]++;r[b]++;s[a]++;s[b]++;if(!valid(...s))continue;
let cells=[p,q,r,s],bits=cells.map(x=>get(...x));if(bits[0]===bits[3]&&bits[1]===bits[2]&&bits[0]!==bits[1]){
let missing=cells.filter((x,i)=>!bits[i]);missing.sort((a,b)=>D.reduce((s,d)=>s+get(b[0]+d[0],b[1]+d[1],b[2]+d[2])-get(a[0]+d[0],a[1]+d[1],a[2]+d[2]),0));todo.add(I(...missing[0]));}}
if(!todo.size)break;for(let p of todo)if(!vox[p]){vox[p]=1;repairs++;}if(t===8)throw Error("corner repair cap");
}
let solidCells=vox.reduce((a,b)=>a+b,0);
function flood(value,boundary){let seen=new Uint8Array(N),queue=new Int32Array(N),s=0,e=0;for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){
if(boundary&&i!==0&&i!==nx-1&&j!==ny-1&&k!==0&&k!==nz-1)continue;if(!boundary&&e)continue;let p=I(i,j,k);if(vox[p]!==value)continue;seen[p]=1;queue[e++]=p;}
while(s<e){let p=queue[s++],i=p%nx,j=Math.floor(p/nx)%ny,k=Math.floor(p/(nx*ny));for(let d of D){let x=i+d[0],y=j+d[1],z=k+d[2];if(!valid(x,y,z))continue;let q=I(x,y,z);if(seen[q]||vox[q]!==value)continue;seen[q]=1;queue[e++]=q;}}
return{seen,count:e};}
const structure=flood(1,false),air=flood(0,true);if(structure.count!==solidCells)throw Error("not single mass");
const rooms={arrival:[0,25,-150],exchange:[0,45,-30],westLower:[-105,45,-75],westUpper:[-100,105,55],eastLower:[110,55,-65],eastUpper:[100,110,75],north:[0,85,140]},checks={};
for(let [name,xyz] of Object.entries(rooms)){let [i,j,k]=xyz.map((x,n)=>Math.floor((x-low[n])/S));checks[name]=valid(i,j,k)&&!get(i,j,k)&&!!air.seen[I(i,j,k)];if(!checks[name])throw Error("room not connected "+name);}
let V=[],F=[],vertexMap=new Map(),quads=0;
function vid(i,j,k){let key=i+","+j+","+k,q=vertexMap.get(key);if(q===undefined){q=V.length;vertexMap.set(key,q);V.push([low[0]+i*S,low[1]+j*S,low[2]+k*S]);}return q;}
function face(i,j,k,d){
let p=d===0?[[i+1,j,k],[i+1,j+1,k],[i+1,j+1,k+1],[i+1,j,k+1]]:d===1?[[i,j,k],[i,j,k+1],[i,j+1,k+1],[i,j+1,k]]:d===2?[[i,j+1,k],[i,j+1,k+1],[i+1,j+1,k+1],[i+1,j+1,k]]:d===3?[[i,j,k],[i+1,j,k],[i+1,j,k+1],[i,j,k+1]]:d===4?[[i,j,k+1],[i+1,j,k+1],[i+1,j+1,k+1],[i,j+1,k+1]]:[[i,j,k],[i,j+1,k],[i+1,j+1,k],[i+1,j,k]];
let a=p.map(x=>vid(...x)),x=low[0]+(i+.5)*S,y=low[1]+(j+.5)*S,z=low[2]+(k+.5)*S,c=d===2?2:1;
if(d!==2&&d!==3&&y>15&&Math.abs(x)<155&&z<132)c=3;
if(z>99&&Math.abs(x)<118&&y>30)c=5;
if(d===2&&y<15&&Math.abs(x)<63)c=4;
if((d===0||d===1)&&Math.abs(x)>154)c=0;
F.push([a[0],a[1],a[2],c],[a[0],a[2],a[3],c]);quads++;
}
for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)if(get(i,j,k))for(let d=0;d<6;d++){let a=D[d];if(!get(i+a[0],j+a[1],k+a[2]))face(i,j,k,d);}
let edges=new Map(),dirs=new Map();for(let t of F)for(let k=0;k<3;k++){let a=t[k],b=t[(k+1)%3],e=Math.min(a,b)+":"+Math.max(a,b),d=a+":"+b;edges.set(e,(edges.get(e)||0)+1);dirs.set(d,(dirs.get(d)||0)+1);}
let invalidEdges=0;for(let [key,count] of edges){let [a,b]=key.split(":");if(count!==2||(dirs.get(a+":"+b)||0)!==1||(dirs.get(b+":"+a)||0)!==1)invalidEdges++;}if(invalidEdges)throw Error("not manifold "+invalidEdges);
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
let prior={id:"A33",v:[],f:[]},m=0,priorMat={stone:0,deep:1,civic:2,inhabited_glass:3,green:4,bronze:5,city:0};
for(let line of reference.split("\n")){if(line.startsWith("v "))prior.v.push(line.trim().split(/\s+/).slice(1,4).map(Number));else if(line.startsWith("usemtl "))m=priorMat[line.slice(7).trim()]??0;else if(line.startsWith("f ")){let t=line.trim().split(/\s+/).slice(1).map(a=>Number(a.split("/")[0])-1);if(t.length===3)prior.f.push([...t,m]);}}
if(prior.v.length!==282||prior.f.length!==484)throw Error("old model mismatch");
function b64(arr){let a="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<arr.length;i+=3){let x=arr[i],y=arr[i+1]??0,z=arr[i+2]??0;out.push(a[x>>2],a[((x&3)<<4)|(y>>4)],i+1<arr.length?a[((y&15)<<2)|(z>>6)]:"=",i+2<arr.length?a[z&63]:"=");}return out.join("");}
function obj(){let s="# A34 SINGLE CONNECTED CARVED CAVITY STUDY (ART HOLD)\nmtllib materials.mtl\n";for(let p of V)s+=`v ${p.join(" ")}\n`;let last=-1;for(let t of F){if(last!==t[3]){last=t[3];s+=`usemtl ${materials[last][0]}\n`;}s+=`f ${t[0]+1} ${t[1]+1} ${t[2]+1}\n`;}return s;}
function glb(){
let pos=new Uint8Array(V.length*12),dv=new DataView(pos.buffer);for(let i=0;i<V.length;i++)for(let k=0;k<3;k++)dv.setFloat32(i*12+k*4,V[i][k],true);
let buf=[...pos],views=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],access=[{bufferView:0,componentType:5126,count:V.length,type:"VEC3",min:[0,1,2].map(k=>Math.min(...V.map(p=>p[k]))),max:[0,1,2].map(k=>Math.max(...V.map(p=>p[k])))}],prim=[];
for(let j=0;j<materials.length;j++){let ids=F.filter(f=>f[3]===j).flatMap(f=>f.slice(0,3));if(!ids.length)continue;let bytes=new Uint8Array(ids.length*4),v=new DataView(bytes.buffer);ids.forEach((x,k)=>v.setUint32(k*4,x,true));let at=buf.length;buf.push(...bytes);views.push({buffer:0,byteOffset:at,byteLength:bytes.length,target:34963});access.push({bufferView:views.length-1,componentType:5125,count:ids.length,type:"SCALAR"});prim.push({attributes:{POSITION:0},indices:access.length-1,material:j,mode:4});}
while(buf.length%4)buf.push(0);
let json=Array.from(JSON.stringify({asset:{version:"2.0",generator:"G4C7 A34 carved single body"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prim}],materials:materials.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],roughnessFactor:.72,metallicFactor:.10},doubleSided:true})),buffers:[{byteLength:buf.length}],bufferViews:views,accessors:access}),x=>x.charCodeAt(0));
while(json.length%4)json.push(32);let all=new Uint8Array(28+json.length+buf.length),d=new DataView(all.buffer);d.setUint32(0,0x46546c67,true);d.setUint32(4,2,true);d.setUint32(8,all.length,true);d.setUint32(12,json.length,true);d.setUint32(16,0x4e4f534a,true);all.set(json,20);let p=20+json.length;d.setUint32(p,buf.length,true);d.setUint32(p+4,0x004e4942,true);all.set(buf,p+8);return{base64:b64(all),bytes:all.length};}
function svgView(name){
let eye=cams[name],forward=unit(sub(target,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),s=`<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="880" viewBox="0 0 1500 880"><rect width="1500" height="880" fill="#13283c"/><defs><clipPath id="c0"><rect x="10" y="50" width="730" height="780"/></clipPath><clipPath id="c1"><rect x="760" y="50" width="730" height="780"/></clipPath></defs>`;
for(let j=0;j<2;j++){
let source=j?{v:V,f:F}:prior,p=source.v.map(v=>{let a=sub(v,target);return[j*750+375+scale*dot(a,right),435-scale*dot(a,up)]});
let box=[Math.min(...p.map(x=>x[0])),Math.min(...p.map(x=>x[1])),Math.max(...p.map(x=>x[0])),Math.max(...p.map(x=>x[1]))];
if(box[0]<j*750+13||box[2]>(j+1)*750-13||box[1]<55||box[3]>829)throw Error("frame cropped "+name+" "+box);
let faces=[];for(let t of source.f){let a=source.v[t[0]],b=source.v[t[1]],c=source.v[t[2]],n=unit(cross(sub(b,a),sub(c,a))),mid=a.map((x,k)=>(x+b[k]+c[k])/3);if(dot(n,sub(eye,mid))<=0)continue;
let col=materials[t[3]][1].slice(1),q=Math.max(.42,Math.min(1.19,.78+.35*dot(n,unit([-.45,.83,-.32])))),fill="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(col.slice(k,k+2),16)*q)).toString(16).padStart(2,"0")).join("");
faces.push({z:dot(sub(mid,eye),forward),pts:t.slice(0,3).map(k=>p[k].map(v=>v.toFixed(2)).join(",")).join(" "),fill});}
faces.sort((a,b)=>b.z-a.z);s+=`<g clip-path="url(#c${j})">`;for(let q of faces)s+=`<polygon points="${q.pts}" fill="${q.fill}" stroke="#1e3949" stroke-width=".11"/>`;s+=`</g><text x="${j*750+16}" y="30" font-size="20" fill="white" font-family="sans-serif">${j?"A34 CARVED ONE-PIECE CITY":"A33 ARCHIVED REJECTED"}</text>`;}
return s+`<text x="15" y="861" fill="#b8d0df" font-size="13" font-family="sans-serif">REAL 3D MESH TRIANGLES / ${name} / unchanged camera and scale 1.03 / expanded COMMON viewport / ART HOLD</text></svg>`;
}
const GL=glb(),files=[],add=(name,content,encoding="utf-8")=>files.push({path:"artifacts/g4c7-a34-carved-single-body/"+name,content,encoding});
add("a34_city.obj",obj());add("a34_city.glb",GL.base64,"base64");
add("materials.mtl",materials.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let name of Object.keys(cams))add("fourview/"+name+"_a33_vs_a34.svg",svgView(name));
let record={phase:"A34 genuine single connected carved urban negative space",date:"2026-10-25 JST",source_head:"b621608fad0984b8f658f667afaa3ca21f99f86a",model:{solid_grid_cells:solidCells,solid_connected_cells:structure.count,corner_cells_repaired:repairs,watertight_bad_edges:invalidEdges,vertices:V.length,triangles:F.length,quads,glb_bytes:GL.bytes},city_cavities:{named_hall_air_reachable_from_exterior:checks,exterior_connected_air_grid_cells:air.count,route_walkability:"NOT TESTED"},fourview:{same_cameras:true,same_scale:scale,larger_common_viewport:[1500,880],reference:"archived A33 genuine OBJ"},qa_done:["single connected occupied mass","edge-manifold oriented triangle surface","selected large carved void samples air-connected to exterior","equal-camera projections"],qa_not_done:["GLB independent reread","3D structural safety","331-body 993-feet QA and negative control","3D external rendering","human walking route","art signoff"],safety:{art_hold:true,construction:"FORBIDDEN",city_integration:"FORBIDDEN",history:"PRESERVED",body_samples:331,feet_samples:993,halfwidth:.65,foot_relative:[.15,3.25],body_interference_max:45,unsupported_feet:0,negative_control:"REQUIRED"}};
add("a34_manifest.json",JSON.stringify(record,null,2));
return{files,record};
};
const ref=fs.readFileSync("artifacts/g4c7-a33-open-city-section-g1/a33_open_city_section.obj","utf8");
const r=model(ref);for(let f of r.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(r.record.model,null,2));
