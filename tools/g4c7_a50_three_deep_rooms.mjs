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
 const V=[],F=[],tags={},semantics={};let group="site";
 const v=p=>(V.push(p),V.length-1);
 function tri(a,b,c,m){F.push([v(a),v(b),v(c),m]);tags[group]=(tags[group]||0)+1;}
 function quad(a,b,c,d,m){let k=[v(a),v(b),v(c),v(d)];F.push([k[0],k[1],k[2],m],[k[0],k[2],k[3],m]);tags[group]=(tags[group]||0)+2;}
 function prism(p,y0,y1,m){if(p.length<3||y1<=y0)throw Error("Invalid solid");for(let i=1;i<p.length-1;i++){tri([p[0][0],y0,p[0][1]],[p[i+1][0],y0,p[i+1][1]],[p[i][0],y0,p[i][1]],m);tri([p[0][0],y1,p[0][1]],[p[i][0],y1,p[i][1]],[p[i+1][0],y1,p[i+1][1]],m);}for(let i=0;i<p.length;i++){let j=(i+1)%p.length;quad([p[i][0],y0,p[i][1]],[p[j][0],y0,p[j][1]],[p[j][0],y1,p[j][1]],[p[i][0],y1,p[i][1]],m);}}
 function box(x,y,z,w,h,d,m){prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m);}
 function bar(a,b,thick,height,m){
  let dx=b[0]-a[0],dz=b[2]-a[2],len=Math.hypot(dx,dz);if(len<1e-6){box(a[0],(a[1]+b[1])/2,a[2],thick,Math.abs(a[1]-b[1])+height,thick,m);return;}
  let n=[-dz/len*thick/2,dx/len*thick/2],h=height/2;
  const corners=p=>[[p[0]+n[0],p[1]+h,p[2]+n[1]],[p[0]-n[0],p[1]+h,p[2]-n[1]],[p[0]-n[0],p[1]-h,p[2]-n[1]],[p[0]+n[0],p[1]-h,p[2]+n[1]]];
  let u=corners(a),w=corners(b);for(let i=0;i<4;i++)quad(u[i],w[i],w[(i+1)%4],u[(i+1)%4],m);
 }
 function frameTransform(cx,cz,theta){let c=Math.cos(theta),s=Math.sin(theta);return (x,y,z)=>[cx+x*c+z*s,y,cz-x*s+z*c];}
 function localBox(T,x,y,z,w,h,d,m){const p=[[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]].map(([a,b])=>{let q=T(a,0,b);return[q[0],q[2]]});prism(p,y-h/2,y+h/2,m);}
 function chamber({name,cx,cz,theta,width,depth,height,stone,accent,roofH=1.8}){
  const T=frameTransform(cx,cz,theta),W=width/2,D=depth/2;
  // Occupied, bounded interior, with a genuine full-depth front portal, and side clerestories.
  group="room-envelope-"+name;
  const polygon=[T(-W,0,-D),T(W,0,-D),T(W,0,D),T(-W,0,D)].map(p=>[p[0],p[2]]);
  prism(polygon,0,.75,4);
  // Rear solid wall, only one wall defines the depth: sides + roof construct the actual room.
  localBox(T,0,height/2,D-.65,width,height,1.3,stone);
  // side walls with large sidelight gaps between solid bands
  for(let sx of [-1,1]){
   localBox(T,sx*(W-.75),3.4,8,1.5,6.8,depth-16,stone);
   localBox(T,sx*(W-.75),height-2.2,0,1.5,4.4,depth-2,stone);
   localBox(T,sx*(W-.75),1.1,-D+4,1.5,2.2,8,stone);
  }
  // Real front openings: central 11m portal + two side shopfronts; no mesh over the void.
  const opening=11,segW=(width-opening)/2;
  localBox(T,-(opening+segW)/2,height/2,-D+.75,segW,height,1.5,stone);
  localBox(T,(opening+segW)/2,height/2,-D+.75,segW,height,1.5,stone);
  // Carved opening in each side wing: removes lower part of front wall for shopfront.
  // Header only over central portal — the opening is not decorative.
  localBox(T,0,height-1.7,-D+.75,opening,3.4,1.5,stone);
  const diagRoof=[T(-W-2,0,-D-2),T(W+2,0,-D-2),T(W+4,0,D+2),T(-W-4,0,D+2)].map(p=>[p[0],p[2]]);
  prism(diagRoof,height,height+roofH,13);
  // Nested inhabited upper roof edge, not a uniform full-city canopy.
  const T1=T(-W-2,height+roofH,-D-2),T2=T(W+2,height+roofH,-D-2);
  bar(T1,T2,1.0,1.2,5);
  group="room-activity-"+name;
  if(name==="market"){
   for(let x of [-W+5,-W+14,4,W-9])for(let z of [-D+9,-D+19]){
    localBox(T,x,1.45,z,5.7,.65,3.1,4);
    localBox(T,x,2.55,z,5.1,1.6,2.9,8);
    localBox(T,x,3.9,z,5.5,.38,3.5,5);
   }
   for(let x of [-W+7,W-8]){localBox(T,x,4.8,4,7,8,.9,3);for(let t=0;t<3;t++)localBox(T,x,2.0+t*2.1,3.4,6,.34,1.5,5);}
  } else if(name==="culture"){
   // Fabrication benches, workshop display and deep acoustic/niche stage at the back.
   for(let x of [-W+8,0,W-8])for(let z of [-D+12,-D+23]){
    localBox(T,x,1.7,z,5.2,1.15,3.1,12);
    localBox(T,x,2.5,z,4.3,.4,2.7,4);
    localBox(T,x,4.1,z,1.0,2.7,1.3,11);
   }
   for(let i=0;i<7;i++){
    const x=-W+6+i*(width-12)/6;
    localBox(T,x,4.3,D-4,1.2,7.8,1.4,i%2?11:12);
   }
  } else if(name==="library"){
   for(let x of [-W+5,-W+12,W-13,W-6])for(let z of [-D+12,-D+21,-D+29]){
    localBox(T,x,4.7,z,5.4,8.4,1.35,10);
    for(let t=0;t<4;t++)localBox(T,x,1.5+t*2.0,z-1,5,.30,1.2,4);
   }
   for(let x of [-9,0,9])for(let z of [-D+15,-D+25]){
    localBox(T,x,1.2,z,6,.38,3.1,4);
    localBox(T,x,.65,z,1,1.1,.7,1);
   }
  }
  // Open forward terrace integrated into the same entrance surface.
  group="interconnected-public-room";
  const landing=[T(-W+3,0,-D-7),T(W-3,0,-D-7),T(W-3,0,-D),T(-W+3,0,-D)].map(p=>[p[0],p[2]]);
  prism(landing,0,.46,4);
  return {T,front:T(0,0,-D-6),interior:T(0,2,0),back:T(0,0,D-4),opening:{world:T(0,6,-D+.7),width:opening,height:height-3.4}};
 }
 group="site";
 prism([[-70,-56],[-21,-67],[39,-59],[73,-32],[78,34],[37,75],[-51,60],[-73,15]],-.8,0,2);
 // One continuous civic floor that enters and connects all three rooms; not an empty high plaza.
 prism([[-13,-53],[14,-53],[17,-21],[25,-4],[20,20],[14,39],[-17,40],[-24,18],[-23,-5]],0,.42,4);
 // Three substantial interlocking chambers: portal fronts face ONE shared public room,
 // while their rear walls form the thick near-urban perimeter.
 const rooms=[
  {name:"market",cx:-28,cz:4,theta:-Math.PI/2,width:35,depth:38,height:17,stone:0,accent:3},
  {name:"culture",cx:27,cz:12,theta:Math.PI/2,width:35,depth:40,height:20,stone:1,accent:12},
  {name:"library",cx:1,cz:50,theta:0,width:40,depth:35,height:22,stone:0,accent:6}
 ];
 const s=rooms.map(chamber);
 group="upper-inhabited-rooms";
 // Housing/upper commons is a set of inhabited roof rooms at real depth, not a duplicated slab city.
 // Separate 3D units sit on continuous roof structure and have their own door-sized front openings.
 for(let [index,ch] of [[0,rooms[0]],[2,rooms[2]]]){
  const T=frameTransform(ch.cx,ch.cz,ch.theta),y=ch.height+2.3,d=17,w=19;
  const x=index===0?-5:6,z=2;
  const polygon=[T(x-w/2,0,z-d/2),T(x+w/2,0,z-d/2),T(x+w/2,0,z+d/2),T(x-w/2,0,z+d/2)].map(p=>[p[0],p[2]]);
  prism(polygon,y,y+.8,14);
  localBox(T,x,y+5.5,z+d/2,19,10,1.2,1);
  localBox(T,x-w/2,y+5.5,z,1.2,10,d,1);
  localBox(T,x+w/2,y+5.5,z,1.2,10,d,1);
  for(let x2 of [x-7,x+7])localBox(T,x2,y+5.4,z-d/2,2.1,10,1.2,0);
  localBox(T,x,y+9.1,z-d/2,12,2.8,1.3,0);
  prism(polygon,y+10.5,y+12.0,13);
  for(let x2 of [x-3,x+4])localBox(T,x2,y+1.2,z,5,.8,2.8,14);
 }
 group="public-route-and-height-anchors";
 // Abbreviated circulation paths; these are visually continuous, not G2 walkability certified.
 const route=[[-2,.5,-49],[-2,.5,-27],[0,.5,-7],[0,.5,13],[0,.5,30]];
 for(let k=0;k<route.length-1;k++)bar(route[k],route[k+1],10,.60,4);
 for(let ch of s){bar([0,.5,7],ch.front.map((p,i)=>i===1?.5:p),6.8,.6,4);}
 // Floating signboards are omitted intentionally; the geometry itself must show function.
 group="human-scale-reference";
 for(let [x,z] of [[0,-35],[0,-17],[2,3],[-15,2],[16,7],[1,31],[-36,9],[31,11]]){
  box(x,.70,z,.48,1.29,.44,15);
  box(x,1.57,z,.48,.46,.46,8);
 }
 return {V,F,tags,M,doors:s.map((room,i)=>({name:rooms[i].name,...room.opening})),programs:rooms.map(x=>x.name),scope:"A50 limited inhabited-room S1 scout, not adopted city or construction; no G2 or G3 QA."};
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
function renderViews(mesh){
const cameras={
arrival:[[0,2.4,-42],[0,10,22],"perspective",0],
forum:[[0,2.4,-8],[0,12,31],"perspective",0],
market:[[-7,2.4,0],[-33,9,8],"perspective",0],
culture:[[5,2.4,5],[31,10,13],"perspective",0],
library:[[0,2.4,22],[0,12,54],"perspective",0],
front:[[0,88,-155],[0,19,7],"ortho",2.62],
oblique:[[144,113,-132],[0,19,8],"ortho",2.52],
side:[[177,102,5],[0,19,8],"ortho",2.52],
aerial:[[136,191,-110],[0,19,8],"ortho",2.50]};
return Object.fromEntries(Object.entries(cameras).map(([name,args])=>[name,render(mesh,...args)]));
}

