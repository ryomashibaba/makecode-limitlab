// MakeCode LimitLab / G4-C7 A45 CIVIC POCKET FOLD real sculpted sectional research and near-plane clipping.
// ART HOLD: exploratory S1 section, not city, no world or Minecraft operations.
// Run in Node as an import via tools/g4c7_a43_inhabited_seam.mjs; see A45 audit for execution.
const M=[
["chalk_stone",[220,222,207]],["shadow_structure",[54,74,78]],["civic_ground",[161,176,167]],
["red_stone",[178,109,83]],["warm_timber",[191,140,102]],["brass_trim",[220,182,101]],
["glass_blue",[103,169,177]],["recessed_dark",[41,56,67]],["warm_glow",[241,205,153]],
["planted_green",[89,151,109]],["book_paper",[209,184,140]],["cultural_red",[173,83,79]],
["workshop_blue",[83,117,137]],["roof_ceramic",[180,198,190]],["garden_green",[111,157,112]],
["people",[61,92,112]]
];
function build(){
 const V=[],F=[],tags={}; let tag="site";
 const add=p=>(V.push(p),V.length-1);
 function tri(a,b,c,m){F.push([add(a),add(b),add(c),m]);tags[tag]=(tags[tag]||0)+1}
 function quad(a,b,c,d,m){const v=[add(a),add(b),add(c),add(d)];F.push([v[0],v[1],v[2],m],[v[0],v[2],v[3],m]);tags[tag]=(tags[tag]||0)+2}
 // The first geometry is the inhabited solid + void and main tectonic fold.
 // No array of boxes is used to choose its architectural silhouette.
 function strip(sections,upperFn,lowerFn,zFront,zBack,mTop,mBottom,mFront,mRear,closedEnds=true){
   const u=sections.map((x,i)=>[x,upperFn(x,i),zFront(x,i)]),l=sections.map((x,i)=>[x,lowerFn(x,i),zFront(x,i)]);
   const U=sections.map((x,i)=>[x,upperFn(x,i),zBack(x,i)]),L=sections.map((x,i)=>[x,lowerFn(x,i),zBack(x,i)]);
   for(let i=0;i<sections.length-1;i++){
     quad(u[i],u[i+1],U[i+1],U[i],mTop);
     quad(L[i],L[i+1],l[i+1],l[i],mBottom);
     quad(l[i],l[i+1],u[i+1],u[i],mFront);
     quad(U[i],U[i+1],L[i+1],L[i],mRear);
   }
   if(closedEnds){let i=0,j=sections.length-1;quad(u[i],U[i],L[i],l[i],mFront);quad(l[j],L[j],U[j],u[j],mFront);}
 }
 function prism(poly,y0,y1,m){
  for(let k=1;k<poly.length-1;k++){tri([poly[0][0],y0,poly[0][1]],[poly[k+1][0],y0,poly[k+1][1]],[poly[k][0],y0,poly[k][1]],m);tri([poly[0][0],y1,poly[0][1]],[poly[k][0],y1,poly[k][1]],[poly[k+1][0],y1,poly[k+1][1]],m);}
  for(let i=0;i<poly.length;i++){let j=(i+1)%poly.length;quad([poly[i][0],y0,poly[i][1]],[poly[j][0],y0,poly[j][1]],[poly[j][0],y1,poly[j][1]],[poly[i][0],y1,poly[i][1]],m)}
 }
 function block(x,y,z,w,h,d,m){prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m)}
 function slab(poly,y,h,m){prism(poly,y,y+h,m)}
 function ribbon(points,w,h,m){
   const tang=(a,b)=>[b[0]-a[0],b[2]-a[2]],sides=[];
   for(let i=0;i<points.length;i++){
    let d=tang(points[Math.max(0,i-1)],points[Math.min(i+1,points.length-1)]),len=Math.hypot(...d)||1,n=[-d[1]/len*w/2,d[0]/len*w/2],p=points[i];
    sides.push([[p[0]+n[0],p[1]+h/2,p[2]+n[1]],[p[0]-n[0],p[1]+h/2,p[2]-n[1]],[p[0]+n[0],p[1]-h/2,p[2]+n[1]],[p[0]-n[0],p[1]-h/2,p[2]-n[1]]]);
   }
   for(let i=0;i<points.length-1;i++){let a=sides[i],b=sides[i+1];
    quad(a[0],b[0],b[1],a[1],m);quad(a[2],a[3],b[3],b[2],m);
    quad(a[0],a[2],b[2],b[0],m);quad(a[3],a[1],b[1],b[3],m);
   }
 }
 function humanoid(x,y,z){block(x,y+.67,z,.44,1.2,.37,15);block(x,y+1.5,z,.49,.46,.49,8);}
 tag="site-and-public-clearing";
 // Ground mass follows a wedge rather than a single square plot.
 slab([[-83,-68],[18,-86],[93,-54],[106,54],[52,94],[-65,68],[-87,11]],-.85,.85,2);
 slab([[-75,-53],[-35,-62],[20,-58],[61,-36],[46,25],[-16,44],[-65,12]],0,.22,4);
 tag="hero-fold-main-thick-body";
 // 15 stations define the architectural language. A continuous, thick, asymmetrical inhabitated canopy.
 const stations=Array.from({length:18},(_,i)=>-72+i*8.05);
 function profile(x) {
   const hump=8*Math.exp(-Math.pow((x-8)/39,2));
   const x0=[-72,-51,-24,-1,24,47,65];
   const h=[31,49,54,60,57,45,24];
   const bottom=[22,32,38,40,34,22,13];
   let j=0;while(j<x0.length-2&&x>x0[j+1])j++;
   const u=Math.max(0,Math.min(1,(x-x0[j])/(x0[j+1]-x0[j])));
   let ease=u*u*(3-2*u);
   return [h[j]*(1-ease)+h[j+1]*ease+1.5*Math.sin(.085*x),bottom[j]*(1-ease)+bottom[j+1]*ease,hump];
 }
 const top=x=>profile(x)[0],bottom=x=>profile(x)[1];
 const front=x=>-24+2.2*Math.sin(x*.052)-.05*x,back=x=>47+5*Math.sin(x*.035)+.02*x;
 // The frontage face of the high fold is visibly perforated: not a blank face.
 strip(stations,top,bottom,front,back,0,1,7,0,true);
 tag="grounded-thick-south-east-buttress";
 // A single descending sculpted inhabited side anchors the east; avoid a freestanding U arch.
 const bank=[21,26,34,43,52,61,69,75];
 function edgeY(x){return 1+Math.max(0,top(Math.min(x,65))-14)*Math.pow((75-x)/54,.88);}
 strip(bank,edgeY,()=>0,x=>-21+1.3*Math.sin(x*.07),x=>50+2*Math.sin(x*.03),0,3,1,0,true);
 tag="active-openings-across-fold-front";
 // Facade is a row of *real apertures*, not glass polygons covering the whole solid:
 // hide sections of the outer front wall behind the entrance frames by inserting narrow thick-depth arches.
 const slots=[[-59,-49],[-41,-30],[-22,-10],[-2,10],[18,30],[38,48]];
 for(let k=0;k<slots.length;k++){const [a,b]=slots[k],x=(a+b)/2,y0=bottom(x)+2.0,y1=Math.min(top(x)-2, y0+9.5);
   const z=front(x)-.4,bezel=1.1,mi=k<2?3:(k<4?6:4);
   block(x,y0,z,b-a,.5,1.5,5);block(x,y1,z,b-a,.7,1.5,5);
   block(a,y0+(y1-y0)/2,z,bezel,y1-y0,1.4,0);block(b,y0+(y1-y0)/2,z,bezel,y1-y0,1.4,0);
   // transparent physical opening is claimed ONLY for this separate decorative frame;
   // the primary solid still has a face here -> no true boolean opening, record this limitation.
   block(x,y0+.9,z+.5,b-a-2.4,1.3,1.1,mi);
 }
 tag="civic-room-inner-occupation";
 // Depth matters: urban civic functions are nested at rear and facing the common room.
 slab([[-51,7],[-29,-2],[-6,9],[3,32],[-19,46],[-49,32]],.35,.85,3);
 slab([[-12,25],[20,17],[34,34],[21,50],[-17,58]],.35,1.2,4);
 // Concrete organic podiums and stepped cultural performance:
 const amph=Array.from({length:4},(_,n)=>({r:8+n*5,y:.7+n*.65}));
 for(let n=0;n<amph.length;n++){const {r,y}=amph[n],points=[];for(let i=0;i<=18;i++){
 const a=-.95*Math.PI/2+i*1.9*Math.PI/18;points.push([10+r*Math.cos(a),22+r*Math.sin(a)]);
 }
 for(let i=0;i<points.length-1;i++){let p=points[i],q=points[i+1];slab([p,q,[q[0]*.99+10*.01,q[1]*.99+22*.01],[p[0]*.99+10*.01,p[1]*.99+22*.01]],y,.46,n%2?11:3);}
 }
 tag="research-residential-inhabited-core";
 // Occupied deep cross-section: not 4 isolated buildings. Interior reading zone and terrace share fold profiles.
 const zones=[[-51,-22,27,37],[-18,8,35,43],[14,40,32,40]];
 for(let i=0;i<zones.length;i++){
  let [a,b,ylo,yhi]=zones[i],z0=5+i*6,z1=33+i*3;
  slab([[a,z0],[b,z0+2],[b,z1],[a,z1-2]],ylo,1.8,i===1?4:0);
  // vertical inhabited recesses, visible behind facade as actual volumes with desks/shelves; scaled people show program.
  for(let x=a+4;x<b-3;x+=6.5){
   block(x,ylo+2.1,z1-3,4.7,4.0,1.0,i===0?10:(i===1?12:8));
   if(i===0){block(x,ylo+1.5,z1-4,3.8,.33,1.5,4);}
   if(i===1){block(x,ylo+1.9,z1-4,3.8,.5,1.7,12);}
   if(i===2){block(x,ylo+1.7,z1-4,4,1.3,2.5,14);}
  }
 }
 tag="public-entry-and-human-reference";
 // No floating access claim: visual pedestrian route on ground, not certified traversable route.
 ribbon([[-30,.4,-62],[-28,.5,-39],[-18,.65,-17],[-8,.8,4],[8,.88,16]],10,.65,5);
 // Market stalls inside cavern, kept minimal to test architecture rather than furnishing as a camouflage.
 for(let [x,z] of [[-43,-1],[-35,12],[-24,24],[-41,31]]){
   block(x,1.35,z,5,.5,3.2,4);
   block(x,2.1,z,4.5,.7,3.1,3);
   block(x,3.5,z,4,.4,2.5,5);
 }
 for(let [x,y,z] of [[-27,0,-35],[-18,0,-14],[-27,0,4],[7,0,14],[19,0,39],[-30,32,13]])humanoid(x,y,z);
 // Few exterior entry indicators are free-standing; they do not count as structure or G2.
 return {V,F,tags,M,anchors:{southArrival:[-30,2,-50],publicRoom:[-13,2,19],market:[-37,2,11],culture:[10,2,22],reading:[-37,29,22],upperHome:[25,39,25]},scope:"A45 early S1 nonbuild mass study. Unproven actual apertures, connectivity and walkability."};
}
function b64(bytes){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";let r="";for(let i=0;i<bytes.length;i+=3){const a=bytes[i],b=bytes[i+1]||0,c=bytes[i+2]||0;r+=abc[a>>2]+abc[((a&3)<<4)|(b>>4)]+(i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=")+(i+2<bytes.length?abc[c&63]:"=")}return r}
function obj(mesh){let s="# G4C7 A45 real mesh - ART HOLD - no construction\nmtllib materials.mtl\n",old=-1;for(let p of mesh.V)s+="v "+p.join(" ")+"\n";for(let f of mesh.F){if(f[3]!==old){old=f[3];s+="usemtl "+M[old][0]+"\n"}s+="f "+(f[0]+1)+" "+(f[1]+1)+" "+(f[2]+1)+"\n"}return s}
function mtl(){return M.map(([name,c])=>"newmtl "+name+"\nKd "+c.map(x=>(x/255).toFixed(6)).join(" ")+"\n").join("\n")}
function glb(mesh){
const p=new Uint8Array(mesh.V.length*12),d=new DataView(p.buffer),bin=[],bv=[],ac=[],prim=[];
mesh.V.forEach((v,i)=>v.forEach((x,j)=>d.setFloat32(i*12+j*4,x,true)));for(let x of p)bin.push(x);
bv.push({buffer:0,byteOffset:0,byteLength:p.length,target:34962});
const range=[0,1,2].map(j=>[Math.min(...mesh.V.map(v=>v[j])),Math.max(...mesh.V.map(v=>v[j]))]);
ac.push({bufferView:0,componentType:5126,count:mesh.V.length,type:"VEC3",min:range.map(x=>x[0]),max:range.map(x=>x[1])});
for(let j=0;j<M.length;j++){const ids=mesh.F.filter(f=>f[3]===j).flatMap(f=>f.slice(0,3));if(!ids.length)continue;
const off=bin.length;for(let i of ids)bin.push(i&255,(i>>8)&255,(i>>16)&255,(i>>>24)&255);
bv.push({buffer:0,byteOffset:off,byteLength:ids.length*4,target:34963});ac.push({bufferView:bv.length-1,componentType:5125,count:ids.length,type:"SCALAR"});prim.push({attributes:{POSITION:0},indices:ac.length-1,material:j,mode:4})}
while(bin.length%4)bin.push(0);
const root={asset:{version:"2.0",generator:"MakeCode LimitLab G4C7 A45 nonbuild art study"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prim}],materials:M.map(([name,c])=>({name,pbrMetallicRoughness:{baseColorFactor:[...c.map(x=>x/255),1],metallicFactor:.04,roughnessFactor:.83},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bv,accessors:ac};
let json=Array.from(JSON.stringify(root)).map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
const out=new Uint8Array(28+json.length+bin.length),v=new DataView(out.buffer);v.setUint32(0,0x46546c67,true);v.setUint32(4,2,true);v.setUint32(8,out.length,true);v.setUint32(12,json.length,true);v.setUint32(16,0x4e4f534a,true);out.set(json,20);const off=20+json.length;v.setUint32(off,bin.length,true);v.setUint32(off+4,0x004e4942,true);out.set(bin,off+8);return{data:out,json:root};
}
function render(mesh,eye,target,mode="ortho",scale=2.4,W=560,H=420){
 const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 const dot=(a,b)=>a.reduce((n,x,i)=>n+x*b[i],0),norm=a=>{let n=Math.hypot(...a)||1;return a.map(x=>x/n)};
 const fw=norm(sub(target,eye)),right=norm(cross([0,1,0],fw)),up=norm(cross(fw,right)),L=norm([-.3,.9,-.35]);
 const near=2,depth=p=>dot(sub(p,eye),fw);
 const point=p=>{let re=sub(p,eye),t=sub(p,target),z=depth(p);return [W/2+(mode==="perspective"?305*dot(re,right)/z:scale*dot(t,right)),H/2-(mode==="perspective"?305*dot(re,up)/z:scale*dot(t,up)),z]};
 const pix=new Uint8Array(W*H),Z=new Float32Array(W*H);Z.fill(Infinity);
 let ignored=0,clipped=0,fullyBehind=0,trianglesRasterized=0;
 function clipNear(polygon){
  let res=[];
  for(let i=0;i<polygon.length;i++){
   let a=polygon[i],b=polygon[(i+1)%polygon.length],za=depth(a)-near,zb=depth(b)-near;
   if(za>=0)res.push(a);
   if((za<0&&zb>0)||(za>0&&zb<0)){let t=za/(za-zb);res.push(a.map((v,j)=>v+t*(b[j]-v)));}
  }
  return res;
 }
 for(let f of mesh.F){
   let orig=f.slice(0,3).map(i=>mesh.V[i]);
   let n=norm(cross(sub(orig[1],orig[0]),sub(orig[2],orig[0])));
   let shade=Math.max(0,Math.min(7,Math.round(2+5*Math.max(0,dot(n,L)))));
   let nearCount=orig.filter(p=>depth(p)<near).length;
   if(nearCount===3){ignored++;fullyBehind++;continue}
   if(nearCount>0){clipped++;ignored++}
   let poly=nearCount?clipNear(orig):orig;
   if(poly.length<3)continue;
   for(let ti=1;ti<poly.length-1;ti++){
     let a=point(poly[0]),b=point(poly[ti]),c=point(poly[ti+1]);trianglesRasterized++;
     let area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
     if(Math.abs(area)<1e-9)continue;
     let x0=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0]))),x1=Math.min(W-1,Math.ceil(Math.max(a[0],b[0],c[0])));
     let y0=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),y1=Math.min(H-1,Math.ceil(Math.max(a[1],b[1],c[1])));
     for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){
       let X=x+.5,Y=y+.5;
       let w1=((X-a[0])*(c[1]-a[1])-(Y-a[1])*(c[0]-a[0]))/area;
       let w2=((b[0]-a[0])*(Y-a[1])-(b[1]-a[1])*(X-a[0]))/area;
       let w0=1-w1-w2;
       if(w0<-.00001||w1<-.00001||w2<-.00001)continue;
       let z=mode==="perspective"?(1/(w0/a[2]+w1/b[2]+w2/c[2])):(w0*a[2]+w1*b[2]+w2*c[2]);
       let i=y*W+x;if(z<Z[i]){Z[i]=z;pix[i]=1+f[3]*8+shade;}
     }
   }
 }
