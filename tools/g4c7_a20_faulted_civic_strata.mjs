// Reproducible G4-C7 A20 geometry constructor. Node v20+.
// Usage: node tools/g4c7_a20_faulted_civic_strata.mjs
import fs from 'node:fs';
import path from 'node:path';
const mats=[{"name":"limestone","rgb":[0.82,0.85,0.84,1],"hex":"#d1d9d6"},{"name":"obsidian","rgb":[0.32,0.43,0.49,1],"hex":"#526e7d"},{"name":"glass","rgb":[0.25,0.68,0.72,1],"hex":"#40adb8"},{"name":"gardens","rgb":[0.44,0.61,0.49,1],"hex":"#709c7d"},{"name":"civic","rgb":[0.9,0.7,0.46,1],"hex":"#e6b276"},{"name":"foundation","rgb":[0.46,0.53,0.57,1],"hex":"#758791"}];
function prismScene(){return {verts:[],faces:[],primitives:[],names:[]}}
function polySide(side,z0,z1,l,k){
 const isW=side==="W",o=isW?-1:1;
 const spread=l*3.2,fade=l*1.8;
 const outer=o*(116-spread-3*Math.sin((k+1)*1.8+l*.8));
 const inner=o*(23+fade+5*Math.sin(k*1.3+l*.5));
 const za=z0+1.4*Math.sin(l+k),zb=z1-1.2*Math.cos(l+2*k),wa=3.2*Math.sin(l*.6+k*1.4),wb=4*Math.cos(l*.5+k);
 return [[outer,z0],[o*(90-spread*.2),z0-5],[inner,za],[inner+o*wa,(z0+z1)/2],[inner+o*wb,zb],[o*(85-spread*.3),z1+3],[outer,z1]];
}
function polyWalk(x0,z0,x1,z1,width){
 const dx=x1-x0,dz=z1-z0,l=Math.hypot(dx,dz),px=-dz/l*width/2,pz=dx/l*width/2;
 return [[x0+px,z0+pz],[x1+px,z1+pz],[x1-px,z1-pz],[x0-px,z0-pz]];
}
function meshSolid(M,foot,y0,y1,mat,label,transform){
 const n=foot.length,base=M.verts.length;
 let lower=foot.map(([x,z])=>[x,y0,z]),upper=foot.map(([x,z],i)=>transform?transform(x,z,i):[x,y1,z]);
 M.verts.push(...lower,...upper);
 const faces=[];
 for(let i=1;i<n-1;i++){faces.push([base,base+i,base+i+1,mat],[base+n,base+n+i+1,base+n+i,mat]);}
 for(let j=0;j<n;j++){let k=(j+1)%n;faces.push([base+j,base+k,base+n+k,mat],[base+j,base+n+k,base+n+j,mat]);}
 let volume=0;for(let [ia,ib,ic] of faces){const [a,b,c]=[M.verts[ia],M.verts[ib],M.verts[ic]];volume+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6;}
 if(Math.abs(volume)<1e-5)throw Error("zero solid "+label);
 if(volume<0){for(const face of faces)[face[1],face[2]]=[face[2],face[1]];volume=-volume;}
 M.faces.push(...faces);M.primitives.push({label,material:mats[mat].name,triangles:faces.length,positive_signed_volume:+volume.toFixed(2)});
}
function urbanA20(){
 let M=prismScene(),sections=[[-88,-50],[-43,-5],[3,37],[44,89]];
 // One continuous inhabited foundation with a multi-part sunken public court; no thin floating platform
 for(let side of ["W","E"]){
  const west=side==="W",x0=west?-119:18,x1=west?-17:121;
  for(let k=0;k<sections.length;k++){
   const [za,zb]=sections[k],w=west?-1:1;
   meshSolid(M,[[x0,za],[x1,za],[x1+(west?-3:3),zb],[x0,zb]],-3,12,5,`grounded_civic_foundation_${side}_${k}`);
  }
 }
 // civic central low commons: three broad transverse connected solids, but preserve 2 giant sunken openings
 for(let [j,z] of [-67,7,72].entries()){
  meshSolid(M,polyWalk(-65,z-4,66,z+4,14),8,16,4,`continuous_transverse_ground_plaza_${j}`);
 }
 const counts={banks:0,terraces:0,bridges:0,ground_supports:0};
 for(const side of ["W","E"]){
  const west=side==="W";
  for(let l=0;l<7;l++){
   const datum=(west?13:12)+l*(west?22.4:20.1)+(west?0:3*Math.sin(l*.8)),setback=l*2.25;
   for(let k=0;k<4;k++){
    if(l>=5 && ((west&&k===3)||(!west&&k===0)))continue; // carve a huge, sky-open stepped negative
    const [rawa,rawb]=sections[k];let z0=rawa+setback*(k<2?1:.2),z1=rawb-setback*(k>1?1:.2);
    if(z1-z0<12)continue;
    const p=polySide(side,z0,z1,l,k),height=12.5+(k%3)*2.5;
    meshSolid(M,p,datum,datum+height,k===2?1:0,`inhabited_fault_ridge_${side}_L${l}_Z${k}`);counts.banks++;
    meshSolid(M,p,datum+height,datum+height+3.5,4,`whole_roof_public_walkway_${side}_L${l}_Z${k}`);counts.terraces++;
    // Deep glazing arcade on canyon-facing wall: a real continuous block, visually subordinate to structural envelope
    let o=west?-1:1,xx=o*(28+l*1.8+4*Math.sin(k*1.3+l*.5)),glassWidth=8.5;
    let gg=[[xx-glassWidth/2,z0+4],[xx+glassWidth/2,z0+4],[xx+glassWidth/2,z1-4],[xx-glassWidth/2,z1-4]];
    meshSolid(M,gg,datum+5,datum+10,2,`inner_canyon_inhabited_glass_${side}_L${l}_Z${k}`);
    // rooftop usable gardens/courts (not needle spires)
    if((l+k)%2===0){let xo=o*(70-l*2),z=(z0+z1)/2;
      meshSolid(M,[[xo-9,z-7],[xo+9,z-7],[xo+9,z+7],[xo-9,z+7]],datum+height+3.5,datum+height+6.2,3,`roof_civic_planting_${side}_L${l}_Z${k}`);
    }
   }
  }
 }
 // massive 3D public ramps span the urban gorge, interwoven, not roof-only or arches
 const bridges=[[-55,29],[-12,51],[43,75],[66,94],[-65,111],[-2,128]];
 for(let j=0;j<bridges.length;j++){
  const [z,y]=bridges[j],tilt=(j%2===0?1:-1)*9;
  meshSolid(M,polyWalk(-50,z-tilt,52,z+tilt,12.5),y,y+4,4,`inhabited_cross_fault_public_link_${j}`);counts.bridges++;
  // broad inhabited gallery aligned with bridge, not a tiny tube
  if(j%2===0){meshSolid(M,polyWalk(-41,z-tilt*.8,43,z+tilt*.8,7),y+4,y+10,2,`cross_city_gallery_${j}`)}
 }
 // Diagonal tapering buttress volumes running from foundation up into tiered banks
 for(let side of ["W","E"]){
  const o=side==="W"?-1:1;
  for(let j=0;j<5;j++){
   let z=-78+j*37,base=[[o*95,z-12],[o*66,z-13],[o*66,z+13],[o*95,z+12]];
   meshSolid(M,base,0,66+7*(j%3),5,`inhabited_vertical_megasupport_${side}_${j}`,(x,zz)=>[x-o*10,66+7*(j%3),zz+2*Math.sin(j)]);
   counts.ground_supports++;
  }
 }
 // Off-axis observation terraces are integrated into the inhabited banks, not separate rings or detached arches
 for(let j=0;j<3;j++){
  let z=-55+j*56,y=145+j*7,x=-83+j*11;
  meshSolid(M,polyWalk(x,z,42,z+14,11),y,y+4,4,`upper_cross_living_esplanade_${j}`);
 }
 return {model:M,counts};
}
function audit(M){
 const counts={verts:M.verts.length,triangles:M.faces.length,closed_primitive_count:M.primitives.length};
 let deg=0,invalid=0,unbalanced=0,volume=0;
 for(const item of M.primitives){if(item.positive_signed_volume<=0)invalid++;volume+=item.positive_signed_volume}
 for(const f of M.faces){let[a,b,c]=f,p=M.verts[a],q=M.verts[b],r=M.verts[c],cross=[(q[1]-p[1])*(r[2]-p[2])-(q[2]-p[2])*(r[1]-p[1]),(q[2]-p[2])*(r[0]-p[0])-(q[0]-p[0])*(r[2]-p[2]),(q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])];if(Math.hypot(...cross)<1e-6)deg++}
 const mn=[Infinity,Infinity,Infinity],mx=[-Infinity,-Infinity,-Infinity];for(let p of M.verts)for(let i=0;i<3;i++){mn[i]=Math.min(mn[i],p[i]);mx[i]=Math.max(mx[i],p[i])}
 return {...counts,degenerate_triangles:deg,nonpositive_primitive_volumes:invalid,bounds:[mn,mx],summed_primitive_volume_proxy:+volume.toFixed(1),boolean_union:"NOT PERFORMED",independent_GLb_reimport:"NOT PERFORMED",route_331_993:"NOT RUN",art_status:"HOLD"};
}
function obj(M){let s="# G4C7 A20 independent urban-mass art study; Y-up; no Minecraft construction\nmtllib a20_materials.mtl\n";for(let v of M.verts)s+="v "+v.map(x=>x.toFixed(4)).join(" ")+"\n";let last=-1;for(const f of M.faces){if(f[3]!==last){last=f[3];s+="usemtl "+mats[last].name+"\n"}s+="f "+f.slice(0,3).map(x=>x+1).join(" ")+"\n"}return s}
function ascii(s){let a=new Uint8Array(s.length);for(let i=0;i<s.length;i++)a[i]=s.charCodeAt(i);return a}
function b64(bytes){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<bytes.length;i+=3){let v=(bytes[i]<<16)|((bytes[i+1]||0)<<8)|(bytes[i+2]||0);out.push(abc[v>>>18&63]+abc[v>>>12&63]+(i+1<bytes.length?abc[v>>>6&63]:"=")+(i+2<bytes.length?abc[v&63]:"="))}return out.join("")}
function glb(M){
 const groups=mats.map((_,id)=>M.faces.filter(f=>f[3]===id));let binLen=M.verts.length*12,views=[{buffer:0,byteOffset:0,byteLength:binLen,target:34962}];for(let group of groups){views.push({buffer:0,byteOffset:binLen,byteLength:group.length*12,target:34963});binLen+=group.length*12}
 const bin=new Uint8Array(binLen),dv=new DataView(bin.buffer),low=[Infinity,Infinity,Infinity],high=[-Infinity,-Infinity,-Infinity];
 M.verts.forEach((p,i)=>p.forEach((x,j)=>{dv.setFloat32(i*12+j*4,x,true);low[j]=Math.min(low[j],x);high[j]=Math.max(high[j],x)}));
 let ptr=M.verts.length*12;for(let group of groups)for(let f of group)for(let j=0;j<3;j++){dv.setUint32(ptr,f[j],true);ptr+=4}
 let acc=[{bufferView:0,componentType:5126,count:M.verts.length,type:"VEC3",min:low,max:high}],prims=[];
 groups.forEach((g,i)=>{acc.push({bufferView:i+1,componentType:5125,count:g.length*3,type:"SCALAR"});if(g.length)prims.push({attributes:{POSITION:0},indices:i+1,material:i,mode:4})});
 const doc={asset:{version:"2.0",generator:"G4C7 A20 integrated urban fault terraces"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prims}],materials:mats.map(m=>({name:m.name,doubleSided:true,pbrMetallicRoughness:{baseColorFactor:m.rgb,roughnessFactor:.66,metallicFactor:.1}})),buffers:[{byteLength:binLen}],bufferViews:views,accessors:acc};
 const text=ascii(JSON.stringify(doc)),jp=(4-text.length%4)%4,bp=(4-bin.length%4)%4,out=new Uint8Array(12+8+text.length+jp+8+bin.length+bp),dd=new DataView(out.buffer);
 dd.setUint32(0,0x46546c67,true);dd.setUint32(4,2,true);dd.setUint32(8,out.length,true);dd.setUint32(12,text.length+jp,true);dd.setUint32(16,0x4e4f534a,true);out.set(text,20);out.fill(32,20+text.length,20+text.length+jp);let pos=20+text.length+jp;dd.setUint32(pos,bin.length+bp,true);dd.setUint32(pos+4,0x004e4942,true);out.set(bin,pos+8);return b64(out)
}
const result=urbanA20();const q=audit(result.model);
if(q.degenerate_triangles||q.nonpositive_primitive_volumes)throw Error('primitive QA failure');
const out='build/g4c7_a20';fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'a20_faulted_civic_strata.obj'),obj(result.model));
fs.writeFileSync(path.join(out,'a20_faulted_civic_strata.glb'),Buffer.from(glb(result.model),'base64'));
fs.writeFileSync(path.join(out,'a20_primitive_qa.json'),JSON.stringify({geometry:q,spaces:result.counts,art:'HOLD',legacy_route_331_993:'NOT TESTED',minecraft:'PROHIBITED',city_integration:'PROHIBITED'},null,2)+'\n');
console.log(JSON.stringify(q,null,2));
