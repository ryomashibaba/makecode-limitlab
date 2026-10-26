// G4-C7 A48 — INHABITED CIVIC FORUM, one S1 real-mesh art scout.
// Render engine reuses A45 near-plane clipping and depth rasterization. ART REJECT / overall ART HOLD.
// Command: node tools/g4c7_a48_inhabited_civic_forum.mjs --write
// Non-build, no Minecraft/world operations, no overwriting prior evidence.
const M=[
["chalk_stone",[220,222,207]],["shadow_structure",[54,74,78]],["civic_ground",[161,176,167]],
["red_stone",[178,109,83]],["warm_timber",[191,140,102]],["brass_trim",[220,182,101]],
["glass_blue",[103,169,177]],["recessed_dark",[41,56,67]],["warm_glow",[241,205,153]],
["planted_green",[89,151,109]],["book_paper",[209,184,140]],["cultural_red",[173,83,79]],
["workshop_blue",[83,117,137]],["roof_ceramic",[180,198,190]],["garden_green",[111,157,112]],
["people",[61,92,112]]
];
function build(){
 const V=[],F=[],tags={};let tag="site";
 const idx=p=>(V.push(p),V.length-1);
 function tri(a,b,c,m){F.push([idx(a),idx(b),idx(c),m]);tags[tag]=(tags[tag]||0)+1}
 function quad(a,b,c,d,m){let j=[idx(a),idx(b),idx(c),idx(d)];F.push([j[0],j[1],j[2],m],[j[0],j[2],j[3],m]);tags[tag]=(tags[tag]||0)+2}
 function prism(poly,y0,y1,m){for(let k=1;k<poly.length-1;k++){tri([poly[0][0],y0,poly[0][1]],[poly[k+1][0],y0,poly[k+1][1]],[poly[k][0],y0,poly[k][1]],m);tri([poly[0][0],y1,poly[0][1]],[poly[k][0],y1,poly[k][1]],[poly[k+1][0],y1,poly[k+1][1]],m);}for(let i=0;i<poly.length;i++){let j=(i+1)%poly.length;quad([poly[i][0],y0,poly[i][1]],[poly[j][0],y0,poly[j][1]],[poly[j][0],y1,poly[j][1]],[poly[i][0],y1,poly[i][1]],m)}}
 function box(x,y,z,w,h,d,m){prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m)}
 function rayBeam(a,b,w,h,m){let dx=b[0]-a[0],dz=b[2]-a[2],len=Math.hypot(dx,dz);if(len<1e-7){let yl=Math.min(a[1],b[1])-h/2,yh=Math.max(a[1],b[1])+h/2;box(a[0],(yl+yh)/2,a[2],w,yh-yl,h,m);return;}let l=len,n=[-dz/l*w/2,dx/l*w/2];let ve=p=>[[p[0]+n[0],p[1]+h/2,p[2]+n[1]],[p[0]-n[0],p[1]+h/2,p[2]-n[1]],[p[0]-n[0],p[1]-h/2,p[2]-n[1]],[p[0]+n[0],p[1]-h/2,p[2]+n[1]]],u=ve(a),v=ve(b);for(let i=0;i<4;i++)quad(u[i],v[i],v[(i+1)%4],u[(i+1)%4],m)}
 function person(x,y,z){box(x,y+.67,z,.5,1.22,.45,15);box(x,y+1.53,z,.52,.48,.5,8)}
 const ctr=[0,18],N=24,thetas=Array.from({length:N+1},(_,i)=>-.12+(Math.PI+.24)*i/N);
 const inRadius=t=>26+2*Math.sin(2.3*t),outRadius=t=>48+3*Math.sin(1.7*t);
 const p=(t,r,y)=>[Math.cos(t)*r,y,ctr[1]+Math.sin(t)*r];
 const band=(t1,t2,ri,ro,y0,y1,material)=>{
   let shape=[[Math.cos(t1)*ri,ctr[1]+Math.sin(t1)*ri],[Math.cos(t2)*ri,ctr[1]+Math.sin(t2)*ri],[Math.cos(t2)*ro,ctr[1]+Math.sin(t2)*ro],[Math.cos(t1)*ro,ctr[1]+Math.sin(t1)*ro]];
   prism(shape,y0,y1,material);
 };
 const roof=t=>25+13*Math.sin(t)+3*Math.sin(2.7*t);
 tag="urban-landscape";
 const outer=Array.from({length:28},(_,i)=>{const a=2*Math.PI*i/28;return [Math.cos(a)*78,22+Math.sin(a)*76]});
 prism(outer,-.75,0,2);
 // Arrival broadens into public floor rather than staying narrow/blank.
 prism([[-17,-56],[17,-56],[19,4],[30,25],[0,43],[-32,25],[-19,4]],0,.38,4);
 tag="inhabited-continuous-deep-band";
 for(let i=0;i<N;i++){
  let a=thetas[i],b=thetas[i+1],t=(a+b)/2,ri=inRadius(t),ro=outRadius(t),h=Math.min(roof(a),roof(b));
  // Deep whole building floor and unusually thick stepped cap; NOT one featureless roofing plane.
  band(a,b,ri,ro,0,1.9,0);
  // Upper occupied floors vary with program; keep vertical voids below
  band(a,b,ri,ro,12.8,15,0);
  if(t>.24&&t<2.85)band(a,b,ri+3,ro,26.5,28.8,13);
  band(a,b,ri+2,ro,h-2.5,h, i>=8&&i<=16?0:13);
  // Outer backing: avoid a blank wall by regularly alternating between wall supports and large fenestration voids.
  if(i%3===0){let c=p(a,ro,0),d=p(a,ro,h);
   rayBeam(c,d,2.6,2.8,1);
  }
  // Mid-occupancy recessed wall sheets visible only at material zones, not whole outer cylinder
  if(i%4===0){
   let u=p(a,ro-2,15),v=p(b,ro-2,15),U=p(a,ro-2,25),Vv=p(b,ro-2,25);
   quad(u,v,Vv,U,3);
  }
  // Radial piers with clear openings between them; no single blank courtyard facade
  if(i%2===0){
    let aP=p(a,ri+3,0),bP=p(a,ri+3,roof(a)-3);
    rayBeam(aP,bP,2.7,2.7,1);
  }
  // Sculptural intermittently shaded canopy at mezzanine edges, not full indoor cavern
  if(i%5===1){let lo=p(a,ri-1,16),hi=p(b,ri-1,20);rayBeam(lo,hi,2.1,1.7,5);}
 }
 tag="market-niches-attached-to-band";
 // East/right arc has an occupied market inside continuous section: walk-up counters and distinctive awning roofs.
 for(let i=1;i<=7;i++){
   const t=thetas[i],center=p(t,inRadius(t)-1,0),e=p(t,inRadius(t)-7,0);
   const x=(center[0]+e[0])/2,z=(center[2]+e[2])/2;
   box(x,1.4,z,4.8,.66,2.4,4);box(x,2.2,z,4.2,1.1,2.4,8);
   let a=p(t-.047,inRadius(t)-8,5.7),b=p(t+.047,inRadius(t)+8,7.4);
   rayBeam(a,b,6,.36,i%2?11:5);
   box(center[0],5.8,center[2],2,7,2,0);
 }
 tag="culture-performance-center";
 // Culture platform directly connected to wall band near back center, with sculpted amphitheatre steps on same program.
 const t=1.60,center=p(t,inRadius(t)-7,0);
 for(let k=0;k<5;k++){
  const z=center[2]-k*2.6;
  box(center[0],.45+k*.40,z,17-k*1.65,.85,2.5,k%2?3:11);
 }
 // Cultural backdrop is architectural acoustic louvres, not a single flat back wall.
 for(let k=-4;k<=4;k++){let x=center[0]+k*2.2;rayBeam([x,1,center[2]+9],[x,13+(4-Math.abs(k))*.9,center[2]+9.8],1.35,1.2,k%2?11:12);}
 tag="library-reading-gallery";
 // West/left arc: floor-to-upper-band shelves + visible desks in deep recessed bay.
 for(let i=18;i<=23;i++){
 const t=thetas[i],r=inRadius(t)+5,a=p(t,r,0),outer=p(t,r+10,0),x=(a[0]+outer[0])/2,z=(a[2]+outer[2])/2;
 box(x,6.0,z,2.4,10.3,1.6,10);
 for(let j=0;j<4;j++)box(x,2.3+j*2.5,z-.85,2.2,.28,2,4);
 const front=p(t,inRadius(t)-3,0);box(front[0],1.2,front[2],4.5,.36,2.5,4);box(front[0],.56,front[2],.45,1.1,.5,1);
 }
 tag="upper-residential-visible-occupation";
 // Third dimension inhabited, not roof/blank wall; apartments have large external room terraces.
 for(let i of [3,5,7,10,12,14,17,20,22]){
  const t=thetas[i],ri=inRadius(t)+3,ro=outRadius(t)-5,c=p(t,(ri+ro)/2,15);
  box(c[0],16.8,c[2],6.7,2.3,7.2,14);
  box(c[0],18.7,c[2],5.8,.5,5.5,9);
  box(c[0],21.6,c[2],6,4,1.2,6);
 }
 tag="civic-structure-and-route-legibility";
 // Three short approaches target the same public chamber rather than divergent pavilions.
 const path=[[0,.5,-53],[0,.6,-22],[0,.7,3],[0,.8,20]],along=(a,b)=>rayBeam(a,b,11,.8,4);
 for(let i=0;i<path.length-1;i++)along(path[i],path[i+1]);
 for(const t of [.45,1.5,2.62]){let c=p(t,20,.8),d=p(t,28,.8);along(c,d);}
 // Public core is deliberately compact, densely inhabited instead of empty campus plaza.
 for(let [x,z] of [[-8,13],[0,24],[11,19]]){box(x,.8,z,3.4,1.4,4.2,3);box(x,2.9,z,1.5,2.5,1.8,9);}
 tag="people-proportion-reference";
 for(let [x,y,z] of [[0,0,-32],[0,0,-17],[11,0,10],[5,0,30],[-11,0,15],[-21,0,39],[24,0,31],[40,0,17],[-43,0,21]])person(x,y,z);
 return {V,F,tags,M,scope:"A48 one S1 scout from G0: inhabited radial continuous building around open civic chamber; not a city or G2/G3 proof",programGroups:["market","culture","library","upper housing"],center:ctr};
}
function b64(bytes){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";let r="";for(let i=0;i<bytes.length;i+=3){const a=bytes[i],b=bytes[i+1]||0,c=bytes[i+2]||0;r+=abc[a>>2]+abc[((a&3)<<4)|(b>>4)]+(i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=")+(i+2<bytes.length?abc[c&63]:"=")}return r}
function obj(mesh){let s="# G4C7 A48 real mesh - ART HOLD - no construction\nmtllib materials.mtl\n",old=-1;for(let p of mesh.V)s+="v "+p.join(" ")+"\n";for(let f of mesh.F){if(f[3]!==old){old=f[3];s+="usemtl "+M[old][0]+"\n"}s+="f "+(f[0]+1)+" "+(f[1]+1)+" "+(f[2]+1)+"\n"}return s}
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
const root={asset:{version:"2.0",generator:"MakeCode LimitLab G4C7 A48 nonbuild art study"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prim}],materials:M.map(([name,c])=>({name,pbrMetallicRoughness:{baseColorFactor:[...c.map(x=>x/255),1],metallicFactor:.04,roughnessFactor:.83},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bv,accessors:ac};
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
function renderViews(mesh){const cameras={
atrium_arrival:[[0,2.1,-35],[0,9,47],"perspective",0],
civic_forum:[[0,2.4,1],[0,13,51],"perspective",0],
market_room:[[8,2,1],[28,8,26],"perspective",0],
reading_room:[[-8,2,0],[-28,12,28],"perspective",0],
front:[[0,96,-191],[0,22,20],"ortho",2.26],
oblique:[[141,119,-146],[0,22,20],"ortho",2.26],
side:[[193,116,20],[0,22,20],"ortho",2.26],
aerial:[[131,194,-115],[0,19,20],"ortho",2.26]
};return Object.fromEntries(Object.entries(cameras).map(([n,v])=>[n,render(mesh,...v)]));}

import fs from "node:fs";
import path from "node:path";
if(process.argv.includes("--write")){
 const root="artifacts/g4c7-a48-inhabited-civic-forum-s1",m=build(),pics=renderViews(m);
 const files=[["a48_inhabited_civic_forum.obj",obj(m)],["a48_inhabited_civic_forum.glb",Buffer.from(glb(m).data)],["materials.mtl",mtl()],...Object.entries(pics).map(([n,v])=>["verified-png/"+n+".png",Buffer.from(v.data)])];
 for(const [n] of files){if(fs.existsSync(path.join(root,n)))throw Error("A48 original preserved. Cannot overwrite "+n);}
 for(const [n,c] of files){let f=path.join(root,n);fs.mkdirSync(path.dirname(f),{recursive:true});fs.writeFileSync(f,c);}
 console.log("G4C7 A48 geometry and 8 real depth PNGs generated. ART REJECT / HOLD; no Minecraft writes.");
}
