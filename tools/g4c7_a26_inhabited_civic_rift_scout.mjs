#!/usr/bin/env node
// A26 geometrically reproducible ART-FIRST scout. DOES NOT run Minecraft construction.
import fs from "node:fs";import path from "node:path";
const buildA26=function buildA26(referenceOBJ){
const DIR="artifacts/g4c7-a26-inhabited-civic-rift/",cameras={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270],inner:[72,105,-160]},target=[0,78,0],scale=1.03;
const mats=[
{name:"ceramic_megafold",hex:"#d4e5ee",rgba:[.831,.898,.933,1]},
{name:"graphite_foundation",hex:"#3c586e",rgba:[.235,.345,.431,1]},
{name:"living_light",hex:"#61c4cb",rgba:[.38,.769,.796,1]},
{name:"civic_stone",hex:"#e8c39a",rgba:[.91,.765,.604,1]},
{name:"sky_gardens",hex:"#75b69f",rgba:[.459,.714,.624,1]},
{name:"bronze_bracing",hex:"#b69577",rgba:[.714,.584,.467,1]},
{name:"urban_envelope",hex:"#8199ad",rgba:[.506,.60,.678,1]}
],refColors={"pale_ceramic":0,"graphite_support":1,"inhabited_glass":2,"public_terrace":3,"garden":4,"warm_copper":5,"deep_urban":6};
const sub=(a,b)=>a.map((x,i)=>x-b[i]),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],unit=a=>a.map(x=>x/Math.hypot(...a));
const m={name:"A26 CIVIC SKY-RIFT / INHABITED MEGAFOLD",v:[],f:[],components:[],program:{primary_tectonic_spines:0,civic_terraces:0,inhabited_midscale_blocks:0,green_squares:0,public_bridges:0,urban_portals:0,urban_wing_ribs:0}};
function closed(V,F,material,label){
 let vol=0,deg=0,edges=new Map(),direct=new Map();
 for(let f of F){let a=V[f[0]],b=V[f[1]],c=V[f[2]],n=cross(sub(b,a),sub(c,a));if(Math.hypot(...n)<1e-6)deg++;vol+=dot(a,cross(b,c))/6;}
 if(vol<0){F=F.map(f=>[f[0],f[2],f[1]]);vol=-vol;}
 for(let f of F)for(let j=0;j<3;j++){let a=f[j],b=f[(j+1)%3],k=Math.min(a,b)+":"+Math.max(a,b);edges.set(k,(edges.get(k)||0)+1);let directKey=a+":"+b;direct.set(directKey,(direct.get(directKey)||0)+1);}
 let loose=0,reverse=0;for(let [k,n] of edges){if(n!==2)loose++;let [a,b]=k.split(":");if((direct.get(a+":"+b)||0)!==1||(direct.get(b+":"+a)||0)!==1)reverse++;}
 if(loose||reverse||deg||vol<=.00001)throw Error("A26 geometric FAIL "+label+" "+JSON.stringify({loose,reverse,deg,vol}));
 let start=m.v.length;m.v.push(...V);m.f.push(...F.map(f=>[f[0]+start,f[1]+start,f[2]+start,material]));m.components.push({label,triangles:F.length,positive_volume:Math.round(vol*100)/100});
}
function extrude(poly,y0,y1,mat,label){
 let area=poly.reduce((s,p,i)=>{let q=poly[(i+1)%poly.length];return s+p[0]*q[1]-q[0]*p[1]},0),P=area>0?poly:[...poly].reverse(),n=P.length;
 if(Math.abs(area)<.0001||y1<=y0)throw Error("invalid "+label);
 let V=[],F=[];for(let y of [y0,y1])for(let p of P)V.push([p[0],y,p[1]]);
 for(let i=1;i<n-1;i++){F.push([0,i+1,i],[n,n+i,n+i+1]);}
 for(let j=0;j<n;j++){let k=(j+1)%n;F.push([j,k,n+k],[j,n+k,n+j]);}
 closed(V,F,mat,label);
}
function rect(cx,cz,w,d,a=0){let c=Math.cos(a),s=Math.sin(a);return [[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([x,z])=>[cx+x*c-z*s,cz+x*s+z*c]);}
function box(x,z,w,d,y0,y1,mat,label,angle=0){extrude(rect(x,z,w,d,angle),y0,y1,mat,label);}
function loft(path,width,lo,hi,mat,label){
 let N=path.length,V=[],F=[];
 for(let i=0;i<N;i++){
 let p=path[i],a=path[Math.max(0,i-1)],b=path[Math.min(N-1,i+1)],vx=b[0]-a[0],vz=b[1]-a[1],length=Math.hypot(vx,vz);if(length<1e-4)throw Error("zero path");
 let nx=-vz/length,nz=vx/length,w=Array.isArray(width)?width[i]:width,l=Array.isArray(lo)?lo[i]:lo,h=Array.isArray(hi)?hi[i]:hi;
 if(h<=l||w<=0)throw Error("negative loft "+label);
 V.push([p[0]+nx*w/2,l,p[1]+nz*w/2],[p[0]-nx*w/2,l,p[1]-nz*w/2],[p[0]-nx*w/2,h,p[1]-nz*w/2],[p[0]+nx*w/2,h,p[1]+nz*w/2]);
 }
 for(let i=0;i<N-1;i++)for(let j=0;j<4;j++){let a=4*i+j,b=4*i+(j+1)%4,c=4*(i+1)+(j+1)%4,d=4*(i+1)+j;F.push([a,b,c],[a,c,d]);}
 F.push([0,2,1],[0,3,2]);let k=(N-1)*4;F.push([k,k+1,k+2],[k,k+2,k+3]);
 closed(V,F,mat,label);
}
function street(A,B,w,lo,hi,material,label){let dx=B[0]-A[0],dz=B[1]-A[1],len=Math.hypot(dx,dz),ox=-dz/len*w/2,oz=dx/len*w/2;extrude([[A[0]+ox,A[1]+oz],[B[0]+ox,B[1]+oz],[B[0]-ox,B[1]-oz],[A[0]-ox,A[1]-oz]],lo,hi,material,label);}
function steppedProcession(path,heights,label,width){
 for(let i=0;i<path.length-1;i++){
  let a=path[i],b=path[i+1],y0=heights[i],y1=heights[i+1];
  loft([a,[(a[0]+b[0])/2,(a[1]+b[1])/2],b],[width[i],(width[i]+width[i+1])/2,width[i+1]],[y0-3,(y0+y1)/2-3,y1-3],[y0,(y0+y1)/2,y1],3,label+"_continuous_ramp_"+i);m.program.public_bridges++;
 }
}
function civicDistrict(origin,alpha,widths,heights,name){
 // Deep arc of inhabited inner facade with 3 distinct tiers, not hundreds of identical cells
 let rpath=[];for(let i=0;i<5;i++){let t=i/4,a=alpha[0]+(alpha[1]-alpha[0])*t,r=widths.radius*(1+.08*Math.sin(i*1.4));
  rpath.push([origin[0]+Math.cos(a)*r,origin[1]+Math.sin(a)*r]);}
 for(let lv=0;lv<3;lv++){
  let y=heights[0]+lv*heights[1],wide=widths.wide-lv*4.3;
  // The public promenade is a sweeping curvilinear TERRACE, not rings closing around the center
  loft(rpath,wide,y,y+5,3,`${name}_swept_habitable_concourse_${lv}`);m.program.civic_terraces++;
  for(let j=0;j<3;j++){
   let p0=rpath[j],p1=rpath[j+1],mid=[(p0[0]+p1[0])/2,(p0[1]+p1[1])/2],theta=-Math.atan2(p1[0]-p0[0],p1[1]-p0[1]),size=[22,32,27][j],height=[21,27,19][j]+lv*2.4;
   box(mid[0],mid[1],size,28,y+5,y+5+height,6,`${name}_inhabited_cliff_block_${lv}_${j}`,theta);m.program.inhabited_midscale_blocks++;
   let ox=mid[0]+Math.sin(theta)*17,oz=mid[1]+Math.cos(theta)*17;
   box(ox,oz,size*.8,1.5,y+9,y+18,2,`${name}_integrated_interior_glass_${lv}_${j}`,theta);
   box(mid[0],mid[1],size+5,30,y+height+4,y+height+6,0,`${name}_rising_urban_crest_${lv}_${j}`,theta);
  }
  if(lv!==2){let p=rpath[1+lv];box(p[0],p[1],31,26,y+5,y+7,4,`${name}_intermediate_public_hanging_garden_${lv}`,lv*.31);m.program.green_squares++;}
 }
}
function build(){
 // Complex open-edged urban floor is deliberately not an empty surplus void.
 extrude([[-152,-130],[-78,-154],[26,-142],[132,-109],[159,-20],[141,90],[38,145],[-74,128],[-155,39]],-4,10,1,"entire_connected_urban_base");
 extrude([[-71,-72],[24,-80],[83,-17],[62,63],[-24,85],[-85,19]],10,14,3,"monumental_open_civic_room_lower_basin");m.program.civic_terraces++;
 extrude([[-38,-39],[23,-44],[44,-1],[30,40],[-20,53],[-47,11]],14,17,4,"civic_void_center_terraced_public_garden");m.program.green_squares++;
 // Main folded tectonic city silhouette: diagonal ascent and asymmetry; each megaspine anchored inside an inhabited urban wing.
 let north=[[-143,15],[-122,52],[-93,84],[-50,104],[12,121],[79,132],[139,100]];
 let northLow=[-4,17,32,67,102,109,64],northHigh=[52,80,124,177,188,152,99];
 loft(north,[33,34,38,36,31,26,17],northLow,northHigh,0,"north_bifurcating_inhabited_megafold_city_ridge");m.program.primary_tectonic_spines++;
 // Another wing is a deep diagonal transverse architecture; its height is deliberately not parallel to north (not a two-wall canyon)
 let south=[[119,-120],[107,-76],[68,-42],[24,-17],[-26,-7],[-105,-14]];
 let southLo=[-4,10,26,42,54,20],southHi=[44,66,102,136,116,60];
 loft(south,[38,35,33,34,25,18],southLo,southHi,6,"south_angled_civic_city_scarp");m.program.primary_tectonic_spines++;
 // Huge public skybridge visually defines an actual central civic space below; this is thick and inhabited, not a standalone snake ribbon
 loft([[-86,17],[-54,5],[-9,11],[36,42],[93,69]],[23,25,32,29,19],[82,96,112,123,110],[96,111,136,141,121],0,"sky_city_doubleheight_public_bridge");m.program.primary_tectonic_spines++;
 // The below-civic opening is about 95 x 70 conceptual units in projection, traversed by clearly associated inhabited tier fragments.
 civicDistrict([-16,20],[.80,2.75],{radius:87,wide:39},[28,35],"ascending_northwest_urban_amphitheatre");
 civicDistrict([6,-4],[-1.42,.63],{radius:75,wide:36},[24,29],"descending_southeast_civic_frontage");
 // Interior walkable looking social stair as an actual stepped/sloping volumetric street across the public void.
 steppedProcession([[-55,-122],[-45,-85],[-33,-38],[-16,-2],[8,48],[21,99]],[15,26,43,61,82,104],"grand_public_processional_ascent",[27,27,23,22,24,18]);
 // Deliberate cross sectional destinations across four visible public levels
 street([-95,-21],[-34,-20],20,43,50,3,"first_civic_aerial_boulevard");m.program.public_bridges++;
 street([-18,30],[80,48],23,82,88,3,"middle_transverse_urban_boulevard");m.program.public_bridges++;
 street([-52,84],[35,92],19,115,121,3,"upper_ridge_public_terrace");m.program.public_bridges++;
 street([0,-64],[72,-46],22,31,37,3,"base_sidewalk_market_east");m.program.public_bridges++;
 // Spatial structural ribs (mid-scale and explicitly anchored to the main mass)
 for(let [j,p,y0,y1] of [[0,[-115,66],-4,94],[1,[-75,100],-4,123],[2,[103,-91],-4,67],[3,[125,81],-4,104],[4,[17,120],11,150]]){
   box(p[0],p[1],[17,15,23,19,16][j],21,y0,y1,1,"landscape_connected_tectonic_support_"+j,j%2?.28:-.14);m.program.urban_wing_ribs++;
 }
 // Four DISTINCT terminal public urban block groups (not a regular grid and not a few isolated towers)
 let quarters=[
  {id:"west_civic_gateway",p:[-116,-69],angle:-.43,w:61,d:47,base:14,h:46},
  {id:"south_market_quarter",p:[64,-105],angle:.39,w:65,d:42,base:14,h:36},
  {id:"high_sky_observatory",p:[69,106],angle:.26,w:47,d:36,base:93,h:56},
  {id:"north_entrance_gallery",p:[-90,100],angle:-.20,w:54,d:45,base:65,h:37}
 ];
 for(let q of quarters){
  let {p,angle,w,d,base,h,id}=q;
  box(p[0],p[1],w,d,base,base+5,3,id+"_genuine_public_urban_foyer",angle);m.program.civic_terraces++;
  box(p[0]-w*.19,p[1],w*.36,d*.82,base+5,base+h,6,id+"_variegated_inhabited_gallery",angle);m.program.inhabited_midscale_blocks++;
  box(p[0]+w*.21,p[1]-d*.06,w*.29,d*.63,base+5,base+h*.75,0,id+"_upper_civic_block",angle);m.program.inhabited_midscale_blocks++;
  box(p[0]-w*.19,p[1]-d*.42,w*.25,2,base+8,base+16,2,id+"_large_street_window",angle);
  box(p[0],p[1],w*.66,d*.3,base+h-5,base+h-2,4,id+"_usable_green_civic_terrace",angle);m.program.green_squares++;
 }
 // Three void portal markers integrated into structural skin, to prevent cavern looking accidental
 for(let [j,p] of [[0,[-83,-47]],[1,[47,12]],[2,[-11,90]]]){
   let y=[30,57,89][j];box(p[0],p[1],28+j*6,20,y,y+4,3,"public_civic_portal_landing_"+j,(j-1)*.17);
   box(p[0]-16,p[1]+3,5,22,y+4,y+22,5,"portal_embedded_structure_"+j);m.program.urban_portals++;
 }
}
build();
function reference(text){
 let v=[],f=[],mat=0;
 for(let line of text.split("\n")){if(line.startsWith("v ")){let p=line.trim().split(/\s+/);v.push(p.slice(1,4).map(Number));}
 else if(line.startsWith("usemtl ")){let name=line.slice(7).trim();mat=refColors[name]??0;}
 else if(line.startsWith("f ")){let ids=line.trim().split(/\s+/).slice(1).map(s=>parseInt(s.split("/")[0],10)-1);if(ids.length===3)f.push([...ids,mat]);}}
 if(v.length<2000||f.length<4000)throw Error("A25 reference parsing failed "+v.length+" "+f.length);
 return{name:"A25-B ART REJECT reference",v,f};
}
const ref=reference(referenceOBJ);
function qastats(v,f){
 let min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 for(let p of v)for(let j=0;j<3;j++){min[j]=Math.min(min[j],p[j]);max[j]=Math.max(max[j],p[j]);}
 return{vertices:v.length,triangles:f.length,bounds:[min,max]};
}
const qa=qastats(m.v,m.f),referenceQA=qastats(ref.v,ref.f);
function toOBJ(){
 let s=`# ${m.name}, ART HOLD - not structurally integrated\nmtllib materials.mtl\n`;
 for(let p of m.v)s+=`v ${p.map(x=>x.toFixed(5)).join(" ")}\n`;
 let prev=-1;for(let f of m.f){if(f[3]!==prev){s+=`usemtl ${mats[f[3]].name}\n`;prev=f[3];}s+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}
 return s;
}
function b64(u){const letters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<u.length;i+=3){let x=u[i],y=u[i+1]??0,z=u[i+2]??0;out.push(letters[x>>2],letters[((x&3)<<4)|(y>>4)],i+1<u.length?letters[((y&15)<<2)|(z>>6)]:"=",i+2<u.length?letters[z&63]:"=");}return out.join("");}
function toGLB(){
 let pos=new Uint8Array(m.v.length*12),dv=new DataView(pos.buffer);for(let i=0;i<m.v.length;i++)for(let k=0;k<3;k++)dv.setFloat32(i*12+4*k,m.v[i][k],true);
 let raw=[...pos],bv=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],acc=[{bufferView:0,componentType:5126,count:m.v.length,type:"VEC3",min:qa.bounds[0],max:qa.bounds[1]}],pr=[];
 for(let mat=0;mat<mats.length;mat++){let ids=m.f.filter(f=>f[3]===mat).flatMap(f=>f.slice(0,3));if(!ids.length)continue;
  let b=new Uint8Array(ids.length*4),u=new DataView(b.buffer);ids.forEach((x,j)=>u.setUint32(j*4,x,true));let offset=raw.length;raw.push(...b);bv.push({buffer:0,byteOffset:offset,byteLength:b.length,target:34963});acc.push({bufferView:bv.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:acc.length-1,material:mat,mode:4});}
 while(raw.length%4)raw.push(0);
 let gltf={asset:{version:"2.0",generator:"G4C7-A26-ART-FIRST-CIVIC-RIFT"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:m.name}],meshes:[{primitives:pr}],materials:mats.map(x=>({name:x.name,pbrMetallicRoughness:{baseColorFactor:x.rgba,metallicFactor:.12,roughnessFactor:.70},doubleSided:true})),buffers:[{byteLength:raw.length}],bufferViews:bv,accessors:acc};
 let json=[...JSON.stringify(gltf)].map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
 let result=new Uint8Array(28+json.length+raw.length),h=new DataView(result.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,result.length,true);h.setUint32(12,json.length,true);h.setUint32(16,0x4e4f534a,true);result.set(json,20);let p=20+json.length;h.setUint32(p,raw.length,true);h.setUint32(p+4,0x004e4942,true);result.set(raw,p+8);
 return{data:b64(result),bytes:result.length,material_primitives:pr.length};
}
function project(model,view){
 let eye=cameras[view],front=unit(sub(target,eye)),right=unit(cross([0,1,0],front)),up=unit(cross(front,right));
 let points=model.v.map(p=>{let diff=sub(p,target);return[dot(diff,right)*scale,-dot(diff,up)*scale]});
 return{points,eye,front,right,up};
}
const frames={};
function compare(view){
 const w=1600,h=680,P=800,cy=345,groups=[ref,m];let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#0d1e30"/><defs><clipPath id="left"><rect x="9" y="54" width="782" height="575"/></clipPath><clipPath id="right"><rect x="809" y="54" width="782" height="575"/></clipPath></defs><text x="1585" y="16" font-family="sans-serif" font-size="14" fill="#d2e3ee" text-anchor="end">G4-C7 ${view.toUpperCase()}  •  A25-B vs A26  •  SAME EYE + TARGET + SCALE ${scale}</text>`;
 frames[view]=[];
 for(let i=0;i<groups.length;i++){
 let model=groups[i],pr=project(model,view),cx=i*P+400;
 let coords=pr.points.map(p=>[cx+p[0],cy+p[1]]);
 let min=[Infinity,Infinity],max=[-Infinity,-Infinity];
 for(let p of coords){min[0]=Math.min(min[0],p[0]);min[1]=Math.min(min[1],p[1]);max[0]=Math.max(max[0],p[0]);max[1]=Math.max(max[1],p[1]);}
 const fit=min[0]>=i*P+13&&max[0]<=(i+1)*P-13&&min[1]>=58&&max[1]<=625;frames[view].push({model:i?"A26":"A25-B",min,max,in_frame:fit});
 if(!fit)throw Error("A26 frame clipped "+view+" "+JSON.stringify(frames[view]));
 s+=`<rect x="${i*P+9}" y="54" width="782" height="575" fill="#152a3d" stroke="#597590"/><g clip-path="url(#${i?"right":"left"})">`;
 let triangles=[];
 for(let f of model.f){
  let A=model.v[f[0]],B=model.v[f[1]],C=model.v[f[2]],normal=unit(cross(sub(B,A),sub(C,A))),mid=A.map((x,j)=>(x+B[j]+C[j])/3);
  if(dot(normal,sub(pr.eye,mid))<=0)continue;
  let shade=.77+.36*dot(normal,unit([-.44,.82,-.35])),factor=Math.max(.44,Math.min(1.21,shade)),color=mats[f[3]??0].hex.slice(1),hex="#"+[0,2,4].map(j=>Math.max(0,Math.min(255,Math.round(parseInt(color.slice(j,j+2),16)*factor))).toString(16).padStart(2,"0")).join("");
  triangles.push({depth:dot(sub(mid,pr.eye),pr.front),color:hex,points:f.slice(0,3).map(k=>coords[k].map(x=>x.toFixed(2)).join(",")).join(" ")});
 }
 triangles.sort((a,b)=>b.depth-a.depth);for(let f of triangles)s+=`<polygon points="${f.points}" fill="${f.color}" stroke="#233c4f" stroke-width=".25"/>`;
 s+=`</g><text x="${i*P+23}" y="40" font-family="sans-serif" font-size="24" fill="#f1f8fb" font-weight="bold">${i?"A26 NEW - CIVIC SKY-RIFT":"A25-B OLD - ART REJECT"}</text><text x="${i*P+24}" y="651" font-family="sans-serif" font-size="15" fill="#b5cbd8">${model.f.length} real 3D triangles | ART HOLD / NO CONSTRUCTION</text>`;
 }
 return s+"</svg>";
}
function inner(){
 let w=1200,h=780,pr=project(m,"inner"),pts=pr.points.map(p=>[600+p[0]*1.3,395+p[1]*1.3]);
 let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><rect width="${w}" height="${h}" fill="#11273b"/><text x="25" y="38" font-family="sans-serif" fill="#e0ecf3" font-size="24">A26 INTERIOR VIEW / CIVIC PUBLIC VOID STUDY</text><text x="25" y="764" font-family="sans-serif" fill="#a9c5d7" font-size="15">True mesh, view from front-to-void, not measured pedestrian access</text>`;
 let fs=[];for(let f of m.f){let A=m.v[f[0]],B=m.v[f[1]],C=m.v[f[2]],mid=A.map((x,j)=>(x+B[j]+C[j])/3),N=unit(cross(sub(B,A),sub(C,A)));if(dot(N,sub(pr.eye,mid))<=0)continue;
 let color=mats[f[3]].hex.slice(1),factor=Math.max(.43,Math.min(1.17,.78+.36*dot(N,unit([-.42,.82,-.3])))),hex="#"+[0,2,4].map(j=>Math.round(parseInt(color.slice(j,j+2),16)*factor).toString(16).padStart(2,"0")).join("");
 fs.push({z:dot(sub(mid,pr.eye),pr.front),points:f.slice(0,3).map(k=>pts[k].map(x=>x.toFixed(2)).join(",")).join(" "),hex});}
 fs.sort((a,b)=>b.z-a.z);for(let f of fs)s+=`<polygon points="${f.points}" fill="${f.hex}" stroke="#294b5e" stroke-width=".25"/>`;
 return s+"</svg>";
}
let out=[],add=(name,content,encoding="utf-8")=>out.push({path:DIR+name,content,encoding}),g=toGLB();
add("a26_civic_rift.obj",toOBJ());add("a26_civic_rift.glb",g.data,"base64");
add("materials.mtl",mats.map(x=>`newmtl ${x.name}\nKd ${x.rgba.slice(0,3).join(" ")}\n`).join("\n"));
for(let name of ["front","oblique","side","aerial"])add("fourview/"+name+"_a25b_vs_a26.svg",compare(name));
add("interior/a26_civic_void_inside.svg",inner());
let manifest={stage:"A26: inhabited monumental civic section architecture; ART HOLD",parent_commit:"fac540f4879c2dafa3355c6789f42fc4aafb2ea2",reference_source:"artifacts/g4c7-a25-urban-life-scout/a25_b.obj",reference_stats:referenceQA,candidate:qa,program:m.program,closed_individual_solids:m.components.length,glb_bytes:g.bytes,glb_material_primitives:g.material_primitives,view_params:{cameras,target,scale,note:"A25-B reprojected from archived OBJ using exactly A26 camera target scale; not historic original PNG"},view_fit:frames,geometry_tests:{per_solid_positive_volume:true,per_solid_edge_pairing:true,per_solid_oriented_edge_pairing:true,zero_area_triangles:0},known_absent:["boolean union of separate solids","cross-solid self-intersections","independent GLB re-read","331 human/993 feet, inherited 45 body interferences","city structural loads","inter-level walk, safety, egress","aesthetic approval"],state:"ART HOLD",construction:"NO",city_integration:"NO",preservation:"ALL OLD MODELS AND WORLD DATA UNCHANGED"};
add("a26_manifest.json",JSON.stringify(manifest,null,2));
return {files:out,stats:qa,reference_stats:referenceQA,program:m.program,frames,glb_bytes:g.bytes,solids:m.components.length};
};
const old=fs.readFileSync("artifacts/g4c7-a25-urban-life-scout/a25_b.obj","utf8");
const result=buildA26(old);
for(let f of result.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify({stats:result.stats,program:result.program,frames:result.frames},null,2));
