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
const V=[],F=[],sections={},anchors={};let part="site";
const put=p=>(V.push(p),V.length-1);
const tri=(a,b,c,m)=>{F.push([put(a),put(b),put(c),m]);sections[part]=(sections[part]||0)+1;};
const q=(a,b,c,d,m)=>{const v=[put(a),put(b),put(c),put(d)];F.push([v[0],v[1],v[2],m],[v[0],v[2],v[3],m]);sections[part]=(sections[part]||0)+2;};
const prism=(p,y0,y1,m)=>{for(let i=1;i<p.length-1;i++){tri([p[0][0],y0,p[0][1]],[p[i+1][0],y0,p[i+1][1]],[p[i][0],y0,p[i][1]],m);tri([p[0][0],y1,p[0][1]],[p[i][0],y1,p[i][1]],[p[i+1][0],y1,p[i+1][1]],m)}for(let i=0;i<p.length;i++){let k=(i+1)%p.length;q([p[i][0],y0,p[i][1]],[p[k][0],y0,p[k][1]],[p[k][0],y1,p[k][1]],[p[i][0],y1,p[i][1]],m);}};
const box=(x,y,z,w,h,d,m)=>prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m);
const slab=(p,y,h,m)=>prism(p,y,y+h,m);
const fillquad=(a,b,c,d,m)=>q(a,b,c,d,m);
const beam=(pts,w,h,m)=>{for(let i=0;i<pts.length-1;i++){let a=pts[i],b=pts[i+1],dx=b[0]-a[0],dz=b[2]-a[2],len=Math.hypot(dx,dz)||1,n=[-dz/len*w/2,dx/len*w/2];const v=p=>[[p[0]+n[0],p[1]+h/2,p[2]+n[1]],[p[0]-n[0],p[1]+h/2,p[2]-n[1]],[p[0]-n[0],p[1]-h/2,p[2]-n[1]],[p[0]+n[0],p[1]-h/2,p[2]+n[1]]];let u=v(a),z=v(b);for(let j=0;j<4;j++)q(u[j],z[j],z[(j+1)%4],u[(j+1)%4],m)}};
function person(x,y,z){box(x,y+.75,z,.44,1.31,.44,15);box(x,y+1.68,z,.45,.47,.47,8)}
part="urban-site";
slab([[-88,-69],[-46,-83],[8,-85],[70,-68],[85,-16],[78,62],[23,85],[-60,68],[-88,19]],-.7,.7,2);
slab([[-17,-74],[10,-74],[12,-21],[20,-6],[18,70],[-4,74],[-15,13]],0,.46,4);
anchors.south=[0,2,-63];
part="one-thick-braided-urban-body";
// A continuous inhabitated body follows a kinked urban seam across the public ground.
// Each segment has real depth; a true through-gate breaks the facade across TWO faces.
const spine=[[-73,-12,28],[-52,5,35],[-24,21,42],[3,30,53],[31,24,47],[66,10,31]];
const thicks=[20,25,29,34,29,24];
const A=[],B=[];
for(let i=0;i<spine.length;i++){let p=spine[i];let left=spine[Math.max(0,i-1)],right=spine[Math.min(i+1,spine.length-1)],dx=right[0]-left[0],dz=right[1]-left[1],len=Math.hypot(dx,dz)||1;let nx= -dz/len,nz=dx/len,half=thicks[i]/2;
 A.push([p[0]-nx*half,p[1]-nz*half,p[2]]);
 B.push([p[0]+nx*half,p[1]+nz*half,p[2]]);
}
const h0=[28,35,42,53,47,31],hLo=[0,1,0,0,0,0];
for(let i=0;i<A.length-1;i++){
 let a=A[i],b=A[i+1],c=B[i],d=B[i+1];
 // roof is a sequence of sloping facets and exposed thick parapets, NOT a flat enclosing mega roof.
 q([a[0],h0[i],a[1]],[b[0],h0[i+1],b[1]],[d[0],h0[i+1],d[1]],[c[0],h0[i],c[1]],i===2?13:0);
 q([a[0],h0[i]-4,a[1]],[c[0],h0[i]-4,c[1]],[d[0],h0[i+1]-4,d[1]],[b[0],h0[i+1]-4,b[1]],7);
 // side walls have openings in lower layer: segment 2 is actual public passage through depth
 function wall(p,z,front){
   const yTop=h0[i],yTop2=h0[i+1],u=[p[0],0,p[1]],v=[z[0],0,z[1]],uT=[p[0],yTop,p[1]],vT=[z[0],yTop2,z[1]],gate=(i===2);
   if(gate){let left=[p[0]*.67+z[0]*.33,0,p[1]*.67+z[1]*.33],right=[p[0]*.34+z[0]*.66,0,p[1]*.34+z[1]*.66];
    q(u,left,[left[0],17,left[2]],[p[0],17,p[1]],1);
    q(right,v,[z[0],17,z[1]],[right[0],17,right[2]],1);
    q([p[0],17,p[1]],[z[0],17,z[1]],vT,uT,front?0:3);
    // actual no face in centre range (both front and rear)
   } else {
    q(u,v,vT,uT,front?3:1);
   }
 }
 wall(a,b,true);wall(c,d,false);
 // end walls for gate: wall thickness into section, + overhead soffit
 if(i===2){let gateL=[a[0]*.67+b[0]*.33,a[1]*.67+b[1]*.33],gateR=[a[0]*.34+b[0]*.66,a[1]*.34+b[1]*.66];
 let gateLC=[c[0]*.67+d[0]*.33,c[1]*.67+d[1]*.33],gateRC=[c[0]*.34+d[0]*.66,c[1]*.34+d[1]*.66];
 q([gateL[0],0,gateL[1]],[gateLC[0],0,gateLC[1]],[gateLC[0],17,gateLC[1]],[gateL[0],17,gateL[1]],0);
 q([gateRC[0],0,gateRC[1]],[gateR[0],0,gateR[1]],[gateR[0],17,gateR[1]],[gateRC[0],17,gateRC[1]],0);
 q([gateL[0],17,gateL[1]],[gateR[0],17,gateR[1]],[gateRC[0],17,gateRC[1]],[gateLC[0],17,gateLC[1]],0);
 }
}
anchors.portal=[-10,2,25];
part="civic-occupied-terraces-and-deep-recesses";
// Deep programmed terraces fold inward at unequal heights, clearly made as spatial volumes not floorplate stack.
const terraces=[
 {poly:[[-76,-34],[-43,-22],[-24,3],[-44,16],[-69,-4]],y:8,m:4,kind:"market"},
 {poly:[[-57,15],[-22,5],[-2,38],[-32,42]],y:20,m:12,kind:"culture"},
 {poly:[[6,8],[43,-6],[66,24],[28,39],[8,32]],y:12,m:5,kind:"reading"},
 {poly:[[-54,13],[-20,17],[-7,42],[-38,44]],y:29,m:14,kind:"residential"},
 {poly:[[4,26],[30,9],[52,30],[37,52],[8,44]],y:35,m:6,kind:"research"}
];
for(const t of terraces){slab(t.poly,t.y,1.6,t.m);}
part="street-that-enters-occupied-section";
// A public route enters the main arch and winds toward nonparallel program branches.
// Note: represented as study geometry, not walking-proven.
beam([[0,.7,-70],[-4,.9,-41],[-10,1.2,-11],[-9,2,16],[-2,2.8,36],[12,3.2,54]],11,.8,4);
beam([[-9,1,17],[-32,2,17],[-50,2,2]],8,.7,4);
beam([[-9,1,17],[15,2,17],[41,2,9]],8,.7,4);
part="active-market-life";
for(let [x,z] of [[-56,-26],[-47,-18],[-42,-7],[-56,2],[-31,-8]]){
  box(x,1.1,z,6,.65,3.3,4);box(x,2,z,5.8,1.3,2.8,8);box(x,3.05,z,6,.34,3.2,5);
}
part="visible-culture";
for(let [x,z] of [[-44,20],[-36,25],[-27,29]]){
  box(x,20.8,z,6,.6,3.2,11);box(x,22.1,z,3.2,1.2,2.5,4);
}
beam([[-38,24,32],[-23,30,37],[-4,32,41]],2.5,1.5,5);
part="reading-with-deep-room";
for(let x of [18,26,34,42])for(let z of [10,18,26]){
  box(x,13.4,z,5.7,5.7,1.3,10);box(x,12.3,z,5.3,.3,1.8,4);
}
for(let [x,z] of [[18,3],[32,-2],[49,9]]){box(x,13.9,z,5,.4,3.3,4);box(x,13.1,z,1,1.6,1,1);}
part="residential-and-research-activity";
for(let x of [-38,-28,-18]){
  box(x,30.9,28,6,1.3,3,14);box(x,32,28,5,.4,2,9);
}
for(let x of [15,25,35,44]){box(x,36.7,38,6,1.3,3.2,12);box(x,37.5,38,5,.25,2.5,5)}
part="silhouette-articulation";
beam([[-73,30,-10],[-50,43,6],[-20,52,25],[7,61,30],[32,55,22],[66,33,9]],4,4,0);
// Ground-based oblique visible inhabited fins (not ornamental repeated high-rise boxes).
beam([[-54,0,-31],[-43,19,-19],[-22,42,7]],3,4,0);
beam([[58,1,-14],[49,21,3],[32,47,24]],3.5,4.5,0);
part="human-scale";
for(let [x,z,y] of [[0,-56,0],[-8,-18,0],[-7,10,0],[-34,-8,0],[-48,-13,0],[25,13,12],[36,9,12],[-32,28,20]])person(x,y,z);
return {V,F,tags:sections,M,anchors,scope:"A47 G0-selected one-scene S1 aesthetic scout, not a whole city, no G2/G3 claim."};
}
function b64(bytes){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";let r="";for(let i=0;i<bytes.length;i+=3){const a=bytes[i],b=bytes[i+1]||0,c=bytes[i+2]||0;r+=abc[a>>2]+abc[((a&3)<<4)|(b>>4)]+(i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=")+(i+2<bytes.length?abc[c&63]:"=")}return r}
function obj(mesh){let s="# G4C7 A47 real mesh - ART HOLD - no construction\nmtllib materials.mtl\n",old=-1;for(let p of mesh.V)s+="v "+p.join(" ")+"\n";for(let f of mesh.F){if(f[3]!==old){old=f[3];s+="usemtl "+M[old][0]+"\n"}s+="f "+(f[0]+1)+" "+(f[1]+1)+" "+(f[2]+1)+"\n"}return s}
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
const root={asset:{version:"2.0",generator:"MakeCode LimitLab G4C7 A47 nonbuild art study"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prim}],materials:M.map(([name,c])=>({name,pbrMetallicRoughness:{baseColorFactor:[...c.map(x=>x/255),1],metallicFactor:.04,roughnessFactor:.83},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bv,accessors:ac};
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
function renderViews(mesh){const camera={
arrival:[[0,2.3,-79],[-9,15,20],"perspective",0],
public_portal:[[-8,3,-21],[-7,15,25],"perspective",0],
market_inhabited:[[-24,4,-29],[-45,13,-3],"perspective",0],
reading_destination:[[0,11,-18],[31,20,12],"perspective",0],
front:[[0,111,-185],[0,26,0],"ortho",2.2],
oblique:[[160,115,-152],[0,27,4],"ortho",2.2],
side:[[197,110,0],[0,27,4],"ortho",2.2],
aerial:[[149,196,-115],[0,27,4],"ortho",2.2]
};return Object.fromEntries(Object.entries(camera).map(([k,a])=>[k,render(mesh,...a)]));}
({M,build,b64,obj,mtl,glb,render,renderViews});
import fs from "node:fs";
import path from "node:path";
if(process.argv.includes("--write")){
  const root="artifacts/g4c7-a47-braided-civic-threshold-s1";
  const m=build();
  const images=renderViews(m);
  const targets=[["a47_braided_civic_threshold.obj",obj(m)],["a47_braided_civic_threshold.glb",Buffer.from(glb(m).data)],["materials.mtl",mtl()],...Object.entries(images).map(([n,v])=>["verified-png/"+n+".png",Buffer.from(v.data)])];
  for(const [name] of targets){if(fs.existsSync(path.join(root,name)))throw Error("A47 evidence exists — will not overwrite: "+name);}
  for(const [name,contents] of targets){const file=path.join(root,name);fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,contents);}
  console.log("A47 S1 study saved; artistic result REJECT, Minecraft construction forbidden.");
}
