#!/usr/bin/env node
// G4-C7 visual REVIEW ONLY. Deterministic 3D cuboid mesh + orthographic SVG.
// Not Minecraft build code. Outputs ONLY to an explicitly supplied NEW directory.
'use strict';
const fs=require('fs'),path=require('path');
const {create,validate}=require('./g4c7_urban_layout_lab');
const cameras={
 front:{az:0,elev:16,label:'FRONT / 南側から',subset:null},
 side:{az:90,elev:16,label:'SIDE / 東側から',subset:null},
 oblique:{az:42,elev:32,label:'OBLIQUE / 斜め俯瞰',subset:null},
 aerial:{az:42,elev:78,label:'AERIAL / ほぼ真俯瞰',subset:null}
};
const palette={
 A:{concrete:'#b5c1d0','glass-and-frame':'#528aa7',glass:'#79b8d1',stone:'#d7dce7'},
 B:{concrete:'#cfbca0',stone:'#efe1c8',glass:'#9ac6bc'},
 C:{concrete:'#a3b6a2',stone:'#759982',glass:'#85b7a4'},
 D:{concrete:'#9aafc7',stone:'#b3cae6',glass:'#5b9fba'}
};
function clamp(n,min,max){return Math.max(min,Math.min(max,n))}
function shade(hex,k){
 const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
 return '#'+[r,g,b].map(x=>clamp(Math.round(x*k),0,255).toString(16).padStart(2,'0')).join('');
}
function corners(b){
 const x=b.x,y=b.y,z=b.z,X=x+b.w,Y=y+b.h,Z=z+b.d;
 return [[x,y,z],[X,y,z],[X,y,Z],[x,y,Z],[x,Y,z],[X,Y,z],[X,Y,Z],[x,Y,Z]];
}
const faceDefs=[
 {v:[3,2,6,7],n:[0,0,1],factor:.82}, // +z
 {v:[0,4,5,1],n:[0,0,-1],factor:.66},
 {v:[1,5,6,2],n:[1,0,0],factor:.74},
 {v:[0,3,7,4],n:[-1,0,0],factor:.89},
 {v:[4,7,6,5],n:[0,1,0],factor:1.12},
 {v:[0,1,2,3],n:[0,-1,0],factor:.54}
];
function basis(cam){
 const a=cam.az*Math.PI/180,e=cam.elev*Math.PI/180;
 const view=[Math.sin(a)*Math.cos(e),Math.sin(e),Math.cos(a)*Math.cos(e)];
 const right=[Math.cos(a),0,-Math.sin(a)];
 const up=[-Math.sin(a)*Math.sin(e),Math.cos(e),-Math.cos(a)*Math.sin(e)];
 return {view,right,up};
}
function dot(a,b){return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]}
function primitives(plan,cam){
 const mat=basis(cam),projection=p=>[dot(p,mat.right),-dot(p,mat.up)];
 let items=[];
 // Ground and open civic plots. Ground only as neutral outline, NOT a rendered completed road.
 const ground={x:0,y:1,z:0,w:372,h:1,d:372};
 for(const box of [ground,...plan.boxes]){
  const pts=corners(box),reg=box.id?box.id[0]:'A';
  for(const f of faceDefs){
   if(dot(f.n,mat.view)<=0)continue;
   const q=f.v.map(i=>pts[i]),center=[
    q.reduce((n,v)=>n+v[0],0)/4,q.reduce((n,v)=>n+v[1],0)/4,
    q.reduce((n,v)=>n+v[2],0)/4
   ];
   const color=box===ground?'#263944':shade((palette[reg]&&palette[reg][box.material])||'#bbc9d7',f.factor);
   items.push({points:q.map(projection),depth:dot(center,mat.view),color,
     label:box.id?box.id+' '+box.role:'BASE REFERENCE ONLY'});
  }
 }
 items.sort((a,b)=>a.depth-b.depth);
 return items;
}
function escapeXml(s){return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;')}
function svg(plan,camName,opts={}){
 const cam=cameras[camName];if(!cam)throw Error('Unknown camera '+camName);
 const W=1200,H=900,margin=76,upper=108,footer=52;
 const items=primitives(plan,cam),pts=items.flatMap(x=>x.points);
 const xs=pts.map(x=>x[0]),ys=pts.map(x=>x[1]);
 const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
 const scale=Math.min((W-2*margin)/(maxX-minX),(H-upper-footer)/(maxY-minY));
 const cx=(minX+maxX)/2,cy=(minY+maxY)/2;
 const tx=p=>(W/2+(p[0]-cx)*scale).toFixed(2)+','+(upper+(H-upper-footer)/2+(p[1]-cy)*scale).toFixed(2);
 const polys=items.map(f=>'<polygon points="'+f.points.map(tx).join(' ')+'" fill="'+f.color+
   '" fill-opacity="'+(f.label==='BASE REFERENCE ONLY'?.18:.94)+
   '" stroke="#162e37" stroke-width=".65" stroke-opacity=".3"><title>'+escapeXml(f.label)+'</title></polygon>').join('\n');
 const scores=assess(plan);
 return '<?xml version="1.0" encoding="UTF-8"?>\n'+
   '<svg xmlns="http://www.w3.org/2000/svg" width="'+W+'" height="'+H+'" viewBox="0 0 '+W+' '+H+'">'+
   '<rect width="'+W+'" height="'+H+'" fill="#f1f5f6"/>'+
   '<rect width="'+W+'" height="102" fill="#102633"/>'+
   '<text x="46" y="48" fill="#ffffff" font-size="26" font-family="Arial,sans-serif" font-weight="700">G4-C7 / A2-A5 • '+escapeXml(cam.label)+'</text>'+
   '<text x="46" y="77" fill="#acbdc6" font-size="16" font-family="Arial,sans-serif">'+
   'CONCEPT ONLY • 22 masses / 4 districts • no ground-level usability approved</text>'+
   polys+
   '<text x="46" y="864" font-size="17" font-family="Arial,sans-serif" fill="#243847">'+
   'A Finance    B Culture    C Courtyard homes    D Laboratories    |    REVIEW STATUS: '+scores.verdict+'</text>'+
   '</svg>';
}
function toObj(plan){
 let lines=['# G4-C7 conceptual cuboid mesh; NOT a Minecraft/Blender build pass.','mtllib g4c7_review.mtl'];
 let offset=0;
 for(const box of plan.boxes){
  lines.push('o '+box.id+'_'+box.role.replace(/[^a-z0-9_-]/gi,'_'));
  lines.push('usemtl '+box.id[0]+'_'+box.material.replace(/[^a-z0-9_-]/gi,'_'));
  const pts=corners(box);
  for(const p of pts)lines.push('v '+p.join(' ')); // Y-UP, unit=1 block
  for(const face of faceDefs)lines.push('f '+face.v.map(i=>offset+i+1).join(' '));
  offset+=8;
 }
 return lines.join('\n')+'\n';
}
function mtl(){
 const out=['# Synthetic material placeholders; NOT actual Minecraft shader/materials'];
 const seen=new Set();
 for(const [reg,cs] of Object.entries(palette)){
  for(const [material,hex] of Object.entries(cs)){
   const name=reg+'_'+material.replace(/[^a-z0-9_-]/gi,'_');
   if(seen.has(name))continue;seen.add(name);
   const rgb=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255);
   out.push('newmtl '+name,'Kd '+rgb.join(' '),'Ka 0.15 0.15 0.15','d 1','');
  }
 }
 return out.join('\n');
}
function assess(plan){
 const groups={};
 for(const building of plan.buildings){
  let b=plan.boxes.filter(x=>x.id===building.id);
  const bx=Math.min(...b.map(x=>x.x)),bz=Math.min(...b.map(x=>x.z));
  // Ignore material colors and height variation, since a recolored tower
  // or merely taller version should NOT count as a new architectural type.
  const signature=b.map(x=>x.role+':'+(x.x-bx)+','+(x.z-bz)+','+x.w+'x'+x.d).sort().join('|');
  (groups[building.region]??=[]).push({id:building.id,signature});
 }
 const distribution={};
 for(const [reg,items] of Object.entries(groups)){
  const signatures=[...new Set(items.map(i=>i.signature))];
  const clusters=signatures.map(sig=>items.filter(x=>x.signature===sig).map(x=>x.id));
  distribution[reg]={buildings:items.length,distinctFootprintFamilies:signatures.length,
    repeatingClusters:clusters.filter(x=>x.length>=3)};
 }
 const allPass=Object.values(distribution).every(x=>x.distinctFootprintFamilies>=2&&
   x.repeatingClusters.length===0);
 return {kind:'OFFLINE_ART_REPETITION_METRIC_NOT_HUMAN_VISUAL_QA',
  measurement:'Geometric footprint and role signature; material changes and height alone excluded',
  distribution,
  verdict:allPass?'REQUIRES_HUMAN_ART_REVIEW':'REJECT_REPEATED_FOOTPRINT_FAMILIES'};
}
function writeNew(out,filename,data){
 const p=path.join(out,filename);
 fs.writeFileSync(p,data,{encoding:'utf8',flag:'wx'}); // never overwrite
}
function main(){
 const i=process.argv.indexOf('--out');
 if(i<0||!process.argv[i+1])throw Error('Usage: --out NEW_EMPTY_DIRECTORY');
 const folder=path.resolve(process.argv[i+1]);
 if(fs.existsSync(folder))throw Error('Output directory already exists; no overwrite '+folder);
 validate(); const plan=create(); const report=assess(plan);
 fs.mkdirSync(folder,{recursive:false});
 for(const name of Object.keys(cameras))writeNew(folder,name+'.svg',svg(plan,name));
 writeNew(folder,'g4c7_review.obj',toObj(plan));
 writeNew(folder,'g4c7_review.mtl',mtl());
 writeNew(folder,'review_quality.json',JSON.stringify(report,null,2)+'\n');
 writeNew(folder,'source_geometry.json',JSON.stringify(plan,null,2)+'\n');
 console.log(JSON.stringify({out:folder,files:Object.keys(cameras).length+4,
  buildings:plan.buildingCount,boxes:plan.boxes.length,quality:report.verdict,
  footprintFamilies:Object.fromEntries(Object.entries(report.distribution).map(([k,v])=>[k,v.distinctFootprintFamilies]))}));
}
if(require.main===module)main();
module.exports={svg,toObj,mtl,assess,primitives,basis,cameras};
