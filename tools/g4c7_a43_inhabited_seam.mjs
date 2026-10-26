// MakeCode LimitLab / G4-C7 A43 "INHABITED SEAM" pure geometry and depth renderer.
// ART HOLD: exploratory S1 section, not city, no world or Minecraft operations.
// Run in Node as an import via tools/g4c7_a43_inhabited_seam.mjs; see A43 audit for execution.
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
 const id=p=>(V.push(p),V.length-1);
 function q(a,b,c,d,m){const j=[id(a),id(b),id(c),id(d)];F.push([j[0],j[1],j[2],m],[j[0],j[2],j[3],m]);tags[tag]=(tags[tag]||0)+2}
 function box(x,y,z,w,h,d,m){const a=x-w/2,b=x+w/2,c=y-h/2,e=y+h/2,f=z-d/2,g=z+d/2;
 q([a,c,f],[b,c,f],[b,e,f],[a,e,f],m);q([b,c,g],[a,c,g],[a,e,g],[b,e,g],m);
 q([a,c,g],[a,c,f],[a,e,f],[a,e,g],m);q([b,c,f],[b,c,g],[b,e,g],[b,e,f],m);
 q([a,e,f],[b,e,f],[b,e,g],[a,e,g],m);q([a,c,g],[b,c,g],[b,c,f],[a,c,f],m)}
 function beam(a,b,w,h,m){let dx=b[0]-a[0],dz=b[2]-a[2],L=Math.hypot(dx,dz)||1,s=[-dz/L*w/2,dx/L*w/2];
 const rim=p=>[[p[0]-s[0],p[1]-h/2,p[2]-s[1]],[p[0]+s[0],p[1]-h/2,p[2]+s[1]],[p[0]+s[0],p[1]+h/2,p[2]+s[1]],[p[0]-s[0],p[1]+h/2,p[2]-s[1]]];
 const u=rim(a),v=rim(b);for(let i=0;i<4;i++)q(u[i],v[i],v[(i+1)%4],u[(i+1)%4],m);
 q(u[3],u[2],u[1],u[0],m);q(v[0],v[1],v[2],v[3],m)}
 function line(p,w,h,m){for(let i=0;i<p.length-1;i++)beam(p[i],p[i+1],w,h,m)}
 function person(x,y,z){box(x,y+.65,z,.43,1.16,.4,15);box(x,y+1.48,z,.5,.47,.47,8)}
 function tabletop(x,y,z,m){box(x,y+.95,z,3.8,.3,1.9,m);box(x-1.45,y+.47,z,.25,.9,.35,1);box(x+1.45,y+.47,z,.25,.9,.35,1)}
 function framesX(x,z,y,span,height,m){for(let i=0;i<=3;i++)box(x-span/2+i*span/3,y+height/2,z,1.5,height,1.4,m);
 box(x,y+.6,z,span,1.2,1.4,m);box(x,y+height-.75,z,span,1.5,1.4,m)}
 function framesZ(x,z,y,span,height,m){for(let i=0;i<=3;i++)box(x,y+height/2,z-span/2+i*span/3,1.4,height,1.5,m);
 box(x,y+.6,z,1.4,1.2,span,m);box(x,y+height-.75,z,1.4,1.5,span,m)}
 tag="street-to-interior";
 box(-1,-.7,-18,96,1.4,117,2);
 box(-2,.06,-39,12,.15,25,4);box(-1,.12,-14,15,.24,30,2);box(4,.15,18,16,.3,46,4);
 for(let [x,z] of [[-41,-28],[38,-24],[-41,40],[38,35]]){box(x,.52,z,4,1.05,6,3);box(x,1.3,z,3,.5,3.5,9)}
 tag="one-deep-urban-body";
 // Three spatially overlapping and visibly interlocked inhabited layers;
 // these are NOT standalone pavilions on a square.
 box(-34,2,4,27,4,71,0);box(30,3,6,28,6,70,0);
 box(-28,13.5,22,32,3.8,58,3);box(27,18.2,21,34,4.2,63,0);
 box(-22,26,30,35,3.6,46,0);box(19,32,38,41,4.5,42,13);
 box(0,5,56,43,8,19,3);
 box(1,16,60,46,1.7,24,0);
 tag="market-with-depth";
 for(let z of [-24,-8,9,25]) {
   box(-34,4.3,z,24,1.5,11,8);
   for(let x of [-42,-32,-22]) {tabletop(x,4.1,z,4);box(x,5.9,z,4.6,.5,3,5);}
   box(-34,9.7,z,24,.9,12,4);
 }
 for(let z of [-27,-11,5,21,37])box(-19,9.8,z,1.6,19,1.8,1);
 framesZ(-19,4,0,54,11,1);
 tag="makers-culture-with-depth";
 for(let z of [-20,0,22]){
 box(30,6.8,z,22,1.3,13,12);
 box(32,8.1,z,10,1.7,7,4);
 for(let x of [26,37])box(x,10.0,z,2.5,2.2,3,5);
 box(18,9.3,z,2.7,5,12,11);
 }
 framesZ(16,8,0,60,17,1);
 for(let z of [-21,0,21]){box(39,12,z,3,15,9,6);box(36,14,z,5,.75,6,5);}
 tag="library-terrace-visible";
 box(-10,16,48,40,1.8,26,4);
 framesX(-10,38,16,39,12,1);
 for(let x of [-27,-19,-11,-3,5])for(let k=0;k<3;k++){
 box(x,18.7+k*3,64,6.2,2.7,1.7,10);
 for(let j=0;j<4;j++)box(x-2.2+j*1.4,18.8+k*3,62.8,.64,2.2,.8,j%2?11:12);
 }
 for(let x of [-19,-5,8]){tabletop(x,17,47,4);person(x+3,17,47)}
 box(-10,29,57,42,2.8,23,13);
 tag="residential-depth-not-plate-stack";
 for(let [x,y,z,w,d] of [[-33,17,-6,25,17],[-26,29,19,31,20],[29,23,-1,28,19],[19,35,32,35,20]]){
 box(x,y,z,w,2,d,0);
 box(x,y+5,z+d*.25,w,9,d*.5,13);
 framesX(x,z-d*.47,y+1,w-3,8,1);
 for(let dx of [-w*.28,0,w*.28]){
 box(x+dx,y+.7,z-d*.49,w*.24,1.1,3.5,14);
 box(x+dx,y+1.55,z-d*.47,w*.22,.65,2.9,9);
 box(x+dx,y+4.3,z-d*.45,w*.22,2.3,.6,8);
 }
 }
 tag="diagonal-public-continuity";
 line([[-5,.8,-34],[-4,1.1,-11],[1,4.5,9],[8,10,27],[10,15,44]],9,1.5,4);
 for(let [x,y,z] of [[-5,2,-16],[1,5,10],[8,11,29]]){
 box(x,y-.4,z,11,1.2,7,2);box(x+5.3,y+.3,z,1.1,2.5,6,5)
 }
 tag="folded-tectonic-silhouette";
 line([[-46,12,-22],[-34,26,-3],[-6,35,22],[26,41,48],[42,25,58]],6.4,6,0);
 line([[-39,13,42],[-24,25,45],[9,37,48],[38,27,45]],5.3,4.5,3);
 line([[-43,13,2],[-30,19,10],[-12,28,32],[8,33,44]],3.2,3,13);
 // Individual pavilions have vanished but this rib must be ART-judged, not assumed beautiful.
 tag="public-inhabitants";
 for(let [x,y,z] of [[-8,0,-28],[5,0,-18],[2,0,2],[-8,0,20],[10,1,30],[-18,4,8],[17,6,8],[28,6,25],[-11,16,42]])person(x,y,z);
 for(let [x,z] of [[-14,-32],[10,3],[9,23],[-4,42]]){box(x,.5,z,3.7,1,3.7,3);box(x,2.5,z,1.2,3,1.2,1);box(x,5.4,z,4,2.7,4,9)}
 return {V,F,tags,M,anchors:{arrival:[-5,2,-35],civic:[1,4,9],market:[-20,5,3],maker:[16,7,9],library:[-10,18,45],housing:[-26,30,19]},scope:"S1 only / ART HOLD"};
}
function b64(bytes){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";let r="";for(let i=0;i<bytes.length;i+=3){const a=bytes[i],b=bytes[i+1]||0,c=bytes[i+2]||0;r+=abc[a>>2]+abc[((a&3)<<4)|(b>>4)]+(i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=")+(i+2<bytes.length?abc[c&63]:"=")}return r}
function obj(mesh){let s="# G4C7 A43 real mesh - ART HOLD - no construction\nmtllib materials.mtl\n",old=-1;for(let p of mesh.V)s+="v "+p.join(" ")+"\n";for(let f of mesh.F){if(f[3]!==old){old=f[3];s+="usemtl "+M[old][0]+"\n"}s+="f "+(f[0]+1)+" "+(f[1]+1)+" "+(f[2]+1)+"\n"}return s}
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
const root={asset:{version:"2.0",generator:"MakeCode LimitLab G4C7 A43 nonbuild art study"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:prim}],materials:M.map(([name,c])=>({name,pbrMetallicRoughness:{baseColorFactor:[...c.map(x=>x/255),1],metallicFactor:.04,roughnessFactor:.83},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bv,accessors:ac};
let json=Array.from(JSON.stringify(root)).map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
const out=new Uint8Array(28+json.length+bin.length),v=new DataView(out.buffer);v.setUint32(0,0x46546c67,true);v.setUint32(4,2,true);v.setUint32(8,out.length,true);v.setUint32(12,json.length,true);v.setUint32(16,0x4e4f534a,true);out.set(json,20);const off=20+json.length;v.setUint32(off,bin.length,true);v.setUint32(off+4,0x004e4942,true);out.set(bin,off+8);return{data:out,json:root};
}
function render(mesh,eye,target,mode="ortho",scale=3.3,W=560,H=420){
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((n,x,i)=>n+x*b[i],0),norm=a=>{let n=Math.hypot(...a)||1;return a.map(x=>x/n)};
const fw=norm(sub(target,eye)),right=norm(cross([0,1,0],fw)),up=norm(cross(fw,right)),L=norm([-.3,.9,-.35]);
const P=mesh.V.map(p=>{let re=sub(p,eye),t=sub(p,target),z=dot(re,fw);return [W/2+(mode==="perspective"?305*dot(re,right)/Math.max(z,1):scale*dot(t,right)),H/2-(mode==="perspective"?305*dot(re,up)/Math.max(z,1):scale*dot(t,up)),z]});
const pix=new Uint8Array(W*H),Z=new Float32Array(W*H);Z.fill(Infinity);let ignored=0;
for(let f of mesh.F){const a=P[f[0]],b=P[f[1]],c=P[f[2]];if(a[2]<2||b[2]<2||c[2]<2){ignored++;continue}
const area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);if(Math.abs(area)<1e-8)continue;
const n=norm(cross(sub(mesh.V[f[1]],mesh.V[f[0]]),sub(mesh.V[f[2]],mesh.V[f[0]])));
const shade=Math.max(0,Math.min(7,Math.round(2+5*Math.max(0,dot(n,L)))));
const x0=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0]))),x1=Math.min(W-1,Math.ceil(Math.max(a[0],b[0],c[0]))),y0=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),y1=Math.min(H-1,Math.ceil(Math.max(a[1],b[1],c[1])));
for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){const X=x+.5,Y=y+.5;let w1=((X-a[0])*(c[1]-a[1])-(Y-a[1])*(c[0]-a[0]))/area,w2=((b[0]-a[0])*(Y-a[1])-(b[1]-a[1])*(X-a[0]))/area,w0=1-w1-w2;if(w0<-.00001||w1<-.00001||w2<-.00001)continue;const z=w0*a[2]+w1*b[2]+w2*c[2],i=y*W+x;if(z<Z[i]){Z[i]=z;pix[i]=1+f[3]*8+shade}}}
const pal=[[25,42,55],...M.flatMap(([name,col])=>Array.from({length:8},(_,k)=>col.map(x=>Math.min(255,Math.round(x*(.40+k*.084))))))];
const u32=n=>[(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255],crct=Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0});
const crc=a=>{let c=0xffffffff;for(let x of a)c=crct[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0};
function chunk(k,a){let h=Array.from(k).map(x=>x.charCodeAt(0));return[...u32(a.length),...h,...a,...u32(crc([...h,...a]))]}
let raw=[];for(let y=0;y<H;y++){raw.push(0);for(let x=0;x<W;x++)raw.push(pix[y*W+x])}
let a=1,b=0;for(let x of raw){a=(a+x)%65521;b=(b+a)%65521}
const def=[0x78,1];for(let j=0;j<raw.length;){let len=Math.min(65535,raw.length-j);def.push(j+len===raw.length?1:0,len&255,(len>>8)&255,(~len)&255,((~len)>>8)&255,...raw.slice(j,j+len));j+=len}def.push(...u32(((b<<16)|a)>>>0));
return{data:new Uint8Array([137,80,78,71,13,10,26,10,...chunk("IHDR",[...u32(W),...u32(H),8,3,0,0,0]),...chunk("PLTE",pal.flat()),...chunk("IDAT",def),...chunk("IEND",[])]),covered:pix.reduce((n,x)=>n+(x!==0),0),excluded:ignored};
}
function renderViews(mesh){
const cameras={arrival:[[0,3,-58],[0,12,22],"perspective",0],inner:[[-1,4,-8],[1,16,34],"perspective",0],market:[[-6,3,-19],[-30,8,2],"perspective",0],library:[[6,18,14],[-11,22,54],"perspective",0],front:[[0,93,-157],[0,19,15],"ortho",3.0],oblique:[[131,94,-125],[0,20,15],"ortho",3.05],side:[[176,92,9],[0,20,15],"ortho",3.05],aerial:[[126,180,-100],[0,18,13],"ortho",3.05]};
return Object.fromEntries(Object.entries(cameras).map(([n,c])=>[n,render(mesh,...c)]));
}
({M,build,b64,obj,mtl,glb,render,renderViews});
import fs from "node:fs";
import path from "node:path";
if(process.argv.includes("--write")){
 const root="artifacts/g4c7-a43-inhabited-seam";
 const save=(n,data)=>{let p=path.join(root,n);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,data);};
 const mesh=build();
 save("a43_inhabited_seam.obj",obj(mesh));
 save("a43_inhabited_seam.glb",Buffer.from(glb(mesh).data));
 save("materials.mtl",mtl());
 for(const [k,x] of Object.entries(renderViews(mesh)))save("verified-png/"+k+".png",Buffer.from(x.data));
 console.log("A43 real mesh + 8 Z-buffer PNG saved; S1 REJECT; no Minecraft operations");
}