const pal=[[25,42,55],...M.flatMap(([name,col])=>Array.from({length:8},(_,k)=>col.map(x=>Math.min(255,Math.round(x*(.40+k*.084))))))];
const u32=n=>[(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255],crct=Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0});
const crc=a=>{let c=0xffffffff;for(let x of a)c=crct[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0};
function chunk(k,a){let h=Array.from(k).map(x=>x.charCodeAt(0));return[...u32(a.length),...h,...a,...u32(crc([...h,...a]))]}
let raw=[];for(let y=0;y<H;y++){raw.push(0);for(let x=0;x<W;x++)raw.push(pix[y*W+x])}
let a=1,b=0;for(let x of raw){a=(a+x)%65521;b=(b+a)%65521}
const def=[0x78,1];for(let j=0;j<raw.length;){let len=Math.min(65535,raw.length-j);def.push(j+len===raw.length?1:0,len&255,(len>>8)&255,(~len)&255,((~len)>>8)&255,...raw.slice(j,j+len));j+=len}def.push(...u32(((b<<16)|a)>>>0));
return{data:new Uint8Array([137,80,78,71,13,10,26,10,...chunk("IHDR",[...u32(W),...u32(H),8,3,0,0,0]),...chunk("PLTE",pal.flat()),...chunk("IDAT",def),...chunk("IEND",[])]),covered:pix.reduce((n,x)=>n+(x!==0),0),excluded:ignored,clipped,fullyBehind,trianglesRasterized};
}
function renderViews(mesh){
const cameras={
south_arrival:[[-28,3,-74],[-8,12,24],"perspective",0],
civic_room:[[-11,3,-20],[2,17,25],"perspective",0],
market_portal:[[9,5,-17],[-36,12,16],"perspective",0],
residential_edge:[[18,27,-41],[3,44,24],"perspective",0],
front:[[0,110,-190],[0,26,8],"ortho",2.18],
oblique:[[160,120,-151],[0,25,10],"ortho",2.12],
side:[[196,116,6],[0,26,10],"ortho",2.18],
aerial:[[149,215,-118],[0,25,11],"ortho",2.14]};
return Object.fromEntries(Object.entries(cameras).map(([n,c])=>[n,render(mesh,...c)]));
}
({M,build,b64,obj,mtl,glb,render,renderViews});

import fs from "node:fs";import path from "node:path";
if(process.argv.includes("--write")){
 const root="artifacts/g4c7-a45-civic-pocket-s1";
 const save=(name,data)=>{const dest=path.join(root,name);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,data)};
 const m=build();
 save("a45_civic_pocket_fold.obj",obj(m));
 save("a45_civic_pocket_fold.glb",Buffer.from(glb(m).data));
 save("materials.mtl",mtl());
 for(const [name,im] of Object.entries(renderViews(m)))save("verified-png/"+name+".png",Buffer.from(im.data));
 console.log("A45 real 3D S1 limited art study; ART HOLD; Minecraft untouched.");
}
