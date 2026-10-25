#!/usr/bin/env node
// G4-C7 A33 ART HOLD; real 3D study, NO Minecraft commands or city integration.
import fs from "node:fs";import path from "node:path";
const produce=function produce(oldOBJ){
const DIR="artifacts/g4c7-a33-open-city-section-g1/";
const CAM={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},TAR=[0,78,0],SCALE=1.03;
const MATS=[["stone","#d9e5ec",[.851,.898,.925,1]],["deep","#3f596e",[.247,.349,.431,1]],["civic","#eac294",[.918,.761,.58,1]],["inhabited_glass","#61bdce",[.38,.74,.808,1]],["green","#70b49e",[.439,.706,.62,1]],["bronze","#bb956f",[.733,.584,.435,1]],["city","#89a4ba",[.537,.643,.729,1]]];
let M={v:[],f:[],parts:[],zones:[]};
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(v=>v/Math.hypot(...a));
function add(V,F,mat,label){
let vol=0,deg=0,e=new Map(),ds=new Map();
for(let f of F){let a=V[f[0]],b=V[f[1]],c=V[f[2]],n=cross(sub(b,a),sub(c,a));if(Math.hypot(...n)<.000001)deg++;vol+=dot(a,cross(b,c))/6;}
if(vol<0){F=F.map(x=>[x[0],x[2],x[1]]);vol=-vol;}
for(let f of F)for(let i=0;i<3;i++){let a=f[i],b=f[(i+1)%3],k=Math.min(a,b)+":"+Math.max(a,b),v=a+":"+b;e.set(k,(e.get(k)||0)+1);ds.set(v,(ds.get(v)||0)+1);}
let bad=0;for(let [k,n] of e){let [a,b]=k.split(":");if(n!==2||(ds.get(a+":"+b)||0)!==1||(ds.get(b+":"+a)||0)!==1)bad++;}
if(bad||deg||vol<=1e-5)throw Error("QA geometry "+label+" "+JSON.stringify({bad,deg,vol}));
let at=M.v.length;M.v.push(...V);M.f.push(...F.map(f=>[f[0]+at,f[1]+at,f[2]+at,mat]));M.parts.push({name:label,triangles:F.length,positive_volume:Math.round(vol*10)/10});
}
function prism(P,lo,hi,mat,label){
let n=P.length,area=P.reduce((s,p,i)=>{let q=P[(i+1)%n];return s+p[0]*q[1]-q[0]*p[1]},0);if(Math.abs(area)<.001||lo>=hi)throw Error("bad polygon "+label);
let poly=area>0?P:P.slice().reverse(),V=[],F=[];for(let y of [lo,hi])for(let p of poly)V.push([p[0],y,p[1]]);
for(let k=1;k<n-1;k++)F.push([0,k+1,k],[n,n+k,n+k+1]);
for(let k=0;k<n;k++){let j=(k+1)%n;F.push([k,j,n+j],[k,n+j,n+k]);}
add(V,F,mat,label);
}
function rect(x,z,w,d,lo,hi,mat,label,a=0){let c=Math.cos(a),s=Math.sin(a);prism([[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([px,pz])=>[x+px*c-pz*s,z+px*s+pz*c]),lo,hi,mat,label);}
function sweep(path,width,low,high,mat,label){
let v=[],f=[],n=path.length;
for(let i=0;i<n;i++){let p=path[i],a=path[Math.max(0,i-1)],b=path[Math.min(n-1,i+1)],dx=b[0]-a[0],dz=b[1]-a[1],L=Math.hypot(dx,dz),nx=-dz/L,nz=dx/L,w=width[i],lo=low[i],hi=high[i];if(L<.01||hi<=lo||w<=0)throw Error("sweep param "+label);
v.push([p[0]+nx*w/2,lo,p[1]+nz*w/2],[p[0]-nx*w/2,lo,p[1]-nz*w/2],[p[0]-nx*w/2,hi,p[1]-nz*w/2],[p[0]+nx*w/2,hi,p[1]+nz*w/2]);}
for(let i=0;i<n-1;i++)for(let k=0;k<4;k++){let a=i*4+k,b=i*4+(k+1)%4,c=(i+1)*4+(k+1)%4,d=(i+1)*4+k;f.push([a,b,c],[a,c,d]);}
f.push([0,2,1],[0,3,2]);let a=(n-1)*4;f.push([a,a+1,a+2],[a,a+2,a+3]);add(v,f,mat,label);
}
// 1) One ground footprint with a deliberately huge straight entrance
prism([[-204,-178],[-100,-196],[-65,-170],[-27,-168],[24,-178],[83,-185],[198,-123],[205,32],[150,146],[49,183],[-81,191],[-210,68]],-6,7,1,"anchored_continuous_city_ground");
// 2) No roof across central sky void: major concourse & large landscaped public room
prism([[-82,-139],[-18,-150],[75,-112],[86,-28],[44,54],[-31,61],[-86,2]],7,14,2,"giant_open_public_exchange_plaza");
M.zones.push({program:"ground civic exchange",rough_bounds:"x -86..86; z -150..61; y7..14",evidence:"large open-air floor; no bridging over south look corridor"});
prism([[-40,-83],[27,-86],[55,-10],[25,41],[-26,24]],14,18,4,"deep_civic_botanical_square");
// 3) West urban district is a nonparallel inhabited earthwork, not a floating arch
sweep([[-157,-128],[-158,-77],[-160,-13],[-145,55],[-111,111],[-77,152]],[78,85,91,89,70,42],[-6,3,19,38,60,78],[54,69,91,116,147,167],0,"west_connected_stepped_urban_ground");
M.zones.push({program:"west inhabited urban cityfront",evidence:"terraces/occupied levels face south-east civic void"});
// Urban rooms on east side of western district, integrated with landform, asymmetrically increasing in height
sweep([[-96,-124],[-93,-79],[-88,-32],[-75,24]],[34,37,42,34],[41,42,56,72],[68,77,97,109],6,"west_lower_inhabited_cityfront_hall");
sweep([[-109,-47],[-95,18],[-76,77],[-57,123]],[34,43,41,31],[94,105,120,136],[127,150,165,174],6,"west_upper_open_inhabited_cityfront_hall");
sweep([[-69,-121],[-63,-69],[-55,-17],[-49,35]],[23,27,27,20],[42,47,56,76],[47,53,62,82],2,"west_public_concourse_facing_void");
sweep([[-69,-117],[-64,-69],[-54,-16],[-48,33]],[23,26,26,19],[47,53,62,82],[49,55,64,84],3,"west_civic_glazing_and_occupied_frontage");
M.zones.push({program:"west broad city halls",evidence:"2 distinct large continuously inhabited levels; 1 broad civic procession, not repeated room boxes"});
// 4) East has a DIFFERENT program: low deep cultural quarters with two sculpted pavilions, no mirroring
sweep([[150,-144],[153,-95],[154,-30],[142,39],[112,95]],[88,102,97,79,43],[-6,0,12,29,54],[39,54,69,86,108],1,"east_connected_cultural_earthwork");
sweep([[99,-130],[98,-77],[94,-18],[86,44]],[46,56,59,43],[30,35,49,62],[61,72,84,100],6,"east_deep_cultural_hall");
sweep([[93,-83],[90,-20],[85,48]],[47,51,39],[72,82,92],[78,88,99],2,"east_research_tier_public_boulevard");
sweep([[92,-82],[89,-19],[84,48]],[47,51,39],[78,88,99],[81,91,102],3,"east_public_gallery_facade");
prism([[73,-10],[105,-21],[131,15],[91,58],[61,40]],24,28,4,"east_culture_courtyard_embedded_green");
M.zones.push({program:"east culture and research",evidence:"lower and deeper cultural hall with distinct public court; no 12 repeated residential floors"});
// 5) back-of-void visual arrival: a single OPEN-frontage library/exchange on city-supported upper terraces
sweep([[-69,115],[-34,148],[14,160],[61,146]],[60,88,100,66],[90,118,126,105],[102,130,138,117],1,"north_public_cityland_supported_boulevard");
prism([[-88,131],[-50,111],[34,123],[66,165],[35,199],[-48,190]],120,129,2,"high_north_civic_exchange_terrace");
prism([[-61,143],[-14,130],[43,150],[40,187],[-44,180]],129,185,6,"north_glazed_urban_library_and_public_viewpoint");
prism([[-61,139],[-12,129],[44,147],[43,156],[-44,153]],139,172,3,"north_urban_library_civic_facade");
prism([[-53,135],[-27,128],[2,142],[-28,158]],185,194,4,"north_public_sky_garden_destination");
M.zones.push({program:"northern destination",evidence:"large visible high-level library at z150, no isolated tiny tower, connected by modeled north city terrace"});
// 6) deep supporting ramps along the periphery, no center crossing at 80-140 elevation
prism([[-147,64],[-94,83],[-67,98],[-85,126],[-145,103]],71,78,2,"west_to_north_peripheral_inhabited_walk");
prism([[89,85],[123,65],[141,96],[73,138],[49,119]],60,67,2,"east_to_north_peripheral_public_walk");
// A31 comparison OBJ real geometry
let OLD={v:[],f:[],id:"A31"},active=0,mp={shell:0,base:1,civic:2,window:3,garden:4,warm:5,inhabited:6};
for(let l of oldOBJ.split("\n")){
if(l.startsWith("v "))OLD.v.push(l.trim().split(/\s+/).slice(1,4).map(Number));
else if(l.startsWith("usemtl "))active=mp[l.slice(7).trim()]??0;
else if(l.startsWith("f ")){let q=l.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(q.length===3)OLD.f.push([...q,active]);}}
if(OLD.v.length!==638||OLD.f.length!==1016)throw Error("A31 baseline corrupt");
function bounds(v){let low=[Infinity,Infinity,Infinity],high=[-Infinity,-Infinity,-Infinity];for(let p of v)for(let j=0;j<3;j++){low[j]=Math.min(low[j],p[j]);high[j]=Math.max(high[j],p[j]);}return[low,high];}
function obj(){
let out="# A33 REAL 3D urban civic section, ART HOLD, NO CONSTRUCTION\nmtllib materials.mtl\n";
for(let p of M.v)out+=`v ${p.map(x=>x.toFixed(5)).join(" ")}\n`;let before=-1;for(let f of M.f){if(before!==f[3]){before=f[3];out+=`usemtl ${MATS[before][0]}\n`;}out+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return out;
}
function base64(bytes){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<bytes.length;i+=3){let a=bytes[i],b=bytes[i+1]??0,c=bytes[i+2]??0;out.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<bytes.length?abc[c&63]:"=");}return out.join("");}
function glb(){
let pos=new Uint8Array(M.v.length*12),pv=new DataView(pos.buffer);for(let i=0;i<M.v.length;i++)for(let k=0;k<3;k++)pv.setFloat32(i*12+k*4,M.v[i][k],true);
let buf=[...pos],BV=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],AC=[{bufferView:0,componentType:5126,count:M.v.length,type:"VEC3",min:bounds(M.v)[0],max:bounds(M.v)[1]}],pr=[];
for(let k=0;k<MATS.length;k++){let ids=M.f.filter(f=>f[3]===k).flatMap(x=>x.slice(0,3));if(!ids.length)continue;let ix=new Uint8Array(ids.length*4),v=new DataView(ix.buffer);ids.forEach((id,i)=>v.setUint32(i*4,id,true));let off=buf.length;buf.push(...ix);BV.push({buffer:0,byteOffset:off,byteLength:ix.length,target:34963});AC.push({bufferView:BV.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:AC.length-1,material:k,mode:4});}
while(buf.length%4)buf.push(0);
let j={asset:{version:"2.0",generator:"G4-C7-A33 G1 real open section"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:"A33 Open City Section G1"}],meshes:[{primitives:pr}],materials:MATS.map(p=>({name:p[0],pbrMetallicRoughness:{baseColorFactor:p[2],metallicFactor:.1,roughnessFactor:.71},doubleSided:true})),buffers:[{byteLength:buf.length}],bufferViews:BV,accessors:AC};
let json=[...JSON.stringify(j)].map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
let final=new Uint8Array(28+json.length+buf.length),d=new DataView(final.buffer);
d.setUint32(0,0x46546c67,true);d.setUint32(4,2,true);d.setUint32(8,final.length,true);d.setUint32(12,json.length,true);d.setUint32(16,0x4e4f534a,true);final.set(json,20);
let off=20+json.length;d.setUint32(off,buf.length,true);d.setUint32(off+4,0x004e4942,true);final.set(buf,off+8);return {content:base64(final),bytes:final.length};
}
const viewStats={};
function view(name){
let W=1500,H=600,cell=750,cy=292,eye=CAM[name],forward=unit(sub(TAR,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right));
let sets=[OLD,{v:M.v,f:M.f,id:"A33"}];
let S=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#0e2133"/><defs><clipPath id="c0"><rect x="11" y="57" width="728" height="493"/></clipPath><clipPath id="c1"><rect x="761" y="57" width="728" height="493"/></clipPath></defs>`;
viewStats[name]=[];
for(let i=0;i<sets.length;i++){
let mod=sets[i],cx=i*cell+cell/2,P=mod.v.map(v=>{let q=sub(v,TAR);return[cx+SCALE*dot(q,right),cy-SCALE*dot(q,up)]});
let b=[Math.min(...P.map(x=>x[0])),Math.min(...P.map(x=>x[1])),Math.max(...P.map(x=>x[0])),Math.max(...P.map(x=>x[1]))],fits=b[0]>=i*cell+18&&b[2]<=(i+1)*cell-18&&b[1]>=62&&b[3]<=546;
if(!fits)throw Error("VIEW CROPPED "+name+" "+mod.id+" "+b);
viewStats[name].push({model:mod.id,bbox:b,inFrame:fits});
let faces=[];
for(let f of mod.f){
let a=mod.v[f[0]],b0=mod.v[f[1]],c=mod.v[f[2]],n=unit(cross(sub(b0,a),sub(c,a))),md=a.map((x,j)=>(x+b0[j]+c[j])/3);
if(dot(n,sub(eye,md))<=0)continue;
let col=MATS[f[3]][1].slice(1),sh=Math.max(.42,Math.min(1.18,.78+.35*dot(n,unit([-.42,.83,-.32])))),fill="#"+[0,2,4].map(j=>Math.min(255,Math.round(parseInt(col.slice(j,j+2),16)*sh)).toString(16).padStart(2,"0")).join("");
faces.push({depth:dot(sub(md,eye),forward),fill,points:f.slice(0,3).map(k=>P[k].map(x=>x.toFixed(2)).join(",")).join(" ")});
}
faces.sort((a,b)=>b.depth-a.depth);
S+=`<rect x="${i*cell+11}" y="57" width="728" height="493" fill="#21384c" stroke="#54768c"/><g clip-path="url(#c${i})">`;
for(let f of faces)S+=`<polygon points="${f.points}" fill="${f.fill}" stroke="#233b4c" stroke-width=".28"/>`;
S+=`</g><text x="${i*cell+20}" y="41" fill="#f2f6fb" font-family="sans-serif" font-size="22">${i?"A33 G1 - OPEN CITY SECTION":"A31 ARCHIVED - ART REJECT"}</text>`;
}
return S+`<text x="18" y="585" fill="#acc7d6" font-family="sans-serif" font-size="13">REAL 3D TRIANGLES / ${name.toUpperCase()} / same historical A31 orthographic camera and scale 1.03 / ART HOLD</text></svg>`;
}
const internalStats={};
function perspective(camera,look,id){
let fw=unit(sub(look,camera)),right=unit(cross([0,1,0],fw)),up=unit(cross(fw,right)),focal=445,faces=[],W=1100,H=750,excludedNear=0;
for(let f of M.f){
let a=M.v[f[0]],b=M.v[f[1]],c=M.v[f[2]],n=unit(cross(sub(b,a),sub(c,a))),mid=a.map((x,j)=>(x+b[j]+c[j])/3);
if(dot(n,sub(camera,mid))<=0)continue;
let v=f.slice(0,3).map(i=>sub(M.v[i],camera)),depth=v.map(x=>dot(x,fw));if(depth.some(z=>z<=3)){excludedNear++;continue;}
let ps=v.map((p,i)=>(550+focal*dot(p,right)/depth[i]).toFixed(2)+","+(374-focal*dot(p,up)/depth[i]).toFixed(2)).join(" ");
let col=MATS[f[3]][1].slice(1),sh=Math.max(.42,Math.min(1.18,.79+.36*dot(n,unit([-.42,.83,-.32])))),fill="#"+[0,2,4].map(j=>Math.min(255,Math.round(parseInt(col.slice(j,j+2),16)*sh)).toString(16).padStart(2,"0")).join("");
faces.push({depth:depth.reduce((a,b)=>a+b,0)/3,ps,fill});
}
faces.sort((a,b)=>b.depth-a.depth);let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#192d42"/><text x="22" y="32" fill="#f0f7fb" font-family="sans-serif" font-size="21">A33 ${id} G2 CONCEPT / CAMERA ${camera.join(",")} / NOT ACCESS VERIFIED</text>`;
for(let f of faces)s+=`<polygon points="${f.ps}" fill="${f.fill}" stroke="#274156" stroke-width=".32"/>`;
s+=`<text x="22" y="726" fill="#b8cedc" font-family="sans-serif" font-size="14">Look ${look.join(",")} | near clipping by triangle omission | concept perspective, not renderer or safe walking proof</text></svg>`;
internalStats[id]={camera,look,visible_triangles:faces.length,near_triangles_skipped:excludedNear};return s;
}
const files=[],put=(path,content,encoding="utf-8")=>files.push({path:DIR+path,content,encoding});let G=glb();
put("a33_open_city_section.obj",obj());
put("a33_open_city_section.glb",G.content,"base64");
put("materials.mtl",MATS.map(m=>`newmtl ${m[0]}\nKd ${m[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let name of Object.keys(CAM))put("fourview/"+name+"_a31_vs_a33.svg",view(name));
put("interior/arrival_civic_axis.svg",perspective([0,24,-143],[-15,161,164],"SOUTH_ARRIVAL"));
put("interior/central_court_to_destination.svg",perspective([0,24,-35],[-15,165,166],"CIVIC_COURT"));
let report={stage:"A33 G1 initial one-candidate 3D vs preserved A31 model",parent:"207222e9e6a867dd74ea19e4f5f5355f928df31f",name:"OPEN CITY SECTION -- urban program-first singular massing",scope:"ACTUAL 3D STUDY, not constructed or architecturally certified",model:{vertices:M.v.length,triangles:M.f.length,individual_closed_solids:M.parts.length,bounds:bounds(M.v),file_bytes_GLB:G.bytes,parts:M.parts,zones:M.zones},compare:{baseline:"A31 archived actual OBJ",sameCamera:true,cameras:CAM,target:TAR,scale:SCALE,frameAudit:viewStats},perspective:internalStats,qa_passed:["isolated closed solid positive volume","oriented paired edges each component","zero degenerate triangles","real GLB and OBJ from same face list","equal camera reference four views fully in frame"],qa_not_run:["GLB independent readback","actual geometric union and support","visual art G1 and G2 inspection","physically located safe pedestrian positions and destination route","331 bodies/993 feet with negative blocker","external reader, Minecraft build, city integration"],art:"ART HOLD PENDING INSPECTION",constraints:{art_hold:true,minecraft_construction:"FORBIDDEN",city_integration:"FORBIDDEN",body_samples:331,foot_samples:993,halfwidth:.65,relative_foot_height:[.15,3.25],historical_body_interference_ceiling:45,unsupported_foot_ceiling:0,negative_blocker:"REQUIRED",work_requires_permission:true}};
put("a33_initial_manifest.json",JSON.stringify(report,null,2));
return {files,report};
};
const old=fs.readFileSync("artifacts/g4c7-a31-civic-valley-scout/a31_civic_valley.obj","utf8");
const result=produce(old);for(const f of result.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(result.report.model,null,2));
