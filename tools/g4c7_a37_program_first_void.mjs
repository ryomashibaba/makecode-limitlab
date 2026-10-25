#!/usr/bin/env node
// G4-C7 A37 research-only 3D, preserve ART HOLD, no Minecraft commands.
import fs from "node:fs"; import path from "node:path";
const makeA37=function makeA37(previousObj){
const root="artifacts/g4c7-a37-inhabited-open-section/",n=[46,27,46],step=10,O=[-230,-10,-230],N=n[0]*n[1]*n[2],vox=new Uint8Array(N),dirs=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const cam={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},look=[0,78,0],scale=1.03;
const material=[["pale_structural","#d9e9ed",[.851,.914,.929,1]],["deep_shadow","#3e5a70",[.243,.353,.439,1]],["civic_sandstone","#e7bb8b",[.906,.733,.545,1]],["inhabited_glass","#5fbfc6",[.373,.749,.776,1]],["public_green","#7db89c",[.49,.722,.612,1]],["north_library","#b4c6ca",[.706,.776,.792,1]]];
const inside=(i,j,k)=>i>=0&&j>=0&&k>=0&&i<n[0]&&j<n[1]&&k<n[2],ix=(i,j,k)=>(k*n[1]+j)*n[0]+i,get=(i,j,k)=>inside(i,j,k)?vox[ix(i,j,k)]:0;
function occupancy(x,y,z){
 if(y<0||y>245)return false;
 const base = y<16 && Math.pow(x/205,2)+Math.pow((z+4)/205,2)<1.31;
 let west=z>-192&&z<178&&x> -199+16*Math.sin((z+80)/55)&&x<(-34+9*Math.sin(z/66))&&y<115+0.36*(z+120)+.12*(-x-25)+14*Math.sin(z/50);
 let east=z>-172&&z<158&&x>50+12*Math.sin((z+20)/50)&&x<185-11*Math.cos(z/46)&&y<106+.12*(z+120)+12*Math.sin(z/65);
 let north=z>76&&z<195&&x>-125&&x<133&&y<167+22*Math.sin((x+40)/70)+.14*(z-70);
 let solid=base||west||east||north;
 if(!solid||y<=15)return solid;
 // Main south entrance and monumental open-to-sky public concourse.
 if(z>-208&&z<110&&x>-67+8*Math.sin(z/55)&&x<66+6*Math.sin(z/63)&&y>15)return false;
 // An intentionally exposed, large inhabited western public gallery; both urban facades face the shared plaza.
 if(x>-173&&x<-17&&z>-160&&z<67&&y>36&&y<82)return false;
 if(x>-163&&x<-22&&z>-30&&z<130&&y>104&&y<151)return false;
 // Deep east cultural hall and elevated reading rooms, not copies of the western urban tiers.
 if(x>36&&x<177&&z>-146&&z<45&&y>31&&y<92)return false;
 if(x>40&&x<166&&z>1&&z<135&&y>110&&y<151)return false;
 // North endpoint is an actual excavated civic room opening into the central public space.
 if(z>76&&z<192&&x>-76&&x<81&&y>43&&y<162)return false;
 // A light court above the north destination connects directly to sky.
 if(z>118&&z<188&&x>-42&&x<46&&y>=162)return false;
 return true;
}
for(let k=0;k<n[2];k++)for(let j=0;j<n[1];j++)for(let i=0;i<n[0];i++){
const p=[i,j,k].map((v,a)=>O[a]+(v+.5)*step);vox[ix(i,j,k)]=occupancy(...p)?1:0;}
let repairCount=0;for(let iteration=0;iteration<7;iteration++){
let todo=new Set();
for(let k=0;k<n[2]-1;k++)for(let j=0;j<n[1]-1;j++)for(let i=0;i<n[0]-1;i++)for(let [a,b] of [[0,1],[0,2],[1,2]]){
let p=[i,j,k],u=p.slice(),v=p.slice(),w=p.slice();u[a]++;v[b]++;w[a]++;w[b]++;
let items=[p,u,v,w],bits=items.map(p=>get(...p));
if(bits[0]===bits[3]&&bits[1]===bits[2]&&bits[0]!==bits[1]){
 const empty=items.filter((q,z)=>!bits[z]);empty.sort((p,q)=>dirs.reduce((s,d)=>s+get(q[0]+d[0],q[1]+d[1],q[2]+d[2])-get(p[0]+d[0],p[1]+d[1],p[2]+d[2]),0));todo.add(ix(...empty[0]));}
}
if(!todo.size)break;for(let p of todo)if(!vox[p]){vox[p]=1;repairCount++;}if(iteration===6)throw Error("diagonal contact repair cap");}
const countSolid=vox.reduce((a,b)=>a+b,0),flood=(want,allOuter)=>{
let seen=new Uint8Array(N),queue=new Int32Array(N),h=0,t=0;
for(let k=0;k<n[2];k++)for(let j=0;j<n[1];j++)for(let i=0;i<n[0];i++){
 if(allOuter&&i!==0&&i!==n[0]-1&&j!==n[1]-1&&k!==0&&k!==n[2]-1)continue;
 if(!allOuter&&t)continue;
 let p=ix(i,j,k);if(vox[p]!==want||seen[p])continue;seen[p]=1;queue[t++]=p;}
while(h<t){let p=queue[h++],i=p%n[0],j=Math.floor(p/n[0])%n[1],k=Math.floor(p/(n[0]*n[1]));for(let d of dirs){let x=i+d[0],y=j+d[1],z=k+d[2];if(!inside(x,y,z))continue;let q=ix(x,y,z);if(vox[q]!==want||seen[q])continue;seen[q]=1;queue[t++]=q;}}
return{seen,count:t};};
const body=flood(1,false),air=flood(0,true);
if(body.count!==countSolid)throw Error("A37 disconnected occupied mass "+body.count+" != "+countSolid);
const places={entrance:[0,45,-155],civic_center:[0,70,-5],west_lower_gallery:[-105,55,-80],west_upper_gallery:[-100,125,60],east_culture:[112,64,-65],east_library:[105,125,65],north_destination:[0,112,146]};
let probes={};for(let [key,pos]of Object.entries(places)){let cell=pos.map((a,i)=>Math.floor((a-O[i])/step)),good=inside(...cell)&&!get(...cell)&&!!air.seen[ix(...cell)];probes[key]={xyz:pos,voxel:cell,empty:!get(...cell),exteriorConnected:!!air.seen[ix(...cell)]};if(!good)throw Error("A37 mandatory public opening invalid "+key+" "+JSON.stringify(probes[key]));}
let V=[],F=[],map=new Map(),facesByDir=[0,0,0,0,0,0];
function vertex(i,j,k){let name=i+":"+j+":"+k,old=map.get(name);if(old===undefined){old=V.length;V.push([O[0]+i*step,O[1]+j*step,O[2]+k*step]);map.set(name,old);}return old;}
function addFace(i,j,k,d){
let P=d===0?[[i+1,j,k],[i+1,j+1,k],[i+1,j+1,k+1],[i+1,j,k+1]]:d===1?[[i,j,k],[i,j,k+1],[i,j+1,k+1],[i,j+1,k]]:d===2?[[i,j+1,k],[i,j+1,k+1],[i+1,j+1,k+1],[i+1,j+1,k]]:d===3?[[i,j,k],[i+1,j,k],[i+1,j,k+1],[i,j,k+1]]:d===4?[[i,j,k+1],[i+1,j,k+1],[i+1,j+1,k+1],[i,j+1,k+1]]:[[i,j,k],[i,j+1,k],[i+1,j+1,k],[i+1,j,k]];
let Q=P.map(x=>vertex(...x)),x=O[0]+(i+.5)*step,y=O[1]+(j+.5)*step,z=O[2]+(k+.5)*step;
let c=d===2?2:d===3?1:0;
if(d===2&&y<21&&Math.abs(x)<80)c=4;
if(d!==3&&y>28&&((x<0&&x>-180)||(x>0&&x<180))&&z<130)c=3;
if(z>90&&Math.abs(x)<100&&y>25)c=5;
if(d===3)c=1;
F.push([Q[0],Q[1],Q[2],c],[Q[0],Q[2],Q[3],c]);facesByDir[d]++;
}
for(let k=0;k<n[2];k++)for(let j=0;j<n[1];j++)for(let i=0;i<n[0];i++)if(get(i,j,k))for(let d=0;d<6;d++){let a=dirs[d];if(!get(i+a[0],j+a[1],k+a[2]))addFace(i,j,k,d);}
const edgeCount=new Map(),directed=new Map();for(let tri of F)for(let k=0;k<3;k++){let a=tri[k],b=tri[(k+1)%3],key=Math.min(a,b)+":"+Math.max(a,b),direction=a+":"+b;edgeCount.set(key,(edgeCount.get(key)||0)+1);directed.set(direction,(directed.get(direction)||0)+1);}
let badEdges=0;for(let [key,c]of edgeCount){let [a,b]=key.split(":");if(c!==2||(directed.get(a+":"+b)||0)!==1||(directed.get(b+":"+a)||0)!==1)badEdges++;}
if(badEdges)throw Error("A37 triangulated surface non-manifold at "+badEdges+" edges");
let prior={v:[],f:[]},active=0,priorMaterials={white:0,stone:0,basalt:1,deep:1,public:2,glass:3,green:4,north:5,limestone:0,shadow:1,civic:2,city:3};
for(let ln of previousObj.split("\n")){
if(ln.startsWith("v "))prior.v.push(ln.trim().split(/\s+/).slice(1,4).map(Number));
else if(ln.startsWith("usemtl "))active=priorMaterials[ln.slice(7).trim()]??0;
else if(ln.startsWith("f ")){let ids=ln.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(ids.length===3)prior.f.push([...ids,active]);}}
if(prior.v.length!==7418||prior.f.length!==14844)throw Error("A36 baseline real-geometry count incorrect "+prior.v.length+","+prior.f.length);
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function bounds(P){let min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];for(let p of P)for(let k=0;k<3;k++){min[k]=Math.min(min[k],p[k]);max[k]=Math.max(max[k],p[k]);}return{min,max};}
function OBJ(){let s="# A37 programmed-inhabited-open-section REAL model; ART HOLD / NO MINECRAFT\nmtllib materials.mtl\n";for(let p of V)s+=`v ${p.join(" ")}\n`;let prev=-1;for(let t of F){if(prev!==t[3]){prev=t[3];s+=`usemtl ${material[prev][0]}\n`;}s+=`f ${t[0]+1} ${t[1]+1} ${t[2]+1}\n`;}return s;}
function base64(arr){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<arr.length;i+=3){let a=arr[i],b=arr[i+1]??0,c=arr[i+2]??0;out.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<arr.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<arr.length?abc[c&63]:"=");}return out.join("");}
function GLB(){
let pos=new Uint8Array(V.length*12),d=new DataView(pos.buffer);for(let i=0;i<V.length;i++)for(let k=0;k<3;k++)d.setFloat32(i*12+k*4,V[i][k],true);
let bin=[...pos],views=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],acc=[{bufferView:0,componentType:5126,count:V.length,type:"VEC3",min:bounds(V).min,max:bounds(V).max}],pr=[];
for(let m=0;m<material.length;m++){let ids=F.filter(x=>x[3]===m).flatMap(x=>x.slice(0,3));if(!ids.length)continue;let b=new Uint8Array(ids.length*4),v=new DataView(b.buffer);ids.forEach((id,k)=>v.setUint32(k*4,id,true));let off=bin.length;bin.push(...b);views.push({buffer:0,byteOffset:off,byteLength:b.length,target:34963});acc.push({bufferView:views.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:acc.length-1,material:m,mode:4});}
while(bin.length%4)bin.push(0);let js=[...JSON.stringify({asset:{version:"2.0",generator:"G4-C7 A37 purposeful urban rooms"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:material.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],roughnessFactor:.7,metallicFactor:.12},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:views,accessors:acc})].map(c=>c.charCodeAt(0));while(js.length%4)js.push(32);
let all=new Uint8Array(28+js.length+bin.length),h=new DataView(all.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,all.length,true);h.setUint32(12,js.length,true);h.setUint32(16,0x4e4f534a,true);all.set(js,20);let p=20+js.length;h.setUint32(p,bin.length,true);h.setUint32(p+4,0x004e4942,true);all.set(bin,p+8);return{base64:base64(all),bytes:all.length};}
let viewQA={};
function view(name){
let eye=cam[name],forward=unit(sub(look,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),models=[{v:prior.v,f:prior.f,id:"A36"},{v:V,f:F,id:"A37"}],W=1500,H=980,cY=480;
let text=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#13283b"/><defs><clipPath id="panel0"><rect x="10" y="48" width="730" height="880"/></clipPath><clipPath id="panel1"><rect x="760" y="48" width="730" height="880"/></clipPath></defs>`;
viewQA[name]=[];
for(let t=0;t<2;t++){let obj=models[t],P=obj.v.map(p=>{let v=sub(p,look);return[t*750+375+scale*dot(v,right),cY-scale*dot(v,up)]});
let frame=[Math.min(...P.map(p=>p[0])),Math.min(...P.map(p=>p[1])),Math.max(...P.map(p=>p[0])),Math.max(...P.map(p=>p[1]))],fit=frame[0]>t*750+13&&frame[2]<(t+1)*750-13&&frame[1]>52&&frame[3]<924;if(!fit)throw Error("framing error "+name+" "+obj.id+" "+frame);
viewQA[name].push({model:obj.id,bbox:frame,uncropped:true});
let faces=[];for(let f of obj.f){let a=obj.v[f[0]],b=obj.v[f[1]],c=obj.v[f[2]],normal=unit(cross(sub(b,a),sub(c,a))),mid=a.map((x,i)=>(x+b[i]+c[i])/3);if(dot(normal,sub(eye,mid))<=0)continue;let hex=material[f[3]][1].slice(1),lit=Math.max(.43,Math.min(1.20,.8+.34*dot(normal,unit([-.43,.84,-.32])))),fill="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(hex.slice(k,k+2),16)*lit)).toString(16).padStart(2,"0")).join("");
faces.push({depth:dot(sub(mid,eye),forward),pts:f.slice(0,3).map(i=>P[i].map(x=>x.toFixed(2)).join(",")).join(" "),fill});}
faces.sort((a,b)=>b.depth-a.depth);text+=`<rect x="${t*750+10}" y="48" width="730" height="880" fill="#253f52"/><g clip-path="url(#panel${t})">`;
for(let f of faces)text+=`<polygon points="${f.pts}" fill="${f.fill}" stroke="#1d3a4c" stroke-width=".12"/>`;
text+=`</g><text x="${t*750+18}" y="31" fill="#f4f9fc" font-family="sans-serif" font-size="23">${t?"A37 - PROGRAM-FIRST CIVIC SECTION":"A36 - PREVIOUS REJECT"}</text>`;}
return text+`<text x="15" y="955" fill="#bdd2df" font-family="sans-serif" font-size="13">${name.toUpperCase()} | REAL TRIANGLES | unchanged A36 historical camera, target [0,78,0], scale 1.03 | shared expanded viewport</text></svg>`;
}
const diagnostic={};
function interior(id,eye,target){
let fw=unit(sub(target,eye)),right=unit(cross([0,1,0],fw)),up=unit(cross(fw,right)),faces=[],missed=0;
for(let f of F){let a=V[f[0]],b=V[f[1]],c=V[f[2]],normal=unit(cross(sub(b,a),sub(c,a))),mid=a.map((x,i)=>(x+b[i]+c[i])/3);if(dot(normal,sub(eye,mid))<=0)continue;let ps=f.slice(0,3).map(k=>sub(V[k],eye)),z=ps.map(q=>dot(q,fw));if(z.some(q=>q<=4)){missed++;continue;}
let points=ps.map((p,i)=>(520+470*dot(p,right)/z[i]).toFixed(2)+","+(382-470*dot(p,up)/z[i]).toFixed(2)).join(" ");
let hex=material[f[3]][1].slice(1),lit=Math.max(.43,Math.min(1.18,.8+.33*dot(normal,unit([-.43,.84,-.33])))),fill="#"+[0,2,4].map(k=>Math.min(255,Math.round(parseInt(hex.slice(k,k+2),16)*lit)).toString(16).padStart(2,"0")).join("");
faces.push({z:z.reduce((a,b)=>a+b,0)/3,points,fill});}
faces.sort((a,b)=>b.z-a.z);diagnostic[id]={camera:eye,target,visibleFaces:faces.length,nearClippedFaces:missed,certifiedPedestrianPosition:false};
let text=`<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="770" viewBox="0 0 1040 770"><rect width="1040" height="770" fill="#172f43"/><text x="17" y="30" font-size="20" font-family="sans-serif" fill="#edf7fc">A37 ${id} - from actual 3D mesh, diagnostic only</text>`;
for(let f of faces)text+=`<polygon points="${f.points}" fill="${f.fill}" stroke="#263f51" stroke-width=".1"/>`;
return text+`<text x="17" y="749" fill="#b5cedc" font-size="13" font-family="sans-serif">eye (${eye}) / look (${target}) / near-plane triangles omitted / NO WALKABILITY QA</text></svg>`;
}
const output=[],save=(path,content,encoding="utf-8")=>output.push({path:root+path,content,encoding}),g=GLB();
save("a37_inhabited_city.obj",OBJ());save("a37_inhabited_city.glb",g.base64,"base64");save("materials.mtl",material.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let v of Object.keys(cam))save("fourview/"+v+"_a36_vs_a37.svg",view(v));
save("interior/south_entrance.svg",interior("SOUTH ARRIVAL",[0,45,-155],[0,118,148]));
save("interior/west_gallery.svg",interior("WEST HABITAT GALLERY",[-105,55,-80],[-10,91,32]));
save("interior/north_public_room.svg",interior("NORTH DESTINATION",[0,112,146],[12,139,184]));
let meta={stage:"A37 programmed inhabitable civic void before forming occupied solid",source_head:"9aaf018b6a1db574c85678fc56ec9baf64db741b",date_jst:"2026-10-26",solid_model:{cells:countSolid,reachable_cells:body.count,components:1,corner_repairs:repairCount,vertices:V.length,triangles:F.length,nonmanifold_oriented_edges:badEdges,faceQuadsByAxis:facesByDir,glb_bytes:g.bytes,bounds:bounds(V)},voids:{named_open_voids:probes,exteriorConnectedAirCells:air.count,walkable:"NOT VERIFIED"},visual:{comparison:"A36 original real OBJ",historical_cameras:cam,target:look,orthographicScale:scale,viewQA,internalViews:diagnostic},done:["occupied body single connected","7 specified functional void samples empty, external-air connected","indexed triangle mesh paired directed edges","same camera/magnification A36 four views"],not_done:["3d engine external importer","body 331, feet 993 and blocker negative","human-sized clearance paths, stairs and egress","architectural aesthetics judging","structural load","real physical km scale"],safety:{art_hold:true,construction:"FORBIDDEN",integration:"FORBIDDEN",history:"PRESERVED",bodies:331,feet:993,halfwidth:.65,feetOffset:[.15,3.25],oldBodyInterferenceMax:45,unsupportedFeetMax:0,negativeBlocker:"REQUIRED"}};
save("a37_initial_manifest.json",JSON.stringify(meta,null,2));return{output,meta};
};
const baseline=fs.readFileSync("artifacts/g4c7-a36-civic-delta-scout/a36_delta.obj","utf8");
const result=makeA37(baseline);for(const f of result.output){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.meta.solid_model,null,2));
