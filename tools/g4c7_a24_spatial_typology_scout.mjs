#!/usr/bin/env node
// A24 ART-FIRST sculpted urban tissue study; offline output only. No world/USED writes.
import fs from 'node:fs';import path from 'node:path';
const a24Build=function a24Build(){
const ROOT="artifacts/g4c7-a24-spatial-typology-scout/",CAM={front:[0,178,-392],oblique:[290,228,-305],side:[403,196,0],aerial:[188,456,-208]},TARGET=[0,70,0],SCALE=1.10;
const MATS=[["enamel_stone","#d4e0e7",[.831,.878,.906,1]],["dark_structure","#455e76",[.271,.369,.463,1]],["living_glazing","#58b6c3",[.345,.714,.765,1]],["public_floor","#e7b27d",[.906,.698,.49,1]],["verdure","#78b398",[.471,.702,.596,1]],["accent_bronze","#bf987b",[.749,.596,.482,1]]];
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],sub=(a,b)=>a.map((x,j)=>x-b[j]),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function fresh(name,id){return {id,name,V:[],F:[],solidQA:[],program:{walks:0,frontages:0,greens:0,crossings:0,void_name:""}};}
function emit(m,points,tris,mat,label){
  let vol=0,deg=0,edges=new Map(),dir=new Map();
  for(let f of tris){let [a,b,c]=f,A=points[a],B=points[b],C=points[c],n=cross(sub(B,A),sub(C,A));
    if(Math.hypot(...n)<1e-7)deg++;
    vol+=dot(A,cross(B,C))/6;
  }
  if(vol<0){tris=tris.map(t=>[t[0],t[2],t[1]]);vol=-vol;}
  for(let f of tris)for(let j=0;j<3;j++){let x=f[j],y=f[(j+1)%3],key=Math.min(x,y)+":"+Math.max(x,y),or=x+":"+y;edges.set(key,(edges.get(key)||0)+1);dir.set(or,(dir.get(or)||0)+1);}
  let unpaired=0,mismatch=0;
  for(let [k,n] of edges){if(n!==2)unpaired++;let [a,b]=k.split(":");if((dir.get(a+":"+b)||0)!==1||(dir.get(b+":"+a)||0)!==1)mismatch++;}
  if(deg||unpaired||mismatch||vol<=1e-5)throw Error(label+" invalid isolated hull "+JSON.stringify({deg,unpaired,mismatch,vol}));
  let b=m.V.length;m.V.push(...points);m.F.push(...tris.map(t=>[b+t[0],b+t[1],b+t[2],mat]));m.solidQA.push({label,triangles:tris.length,volume:Math.round(vol*100)/100});
}
function slab(m,poly,y0,y1,mat,label){
  const area=poly.reduce((s,p,j)=>{let q=poly[(j+1)%poly.length];return s+p[0]*q[1]-p[1]*q[0]},0);
  let P=area>=0?poly:[...poly].reverse(),n=P.length,V=[],F=[];
  for(let y of [y0,y1])for(let p of P)V.push([p[0],y,p[1]]);
  for(let j=1;j<n-1;j++){F.push([0,j+1,j],[n,n+j,n+j+1]);}
  for(let j=0;j<n;j++){let k=(j+1)%n;F.push([j,k,n+k],[j,n+k,n+j]);}
  emit(m,V,F,mat,label);
}
function quad(x,z,w,d,angle=0){
  let c=Math.cos(angle),s=Math.sin(angle);return [[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(p=>[x+p[0]*c-p[1]*s,z+p[0]*s+p[1]*c]);
}
function block(m,x,z,w,d,y0,y1,mat,label,angle=0){slab(m,quad(x,z,w,d,angle),y0,y1,mat,label);}
function loft(m,P,widths,low,high,mat,label){
  const N=P.length,V=[],F=[];
  for(let i=0;i<N;i++){
    let prev=P[Math.max(0,i-1)],next=P[Math.min(N-1,i+1)],dx=next[0]-prev[0],dz=next[1]-prev[1],l=Math.hypot(dx,dz),nx=-dz/l,nz=dx/l,h0=Array.isArray(low)?low[i]:low,h1=Array.isArray(high)?high[i]:high,w=Array.isArray(widths)?widths[i]:widths;
    if(h0>=h1||l<.01)throw Error("invalid loft "+label);
    V.push([P[i][0]+nx*w/2,h0,P[i][1]+nz*w/2],[P[i][0]-nx*w/2,h0,P[i][1]-nz*w/2],[P[i][0]-nx*w/2,h1,P[i][1]-nz*w/2],[P[i][0]+nx*w/2,h1,P[i][1]+nz*w/2]);
  }
  for(let i=0;i<N-1;i++)for(let k=0;k<4;k++){let a=i*4+k,b=i*4+(k+1)%4,c=(i+1)*4+(k+1)%4,d=(i+1)*4+k;F.push([a,b,c],[a,c,d]);}
  F.push([0,2,1],[0,3,2]);let b=(N-1)*4;F.push([b,b+1,b+2],[b,b+2,b+3]);
  emit(m,V,F,mat,label);
}
function between(A,B,n){return Array.from({length:n},(_,i)=>{let t=i/(n-1);return A.map((a,k)=>a*(1-t)+B[k]*t);});}
function cA(){
 let m=fresh("CONFLUENCE OF THREE INHABITED WINGS","a");m.program.void_name="asymmetric open civic confluence with three landscape-to-city corridors";
 // A horizontal branching city: arms all attach to one broad occupied civic hub. Not parallel walls, not circular stadium.
 slab(m,[[-45,-32],[10,-50],[62,-19],[53,39],[-7,65],[-58,17]],-4,11,1,"grounded_open_civic_hub");
 slab(m,[[-34,-22],[9,-36],[41,-10],[27,31],[-7,47],[-39,13]],11,14,3,"open_urban_confluence_plaza");
 let branches=[
  {id:"south",nodes:[[-4,-11],[-12,-48],[-24,-81],[-47,-120],[-76,-156]],width:[51,43,40,32,25],top:[49,67,89,108,125],accent:0},
  {id:"east",nodes:[[12,3],[42,21],[78,49],[113,81],[146,112]],width:[49,43,38,31,23],top:[79,99,131,149,121],accent:1},
  {id:"northwest",nodes:[[-20,15],[-44,45],[-78,75],[-100,112],[-125,141]],width:[52,47,39,31,22],top:[54,72,89,110,93],accent:2}
 ];
 for(let arm of branches){
  let pts=arm.nodes,lo=pts.map(()=>10),base=arm.top.map(t=>Math.max(23,t*.6));
  loft(m,pts,arm.width,-4,base,1,"continuous_grounded_inhabited_wing_"+arm.id);
  loft(m,pts,arm.width.map(w=>w*.64),base.map(v=>v-10),arm.top,0,"rising_occupied_crest_"+arm.id);
  loft(m,pts,arm.width.map(w=>w*.42),base.map(v=>v+3),base.map(v=>v+5.5),3,"broad_public_civic_access_"+arm.id);
  m.program.walks++;
  for(let i=0;i<4;i++){
   let A=pts[i],B=pts[i+1],cx=(A[0]+B[0])/2,cz=(A[1]+B[1])/2,angle=-Math.atan2(B[0]-A[0],B[1]-A[1]),height=Math.min(arm.top[i],arm.top[i+1]),span=Math.hypot(B[0]-A[0],B[1]-A[1])*.73;
   let rise=i%2?11:0;
   // Higher platforms are short, staggered civic rooms; no repeated linear shelving.
   let y=base[i]*.66+rise;
   block(m,cx,cz,arm.width[i]*.75,span,y,y+4,3,"projecting_common_floor_"+arm.id+"_"+i,angle);
   block(m,cx,cz,arm.width[i]*.5,span*.66,y+4,y+15,2,"lit_city_frontage_"+arm.id+"_"+i,angle);
   block(m,cx+(i%2?7:-8),cz+4,9,10,y+4,y+6,4,"garden_residency_"+arm.id+"_"+i);
   m.program.frontages++;m.program.greens++;
   // Architectural serrated fins follow each arm, not a decorative detached roof.
   if(i%2===0)block(m,cx+2,cz-3,14,span*.56,height-13,height+8,5,"urban_crest_"+arm.id+"_"+i,angle);
  }
 }
 // One singular offset atrium and a sheltered civic exchange, actual 3D geometry but access not certified.
 block(m,2,5,28,32,14,37,2,"public_exchange_gallery");
 block(m,3,-3,18,20,37,54,0,"inhabited_exchange_landmark");
 block(m,23,2,16,24,12,15,4,"sunken_watergarden");
 loft(m,[[-39,-28],[-18,-18],[12,-4],[30,11]],[10,12,14,9],[16,20,25,29],[20,24,29,33],3,"public_cross_confluence_bridge");
 m.program.crossings++;
 return m;
}
function cB(){
 let m=fresh("ASYMMETRIC TERRAIN CITY","b");m.program.void_name="exposed stepped public uplands with deep off-axis canyon courts";
 // A single continuous inhabited promontory / sculpted inhabited terrain rather than two canyon walls.
 let P=[[-130,-118],[-110,-78],[-80,-35],[-54,12],[-23,61],[20,98],[75,123],[121,130]],w=[82,91,91,85,76,61,42,20],t=[40,53,75,111,140,164,139,97];
 loft(m,P,w,-4,t,0,"one_piece_inhabited_rising_terrain_core");
 // Along the entire body one side becomes open walkable terrace / gardens; facades are both sides.
 loft(m,P,w.map(x=>x*.72),t.map(x=>x-21),t.map(x=>x-16),3,"city_length_public_crystal_ridge");
 m.program.walks++;
 for(let i=0;i<P.length-1;i++){
  let a=P[i],b=P[i+1],dx=b[0]-a[0],dz=b[1]-a[1],l=Math.hypot(dx,dz),nx=-dz/l,nz=dx/l,cx=(a[0]+b[0])/2,cz=(a[1]+b[1])/2,angle=-Math.atan2(dx,dz),h=(t[i]+t[i+1])/2;
  let side=(i%3===1)?-1:1,off=side*w[i]*.39;
  // Cut-out public bays: outer platforms punctuate sculptural terrain; not repeated garage levels.
  if(i%2===0||i===3){
    block(m,cx+nx*off,cz+nz*off,w[i]*.44,24,h*.45,h*.45+5,3,"public_cantilever_court_"+i,angle);
    block(m,cx+nx*off,cz+nz*off,w[i]*.31,20,h*.45+5,h*.45+19,2,"active_street_wall_"+i,angle);
    block(m,cx+nx*(off+6),cz+nz*(off+6),15,12,h*.45+5,h*.45+8,4,"elevated_garden_"+i,angle);
    m.program.frontages++;m.program.greens++;
  }
  // Outer facade is visibly urban: repeating fine vertical windows on the diagonal mega-wall, not a featureless cliff.
  for(let j=0;j<3;j++){
    let k=(j+1)/4,xx=a[0]*(1-k)+b[0]*k,zz=a[1]*(1-k)+b[1]*k,y0=h*.38+(j%2)*8;
    block(m,xx-nx*w[i]*.41,zz-nz*w[i]*.41,7,13,y0,y0+18,2,"civic_window_cut_"+i+"_"+j,angle);
    m.program.frontages++;
  }
 }
 // Three genuine lateral city neighbourhoods, integrated into continuous terrain through overlapping footpaths, not three separated blobs.
 for(let j=0;j<3;j++){
  let i=[1,3,5][j],p=P[i],height=[41,71,104][j],tow=[-114,-21,93][j],end=[[-146,-4],[3,29],[122,61]][j],width=[38,32,27][j];
  loft(m,[p,[(p[0]+end[0])/2,(p[1]+end[1])/2],end],[width+14,width,width*.8],[-4,15,32],[height,height+25,height+32],1,"grounded_lateral_urban_terrace_"+j);
  loft(m,[p,[(p[0]+end[0])/2,(p[1]+end[1])/2],end],[width*.7,width*.65,width*.5],[height-7,height+9,height+21],[height-2,height+14,height+26],3,"occupied_branch_public_walk_"+j);m.program.walks++;
  block(m,end[0],end[1],20,20,height+26,height+45,2,"lateral_sky_civic_room_"+j);m.program.frontages++;
 }
 // A grand inhabitable public forecourt, open on three edges, distinct from a detached canopy.
 slab(m,[[-123,-124],[-44,-104],[-7,-75],[-34,-45],[-108,-75]],-4,8,1,"public_forecourt_inhabited_foundation");
 slab(m,[[-112,-115],[-51,-98],[-19,-73],[-38,-58],[-102,-84]],8,11,3,"open_terraced_entry_square");
 return m;
}
function cC(){
 let m=fresh("VERTICAL SKYBOROUGH","c");m.program.void_name="three-height skyline growing from a single linked inhabited exchange, open diagonal sky courtyards";
 // A vertical rather than horizontal city: one central tower-like inhabitable mast dissolves into three staggered vertical neighborhoods.
 let spine=[[0,-76],[9,-44],[20,-10],[14,28],[3,71],[12,110]],w=[62,64,55,46,37,18],tops=[37,64,102,160,189,158];
 loft(m,spine,w,-4,tops,0,"one_continuous_open_spine_city");
 loft(m,spine,w.map(a=>a*.48),tops.map(y=>y-22),tops.map(y=>y-16),3,"main_elevated_civic_route");m.program.walks++;
 // Two broad branching populated podium districts, but unlike A these do not form a three-arm branching plan; one anchored multi-height skyline.
 let branches=[
 {path:[[-8,-45],[-39,-49],[-78,-52],[-119,-47]],heights:[48,67,84,60],width:[65,49,35,22]},
 {path:[[15,32],[45,29],[83,31],[128,20]],heights:[112,92,70,48],width:[46,40,35,23]}
 ];
 for(let j=0;j<branches.length;j++){
 let b=branches[j];
 loft(m,b.path,b.width,[-4,7,13,7],b.heights,1,"elevated_occupied_skylane_"+j);
 loft(m,b.path,b.width.map(w=>w*.7),b.heights.map(h=>h-10),b.heights.map(h=>h-6),3,"open_sky_civic_path_"+j);
 m.program.walks++;
 for(let i=0;i<b.path.length-1;i++){let a=b.path[i],d=b.path[i+1],cx=(a[0]+d[0])/2,cz=(a[1]+d[1])/2,h=(b.heights[i]+b.heights[i+1])/2;
 block(m,cx,cz,20,18,h-25,h-8,2,"inhabited_branch_gallery_"+j+"_"+i);
 block(m,cx+(j?8:-8),cz+8,15,12,h-8,h-6,4,"branch_sky_park_"+j+"_"+i);m.program.frontages++;m.program.greens++;
 }
 }
 // Three offset and non-repetitive sky neighborhoods wrapped as planted streets with visible working floors.
 let terraces=[
 {x:-36,z:-16,w:59,d:41,lo:53,hi:59},
 {x:44,z:27,w:52,d:39,lo:94,hi:101},
 {x:-17,z:62,w:38,d:35,lo:143,hi:149}
 ];
 for(let j=0;j<terraces.length;j++){let s=terraces[j],angle=[-.17,.23,-.3][j];
 block(m,s.x,s.z,s.w,s.d,s.lo,s.hi,3,"civic_sky_square_"+j,angle);
 block(m,s.x-8,s.z+3,s.w*.48,s.d*.66,s.hi,s.hi+17,2,"inhabited_stacked_sky_hall_"+j,angle);
 block(m,s.x+13,s.z-6,12,19,s.hi,s.hi+3,4,"perched_public_garden_"+j,angle);
 m.program.frontages++;m.program.greens++;
 }
 // Splayed sculpted vertical roof crown actually on the city spine, not an isolated monumental slab.
 loft(m,[[6,40],[9,63],[12,89],[17,119]],[41,34,24,12],[154,164,157,133],[173,190,177,148],0,"inhabited_ascending_urban_crown");
 block(m,19,53,22,36,110,140,2,"exposed_high_sky_neighborhood");
 // ground floor civic core with an urban-sized open space and physical podium linking wings
 slab(m,[[-70,-83],[54,-83],[83,-27],[69,35],[-35,46],[-81,0]],-4,11,1,"linked_ground_exchange");
 slab(m,[[-59,-65],[44,-65],[60,-22],[47,19],[-27,25],[-66,0]],11,14,3,"open_ground_exchange_court");
 return m;
}
const model=[cA(),cB(),cC()],stats=model.map(m=>{
 let min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 for(let p of m.V)for(let j=0;j<3;j++){min[j]=Math.min(min[j],p[j]);max[j]=Math.max(max[j],p[j]);}
 return {id:m.id,name:m.name,vertices:m.V.length,triangles:m.F.length,closed_individual_solids:m.solidQA.length,bounds:[min,max],program:m.program,geometry_audit:"all isolated solids have positive volume, paired directed edges, no zero-area triangles",union:"UNTESTED",human331_feet993:"NOT RUN",art:"ART HOLD"};
});
function obj(m){let text=`# G4-C7 A24 ${m.name}, Y-UP conceptual units, ART HOLD\nmtllib materials.mtl\n`;
 for(let p of m.V)text+=`v ${p.map(x=>x.toFixed(4)).join(" ")}\n`;let last=-1;
 for(let f of m.F){if(f[3]!==last){text+=`usemtl ${MATS[f[3]][0]}\n`;last=f[3];}text+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}
 return text;}
function b64(u){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",o=[];for(let i=0;i<u.length;i+=3){let a=u[i],b=u[i+1]??0,c=u[i+2]??0;o.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<u.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<u.length?abc[c&63]:"=");}return o.join("");}
function glb(m){let pos=new Uint8Array(m.V.length*12),pd=new DataView(pos.buffer);for(let i=0;i<m.V.length;i++)for(let k=0;k<3;k++)pd.setFloat32(i*12+4*k,m.V[i][k],true);
let raw=[...pos],BV=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],A=[{bufferView:0,componentType:5126,count:m.V.length,type:"VEC3",min:[0,1,2].map(j=>Math.min(...m.V.map(p=>p[j]))),max:[0,1,2].map(j=>Math.max(...m.V.map(p=>p[j])))}],PR=[];
for(let mat=0;mat<MATS.length;mat++){let ix=m.F.filter(f=>f[3]===mat).flatMap(f=>f.slice(0,3));if(!ix.length)continue;let b=new Uint8Array(ix.length*4),dv=new DataView(b.buffer);ix.forEach((x,i)=>dv.setUint32(i*4,x,true));let offset=raw.length;raw.push(...b);BV.push({buffer:0,byteOffset:offset,byteLength:b.length,target:34963});A.push({bufferView:BV.length-1,componentType:5125,count:ix.length,type:"SCALAR"});PR.push({attributes:{POSITION:0},indices:A.length-1,material:mat,mode:4});}
while(raw.length%4)raw.push(0);
let structure={asset:{version:"2.0",generator:"G4-C7 A24 visual ART-HOLD scout"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:m.name}],meshes:[{primitives:PR}],materials:MATS.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],metallicFactor:.12,roughnessFactor:.7},doubleSided:true})),buffers:[{byteLength:raw.length}],bufferViews:BV,accessors:A};
let J=Array.from(JSON.stringify(structure),c=>c.charCodeAt(0));while(J.length%4)J.push(32);
let out=new Uint8Array(28+J.length+raw.length),v=new DataView(out.buffer);v.setUint32(0,0x46546c67,true);v.setUint32(4,2,true);v.setUint32(8,out.length,true);v.setUint32(12,J.length,true);v.setUint32(16,0x4e4f534a,true);out.set(J,20);let off=20+J.length;v.setUint32(off,raw.length,true);v.setUint32(off+4,0x004e4942,true);out.set(raw,off+8);
return{content:b64(out),binarySize:out.length,glbStructure:structure};
}
function project(m,camera){
 let eye=CAM[camera],fw=unit(sub(TARGET,eye)),right=unit(cross([0,1,0],fw)),up=unit(cross(fw,right));
 const coords=m.V.map(v=>{let p=sub(v,TARGET);return [dot(p,right)*SCALE,-dot(p,up)*SCALE];});
 return{coords,eye,fw,right,up,
  extents:[Math.min(...coords.map(p=>p[0])),Math.min(...coords.map(p=>p[1])),Math.max(...coords.map(p=>p[0])),Math.max(...coords.map(p=>p[1]))]};
}
const graphics={};
function svg(view){
 let W=1512,H=584,P=504,s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#0d1929"/><defs>`;
 for(let i=0;i<3;i++)s+=`<clipPath id="p${i}"><rect x="${i*P+6}" y="61" width="492" height="471"/></clipPath>`;
 s+=`</defs><text x="${W-18}" y="20" fill="#b8cce1" font-size="12" font-family="sans-serif" text-anchor="end">G4-C7 A24 ${view.toUpperCase()} · SAME CAMERA ALL A24 · SCALE ${SCALE} · REAL TRIANGLES · ART HOLD</text>`;
 graphics[view]=[];
 for(let i=0;i<3;i++){
  let m=model[i],p=project(m,view),cx=i*P+P/2,cy=297;
  const span={left:cx+p.extents[0],right:cx+p.extents[2],top:cy+p.extents[1],bottom:cy+p.extents[3]};
  graphics[view].push({id:m.id,span,fully_in_frame:span.left>=i*P+9&&span.right<=(i+1)*P-9&&span.top>=65&&span.bottom<=530});
  s+=`<rect x="${i*P+6}" y="61" width="492" height="471" fill="#182b40" stroke="#58728b"/><g clip-path="url(#p${i})">`;
  let triangles=[];for(let f of m.F){
   let A=m.V[f[0]],B=m.V[f[1]],C=m.V[f[2]],normal=unit(cross(sub(B,A),sub(C,A))),mid=A.map((x,j)=>(x+B[j]+C[j])/3);
   if(dot(normal,sub(p.eye,mid))<=0)continue;
   let col=MATS[f[3]][1].slice(1),lit=Math.max(.43,Math.min(1.22,.73+.40*dot(normal,unit([-.43,.79,-.37])))),color="#"+[0,2,4].map(j=>Math.max(0,Math.min(255,Math.round(parseInt(col.slice(j,j+2),16)*lit))).toString(16).padStart(2,"0")).join("");
   triangles.push({z:dot(sub(mid,p.eye),p.fw),color,xy:f.slice(0,3).map(ix=>(cx+p.coords[ix][0]).toFixed(2)+","+(cy+p.coords[ix][1]).toFixed(2)).join(" ")});
  }
  triangles.sort((a,b)=>b.z-a.z);
  for(let tri of triangles)s+=`<polygon points="${tri.xy}" fill="${tri.color}" stroke="#213347" stroke-width=".36"/>`;
  s+=`</g><text x="${i*P+20}" y="42" font-size="18" font-weight="bold" fill="#eff5fc" font-family="sans-serif">A24-${"ABC"[i]} ${m.name}</text><text x="${i*P+20}" y="560" font-size="12" font-family="sans-serif" fill="#b6cddd">${m.F.length} triangles · NOT BUILDABLE · ART HOLD</text>`;
 }
 return s+"</svg>";
}
let files=[],out=(name,content,encoding="utf-8")=>files.push({path:ROOT+name,content,encoding}),sizes={};
model.forEach(m=>{out(`a24_${m.id}.obj`,obj(m));let g=glb(m);out(`a24_${m.id}.glb`,g.content,"base64");sizes[m.id]=g.binarySize;});
out("materials.mtl",MATS.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
Object.keys(CAM).forEach(v=>out(`fourview/${v}_a24_abc.svg`,svg(v)));
let manifest={stage:"G4-C7 A24 structurally different concept scout",date:"2026-10-25 JST",parent_commit:"e95d5a9af99ad84fd6d09759ceeea51d1c8e5215",projection:{cameras:CAM,target:TARGET,scale:SCALE,note:"A24 comparisons use equal cameras/scale. Scale is deliberately different from A22/A23 1.27 and NOT an identical-size historic comparison."},statistics:stats,glb_file_bytes:sizes,view_extent_audit:graphics,checks_performed:["closed mesh of every separate prism/loft","positive oriented signed volume","each local directed edge paired once in each direction","nondegenerate triangle area","genuine OBJ faces GLB mesh geometry","four fixed-view real triangle orthographic projections","per-view scene silhouette frame containment"],checks_missing:["independent third-party GLB re-import","Boolean union of overlapping parts","self-intersections across all solids","physical access between elements","lateral and seismic load","historic 331 bodies / 993 feet clearance with negative blocker","walk graph","human aesthetic approval"],status:"ART HOLD / INDEPENDENT ART REVIEW PENDING",world_construction:"PROHIBITED",city_integration:"PROHIBITED",historic_assets:"PROTECTED",unchanged_limits:{body:331,feet:993,halfwidth:.65,feet_relative:[.15,3.25],body_collision_upper_bound:45,unsupported_feet:0}};
if(Object.values(graphics).some(row=>row.some(c=>!c.fully_in_frame)))throw Error("A24 framing breach "+JSON.stringify(graphics));
out("a24_manifest.json",JSON.stringify(manifest,null,2));
return{files,stats,graphics,sizes};
};
const data=a24Build();
for(let f of data.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify({stats:data.stats,graphics:data.graphics},null,2));
