#!/usr/bin/env node
// G4-C7 A22: authentic geometry, 4-view and QA reproducible study; no Minecraft world writes.
import fs from 'node:fs';import path from 'node:path';
const SET={"project":"G4-C7 A22 City-fabric-first architectural study","step":"LIGHT ART SCOUT","names":["OPEN CIVIC CRESCENT","BRAIDED INHABITED GORGE","DELTA CITY COMMONS"],"captions":["前面を大きく開いた公共湾岸都市","縦断公共街路が編み込む峡谷都市","中央公共核から広がる三方向都市"],"cameras":{"front":[0,178,-392],"oblique":[290,228,-305],"side":[403,196,0],"aerial":[188,456,-208]},"target":[0,70,0],"scale":1.27,"mats":[["white_stone","#d2dce0",[0.82,0.86,0.88,1]],["shadow_support","#607784",[0.38,0.47,0.52,1]],["urban_glazing","#56b8c0",[0.34,0.72,0.75,1]],["civic_deck","#e8ba7e",[0.91,0.73,0.49,1]],["green_court","#7ea891",[0.49,0.66,0.57,1]]]};
const PI=Math.PI;
function radquad(cx,cz,r0,r1,a0,a1){return [[cx+r0*Math.cos(a0),cz+r0*Math.sin(a0)],[cx+r1*Math.cos(a0),cz+r1*Math.sin(a0)],[cx+r1*Math.cos(a1),cz+r1*Math.sin(a1)],[cx+r0*Math.cos(a1),cz+r0*Math.sin(a1)]]}
function rect(cx,cz,w,l,turn=0){const c=Math.cos(turn),s=Math.sin(turn);return [[-w/2,-l/2],[w/2,-l/2],[w/2,l/2],[-w/2,l/2]].map(([x,z])=>[cx+x*c-z*s,cz+x*s+z*c])}
function street(x1,z1,x2,z2,width){let dx=x2-x1,dz=z2-z1,l=Math.hypot(dx,dz),ox=-dz/l*width/2,oz=dx/l*width/2;return[[x1+ox,z1+oz],[x2+ox,z2+oz],[x2-ox,z2-oz],[x1-ox,z1-oz]]}
function add(m,foot,lo,hi,material,label){
 if(!(hi>lo)||foot.length<3)throw Error("invalid "+label);
 const signed=foot.reduce((s,p,i)=>{let q=foot[(i+1)%foot.length];return s+p[0]*q[1]-q[0]*p[1]},0);
 if(Math.abs(signed)<.00001)throw Error("degenerate footprint "+label);
 const P=signed>0?foot:[...foot].reverse(),n=P.length,b=m.v.length;
 for(let h of [lo,hi])for(let p of P)m.v.push([p[0],h,p[1]]);
 const faces=[];
 for(let j=1;j<n-1;j++){faces.push([b,b+j,b+j+1,material],[b+n,b+n+j+1,b+n+j,material]);}
 for(let j=0;j<n;j++){let k=(j+1)%n;faces.push([b+j,b+n+k,b+k,material],[b+j,b+n+j,b+n+k,material]);}
 // Each isolated prism gets a normal-orientation and signed-volume audit.
 const V=m.v;let vol=0;for(const [a,b,c] of faces){let A=V[a],B=V[b],C=V[c];vol+=(A[0]*(B[1]*C[2]-B[2]*C[1])+A[1]*(B[2]*C[0]-B[0]*C[2])+A[2]*(B[0]*C[1]-B[1]*C[0]))/6}
 if(Math.abs(vol)<1e-6)throw Error("invalid volume "+label);
 if(vol<0){for(let f of faces){let tmp=f[1];f[1]=f[2];f[2]=tmp}vol=-vol}
 m.f.push(...faces);m.solids.push({label,material,volume:Math.round(vol),tris:faces.length});
}
function box(m,x,z,w,l,y0,y1,mat,label,t=0){add(m,rect(x,z,w,l,t),y0,y1,mat,label)}
function band(m,cx,cz,r0,r1,start,end,segments,y0,y1,mat,label,level=0,skip=()=>false){
 for(let k=0;k<segments;k++){
  if(skip(k))continue;let a=start+(end-start)*(k+.015)/segments,b=start+(end-start)*(k+.985)/segments;
  const d=(k/segments)*.04;
  add(m,radquad(cx,cz,r0+d*6,r1-d*2,a,b),y0,y1,mat,`${label}_${k}`);
 }
}
function model(id){
 let m={id,v:[],f:[],solids:[],layers:0,urbanFrontages:0,links:0,supports:0};
 if(id==="a"){
  // Large, publicly open crescent: front open, not a complete circular ring.
  const start=-.38,end=3.49,N=18;
  // Embedded foundation, not a detached wafer under three towers.
  band(m,0,5,49,122,start,end,N,-4,12,1,"inhabited_ground_mass");
  band(m,0,5,31,45,start,end,N,6,11,3,"inner_civic_waterfront_walk");
  for(let level=0;level<5;level++){
   const y=15+level*21,r0=50+level*2.8,r1=116-level*8.7;
   for(let k=0;k<N;k++){
    if((k<3||k>15)&&level>=3)continue;
    const a=start+(end-start)*(k+.03)/N,b=start+(end-start)*(k+.97)/N;
    const roofJitter=(k%4)*1.6;
    add(m,radquad(0,5,r0,r1,a,b),y,y+5,3,`public_terrace_floor_${level}_${k}`);
    add(m,radquad(0,5,r1-16,r1-3,a,b),y+5,y+16+roofJitter,0,`inhabited_outer_crescent_${level}_${k}`);
    add(m,radquad(0,5,r1-19,r1-16,a,b),y+6,y+13,2,`street_facing_glass_${level}_${k}`);
    if(k%3===1){let aMid=(a+b)/2,rm=(r0+r1)*.5,x=rm*Math.cos(aMid),z=5+rm*Math.sin(aMid);
      box(m,x,z,11,14,y+5,y+9,4,`inhabited_green_courtyard_${level}_${k}`,aMid);
    }
    m.urbanFrontages++; 
   }m.layers++;
  }
  for(let k=1;k<N;k+=3){
   let a=start+(end-start)*k/N,r=97;
   box(m,r*Math.cos(a),5+r*Math.sin(a),17,14,-4,101-(k%3)*13,1,`civic_wing_grounded_buttress_${k}`,a);
   m.supports++;
  }
  // Four civic routes enter the open waterfront and connect both sides at distinct heights.
  for(let [idx,[z,y]] of [[-43,18],[-12,41],[23,67],[54,87]].entries()){
   add(m,street(-58,z,66,z+(idx%2?15:-8),13),y,y+4,3,`bridge_public_boulevard_${idx}`);
   add(m,street(-48,z+1,57,z+1+(idx%2?15:-8),8),y+4,y+10,2,`active_groundfloor_gallery_${idx}`);m.links++;
  }
  // Active public civic centre is a large, multi-level space, not a needle.
  box(m,-10,-12,41,29,0,11,3,"sunken_active_civic_square");
  box(m,-11,-13,20,15,11,23,2,"civic_public_atrium_volume");
 }
 if(id==="b"){
  // Cross-city braided access: central void remains visible because city frontages are swept wide and broken by streets.
  let slices=12,z0=-115,unit=19;
  for(let k=0;k<slices;k++){
   const z=z0+k*unit+unit/2;
   const meander=14*Math.sin((k+1)*.46);
   for(let side of [-1,1]){
    const c=side*(59+5*Math.cos(k*.6))+meander*.3,rise=side===1?9:0;
    const w=54-(k%4)*3,zlen=unit-1;
    box(m,c,z,w,zlen,-4,10+rise,1,`inhabited_foundation_${side}_${k}`);
    for(let j=0;j<5;j++){
     const y=13+j*22+rise+3*Math.sin((k+j)*.55);
     const inward=side*(17+j*2.2)+meander*.25;
     const x=(c+inward*.35)+(j%2===0?side*2:side*(-1));
     const width=48-2.4*j;
     box(m,x,z,width,zlen,y,y+5,3,`continuous_public_street_${side}_${j}_${k}`);
     // Facades & occupied buildings are the very thickness of the main ramped banks.
     const fx=x+side*(width/2-8);
     box(m,fx,z,13,zlen-3,y+5,y+15+(k%3)*2,0,`inhabited_urban_wall_${side}_${j}_${k}`);
     const gx=fx-side*6;
     box(m,gx,z,3,zlen-4,y+7,y+13,2,`civic_frontage_window_${side}_${j}_${k}`);
     if((j+k)%4===0)box(m,x-side*8,z,13,10,y+5,y+8,4,`public_pocket_garden_${side}_${j}_${k}`);
     m.urbanFrontages++;
    }
    if(k%3===1){box(m,side*77+meander*.1,z,17,zlen,-4,92+rise,1,`inhabited_ground_spine_${side}_${k}`);m.supports++}
   }
  }
  for(let k=0;k<6;k++){
   const z=-97+k*37,y=17+k*16,side=k%2===0?1:-1;
   add(m,street(-62,z-10,64,z+side*14,15),y,y+5,3,`wide_braided_transit_street_${k}`);
   add(m,street(-51,z-9,53,z+side*12,9),y+5,y+11,2,`transit_gallery_${k}`);m.links++;
  }
  // Stepped communal squares read as a second major urban spine.
  for(let k=0;k<4;k++)box(m,0,-88+k*56,34,25,4+k*24,14+k*24,3,`multi_level_civic_public_square_${k}`);
  m.layers=5;
 }
 if(id==="c"){
  // Three large civic branches share a single occupied city centre and connected public plazas.
  box(m,0,0,83,66,-4,16,1,"shared_megacity_ground_civic_core");
  box(m,0,0,58,38,16,23,3,"shared_central_public_agora");
  for(let arm=0;arm<3;arm++){
   const a=-Math.PI*.46+arm*2*Math.PI/3;
   for(let k=0;k<8;k++){
    const r0=31+k*14,r1=r0+20,da=.29-.013*k,from=a-da,to=a+da,low=7+k*6+arm*6,top=low+22+(k%3)*4;
    add(m,radquad(0,0,r0,r1,from,to),-4,low,1,`loaded_branch_foundation_${arm}_${k}`);
    add(m,radquad(0,0,r0,r1,from,to),low,top,0,`integrated_urban_branch_${arm}_${k}`);
    add(m,radquad(0,0,r0+2,r1-3,from,to),top,top+4,3,`occupied_civic_roofdeck_${arm}_${k}`);
    const rMid=(r0+r1)*.5,off=a+(arm===1?.04:-.035);
    box(m,rMid*Math.cos(off),rMid*Math.sin(off),12,9,top+4,top+10,2,`urban_transit_arcade_${arm}_${k}`,a);
    if(k%2===0){
      box(m,(rMid-2)*Math.cos(a),(rMid-2)*Math.sin(a),14,10,top+10,top+13,4,`community_terrace_${arm}_${k}`,a);
    }
    m.urbanFrontages++;
   }
  }
  // Inhabited broad highways between branches, not isolated sculpture strands.
  for(let k=0;k<4;k++){
   const z=-40+k*27,y=22+k*22;
   add(m,street(-68,z,72,z+(k%2===0?13:-14),16),y,y+5,3,`cross_branch_civic_avenue_${k}`);
   add(m,street(-55,z,58,z+(k%2===0?13:-14),10),y+5,y+13,2,`active_civic_gallery_${k}`);m.links++;
  }
  for(let k=0;k<6;k++){
   const a=k*Math.PI/3,r=31,x=r*Math.cos(a),z=r*Math.sin(a);
   box(m,x,z,12,16,-4,84+(k%3)*13,1,`grounded_urban_interchange_support_${k}`,a);m.supports++;
  }
  m.layers=8;
 }
 return m;
}
function qa(m){
 const V=m.v,E=new Map(),parent=Array.from({length:V.length},(_,i)=>i);
 function root(i){while(parent[i]!==i){parent[i]=parent[parent[i]];i=parent[i]}return i}
 function join(a,b){a=root(a);b=root(b);if(a!==b)parent[b]=a}
 let deg=0,vol=0,invalidSolids=m.solids.filter(s=>s.volume<=0).length;
 for(let f of m.f){const [a,b,c]=f,A=V[a],B=V[b],C=V[c],v=[B[0]-A[0],B[1]-A[1],B[2]-A[2]],w=[C[0]-A[0],C[1]-A[1],C[2]-A[2]],n=[v[1]*w[2]-v[2]*w[1],v[2]*w[0]-v[0]*w[2],v[0]*w[1]-v[1]*w[0]];if(Math.hypot(...n)<1e-8)deg++;vol+=A[0]*(B[1]*C[2]-B[2]*C[1])/6+A[1]*(B[2]*C[0]-B[0]*C[2])/6+A[2]*(B[0]*C[1]-B[1]*C[0])/6;
  for(let [i,j] of [[a,b],[b,c],[c,a]]){let key=i<j?i+","+j:j+","+i,e=E.get(key)||[0,0];e[0]++;e[1]+=i<j?1:-1;E.set(key,e)}
  join(a,b);join(a,c);
 }
 const min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];for(const p of V)for(let i=0;i<3;i++){min[i]=Math.min(min[i],p[i]);max[i]=Math.max(max[i],p[i])}
 return {vertices:V.length,triangles:m.f.length,isolated_convex_urban_solid_count:m.solids.length,degenerate_triangles:deg,nonpositive_primitive_volume:invalidSolids,unpaired_edges:[...E.values()].filter(x=>x[0]!==2).length,directed_edge_mismatch:[...E.values()].filter(x=>x[1]!==0).length,bounds:[min,max],signed_component_volume_sum:+vol.toFixed(1),urbanFrontages:m.urbanFrontages,major_civic_levels:m.layers,public_cross_links:m.links,groundSupports:m.supports,boolean_union:"NOT PERFORMED",overlap_self_intersections:"NOT CHECKED",human_route_331_993:"NOT RUN",art:"HOLD, PENDING VISUAL REVIEW",city_integration:"PROHIBITED",minecraft:"PROHIBITED"};
}
function obj(m){let t="# G4-C7 A22 CITY FABRIC FIRST. ART HOLD, NO MINECRAFT.\nmtllib a22_materials.mtl\n";for(let p of m.v)t+="v "+p.map(x=>x.toFixed(4)).join(" ")+"\n";let prev=-1;for(let f of m.f){if(f[3]!==prev){prev=f[3];t+="usemtl "+SET.mats[prev][0]+"\n"}t+="f "+f.slice(0,3).map(x=>x+1).join(" ")+"\n"}return t}
function ascii(s){let v=new Uint8Array(s.length);for(let i=0;i<s.length;i++)v[i]=s.charCodeAt(i);return v}
function b64(v){const ABC="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<v.length;i+=3){const x=(v[i]<<16)|((v[i+1]||0)<<8)|(v[i+2]||0);out.push(ABC[x>>>18&63]+ABC[x>>>12&63]+(i+1<v.length?ABC[x>>>6&63]:"=")+(i+2<v.length?ABC[x&63]:"="))}return out.join("")}
function glb(m){
 const groups=SET.mats.map((_,j)=>m.f.filter(f=>f[3]===j));
 let off=m.v.length*12,views=[{buffer:0,byteOffset:0,byteLength:off,target:34962}];
 for(let g of groups){views.push({buffer:0,byteOffset:off,byteLength:g.length*12,target:34963});off+=g.length*12}
 const buf=new Uint8Array(off),d=new DataView(buf.buffer),lo=[Infinity,Infinity,Infinity],hi=[-Infinity,-Infinity,-Infinity];
 m.v.forEach((p,i)=>p.forEach((x,j)=>{d.setFloat32(i*12+j*4,x,true);lo[j]=Math.min(lo[j],x);hi[j]=Math.max(hi[j],x)}));
 let ix=m.v.length*12;for(let g of groups)for(let f of g)for(let j=0;j<3;j++){d.setUint32(ix,f[j],true);ix+=4}
 const ac=[{bufferView:0,componentType:5126,count:m.v.length,type:"VEC3",min:lo,max:hi}],prims=[];
 groups.forEach((g,i)=>{ac.push({bufferView:i+1,componentType:5125,count:g.length*3,type:"SCALAR"});if(g.length)prims.push({attributes:{POSITION:0},indices:i+1,material:i,mode:4})});
 const json={asset:{version:"2.0",generator:"G4-C7 A22 existing project art-first civic design"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prims}],materials:SET.mats.map(a=>({name:a[0],doubleSided:true,pbrMetallicRoughness:{baseColorFactor:a[2],metallicFactor:.12,roughnessFactor:.65}})),buffers:[{byteLength:buf.length}],bufferViews:views,accessors:ac};
 const jb=ascii(JSON.stringify(json)),jp=(4-jb.length%4)%4,bp=(4-buf.length%4)%4,out=new Uint8Array(12+8+jb.length+jp+8+buf.length+bp),dv=new DataView(out.buffer);
 dv.setUint32(0,0x46546c67,true);dv.setUint32(4,2,true);dv.setUint32(8,out.length,true);dv.setUint32(12,jb.length+jp,true);dv.setUint32(16,0x4e4f534a,true);out.set(jb,20);out.fill(32,20+jb.length,20+jb.length+jp);let pos=20+jb.length+jp;dv.setUint32(pos,buf.length+bp,true);dv.setUint32(pos+4,0x004e4942,true);out.set(buf,pos+8);return b64(out)
}
function projectionSVG(models,view){
 const W=1440,H=500,Pane=480,eye=SET.cameras[view],target=SET.target,scale=SET.scale,sub=(a,b)=>a.map((v,i)=>v-b[i]),dot=(a,b)=>a.reduce((s,v,i)=>s+v*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],norm=v=>v.map(x=>x/Math.hypot(...v));
 const fw=norm(sub(target,eye)),rt=norm(cross([0,1,0],fw)),up=norm(cross(fw,rt));
 let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#0f1f32"/><defs>`;
 for(let i=0;i<3;i++)s+=`<clipPath id="clip${i}"><rect x="${Pane*i+5}" y="49" width="${Pane-10}" height="410"/></clipPath>`;
 s+="</defs>";
 for(let i=0;i<3;i++){
  const m=models[i],cx=Pane*i+Pane/2,cy=265,points=m.v.map(v=>{let p=sub(v,target);return [cx+dot(p,rt)*scale,cy-dot(p,up)*scale]});
  s+=`<rect x="${Pane*i+5}" y="49" width="${Pane-10}" height="410" fill="#172b3c" stroke="#415a70"/><g clip-path="url(#clip${i})">`;
  let triangles=[];
  for(let f of m.f){const [a,b,c,mi]=f,A=m.v[a],B=m.v[b],C=m.v[c],normal=norm(cross(sub(B,A),sub(C,A))),mid=A.map((x,j)=>(x+B[j]+C[j])/3);
   if(dot(normal,sub(eye,mid))<=0)continue;
   const h=SET.mats[mi][1],light=Math.max(.48,Math.min(1.19,.75+.32*dot(normal,norm([-.38,.83,-.25])))),color="#"+[1,3,5].map(j=>Math.max(0,Math.min(255,Math.round(parseInt(h.slice(j,j+2),16)*light))).toString(16).padStart(2,"0")).join("");
   triangles.push({z:dot(sub(mid,eye),fw),color,coords:[a,b,c].map(j=>points[j].map(x=>x.toFixed(2)).join(",")).join(" ")});
  }
  triangles.sort((a,b)=>b.z-a.z);
  for(let t of triangles)s+=`<polygon points="${t.coords}" fill="${t.color}" stroke="#253849" stroke-width=".3"/>`;
  s+=`</g><text x="${Pane*i+18}" y="31" font-family="sans-serif" font-size="16" font-weight="bold" fill="#e8f2f7">A22-${"ABC"[i]} ${SET.names[i]}</text><text x="${Pane*i+18}" y="483" font-family="sans-serif" font-size="12" fill="#b4c9d6">${m.f.length} triangles | ART HOLD | NOT MINECRAFT</text>`;
 }
 s+=`<text x="1421" y="16" font-family="sans-serif" font-size="11" text-anchor="end" fill="#b1c6d4">${view.toUpperCase()} / MATCHED CAMERA + SCALE / G4-C7 A22</text></svg>`;
 return s;
}
const models=['a','b','c'].map(model),checks=models.map(qa);
if(checks.some(q=>q.degenerate_triangles||q.nonpositive_primitive_volume||q.unpaired_edges||q.directed_edge_mismatch||q.signed_component_volume_sum<=0))throw Error('A22 independent prism topology failed');
const dir='build/g4c7_a22',viewDir=path.join(dir,'fourview');fs.mkdirSync(viewDir,{recursive:true});
for(let i=0;i<3;i++){const id='abc'[i];fs.writeFileSync(path.join(dir,id+'.obj'),obj(models[i]));fs.writeFileSync(path.join(dir,id+'.glb'),Buffer.from(glb(models[i]),'base64'));}
for(const name of Object.keys(SET.cameras))fs.writeFileSync(path.join(viewDir,name+'_matched.svg'),projectionSVG(models,name));
fs.writeFileSync(path.join(dir,'qa.json'),JSON.stringify(checks,null,2));
console.log('G4-C7 A22 ART HOLD; no walk or construction claims',checks);
