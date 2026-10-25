#!/usr/bin/env node
// A37 OBJ independent depth-tested indexed-PNG raster, never invokes Minecraft.
import fs from "node:fs";import path from "node:path";
const renderA37=function renderA37(A36Obj,A37Obj){
const base="artifacts/g4c7-a37-inhabited-open-section/verified-png/",W=600,H=392,ratio=W/1500;
const M={limestone:"#d9e7eb",garden:"#7db89c",deep:"#3e5a70",inhabited:"#5fbfc6",civic:"#e7bb8b",upper:"#b4c6ca",pale_structural:"#d9e9ed",deep_shadow:"#3e5a70",public_green:"#7db89c",civic_sandstone:"#e7bb8b",inhabited_glass:"#5fbfc6",north_library:"#b4c6ca"};
const HEX=[...new Set(Object.values(M))],colorBy={};HEX.forEach((x,k)=>colorBy[x]=k);
const PALETTE=[35,57,76];for(let c of HEX)for(let s=0;s<8;s++){let scale=.55+s*.10;for(let k of [1,3,5])PALETTE.push(Math.min(255,Math.round(parseInt(c.slice(k,k+2),16)*scale)));}
function readOBJ(src){let vertices=[],faces=[],mtl="limestone";for(let ln of src.split("\n")){if(ln.startsWith("v "))vertices.push(ln.trim().split(/\s+/).slice(1,4).map(Number));else if(ln.startsWith("usemtl "))mtl=ln.slice(7).trim();else if(ln.startsWith("f ")){let f=ln.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(f.length===3)faces.push({f,mat:colorBy[M[mtl]]??0});}}return{vertices,faces};}
const S=[readOBJ(A36Obj),readOBJ(A37Obj)],cam={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]};
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
const T=new Uint32Array(256);for(let i=0;i<256;i++){let q=i;for(let j=0;j<8;j++)q=q&1?0xedb88320^(q>>>1):q>>>1;T[i]=q>>>0;}
const be=x=>[(x>>>24)&255,(x>>>16)&255,(x>>>8)&255,x&255],crc=arr=>{let c=0xffffffff;for(let x of arr)c=T[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0},chunk=(s,body)=>{let a=[...s].map(c=>c.charCodeAt(0)).concat(body);return[...be(body.length),...a,...be(crc(a))];};
function b64(bytes){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<bytes.length;i+=3){let a=bytes[i],b=bytes[i+1]??0,c=bytes[i+2]??0;out.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<bytes.length?abc[c&63]:"=");}return out.join("");}
function PNG(pixels){let scan=new Uint8Array(H*(W+1));for(let y=0;y<H;y++)scan.set(pixels.subarray(y*W,(y+1)*W),y*(W+1)+1);
let zip=[120,1],a=1,b=0;for(let x of scan){a=(a+x)%65521;b=(b+a)%65521;}for(let i=0;i<scan.length;i+=65535){let n=Math.min(65535,scan.length-i);zip.push(i+n===scan.length?1:0,n&255,n>>8,(~n)&255,((~n)>>8)&255);for(let j=i;j<i+n;j++)zip.push(scan[j]);}zip.push(b>>8,b&255,a>>8,a&255);
let PNG=[137,80,78,71,13,10,26,10,...chunk("IHDR",[...be(W),...be(H),8,3,0,0,0]),...chunk("PLTE",PALETTE),...chunk("IDAT",zip),...chunk("IEND",[])];return{b64:b64(PNG),bytes:PNG.length};}
function render(name,eyes,lookAt,perspective=false,which=[0,1]){
const px=new Uint8Array(W*H),zbuffer=new Float32Array(W*H);zbuffer.fill(Infinity);
let drawn=0,triangles=0,skipped=0;
for(let pane=0;pane<which.length;pane++){
 const current=which[pane],mod=S[current],eye=eyes,forward=unit(sub(lookAt,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right));
 const cx=which.length===1?W*.5:(pane?W*.75:W*.25),cy=H*.49,projections=mod.vertices.map(v=>{
 let diff=sub(v,perspective?eye:lookAt),dp=pane===-1?0:dot(sub(v,eye),forward);let fac=perspective?(dp>1?320/dp:1e7):1.03*ratio;
 return [cx+dot(diff,right)*fac,cy-dot(diff,up)*fac,dp];});
 for(let f of mod.faces){
  let a=mod.vertices[f.f[0]],b=mod.vertices[f.f[1]],c=mod.vertices[f.f[2]],mid=a.map((x,i)=>(x+b[i]+c[i])/3),N=cross(sub(b,a),sub(c,a)),nlen=Math.hypot(...N);
  if(nlen===0)continue;
  if(dot(N,sub(eye,mid))<=0){skipped++;continue;}
  let [A,B,C]=f.f.map(i=>projections[i]);if(perspective&&[A,B,C].some(x=>x[2]<4))continue;
  const x1=A[0],y1=A[1],x2=B[0],y2=B[1],x3=C[0],y3=C[1],den=(y2-y3)*(x1-x3)+(x3-x2)*(y1-y3);
  if(Math.abs(den)<1e-4)continue;
  let xmin=Math.max(which.length===2?(pane?W/2:0):0,Math.floor(Math.min(x1,x2,x3))),xmax=Math.min(which.length===2?(pane?W:W/2):W,Math.ceil(Math.max(x1,x2,x3))),ymin=Math.max(0,Math.floor(Math.min(y1,y2,y3))),ymax=Math.min(H,Math.ceil(Math.max(y1,y2,y3)));
  let nl=N.map(v=>v/nlen),shade=Math.max(0,Math.min(7,Math.round((.72+.40*dot(nl,unit([-.45,.82,-.34]))-.55)*10)));
  let color=1+f.mat*8+shade;triangles++;
  for(let y=ymin;y<ymax;y++)for(let x=xmin;x<xmax;x++){
    let u=((y2-y3)*(x+.5-x3)+(x3-x2)*(y+.5-y3))/den,v=((y3-y1)*(x+.5-x3)+(x1-x3)*(y+.5-y3))/den,w=1-u-v;
    if(u<0||v<0||w<0)continue;let depth=u*A[2]+v*B[2]+w*C[2],at=y*W+x;
    if(depth<zbuffer[at]){zbuffer[at]=depth;px[at]=color;drawn++;}}
 }
}
return{image:PNG(px),coverage:px.filter(x=>x!==0).length/(W*H),drawn,triangles,skipped};
}
const files=[],summary={renderer:"independent OBJ-based software depth-tested RGB-palette PNG; no oversized SVG parse",size:[W,H],views:{}};
for(let [name,camera] of Object.entries(cam)){let out=render(name,camera,[0,78,0]);files.push({path:base+name+"_a36_vs_a37.png",content:out.image.b64,encoding:"base64"});summary.views[name]={coverage:out.coverage,triangles:out.triangles,bytes:out.image.bytes};}
for(let [name,eye,target] of [["south",[0,45,-155],[0,118,148]],["west",[-105,55,-80],[-10,91,32]],["north",[0,112,146],[12,139,184]]]){
 let out=render(name,eye,target,true,[1]);files.push({path:base+"interior_"+name+".png",content:out.image.b64,encoding:"base64"});summary.views["interior_"+name]={coverage:out.coverage,triangles:out.triangles,bytes:out.image.bytes,eye,target,physicalAccess:"NOT VALIDATED"};}
return{files,summary};
};
const before=fs.readFileSync("artifacts/g4c7-a36-civic-delta-scout/a36_delta.obj","utf8");
const after=fs.readFileSync("artifacts/g4c7-a37-inhabited-open-section/a37_inhabited_city.obj","utf8");
const out=renderA37(before,after);for(const file of out.files){fs.mkdirSync(path.dirname(file.path),{recursive:true});fs.writeFileSync(file.path,Buffer.from(file.content,"base64"));}
console.log(JSON.stringify(out.summary,null,2));
