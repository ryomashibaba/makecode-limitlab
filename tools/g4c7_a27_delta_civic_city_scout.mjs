#!/usr/bin/env node
// A27 ART HOLD city-first actual 3D scout, no Minecraft operations.
import fs from "node:fs";import path from "node:path";
const craft=function craft(){
const ROOT="artifacts/g4c7-a27-delta-civic-city/", CAM={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270],interior:[55,112,-280]},target=[0,78,0],scale=1.03;
const colors=[["white_urban","#d4e1e7",[.83,.882,.906,1]],["basalt_support","#466276",[.275,.384,.463,1]],["city_glazing","#5cbbc7",[.36,.733,.78,1]],["open_civic","#edc18c",[.93,.757,.55,1]],["gardens","#79b59b",[.475,.71,.608,1]],["bronze_brace","#ba9272",[.73,.572,.45,1]],["inhabited_cladding","#8397aa",[.514,.592,.667,1]]];
let m={V:[],F:[],solids:[],program:{inhabited_halls:0,visible_windows:0,broad_public_walks:0,civic_courts:0,green:0,mega_ridges:0,sky_bridges:0}};
const sub=(a,b)=>a.map((v,i)=>v-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function add(V,F,mat,label){
let vol=0,deg=0,paired=new Map(),orient=new Map();
for(let f of F){let a=V[f[0]],b=V[f[1]],c=V[f[2]],normal=cross(sub(b,a),sub(c,a));if(Math.hypot(...normal)<1e-7)deg++;vol+=dot(a,cross(b,c))/6;}
if(vol<0){F=F.map(f=>[f[0],f[2],f[1]]);vol=-vol;}
for(let f of F)for(let k=0;k<3;k++){let a=f[k],b=f[(k+1)%3],key=Math.min(a,b)+":"+Math.max(a,b),ord=a+":"+b;paired.set(key,(paired.get(key)||0)+1);orient.set(ord,(orient.get(ord)||0)+1);}
let bad=0;for(let [key,n] of paired){let [a,b]=key.split(":");if(n!==2||(orient.get(a+":"+b)||0)!==1||(orient.get(b+":"+a)||0)!==1)bad++;}
if(vol<1e-5||deg||bad)throw Error("BROKEN "+label+" "+JSON.stringify({vol,deg,bad}));
let start=m.V.length;m.V.push(...V);m.F.push(...F.map(f=>[start+f[0],start+f[1],start+f[2],mat]));m.solids.push({label,triangles:F.length,volume:+vol.toFixed(2)});
}
function poly(p,y0,y1,mat,label){
let area=p.reduce((s,a,k)=>{let b=p[(k+1)%p.length];return s+a[0]*b[1]-a[1]*b[0]},0);
if(Math.abs(area)<1e-4||y1<=y0)throw Error("bad dimensions "+label+" "+y0+" "+y1);
let P=area>0?p:p.slice().reverse(),V=[],F=[],n=P.length;for(let y of [y0,y1])for(let q of P)V.push([q[0],y,q[1]]);
for(let k=1;k<n-1;k++)F.push([0,k+1,k],[n,n+k,n+k+1]);
for(let k=0;k<n;k++){let j=(k+1)%n;F.push([k,j,n+j],[k,n+j,n+k]);}
add(V,F,mat,label);
}
function rect(x,z,w,d,theta=0){let c=Math.cos(theta),s=Math.sin(theta);return [[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(v=>[x+v[0]*c-v[1]*s,z+v[0]*s+v[1]*c]);}
function box(x,z,w,d,y0,y1,mat,label,theta=0){poly(rect(x,z,w,d,theta),y0,y1,mat,label);}
function loft(path,width,lo,hi,mat,label){
let V=[],F=[];
for(let i=0;i<path.length;i++){let a=path[Math.max(0,i-1)],b=path[Math.min(path.length-1,i+1)],p=path[i],dx=b[0]-a[0],dz=b[1]-a[1],len=Math.hypot(dx,dz),nx=-dz/len,nz=dx/len,w=Array.isArray(width)?width[i]:width,y0=Array.isArray(lo)?lo[i]:lo,y1=Array.isArray(hi)?hi[i]:hi;if(y1<=y0||w<=0||len<.1)throw Error("loft dimensions "+label);
V.push([p[0]+nx*w/2,y0,p[1]+nz*w/2],[p[0]-nx*w/2,y0,p[1]-nz*w/2],[p[0]-nx*w/2,y1,p[1]-nz*w/2],[p[0]+nx*w/2,y1,p[1]+nz*w/2]);}
for(let i=0;i<path.length-1;i++)for(let k=0;k<4;k++){let a=i*4+k,b=i*4+(k+1)%4,c=(i+1)*4+(k+1)%4,d=(i+1)*4+k;F.push([a,b,c],[a,c,d]);}
F.push([0,2,1],[0,3,2]);let j=(path.length-1)*4;F.push([j,j+1,j+2],[j,j+2,j+3]);add(V,F,mat,label);
}
function road(A,B,w,lo,hi,mat,key){let dx=B[0]-A[0],dz=B[1]-A[1],l=Math.hypot(dx,dz),nx=-dz/l*w/2,nz=dx/l*w/2;poly([[A[0]+nx,A[1]+nz],[B[0]+nx,B[1]+nz],[B[0]-nx,B[1]-nz],[A[0]-nx,A[1]-nz]],lo,hi,mat,key);}
function hall(x,z,w,d,lo,height,angle,key){
box(x,z,w,d,lo,lo+height,6,key+"_occupied_urban_mass",angle);m.program.inhabited_halls++;
// long glazed inner/exterior faces are true solids, recognizable from distance
for(let s of [-1,1]){let zloc=s*(d/2+.7),xx=x-zloc*Math.sin(angle),zz=z+zloc*Math.cos(angle);box(xx,zz,w*.77,1.4,lo+3,lo+Math.min(height-2,16),2,key+"_public_frontage_"+s,angle);m.program.visible_windows++;}
box(x,z,w+4,d+3,lo+height-2,lo+height+1,0,key+"_occupied_roof_outline",angle);
}
function inhabitedWing(id,path,width,top,offset){
let lower=top.map(y=>Math.max(15,Math.min(y-25,y*.59)));
loft(path,width,-4,lower,1,id+"_inhabited_grounded_base");m.program.mega_ridges++;
for(let i=0;i<path.length-1;i++){
let a=path[i],b=path[i+1],x=(a[0]+b[0])/2,z=(a[1]+b[1])/2,dx=b[0]-a[0],dz=b[1]-a[1],angle=-Math.atan2(dx,dz),len=Math.hypot(dx,dz),street=23+i*13+offset*3,half=(top[i]+top[i+1])/2;
box(x,z,width[i]*.81,len*.88,street,street+5,3,id+"_public_urban_terrace_"+i,angle);m.program.broad_public_walks++;
let shift=[-8,7,12,-8][i%4],XX=x+shift*Math.cos(angle),ZZ=z+shift*Math.sin(angle);
let hallHeight=Math.min(30,22+(i%3)*4);
hall(XX,ZZ,Math.min(width[i]*.67,46),Math.min(len*.75,40),street+5,hallHeight,angle,id+"_populated_concourse_"+i);
if(i!==0){box(x+12,z+6,18,14,street+5,street+7,4,id+"_inhabited_pocket_garden_"+i,angle);m.program.green++;}
let roofLo=street+8,roofHi=Math.min(half-6,street+36);
if(roofHi>roofLo+9){box(x-8,z,Math.min(width[i]*.30,26),len*.57,roofLo,roofHi,0,id+"_rising_inhabited_crest_"+i,angle);}
}
}
poly([[-153,-122],[-69,-158],[39,-149],[143,-95],[159,-10],[132,84],[54,144],[-58,132],[-156,52]],-4,9,1,"multi_city_foundation");
inhabitedWing("western_city_fold",[[-133,-100],[-110,-70],[-106,-27],[-128,18],[-136,64]],[54,65,73,60,38],[45,74,106,146,113],0);
inhabitedWing("southeast_city_fabric",[[123,-121],[103,-78],[73,-45],[67,4],[98,54]],[55,72,77,65,46],[44,73,122,160,149],2);
inhabitedWing("north_ascending_urbanism",[[-52,90],[-15,113],[29,123],[73,115],[92,87]],[55,70,73,56,34],[78,116,169,186,122],3);
// Integrated public civic void, with destinations and geometric sectional progression
poly([[-81,-57],[-30,-71],[38,-45],[56,13],[24,68],[-42,57],[-87,-2]],9,14,3,"grand_arrival_civic_public_square");m.program.civic_courts++;
poly([[-38,-29],[17,-35],[29,12],[5,43],[-30,34]],14,18,4,"public_sunken_garden_destinations");m.program.green++;
let P=[[-22,-130],[-32,-87],[-23,-41],[2,3],[-5,49],[22,89]],YS=[15,29,47,70,95,119],W=[36,41,46,41,37,32];
for(let i=0;i<P.length-1;i++){
let a=P[i],b=P[i+1],center=[(a[0]+b[0])/2,(a[1]+b[1])/2],h=(YS[i]+YS[i+1])/2;
loft([a,center,b],[W[i],(W[i]+W[i+1])/2,W[i+1]],[YS[i]-5,h-5,YS[i+1]-5],[YS[i],h,YS[i+1]],3,"ascending_multilevel_occupied_civic_street_"+i);m.program.broad_public_walks++;
if(i===1||i===3){box(center[0]+16,center[1]+5,24,16,h-4,h-2,4,"public_wide_landing_green_"+i);m.program.green++;}
}
for(let [i,a,b,w,y] of [[0,[-95,-18],[-32,-5],22,48],[1,[-27,47],[51,27],27,87],[2,[50,-29],[106,-40],22,69],[3,[-20,95],[40,104],22,118],[4,[-73,29],[-15,60],23,72]]){
road(a,b,w,y,y+5,3,"sky_district_urban_street_"+i);m.program.sky_bridges++;
}
// Civic program of four DIFFERENT large halls (no repeated housing grid)
hall(-59,-94,36,29,14,28,.16,"west_market_exchange");
hall(59,-90,46,28,14,24,-.32,"south_eastern_gallery");
hall(-27,19,39,30,27,35,.11,"social_hall_over_agora");
hall(22,65,36,30,76,31,-.14,"upper_city_exchange");
// tectonic peaks are inhabited roof extensions and intermittent rather than 1 arch around entire edge
loft([[-122,59],[-111,74],[-86,90]],[30,22,11],[105,121,119],[130,151,138],0,"western_inhabited_city_crown");
loft([[23,119],[45,123],[71,116]],[31,20,11],[143,156,136],[164,184,154],0,"northern_inhabited_city_crown");
loft([[87,25],[99,45],[96,63]],[28,19,11],[123,132,118],[147,163,139],0,"eastern_inhabited_city_crown");
for(let [i,x,z,y] of [[0,-101,-19,55],[1,88,-30,79],[2,20,116,129],[3,-122,21,95]]){
hall(x,z,29,25,y,20,.15*i,"inhabited_midrise_on_urban_structure_"+i);
}
function bbox(V){let lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];for(let p of V)for(let j=0;j<3;j++){lo[j]=Math.min(lo[j],p[j]);hi[j]=Math.max(hi[j],p[j]);}return[lo,hi];}
function exportOBJ(){let out=`# G4-C7 A27 model genuine mesh, ART HOLD\nmtllib materials.mtl\n`;for(let v of m.V)out+=`v ${v.map(x=>x.toFixed(5)).join(" ")}\n`;let last=-1;for(let f of m.F){if(last!==f[3])out+=`usemtl ${colors[f[3]][0]}\n`;last=f[3];out+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return out;}
function base64(bytes){let c="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",o=[];for(let i=0;i<bytes.length;i+=3){let a=bytes[i],b=bytes[i+1]??0,d=bytes[i+2]??0;o.push(c[a>>2],c[((a&3)<<4)|(b>>4)],i+1<bytes.length?c[((b&15)<<2)|(d>>6)]:"=",i+2<bytes.length?c[d&63]:"=");}return o.join("");}
function exportGLB(){
let positions=new Uint8Array(m.V.length*12),view=new DataView(positions.buffer);for(let i=0;i<m.V.length;i++)for(let j=0;j<3;j++)view.setFloat32(12*i+4*j,m.V[i][j],true);
let bin=[...positions],views=[{buffer:0,byteOffset:0,byteLength:positions.length,target:34962}],access=[{bufferView:0,componentType:5126,count:m.V.length,type:"VEC3",min:bbox(m.V)[0],max:bbox(m.V)[1]}],prim=[];
for(let mat=0;mat<colors.length;mat++){let ids=m.F.filter(x=>x[3]===mat).flatMap(f=>f.slice(0,3));if(ids.length===0)continue;let b=new Uint8Array(ids.length*4),dv=new DataView(b.buffer);ids.forEach((x,i)=>dv.setUint32(4*i,x,true));let offset=bin.length;bin.push(...b);views.push({buffer:0,byteOffset:offset,byteLength:b.length,target:34963});access.push({bufferView:views.length-1,componentType:5125,count:ids.length,type:"SCALAR"});prim.push({attributes:{POSITION:0},indices:access.length-1,material:mat,mode:4});}
while(bin.length%4)bin.push(0);
let src={asset:{version:"2.0",generator:"G4-C7-A27-DELTA"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prim}],materials:colors.map(c=>({name:c[0],pbrMetallicRoughness:{baseColorFactor:c[2],roughnessFactor:.74,metallicFactor:.1},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:views,accessors:access};
let j=[...JSON.stringify(src)].map(x=>x.charCodeAt(0));while(j.length%4)j.push(32);let out=new Uint8Array(28+j.length+bin.length),d=new DataView(out.buffer);d.setUint32(0,0x46546c67,true);d.setUint32(4,2,true);d.setUint32(8,out.length,true);d.setUint32(12,j.length,true);d.setUint32(16,0x4e4f534a,true);out.set(j,20);let offset=20+j.length;d.setUint32(offset,bin.length,true);d.setUint32(offset+4,0x004e4942,true);out.set(bin,offset+8);
return{encoded:base64(out),bytes:out.length};}
const frame={};
function render(cam){
let W=1024,H=720,cx=W/2,cy=H/2,eye=CAM[cam],fwd=unit(sub(target,eye)),right=unit(cross([0,1,0],fwd)),up=unit(cross(fwd,right)),pt=m.V.map(v=>{let p=sub(v,target);return[cx+dot(p,right)*scale,cy-dot(p,up)*scale]});
let min=[Infinity,Infinity],max=[-Infinity,-Infinity];for(let p of pt){min[0]=Math.min(min[0],p[0]);min[1]=Math.min(min[1],p[1]);max[0]=Math.max(max[0],p[0]);max[1]=Math.max(max[1],p[1]);}
if(min[0]<25||min[1]<55||max[0]>W-25||max[1]>H-55)throw Error("view clipping "+cam+" "+JSON.stringify({min,max}));
frame[cam]={min,max,in_frame:true};
let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#172b42"/><text x="25" y="33" fill="#f2f7fc" font-size="22" font-family="sans-serif" font-weight="bold">A27 · DELTA CIVIC CITY / ${cam.toUpperCase()}</text><text x="25" y="695" fill="#c2d0e0" font-size="14" font-family="sans-serif">REAL 3D TRIANGLULAR MESH · matched A26 eye, target [0,78,0] and scale 1.03 · ART HOLD</text>`;
let tris=[];for(let f of m.F){let a=m.V[f[0]],b=m.V[f[1]],c=m.V[f[2]],n=unit(cross(sub(b,a),sub(c,a))),mid=a.map((v,j)=>(v+b[j]+c[j])/3);if(dot(n,sub(eye,mid))<=0)continue;
let factor=Math.max(.44,Math.min(1.20,.78+.36*dot(n,unit([-.42,.83,-.32])))),col=colors[f[3]][1].slice(1),hex="#"+[0,2,4].map(j=>Math.min(255,Math.round(parseInt(col.slice(j,j+2),16)*factor)).toString(16).padStart(2,"0")).join("");
tris.push({z:dot(sub(mid,eye),fwd),color:hex,xy:f.slice(0,3).map(i=>pt[i].map(x=>x.toFixed(2)).join(",")).join(" ")});
}
tris.sort((a,b)=>b.z-a.z);for(let t of tris)s+=`<polygon points="${t.xy}" fill="${t.color}" stroke="#273d54" stroke-width=".32"/>`;
return s+"</svg>";}
const glb=exportGLB(),files=[],put=(name,content,encoding="utf-8")=>files.push({path:ROOT+name,content,encoding});
put("a27_delta_civic_city.obj",exportOBJ());put("a27_delta_civic_city.glb",glb.encoded,"base64");
put("materials.mtl",colors.map(c=>`newmtl ${c[0]}\nKd ${c[2].slice(0,3).join(" ")}\n`).join("\n"));
for(let cam of Object.keys(CAM))put(`fourview/${cam}_a27.svg`,render(cam));
const report={stage:"A27 new section-first single civic city",origin_head:"0c1b125c7a804ce98df71fa7db7e81680d8906ae",concept:"Three irregular occupied ridge districts, heavily populated public concourses and five intermediate civic bridges. No single overarching arch.",stats:{vertices:m.V.length,triangles:m.F.length,isolated_closed_solids:m.solids.length,bounds:bbox(m.V),glb_bytes:glb.bytes,program:m.program},cameras:CAM,target,scale,frames:frame,verified:["real positive-volume individually closed lofts/prisms","individual manifold triangle edges with opposite directed orientation","zero-area triangles absent in individual solids","true OBJ + GLB2 generation from same triangles","same A26 eye/target/scale for each cardinal view","all silhouettes within frame"],not_verified:["third-party GLB loader","union/self intersections of overlapping separate components","physical accessibility/support/egress","331 body and 993 foot samples negative control","visual art approval"],status:"ART HOLD",minecraft:"PROHIBITED",city_integration:"PROHIBITED",preservation:"All historic files untouched",legacy:{body_count:331,foot_samples:993,halfwidth:.65,relative_feet:[.15,3.25],old_body_interference_max:45,unsupported_feet_max:0}};
put("a27_manifest.json",JSON.stringify(report,null,2));
return{files,stats:report.stats,frames:frame};
};
const r=craft();for(let f of r.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify(r.stats,null,2));
