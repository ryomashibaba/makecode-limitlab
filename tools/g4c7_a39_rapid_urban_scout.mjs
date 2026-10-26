// G4-C7 A39 / DISTRICT CONFLUENCE - ART RESEARCH ONLY, NO MINECRAFT ACTIONS
// Pure JS geometry, actual Z-buffer rasterization and glTF2 binary serialization.
function buildA39(){
 const V=[],F=[],districtCounts={},M=[
 ["porcelain_superstructure",[217,230,226]],["deep_recess",[43,72,89]],
 ["civic_sand",[212,174,126]],["inhabited_glass",[76,168,177]],
 ["elevated_green",[98,164,130]],["stone_warm",[196,203,190]],
 ["bronze_artery",[213,160,91]],["library_warm",[239,219,171]]];
 let current="misc";
 const v=p=>{V.push(p);return V.length-1};
 const tri=(a,b,c,m)=>{F.push([v(a),v(b),v(c),m]);districtCounts[current]=(districtCounts[current]||0)+1;};
 const quad=(a,b,c,d,m)=>{let A=v(a),B=v(b),C=v(c),D=v(d);F.push([A,B,C,m],[A,C,D,m]);districtCounts[current]=(districtCounts[current]||0)+2};
 function prism(P,y0,y1,m){
  for(let i=1;i<P.length-1;i++){tri([P[0][0],y0,P[0][1]],[P[i+1][0],y0,P[i+1][1]],[P[i][0],y0,P[i][1]],m);tri([P[0][0],y1,P[0][1]],[P[i][0],y1,P[i][1]],[P[i+1][0],y1,P[i+1][1]],m)}
  for(let i=0;i<P.length;i++){let j=(i+1)%P.length;quad([P[i][0],y0,P[i][1]],[P[j][0],y0,P[j][1]],[P[j][0],y1,P[j][1]],[P[i][0],y1,P[i][1]],m)}
 }
 function box(x,y,z,w,h,d,m,rot=0){
   let c=Math.cos(rot),s=Math.sin(rot),P=[[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([dx,dz])=>[x+c*dx-s*dz,z+s*dx+c*dz]);prism(P,y-h/2,y+h/2,m)
 }
 function tapered(cx,cz,y0,y1,w0,d0,w1,d1,m,rotation=0){
   let c=Math.cos(rotation),s=Math.sin(rotation);
   let poly=(w,d,y)=>[[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([x,z])=>[cx+c*x-s*z,y,cz+s*x+c*z]);
   let a=poly(w0,d0,y0),b=poly(w1,d1,y1);quad(a[0],a[3],a[2],a[1],m);quad(b[0],b[1],b[2],b[3],m);
   for(let i=0;i<4;i++){let j=(i+1)%4;quad(a[i],a[j],b[j],b[i],m)}
 }
 function beam(p,q,w,h,m){let dx=q[0]-p[0],dz=q[2]-p[2],len=Math.hypot(dx,dz)||1,n=[-dz/len*w/2,dx/len*w/2];
 const pa=[[p[0]+n[0],p[1]-h/2,p[2]+n[1]],[p[0]-n[0],p[1]-h/2,p[2]-n[1]],[p[0]-n[0],p[1]+h/2,p[2]-n[1]],[p[0]+n[0],p[1]+h/2,p[2]+n[1]]],
 qa=[[q[0]+n[0],q[1]-h/2,q[2]+n[1]],[q[0]-n[0],q[1]-h/2,q[2]-n[1]],[q[0]-n[0],q[1]+h/2,q[2]-n[1]],[q[0]+n[0],q[1]+h/2,q[2]+n[1]]];
 for(let i=0;i<4;i++)quad(pa[i],qa[i],qa[(i+1)%4],pa[(i+1)%4],m);
 quad(pa[3],pa[2],pa[1],pa[0],m);quad(qa[0],qa[1],qa[2],qa[3],m);
 }
 function route(pts,w,h,m){for(let k=0;k<pts.length-1;k++)beam(pts[k],pts[k+1],w,h,m)}
 function ringArc(cx,cz,ir,or,start,end,y0,y1,m,n=12){
  let pt=(r,a)=>[cx+r*Math.cos(a),cz+r*Math.sin(a)];
  for(let k=0;k<n;k++){let a=start+(end-start)*k/n,b=start+(end-start)*(k+1)/n,A=pt(ir,a),B=pt(ir,b),C=pt(or,b),D=pt(or,a);
  prism([A,D,C,B],y0,y1,m)}
 }
 function fence(x,z,y,dir,length,m){for(let j=0;j<=length;j+=18){let p=dir==="x"?[x+j,y,z]:[x,y,z+j];box(p[0],y+7,p[2],3,14,3,m)}}
 // G0 site: three distinct but touching urban precincts, instead of a single anonymous megaslab.
 current="district-ground";
 prism([[-275,-195],[-243,-264],[-92,-263],[-29,-218],[-56,-101],[-168,-76],[-261,-132]],0,15,5);
 prism([[6,-225],[137,-257],[260,-192],[280,-88],[225,30],[117,72],[46,-67]],0,17,5);
 prism([[-141,35],[-34,7],[86,42],[169,103],[169,253],[56,275],[-59,255],[-188,154]],1,24,5);
 prism([[-95,-123],[79,-122],[137,-12],[81,76],[-50,94],[-135,17]],10,21,2);
 // Main city street: visible from arriving south to north research district. Three interchanges at different scales.
 current="public-arteries";
 route([[0,22,-260],[3,23,-161],[-12,25,-52],[20,25,37],[29,31,145],[26,33,240]],22,5,6);
 route([[-233,21,-159],[-153,24,-120],[-69,26,-45],[20,25,37],[128,26,3],[235,22,-101]],15,4,6);
 route([[-142,70,-157],[-95,76,-68],[-31,81,13],[36,88,81],[128,104,136]],13,4,0);
 route([[189,67,-151],[115,76,-79],[51,90,-5],[-22,110,93],[-81,134,166]],12,5,6);
 route([[-213,122,19],[-108,132,77],[-23,153,120],[70,171,154],[134,186,192]],12,6,0);
 // Clearly open civic forum: plazas at different heights, no full shell hiding interior.
 current="civic-center";
 prism([[-68,-92],[48,-99],[118,-22],[77,54],[-29,66],[-98,0]],21,27,5);
 ringArc(5,-9,34,51,-2.9,2.5,27,31,2,16);
 ringArc(5,-9,22,27,0,Math.PI*2,29,33,4,16);
 for(let a=0;a<12;a++){let x=5+Math.cos(a*Math.PI/6)*47,z=-9+Math.sin(a*Math.PI/6)*37;box(x,40,z,2.8,24,2.8,0)}
 for(let p of [[-48,-35],[65,-18],[26,31]]){box(p[0],31,p[1],22,4,12,4);box(p[0],38,p[1],10,10,10,7);}
 // West: densely inhabited ridge with three differently arranged blocks and pedestrian courts.
 current="west-neighborhood";
 const wb=[
 {x:-201,z:-190,w:94,d:73,h:123,rot:-.24},
 {x:-178,z:-64,w:83,d:95,h:158,rot:.13},
 {x:-161,z:77,w:98,d:72,h:195,rot:.37}
 ];
 for(let k=0;k<wb.length;k++){let b=wb[k],ybase=15;
  tapered(b.x,b.z,ybase,ybase+18,b.w,b.d,b.w-6,b.d-5,1,b.rot);
  let n=Math.floor((b.h-14)/22);
  for(let l=0;l<n;l++){
   let y=35+l*22,shift=Math.sin((l+k)*.67)*8,rx=b.x+shift;
   box(rx,y,b.z,b.w-5-l*.8,4,b.d-8-l*1.2,l%3===0?2:0,b.rot);
   box(rx+6,y+9,b.z-4,b.w-21-l*.8,12,b.d-24-l*1.2,3,b.rot);
   // Deep balconies / civic passages visible in facade, not flat tinted walls.
   box(rx-7,y+6,b.z-b.d*.45,b.w*.46,3,13,6,b.rot);
   if(l%2===0)box(rx-b.w*.30,y+10,b.z+17,14,14,14,1,b.rot);
  }
  box(b.x-12,b.h+35,b.z,Math.max(30,b.w-32),5,Math.max(34,b.d-31),4,b.rot);
  box(b.x+30,30,b.z+b.d*.42,26,17,11,7,b.rot);
  fence(b.x-36,b.z-25,39,"z",b.d*.6,7);
 }
 // Public stepped gardens between residences. Buildings share ground-to-elevated connective streets.
 for(let [x,z]of [[-229,-104],[-112,-111],[-109,13],[-91,112],[-221,100]]){
 box(x,32,z,27,4,24,4);box(x,40,z,11,13,11,5);
 }
 route([[-201,92,-190],[-145,87,-128],[-178,106,-65],[-104,110,-6]],16,5,6);
 route([[-178,143,-65],[-106,150,25],[-161,167,77],[-68,161,125]],14,5,0);
 // East: multiwing civic-cultural forum, a shallow open amphitheater rather than a single semicircular facility.
 current="east-culture";
 const halls=[
 {x:167,z:-158,w:121,d:84,h:95,angle:.20},
 {x:196,z:-18,w:109,d:89,h:116,angle:-.3},
 {x:118,z:81,w:93,d:76,h:89,angle:.52}
 ];
 for(let j=0;j<halls.length;j++){let b=halls[j],floors=Math.floor(b.h/22);
  tapered(b.x,b.z,17,32,b.w,b.d,b.w-8,b.d-7,1,b.angle);
  for(let l=0;l<floors;l++){
   let y=34+l*22,w=b.w-10-l*3,d=b.d-12-l*2;
   box(b.x,y,b.z,w,4,d,l%3===1?2:0,b.angle);
   box(b.x,y+9,b.z,w-11,13,d-18,3,b.angle);
   for(let c=-1;c<=1;c++)box(b.x+c*w*.28,y+9,b.z-d*.46,3,18,5,0,b.angle);
  }
  // Deep colonnaded terraces and distinct roof canopy widths.
  box(b.x,b.h+36,b.z,b.w*.7,4,b.d*.65,6,b.angle);
  box(b.x,b.h+43,b.z,b.w*.48,10,b.d*.40,4,b.angle);
 }
 // Entrance market, street courts, cultural facility identity are not only material names.
 ringArc(94,-73,25,41,-1.5,1.7,27,31,5,10);
 ringArc(94,-73,15,24,-1.5,1.7,31,34,4,10);
 route([[251,21,-158],[188,26,-88],[118,32,3],[65,34,25]],15,4,6);
 route([[180,114,-18],[111,123,53],[64,128,120]],16,4,0);
 current="north-research";
 // Three nonparallel research towers mark different destinations but do not dominate whole city.
 const research=[
 {x:-80,z:167,w:76,d:64,h:216,r:-.22},
 {x:16,z:208,w:84,d:77,h:260,r:.15},
 {x:116,z:184,w:70,d:86,h:188,r:-.36}
 ];
 for(let j=0;j<research.length;j++){let t=research[j],base=24,fl=Math.floor((t.h-26)/24);
  tapered(t.x,t.z,base,base+20,t.w+11,t.d+12,t.w,t.d,1,t.r);
  for(let k=0;k<fl;k++){let y=base+22+k*24;
   let dx=Math.sin(k*.72+j)*4,w=t.w-k*1.1,d=t.d-k*.8;
   box(t.x+dx,y,t.z,w,4,d,k%4===0?7:0,t.r);
   box(t.x+dx,y+10,t.z,w-13,16,d-11,3,t.r);
   if(k%3===0)box(t.x+dx-15,y+3,t.z-d*.54,Math.max(18,w-27),4,18,4,t.r);
   for(let s of [-1,1])box(t.x+dx+s*(w*.38),y+10,t.z,3,18,d*.75,0,t.r);
  }
  tapered(t.x,t.z,t.h+28,t.h+51,t.w*.7,t.d*.65,t.w*.42,t.d*.4,6,t.r);
 }
 // Open elevated research quadrangle with multiple clear destinations.
 box(18,47,139,115,5,55,2,.07);box(20,52,139,65,6,29,4,.07);
 route([[-77,123,169],[11,148,193],[118,147,187]],14,6,0);
 route([[-80,78,171],[0,81,122],[113,103,190]],16,6,6);
 current="public-life";
 // Street-scale furniture at actual distinct intervals and vertical scale; do not claim accessibility.
 for(let p of [[-55,-155],[54,-170],[-44,-92],[65,-80],[-32,-13],[92,61],[-44,82],[56,110],[-39,191],[71,225]]){
 box(p[0],31,p[1],4,11,4,1);
 box(p[0],38,p[1],18,5,13,4);
 box(p[0]+10,25,p[1]+8,13,4,5,2);
 }
 for(let x of [-66,-27,12,51])for(let z of [-197,-165]){box(x,30,z,17,4,22,6);box(x,39,z,10,17,11,3);box(x,49,z,21,4,17,7)}
 return {V,F,M,districtCounts};
}
function objA39(m){
 let s="# G4-C7 A39 DISTRICT CONFLUENCE REAL MESH - ART HOLD - NO CONSTRUCTION\nmtllib materials.mtl\n";
 for(const v of m.V)s+="v "+v.join(" ")+"\n";
 let old=-1;for(let f of m.F){if(f[3]!==old){old=f[3];s+="usemtl "+m.M[old][0]+"\n"}s+="f "+(f[0]+1)+" "+(f[1]+1)+" "+(f[2]+1)+"\n"}
 return s;
}
function base64A39(bytes){const abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<bytes.length;i+=3){let a=bytes[i],b=bytes[i+1]||0,c=bytes[i+2]||0;out.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<bytes.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<bytes.length?abc[c&63]:"=")}return out.join("")}
function glbA39(m){
 let p=new Uint8Array(m.V.length*12),d=new DataView(p.buffer);
 for(let i=0;i<m.V.length;i++)for(let k=0;k<3;k++)d.setFloat32(i*12+4*k,m.V[i][k],true);
 let bin=[...p],bv=[{buffer:0,byteOffset:0,byteLength:p.length,target:34962}],bounds=[0,1,2].map(k=>[Math.min(...m.V.map(v=>v[k])),Math.max(...m.V.map(v=>v[k]))]),ac=[{bufferView:0,componentType:5126,count:m.V.length,type:"VEC3",min:bounds.map(v=>v[0]),max:bounds.map(v=>v[1])}],pr=[];
 for(let j=0;j<m.M.length;j++){let ids=m.F.filter(f=>f[3]===j).flatMap(f=>f.slice(0,3));if(!ids.length)continue;
 let a=new Uint8Array(ids.length*4),view=new DataView(a.buffer);ids.forEach((v,k)=>view.setUint32(4*k,v,true));let off=bin.length;for(let n of a)bin.push(n);
 bv.push({buffer:0,byteOffset:off,byteLength:a.length,target:34963});ac.push({bufferView:bv.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:ac.length-1,material:j,mode:4});
 }
 while(bin.length%4)bin.push(0);
 let g={asset:{version:"2.0",generator:"MakeCode LimitLab G4C7 A39 nonbuild art study"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:m.M.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:[...x[1].map(y=>y/255),1],metallicFactor:.06,roughnessFactor:.74},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bv,accessors:ac};
 let json=Array.from(JSON.stringify(g)).map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
 let all=new Uint8Array(28+json.length+bin.length),dv=new DataView(all.buffer);dv.setUint32(0,0x46546c67,true);dv.setUint32(4,2,true);dv.setUint32(8,all.length,true);dv.setUint32(12,json.length,true);dv.setUint32(16,0x4e4f534a,true);all.set(json,20);let off=20+json.length;dv.setUint32(off,bin.length,true);dv.setUint32(off+4,0x004e4942,true);all.set(bin,off+8);
 return {b64:base64A39(all),bytes:all.length,object:g};
}
function pngA39(m,eye,target,W=900,H=720,scale=1.03,perspective=false){
 const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),norm=a=>{let l=Math.hypot(...a)||1;return a.map(x=>x/l)};
 let fw=norm(sub(target,eye)),right=norm(cross([0,1,0],fw)),up=norm(cross(fw,right)),light=norm([-.42,.88,-.25]);
 const P=m.V.map(p=>{let v=sub(p,target),re=sub(p,eye),z=dot(re,fw);return[W/2+(perspective?Math.min(850,Math.max(-850,570*dot(re,right)/Math.max(1,z))):scale*dot(v,right)),H/2-(perspective?Math.min(650,Math.max(-650,570*dot(re,up)/Math.max(1,z))):scale*dot(v,up)),z]});
 const pal=[[26,47,65]];for(let [_,col] of m.M)for(let j=0;j<8;j++){let s=.45+j*.096;pal.push(col.map(c=>Math.max(0,Math.min(255,Math.round(s*c)))))}
 let pix=new Uint8Array(W*H),Z=new Float64Array(W*H);Z.fill(Infinity);let nearIgnored=0;
 for(let f of m.F){let a=P[f[0]],b=P[f[1]],c=P[f[2]];if(a[2]<3||b[2]<3||c[2]<3){nearIgnored++;continue}
 let N=norm(cross(sub(m.V[f[1]],m.V[f[0]]),sub(m.V[f[2]],m.V[f[0]])));
 let shade=Math.max(0,Math.min(7,Math.round(2+5*Math.max(0,dot(N,light))))),shadeIndex=1+f[3]*8+shade;
 let x0=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0]))),x1=Math.min(W-1,Math.ceil(Math.max(a[0],b[0],c[0]))),y0=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),y1=Math.min(H-1,Math.ceil(Math.max(a[1],b[1],c[1])));
 let area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);if(Math.abs(area)<1e-8)continue;
 for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){let xx=x+.5,yy=y+.5,w1=((xx-a[0])*(c[1]-a[1])-(yy-a[1])*(c[0]-a[0]))/area,w2=((b[0]-a[0])*(yy-a[1])-(b[1]-a[1])*(xx-a[0]))/area,w0=1-w1-w2;
 if(w0<-.000001||w1<-.000001||w2<-.000001)continue;let z=w0*a[2]+w1*b[2]+w2*c[2],id=y*W+x;if(z<Z[id]){Z[id]=z;pix[id]=shadeIndex}}
 }
 let raw=[];for(let y=0;y<H;y++){raw.push(0);for(let x=0;x<W;x++)raw.push(pix[y*W+x]);}
 const u32=n=>[(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255],crcTable=Array.from({length:256},(_,n)=>{let c=n;for(let i=0;i<8;i++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0});
 const crc=a=>{let c=0xffffffff;for(let q of a)c=crcTable[(c^q)&255]^(c>>>8);return(c^0xffffffff)>>>0};
 const chunk=(name,data)=>{let nameBytes=Array.from(name).map(c=>c.charCodeAt(0));return[...u32(data.length),...nameBytes,...data,...u32(crc([...nameBytes,...data]))]};
 let ad1=1,ad2=0;for(let b of raw){ad1=(ad1+b)%65521;ad2=(ad2+ad1)%65521}
 let deflate=[0x78,1];for(let i=0;i<raw.length;){let n=Math.min(65535,raw.length-i);deflate.push(i+n===raw.length?1:0,n&255,(n>>8)&255,(~n)&255,((~n)>>8)&255,...raw.slice(i,i+n));i+=n}deflate.push(...u32(((ad2<<16)|ad1)>>>0));
 let png=[137,80,78,71,13,10,26,10,...chunk("IHDR",[...u32(W),...u32(H),8,3,0,0,0]),...chunk("PLTE",pal.flat()),...chunk("IDAT",deflate),...chunk("IEND",[])];
 return{b64:base64A39(png),bytes:png.length,coveredPixels:pix.reduce((s,n)=>s+(n!==0),0),nearIgnored};
}

import fs from "node:fs";
import path from "node:path";
// Reproduce only A39 non-build research geometry and A39 PNG views.
if(process.argv.includes("--write")){
 const root="artifacts/g4c7-a39-urban-scale-gate/";
 const write=(p,x,b64=false)=>{const f=root+p;fs.mkdirSync(path.dirname(f),{recursive:true});fs.writeFileSync(f,b64?Buffer.from(x,"base64"):x)};
 const m=buildA39(), g=glbA39(m);
 write("a39_district_confluence.obj",objA39(m));
 write("a39_district_confluence.glb",g.b64,true);
 write("materials.mtl",m.M.map(x=>"newmtl "+x[0]+"\nKd "+x[1].map(c=>(c/255).toFixed(6)).join(" ")+"\n").join("\n"));
 const cams={front:[[0,220,-450],[0,78,0]],oblique:[[350,282,-365],[0,78,0]],side:[[465,225,0],[0,78,0]],aerial:[[250,525,-270],[0,78,0]],street_eye:[[0,32,-200],[0,77,131]]};
 for(const [name,[eye,target]] of Object.entries(cams))write("verified-png/"+name+".png",pngA39(m,eye,target,900,720,1.03,name==="street_eye").b64,true);
 console.log("A39 REJECT scout regenerated; no Minecraft actions");
}