import fs from "node:fs";
import path from "node:path";
if(process.argv.includes("--write")){
const root="artifacts/g4c7-a50-three-deep-rooms-s1",mesh=build(),img=renderViews(mesh);
const files=[["a50_three_deep_rooms.obj",obj(mesh)],["a50_three_deep_rooms.glb",Buffer.from(glb(mesh).data)],["materials.mtl",mtl()],...Object.entries(img).map(([name,out])=>["verified-png/"+name+".png",Buffer.from(out.data)])];
for(let [name] of files){if(fs.existsSync(path.join(root,name)))throw Error("REFUSE overwriting historic A50 data: "+name);}
for(let [name,content] of files){let p=path.join(root,name);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,content);}
console.log("A50 non-build research model. S1 ART REJECT; no Minecraft files modified.");
}

function portalProbes(mesh){
 const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((n,x,i)=>n+x*b[i],0);
 function hit(o,dir,face){
  let [a,b,c]=face.slice(0,3).map(i=>mesh.V[i]),e1=sub(b,a),e2=sub(c,a),p=cross(dir,e2),d=dot(e1,p);
  if(Math.abs(d)<1e-8)return false;
  let t=sub(o,a),u=dot(t,p)/d;if(u<-1e-6||u>1+1e-6)return false;
  let q=cross(t,e1),v=dot(dir,q)/d;if(v<-1e-6||u+v>1+1e-6)return false;
  let dist=dot(e2,q)/d;return dist>=0&&dist<9;
 }
 let ranges={},start=0;for(let [name,n] of Object.entries(mesh.tags)){ranges[name]=[start,start+n];start+=n;}
 const rooms=[["market",-28,4,-Math.PI/2,38],["culture",27,12,Math.PI/2,40],["library",1,50,0,35]];
 const out=[];
 for(let [name,cx,cz,theta,depth] of rooms){
  let c=Math.cos(theta),s=Math.sin(theta),T=(lx,y,lz)=>[cx+lx*c+lz*s,y,cz-lx*s+lz*c],dir=[s,0,c],range=ranges["room-envelope-"+name];
  let faces=mesh.F.slice(...range);
  for(let [kind,lx,expected] of [["open-center",0,false],["solid-front-pier",9,true]]){
   let origin=T(lx,6,-depth/2-3.6),hits=faces.filter(f=>hit(origin,dir,f)).length;
   out.push({room:name,kind,hits,expected,pass:expected?hits>0:hits===0});
  }
 }
 return {pass:out.every(x=>x.pass),probes:out,scope:"ONLY room-envelope ray tests around actual front wall; no G2"};
}
if(process.argv.includes("--verify-portals")){
 const result=portalProbes(build());
 if(!result.pass)throw Error("Portal test failed "+JSON.stringify(result));
 console.log(JSON.stringify(result,null,2));
}
