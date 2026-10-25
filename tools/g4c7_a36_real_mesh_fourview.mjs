#!/usr/bin/env node
// G4-C7 A36 actual saved OBJ independent four-view renderer. No image fabrication, no Minecraft.
import fs from "node:fs";import path from "node:path";
const render=function render(prev,cur){
const mats={limestone:0,support:1,deep:1,plaza:2,civic:2,facade:3,inhabited:3,garden:4,north:5,upper:5};
function parse(raw){let v=[],f=[],mat=0;for(let line of raw.split("\n")){if(line.startsWith("v "))v.push(line.trim().split(/\s+/).slice(1,4).map(Number));else if(line.startsWith("usemtl "))mat=mats[line.slice(7).trim()]??0;else if(line.startsWith("f ")){let t=line.trim().split(/\s+/).slice(1).map(x=>Number(x.split("/")[0])-1);if(t.length===3)f.push([...t,mat]);}}return {v,f};}
const old=parse(prev),now=parse(cur);
if(old.v.length!==6860||now.v.length!==7418)throw Error("missing OBJ content");
const cameras={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},target=[0,78,0];
const W=800,H=460,one=400,viewScale=1.03*.70;
const col=[[19,37,53],[35,61,81],[216,226,233],[74,100,119],[229,191,139],[86,187,198],[122,181,151],[169,195,204]],palette=col.slice(0,2);
for(let m=0;m<6;m++)for(let j=0;j<8;j++)palette.push(col[m+2].map(c=>Math.max(0,Math.min(255,Math.round(c*(.47+j*.095))))));
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),unit=a=>a.map(x=>x/Math.hypot(...a));
function frame(model,eye,offset,pixels){
let forward=unit(sub(target,eye)),right=unit(cross([0,1,0],forward)),up=unit(cross(forward,right)),positions=model.v.map(p=>{let v=sub(p,target);return[offset+one/2+viewScale*dot(v,right),H/2-viewScale*dot(v,up)]}),faces=[];
for(let t of model.f){let a=model.v[t[0]],b=model.v[t[1]],c=model.v[t[2]],n=unit(cross(sub(b,a),sub(c,a))),mid=a.map((x,k)=>(x+b[k]+c[k])/3);if(dot(n,sub(eye,mid))<=0)continue;
let light=.71+.39*dot(n,unit([-.42,.84,-.32])),shade=Math.max(0,Math.min(7,Math.round((light-.47)/.095))),z=dot(sub(mid,eye),forward);faces.push({z,xy:t.slice(0,3).map(i=>positions[i]),color:2+8*t[3]+shade});}
faces.sort((a,b)=>b.z-a.z);
for(let tri of faces){let [a,b,c]=tri.xy,minY=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),maxY=Math.min(H,Math.ceil(Math.max(a[1],b[1],c[1])));
for(let y=minY;y<maxY;y++){let xs=[];for(let [p,q] of [[a,b],[b,c],[c,a]])if((p[1]<=y+.5&&q[1]>y+.5)||(q[1]<=y+.5&&p[1]>y+.5))xs.push(p[0]+(y+.5-p[1])*(q[0]-p[0])/(q[1]-p[1]));if(xs.length<2)continue;
let lo=Math.max(offset,Math.ceil(Math.min(...xs)-.5)),hi=Math.min(offset+one,Math.floor(Math.max(...xs)-.5)+1);for(let x=lo;x<hi;x++)pixels[y*W+x]=tri.color;}}
return faces.length;
}
const table=new Uint32Array(256);for(let i=0;i<256;i++){let c=i;for(let k=0;k<8;k++)c=c&1?0xedb88320^(c>>>1):c>>>1;table[i]=c>>>0;}
const be=n=>[(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255],crc=a=>{let c=0xffffffff;for(let x of a)c=table[(c^x)&255]^(c>>>8);return(c^0xffffffff)>>>0},ck=(s,a)=>{let d=[...s].map(x=>x.charCodeAt(0)).concat(a);return[...be(a.length),...d,...be(crc(d))];};
function encode(pixels){let rows=new Uint8Array(H*(W+1));for(let y=0;y<H;y++)rows.set(pixels.subarray(y*W,(y+1)*W),y*(W+1)+1);
let zip=[120,1],a=1,b=0;for(let x of rows){a=(a+x)%65521;b=(b+a)%65521;}for(let i=0;i<rows.length;i+=65535){let n=Math.min(65535,rows.length-i);zip.push(i+n===rows.length?1:0,n&255,n>>8,(~n)&255,((~n)>>8)&255);for(let j=i;j<i+n;j++)zip.push(rows[j]);}zip.push(b>>8,b&255,a>>8,a&255);
const bytes=[137,80,78,71,13,10,26,10,...ck("IHDR",[...be(W),...be(H),8,3,0,0,0]),...ck("PLTE",palette.flat()),...ck("IDAT",zip),...ck("IEND",[])],ABC="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];
for(let i=0;i<bytes.length;i+=3){let p=bytes[i],q=bytes[i+1]??0,r=bytes[i+2]??0;out.push(ABC[p>>2],ABC[((p&3)<<4)|(q>>4)],i+1<bytes.length?ABC[((q&15)<<2)|(r>>6)]:"=",i+2<bytes.length?ABC[r&63]:"=");}return out.join("");}
let images=[],report={};
for(let [name,eye] of Object.entries(cameras)){let pixels=new Uint8Array(W*H);pixels.fill(1);let n0=frame(old,eye,0,pixels),n1=frame(now,eye,one,pixels);images.push({path:"artifacts/g4c7-a36-civic-delta-scout/fourview/"+name+"_a35_vs_a36.png",content:encode(pixels),encoding:"base64",name});report[name]={old_triangles_drawn:n0,new_triangles_drawn:n1,camera:eye,scale_source:1.03,thumbnail_factor:.70,images_px:[W,H]};}
return {images,report};
};
const a=fs.readFileSync("artifacts/g4c7-a35-integrated-form-scout/a35_curved_integral_city.obj","utf8");
const b=fs.readFileSync("artifacts/g4c7-a36-civic-delta-scout/a36_delta.obj","utf8");
const out=render(a,b);for(const f of out.images){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,Buffer.from(f.content,"base64"));}
console.log(JSON.stringify(out.report,null,2));
