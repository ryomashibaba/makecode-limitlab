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
 const V=[],F=[],tags={},holes=[];let phase="ground";
 const id=p=>(V.push(p),V.length-1);
 function quad(a,b,c,d,m){let q=[id(a),id(b),id(c),id(d)];F.push([q[0],q[1],q[2],m],[q[0],q[2],q[3],m]);tags[phase]=(tags[phase]||0)+2}
 function triangle(a,b,c,m){F.push([id(a),id(b),id(c),m]);tags[phase]=(tags[phase]||0)+1}
 function prism(poly,y0,y1,m){for(let i=1;i<poly.length-1;i++){triangle([poly[0][0],y0,poly[0][1]],[poly[i+1][0],y0,poly[i+1][1]],[poly[i][0],y0,poly[i][1]],m);triangle([poly[0][0],y1,poly[0][1]],[poly[i][0],y1,poly[i][1]],[poly[i+1][0],y1,poly[i+1][1]],m)}for(let i=0;i<poly.length;i++){let j=(i+1)%poly.length;quad([poly[i][0],y0,poly[i][1]],[poly[j][0],y0,poly[j][1]],[poly[j][0],y1,poly[j][1]],[poly[i][0],y1,poly[i][1]],m)}}
 function box(x,y,z,w,h,d,m){prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m)}
 function slab(poly,y,thick,m){prism(poly,y,y+thick,m)}
 function curve(points,width,height,m){
  for(let i=0;i<points.length-1;i++){let a=points[i],b=points[i+1],dx=b[0]-a[0],dz=b[2]-a[2],l=Math.hypot(dx,dz)||1,n=[-dz/l*width/2,dx/l*width/2];
   let v=p=>[[p[0]-n[0],p[1]-height/2,p[2]-n[1]],[p[0]+n[0],p[1]-height/2,p[2]+n[1]],[p[0]+n[0],p[1]+height/2,p[2]+n[1]],[p[0]-n[0],p[1]+height/2,p[2]-n[1]]],u=v(a),w=v(b);
   for(let j=0;j<4;j++)quad(u[j],w[j],w[(j+1)%4],u[(j+1)%4],m);
  }
 }
 const xCuts=[-65,-54,-29,-14,-10,10,22,25,50,65],yCuts=[0,2.8,13.5,15,19,21,24,29,32,35,43];
 const apertures=[
 {id:"market",x0:-54,x1:-29,y0:2.8,y1:13.5},
 {id:"culture",x0:-10,x1:10,y0:2.8,y1:15},
 {id:"library",x0:25,x1:50,y0:2.8,y1:13.5},
 {id:"residential",x0:-54,x1:-29,y0:24,y1:32},
 {id:"research",x0:-10,x1:10,y0:24,y1:32},
 {id:"commons",x0:25,x1:50,y0:24,y1:32}
 ];
 const solid=(i,j)=>{if(i<0||i>=xCuts.length-1||j<0||j>=yCuts.length-1)return false;let cx=(xCuts[i]+xCuts[i+1])/2,cy=(yCuts[j]+yCuts[j+1])/2;return !apertures.some(h=>cx>h.x0&&cx<h.x1&&cy>h.y0&&cy<h.y1)};
 phase="civic-foreground";
 slab([[-79,-56],[-35,-72],[23,-65],[74,-44],[84,26],[51,59],[-62,58]],-.65,.65,2);
 slab([[-65,-53],[-20,-55],[58,-46],[61,-18],[-64,-18]],0,.28,3);
 slab([[-60,-15],[61,-15],[61,39],[-60,39]],0,.4,2);
 phase="perforated-civic-frontage";
 // Instead of fake frames over a solid shell, material wall cells are omitted through full thickness.
 const zA=-18,zB=-12;
 for(let i=0;i<xCuts.length-1;i++)for(let j=0;j<yCuts.length-1;j++){
  if(!solid(i,j))continue;
  const a=xCuts[i],b=xCuts[i+1],c=yCuts[j],d=yCuts[j+1],m=(j>=9?0:(j>=6?0:3));
  quad([a,c,zA],[b,c,zA],[b,d,zA],[a,d,zA],m);
  quad([b,c,zB],[a,c,zB],[a,d,zB],[b,d,zB],m);
  if(!solid(i-1,j))quad([a,c,zB],[a,c,zA],[a,d,zA],[a,d,zB],1);
  if(!solid(i+1,j))quad([b,c,zA],[b,c,zB],[b,d,zB],[b,d,zA],1);
  if(!solid(i,j-1))quad([a,c,zA],[a,c,zB],[b,c,zB],[b,c,zA],i%2?4:0);
  if(!solid(i,j+1))quad([a,d,zB],[a,d,zA],[b,d,zA],[b,d,zB],0);
 }
 holes.push(...apertures);
 phase="continuous-upper-body";
 // Inhabited depth is provided by two broad, real-volume rear wings and vertical internal court.
 // Hollow frontage is visible; facade apertures are physically empty in both wall layers.
 const roofXs=Array.from({length:21},(_,i)=>-65+i*6.5);
 const zRear=37;
 const height=x=>46+6*Math.exp(-Math.pow((x+9)/25,2))+2.1*Math.sin((x+44)*.042);
 for(let i=0;i<roofXs.length-1;i++){
 let a=roofXs[i],b=roofXs[i+1],h=height(a),H=height(b);
 quad([a,h,-20],[b,H,-20],[b,H,zRear],[a,h,zRear],13);
 quad([a,h-2,-20],[a,h-2,zRear],[b,H-2,zRear],[b,H-2,-20],0);
 quad([a,h-2,-20],[b,H-2,-20],[b,H,-20],[a,h,-20],0);
 quad([a,h,zRear],[b,H,zRear],[b,H-2,zRear],[a,h-2,zRear],1);
 }
 // Rear wall and end walls are architecturally present, roof does not pretend to prove manifold topology.
 box(0,21,37,130,42,2,1);
 box(-64,21,8,2,42,58,1);box(64,21,8,2,42,58,1);
 phase="inhabited-room-depths";
 // These occupied zones are intentionally *behind* real through-openings at z=-18...-12.
 const decks=[
 {poly:[[-63,-8],[-27,-8],[-23,34],[-63,34]],y:18,m:4},
 {poly:[[-23,-8],[22,-8],[20,35],[-24,35]],y:20,m:2},
 {poly:[[23,-8],[63,-8],[63,35],[25,35]],y:18,m:4},
 {poly:[[-63,-9],[-27,-9],[-27,35],[-63,35]],y:33,m:0},
 {poly:[[-17,-9],[16,-9],[18,35],[-17,35]],y:33,m:0},
 {poly:[[23,-9],[63,-9],[63,35],[23,35]],y:33,m:0}
 ];
 for(let d of decks)slab(d.poly,d.y,1.6,d.m);
 // No huge enclosing roof at the civic observer's eye; occupy all three ground bays.
 phase="market-bay";
 for(let z of [-4,9,22])for(let x of [-49,-39,-29]){
 box(x,1.15,z,5,.45,2.3,4);box(x,2.25,z,4.2,1.05,2,8);box(x,3.2,z,4.7,.3,3,5);
 }
 for(let z of [-6,11,27]){box(-58,2.5,z,3,5.1,8,4);box(-58,5.1,z,4,.5,8,3);}
 phase="culture-workshop";
 slab([[-9,-1],[9,-1],[12,25],[-11,25]],.45,.8,12);
 for(let x of [-6,0,6])for(let z of [7,19]){box(x,1.9,z,4,1.4,2.2,8);box(x,3.0,z,3.2,.42,2,5)}
 for(let j=0;j<4;j++){box(2,.7+j*.54,27+j*2.5,16,.75,2.25,j%2?11:4)}
 // Studio's open central performance stage and overhead lighting
 box(0,8,13,17,.5,4,5);
 phase="library-bay";
 for(let x of [28,35,42,49,56])for(let z of [12,25]){
  box(x,3.5,z,5.6,6.8,1.4,10);
  for(let k=0;k<4;k++)box(x,1.0+k*1.45,z-1.1,5.2,.23,1.5,4);
 }
 for(let x of [33,47]){box(x,1.15,3,6,.27,3,4);box(x,.56,3,1,1.05,1,1)}
 phase="upper-visible-program";
 // Real occupied upper windows: bedrooms / laboratory / civic reading terrace behind 3 through-apertures.
 for(let x of [-48,-40,-32]){box(x,34.8,10,5.4,2.2,4,14);box(x,34.1,2,4,.4,2,4)}
 for(let x of [-5,2,9]){box(x,35,8,5,2.2,4,12);box(x,36.5,19,4.6,.25,3,5)}
 for(let x of [30,39,48]){box(x,34.9,20,5.8,3.1,1.5,10);box(x,34,2,5,.4,3,4)}
 // Asymmetric continuous sloped terrace landscape attached to the occupied body, not a roof shell.
 const spine=[[-63,43,-22],[-38,47,-25],[-10,52,-28],[19,49,-22],[47,46,-18],[63,44,-14]];
 curve(spine,3,2,0);
 phase="civic-identity-and-people";
 for(let [x,z] of [[-52,-36],[-32,-35],[0,-40],[29,-33],[49,-34]]){
   box(x,.55,z,4,1.1,3,3);box(x,1.55,z,2.5,.7,2,9);
 }
 const people=[[-44,-3,0],[-39,3,0],[-6,8,0],[3,-3,0],[39,4,0],[50,10,0],[-43,8,33],[5,12,33],[39,9,33]];
 for(let [x,z,y] of people){box(x,y+.69,z,.48,1.24,.42,15);box(x,y+1.55,z,.53,.46,.5,8);}
 return{V,F,tags,M,apertures:holes,scope:"A46 S1 art only, ground-floor portals genuinely removed from facade wall; not structural or walking certification."};
}
function apertureTest(mesh){
 // Independent positive/negative ray test for the facade material at z=-18 and -12;
 // only considers local exterior shell face coordinates, NOT full G2 walking or topology.
 function intersectTri(origin,face){
  const a=mesh.V[face[0]],b=mesh.V[face[1]],c=mesh.V[face[2]];
  const ab=b.map((n,i)=>n-a[i]),ac=c.map((n,i)=>n-a[i]),dir=[0,0,1];
  const p=[-ac[1],ac[0],0],det=ab[0]*p[0]+ab[1]*p[1];if(Math.abs(det)<1e-10)return null;
  const inv=1/det,tv=origin.map((n,i)=>n-a[i]);const u=(tv[0]*p[0]+tv[1]*p[1])*inv;if(u<0||u>1)return null;
  const q=[tv[1]*ab[2]-tv[2]*ab[1],tv[2]*ab[0]-tv[0]*ab[2],tv[0]*ab[1]-tv[1]*ab[0]];
  const v=q[2]*inv;if(v<0||u+v>1)return null;const t=(ac[0]*q[0]+ac[1]*q[1]+ac[2]*q[2])*inv;
  return t>=0?t:null;
 }
 const probes=[
 {name:"market",x:-41,y:8,expect:"open"},{name:"culture",x:0,y:8,expect:"open"},{name:"library",x:38,y:8,expect:"open"},
 {name:"residential",x:-42,y:27,expect:"open"},{name:"research",x:0,y:27,expect:"open"},{name:"commons",x:36,y:27,expect:"open"},
 {name:"solid_wall_negative",x:-20,y:8,expect:"blocked"},{name:"solid_pier_negative",x:18,y:27,expect:"blocked"}
 ];
 const zstart=-24,zEnd=-9;let verdict=[];
 for(let p of probes){
  let hits=0;for(let f of mesh.F){let t=intersectTri([p.x,p.y,zstart],f);if(t!==null&&zstart+t<zEnd&&zstart+t>=zstart)hits++}
  verdict.push({...p,hits,pass:p.expect==="open"?hits===0:hits>0});
 }
 return {probes:verdict,pass:verdict.every(p=>p.pass)};
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
main_arrival:[[0,2.3,-62],[0,11,8],"perspective",0],
market_entry:[[-39,2.3,-49],[-39,9,14],"perspective",0],
culture_entry:[[0,2.3,-49],[0,10,13],"perspective",0],
library_entry:[[40,2.3,-50],[40,9,16],"perspective",0],
front:[[0,88,-178],[0,25,8],"ortho",2.08],
oblique:[[147,103,-138],[0,25,8],"ortho",2.10],
side:[[168,96,5],[0,25,8],"ortho",2.10],
aerial:[[128,172,-102],[0,25,6],"ortho",2.10]
};return Object.fromEntries(Object.entries(cameras).map(([n,c])=>[n,render(mesh,...c)]));
}
({M,build,apertureTest,b64,obj,mtl,glb,render,renderViews});
import fs from "node:fs";
import path from "node:path";
if(process.argv.includes("--write")){
 const root="artifacts/g4c7-a46-open-frontage-s1";
 const mesh=build(),qa=apertureTest(mesh);
 if(!qa.pass)throw Error("A46 positive/negative facade aperture ray probes FAILED; no assets written");
 const assets=[
  ["a46_open_frontage.obj",obj(mesh)],
  ["a46_open_frontage.glb",Buffer.from(glb(mesh).data)],
  ["materials.mtl",mtl()],
  ...Object.entries(renderViews(mesh)).map(([name,r])=>["verified-png/"+name+".png",Buffer.from(r.data)])
 ];
 // Refuse to overwrite even this same stage's saved originals on rerun.
 for(const [n] of assets){if(fs.existsSync(path.join(root,n)))throw Error("Refusing to overwrite prior evidence: "+n)}
 for(const [n,data] of assets){const file=path.join(root,n);fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,data)}
 console.log("A46 geometry and depth PNG saved; art status remains ART REJECT / ART HOLD; Minecraft untouched.");
}
