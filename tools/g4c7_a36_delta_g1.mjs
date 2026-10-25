#!/usr/bin/env node
// G4-C7 A36 one CIVIC DELTA model, no Minecraft action, ART HOLD.
import fs from "node:fs";import path from "node:path";
const make=function make(){
const nx=42,ny=23,nz=42,n=nx*ny*nz,S=10,O=[-210,-10,-210],occ=new Uint8Array(n),D=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],valid=(i,j,k)=>i>=0&&j>=0&&k>=0&&i<nx&&j<ny&&k<nz,I=(i,j,k)=>(k*ny+j)*nx+i,at=(i,j,k)=>valid(i,j,k)?occ[I(i,j,k)]:0;
const arms=[
{points:[[-130,-150],[-38,-48],[35,42],[125,153]],width:76,height:[65,173]},
{points:[[-28,-36],[-91,42],[-166,120]],width:59,height:[89,137]},
{points:[[38,37],[122,-30],[166,-128]],width:62,height:[111,143]}
];
function distance(x,z,arm){let best={d:1e7,t:0};for(let k=0;k<arm.points.length-1;k++){let a=arm.points[k],b=arm.points[k+1],dx=b[0]-a[0],dz=b[1]-a[1],q=Math.max(0,Math.min(1,((x-a[0])*dx+(z-a[1])*dz)/(dx*dx+dz*dz))),d=Math.hypot(x-a[0]-q*dx,z-a[1]-q*dz);if(d<best.d)best={d,t:(k+q)/(arm.points.length-1)};}return best;}
function material(x,y,z){if(y<0||y>208)return false;let tests=arms.map(a=>{let r=distance(x,z,a);return {d:r.d,width:a.width,top:a.height[0]*(1-r.t)+a.height[1]*r.t};});
if(y<=10&&tests.some(v=>v.d<v.width+24))return true;
if(!tests.some(v=>v.d<v.width&&y<v.top))return false;
if(x>-57&&x<58&&z>-60&&z<67&&y>15&&y<118)return false;
if(x>-124&&x<-36&&z>4&&z<108&&y>36&&y<73)return false;
if(x>58&&x<137&&z>-105&&z<36&&y>48&&y<91)return false;
if(x>-110&&x<-19&&z>64&&z<139&&y>98&&y<127)return false;
if(x>19&&x<115&&z>71&&z<171&&y>118&&y<148)return false;
return true;
}
for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)occ[I(i,j,k)]=material(O[0]+(i+.5)*S,O[1]+(j+.5)*S,O[2]+(k+.5)*S)?1:0;
let repairs=0;for(let t=0;t<10;t++){let fix=new Set();for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)for(let [a,b] of [[0,1],[0,2],[1,2]]){let p=[i,j,k],q=p.slice(),r=p.slice(),s=p.slice();q[a]++;r[b]++;s[a]++;s[b]++;if(!valid(...s))continue;let pts=[p,q,r,s],v=pts.map(x=>at(...x));if(v[0]===v[3]&&v[1]===v[2]&&v[0]!==v[1]){let empty=pts.filter((x,k)=>!v[k]);fix.add(I(...empty[0]));}}if(!fix.size)break;for(let p of fix){if(!occ[p]){occ[p]=1;repairs++;}}if(t===9)throw Error("corner contact unresolved");}
let solid=occ.reduce((a,b)=>a+b,0);
function flood(want,outer){let seen=new Uint8Array(n),q=new Int32Array(n),h=0,e=0;for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++){if(outer&&i!==0&&i!==nx-1&&j!==ny-1&&k!==0&&k!==nz-1)continue;if(!outer&&e)continue;let p=I(i,j,k);if(occ[p]===want&&!seen[p]){seen[p]=1;q[e++]=p;}}
while(h<e){let p=q[h++],i=p%nx,j=Math.floor(p/nx)%ny,k=Math.floor(p/(nx*ny));for(let [a,b,c]of D){let x=i+a,y=j+b,z=k+c;if(!valid(x,y,z))continue;let u=I(x,y,z);if(seen[u]||occ[u]!==want)continue;seen[u]=1;q[e++]=u;}}return{seen,count:e};}
let connected=flood(1,false),air=flood(0,true);if(connected.count!==solid)throw Error("not connected "+connected.count+" of "+solid);
let V=[],T=[],map=new Map(),quadCount=0;
function v(i,j,k){let a=[i,j,k].join(","),idx=map.get(a);if(idx===undefined){idx=V.length;V.push([O[0]+S*i,O[1]+S*j,O[2]+S*k]);map.set(a,idx);}return idx;}
function put(i,j,k,d){const P=d===0?[[i+1,j,k],[i+1,j+1,k],[i+1,j+1,k+1],[i+1,j,k+1]]:d===1?[[i,j,k],[i,j,k+1],[i,j+1,k+1],[i,j+1,k]]:d===2?[[i,j+1,k],[i,j+1,k+1],[i+1,j+1,k+1],[i+1,j+1,k]]:d===3?[[i,j,k],[i+1,j,k],[i+1,j,k+1],[i,j,k+1]]:d===4?[[i,j,k+1],[i+1,j,k+1],[i+1,j+1,k+1],[i,j+1,k+1]]:[[i,j,k],[i,j+1,k],[i+1,j+1,k],[i+1,j,k]];
let f=P.map(p=>v(...p)),x=O[0]+(i+.5)*S,y=O[1]+(j+.5)*S,z=O[2]+(k+.5)*S,m=d===2?2:1;
if(y<15&&d===2)m=4;else if(z>75&&y>105)m=5;else if(y>25&&d!==2&&d!==3)m=3;else if(d===0||d===1)m=0;
T.push([f[0],f[1],f[2],m],[f[0],f[2],f[3],m]);quadCount++;}
for(let k=0;k<nz;k++)for(let j=0;j<ny;j++)for(let i=0;i<nx;i++)if(at(i,j,k))for(let d=0;d<6;d++){let a=D[d];if(!at(i+a[0],j+a[1],k+a[2]))put(i,j,k,d);}
let edges=new Map(),oriented=new Map();for(let f of T)for(let j=0;j<3;j++){let a=f[j],b=f[(j+1)%3],key=Math.min(a,b)+":"+Math.max(a,b),dir=a+":"+b;edges.set(key,(edges.get(key)||0)+1);oriented.set(dir,(oriented.get(dir)||0)+1);}
let invalid=0;for(let [key,m]of edges){let [a,b]=key.split(":");if(m!==2||(oriented.get(a+":"+b)||0)!==1||(oriented.get(b+":"+a)||0)!==1)invalid++;}
if(invalid)throw Error("surface nonmanifold "+invalid);
const rgb=[["limestone",[216,226,233]],["deep",[67,95,113]],["civic",[228,184,139]],["inhabited",[91,189,199]],["garden",[116,177,151]],["upper",[173,195,204]]];
function base64(arr){let A="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",r=[];for(let i=0;i<arr.length;i+=3){let a=arr[i],b=arr[i+1]??0,c=arr[i+2]??0;r.push(A[a>>2],A[((a&3)<<4)|(b>>4)],i+1<arr.length?A[((b&15)<<2)|(c>>6)]:"=",i+2<arr.length?A[c&63]:"=");}return r.join("");}
function OBJ(){let s="# A36 Civic Delta divergence study, ART HOLD\nmtllib materials.mtl\n";for(let p of V)s+=`v ${p.join(" ")}\n`;let last=-1;for(let f of T){if(last!==f[3]){last=f[3];s+=`usemtl ${rgb[last][0]}\n`;}s+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return s;}
function GLB(){
let buf=new Uint8Array(V.length*12),d=new DataView(buf.buffer),lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
for(let i=0;i<V.length;i++)for(let j=0;j<3;j++){d.setFloat32(i*12+4*j,V[i][j],true);lo[j]=Math.min(lo[j],V[i][j]);hi[j]=Math.max(hi[j],V[i][j]);}
let bin=[...buf],bvs=[{buffer:0,byteOffset:0,byteLength:buf.length,target:34962}],acs=[{bufferView:0,componentType:5126,count:V.length,type:"VEC3",min:lo,max:hi}],prs=[];
for(let m=0;m<rgb.length;m++){let ix=T.filter(t=>t[3]===m).flatMap(t=>t.slice(0,3));if(!ix.length)continue;let b=new Uint8Array(ix.length*4),dv=new DataView(b.buffer);ix.forEach((v,i)=>dv.setUint32(i*4,v,true));let offset=bin.length;bin.push(...b);bvs.push({buffer:0,byteOffset:offset,byteLength:b.length,target:34963});acs.push({bufferView:bvs.length-1,componentType:5125,count:ix.length,type:"SCALAR"});prs.push({attributes:{POSITION:0},indices:acs.length-1,material:m,mode:4});}
while(bin.length%4)bin.push(0);let doc={asset:{version:"2.0",generator:"G4C7-A36 preliminary real mesh"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prs}],materials:rgb.map(p=>({name:p[0],pbrMetallicRoughness:{baseColorFactor:p[1].map(k=>k/255).concat([1]),metallicFactor:.1,roughnessFactor:.7},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bvs,accessors:acs};
let json=Array.from(JSON.stringify(doc),c=>c.charCodeAt(0));while(json.length%4)json.push(32);
let raw=new Uint8Array(28+json.length+bin.length),h=new DataView(raw.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,raw.length,true);h.setUint32(12,json.length,true);h.setUint32(16,0x4e4f534a,true);raw.set(json,20);let off=20+json.length;h.setUint32(off,bin.length,true);h.setUint32(off+4,0x004e4942,true);raw.set(bin,off+8);return {b64:base64(raw),bytes:raw.length};}
const gl=GLB(),paths=[{path:"artifacts/g4c7-a36-civic-delta-scout/a36_delta.obj",content:OBJ(),encoding:"utf-8"},{path:"artifacts/g4c7-a36-civic-delta-scout/a36_delta.glb",content:gl.b64,encoding:"base64"},{path:"artifacts/g4c7-a36-civic-delta-scout/materials.mtl",content:rgb.map(p=>`newmtl ${p[0]}\nKd ${p[1].map(n=>(n/255).toFixed(5)).join(" ")}\n`).join("\n"),encoding:"utf-8"}];
const probes={};for(let [name,p]of Object.entries({arrival:[-65,40,-95],central:[0,70,10],west:[-91,60,58],east:[103,75,-26],north:[62,145,135]})){let c=p.map((v,k)=>Math.floor((v-O[k])/S));probes[name]={air:!at(...c),externallyConnected:!!air.seen[I(...c)]};}
const m={stage:"A36 selected divergent CIVIC DELTA preliminary GLB",head_source:"6c78e02d48f952d7ce5c9366a547fce69130c476",geometry:{vertices:V.length,triangles:T.length,quads:quadCount,solidCells:solid,connectedCells:connected.count,cornerRepairs:repairs,nonmanifoldEdges:invalid,glbBytes:gl.bytes},void_samples:probes,externalAirCount:air.count,g1:"REVIEW PENDING",g2:"NOT RUN",g3:"NOT RUN",safety:{art_hold:true,minecraft_construction:"FORBIDDEN",city_integration:"FORBIDDEN",bodies:331,feet:993,halfwidth:.65,foot:[.15,3.25],oldBodyCeiling:45,unsupportedFeet:0,negativeControl:"REQUIRED"}};
paths.push({path:"artifacts/g4c7-a36-civic-delta-scout/a36_manifest.json",content:JSON.stringify(m,null,2),encoding:"utf-8"});return{paths,manifest:m};
};
const r=make();for(const f of r.paths){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(r.manifest.geometry,null,2));
