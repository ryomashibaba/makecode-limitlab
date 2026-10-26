// G4-C7 A41: HUMAN-EYE FIRST / URBAN FRONTAGE TEST
// NO Minecraft commands, no world access, no city integration. Pure research geometry.
function buildA41(){
 const V=[],F=[],groups={};
 const M=[
 ["limestone_frame",[216,222,209]],["dark_recess",[42,65,76]],
 ["market_timber",[178,129,84]],["glass_teal",[98,168,174]],
 ["brass_wayfinding",[216,180,105]],["planted_green",[95,151,109]],
 ["pavement_stone",[171,184,177]],["warm_interior",[237,202,154]],
 ["steel_frames",[66,91,102]],["pale_canopies",[235,227,207]],
 ["clay_brick",[166,133,114]],["night_gallery",[76,105,121]]
 ];
 let group="ground";const v=p=>(V.push(p),V.length-1);
 function face(a,b,c,mat){F.push([v(a),v(b),v(c),mat]);groups[group]=(groups[group]||0)+1}
 function quad(a,b,c,d,mat){let A=v(a),B=v(b),C=v(c),D=v(d);F.push([A,B,C,mat],[A,C,D,mat]);groups[group]=(groups[group]||0)+2}
 function prism(poly,lo,hi,m){for(let i=1;i<poly.length-1;i++){face([poly[0][0],lo,poly[0][1]],[poly[i+1][0],lo,poly[i+1][1]],[poly[i][0],lo,poly[i][1]],m);face([poly[0][0],hi,poly[0][1]],[poly[i][0],hi,poly[i][1]],[poly[i+1][0],hi,poly[i+1][1]],m);}
 for(let i=0;i<poly.length;i++){let j=(i+1)%poly.length;quad([poly[i][0],lo,poly[i][1]],[poly[j][0],lo,poly[j][1]],[poly[j][0],hi,poly[j][1]],[poly[i][0],hi,poly[i][1]],m)}}
 function box(x,y,z,w,h,d,m){prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m)}
 function cylindrical(x,z,r,y0,y1,m,n=9){const P=[];for(let i=0;i<n;i++){let a=2*Math.PI*i/n;P.push([x+Math.cos(a)*r,z+Math.sin(a)*r])}prism(P,y0,y1,m)}
 function beam(p,q,w,h,m){let dx=q[0]-p[0],dz=q[2]-p[2],len=Math.hypot(dx,dz)||1,n=[-dz/len*w/2,dx/len*w/2];
 const four=o=>[[o[0]+n[0],o[1]-h/2,o[2]+n[1]],[o[0]-n[0],o[1]-h/2,o[2]-n[1]],[o[0]-n[0],o[1]+h/2,o[2]-n[1]],[o[0]+n[0],o[1]+h/2,o[2]+n[1]]],a=four(p),b=four(q);
 for(let i=0;i<4;i++)quad(a[i],b[i],b[(i+1)%4],a[(i+1)%4],m);quad(a[3],a[2],a[1],a[0],m);quad(b[0],b[1],b[2],b[3],m)}
 function polyline(P,w,h,m){for(let i=0;i<P.length-1;i++)beam(P[i],P[i+1],w,h,m)}
 function walkRamp(x0,z0,x1,z1,y0,y1,w,m){polyline([[x0,y0,z0],[x1,y1,z1]],w,.35,m)}
 function silhouette(x,z,y=0){ // Abstract 1.8m scale proxy: NOT a real citizen or occupancy simulation.
 cylindrical(x,z,.24,y+.05,y+1.26,8,7);cylindrical(x,z,.34,y+1.26,y+1.69,4,9);
 box(x-.16,y+.39,z,.15,.75,.18,8);box(x+.16,y+.39,z,.15,.75,.18,8);}
 // Human-scale meter-research model, NOT guaranteed Minecraft conversion scale.
 group="ground-and-public-route";
 box(0,-.48,22,90,.9,166,6); // base 4-sided study site
 box(0,.035,19.5,18,.12,156,6);
 box(0,.1,20,5,.04,150,9);
 for(let x of [-10.3,10.3]){box(x,.20,20,1.25,.22,153,10);}
 // Functionally navigable visually: paving joints and tactical edges, not a flat empty plane.
 for(let z=-48;z<=75;z+=8){box(0,.16,z,17,.035,.10,9);}
 for(let [x,z] of [[-8,-35],[7,-15],[-8,18],[8,46],[0,63]]){box(x,.15,z,1.8,.13,1.8,4);}
 // Left continuous inhabited building: real open arcade in front and deep shops beyond.
 group="west-occupied-streetfront";
 const westStart=-48,westEnd=72,westernDepth=24;
 box(-22,2.5,12,23,.6,122,6); // ground shop floors, x -33..-10.5
 box(-32,9.0,12,1.35,18,122,10); // deep rear wall; openings on street deliberately left open
 box(-21.6,6.1,12,23,.55,122,0);
 box(-21.6,11.9,12,22.8,.55,122,0);
 box(-22,17.4,12,24,.78,122,9);
 for(let z of [-49,73]){box(-21.5,8.8,z,23,17,.7,0)}
 // true clear 5-meter ground openings; piers at storefront bay boundaries
 const wb=[-48,-28,-9,12,36,55,73];
 for(let i=0;i<wb.length;i++){
  const z=wb[i];box(-10.2,3.13,z,.82,6.2,1.15,0);
  if(i%2===0)box(-9.8,5.7,z,2.15,.65,1.5,4);
 }
 for(let i=0;i<wb.length-1;i++){
  let start=wb[i],end=wb[i+1],z=(start+end)/2,span=end-start;
  // deep visible interior behind the storefront: shelving, cafe, workshop or reading alcove
  box(-30.5,4.2,z,.7,6.4,span-2,11);
  if(i%3===0){for(let k=0;k<3;k++){box(-27.1,1.25+k*1.22,z,5,.28,span*.62,2)}}
  else if(i%3===1){for(let zz=z-span*.25;zz<=z+span*.25;zz+=4){box(-22,2.3,zz,3.3,.18,1.8,7);box(-22,2.7,zz,1.1,.78,1.6,2);}}
  else {box(-24,1.05,z,7,1.5,span*.6,2);for(let k=0;k<3;k++)box(-18,1.7,z-span*.25+k*span*.25,1.7,3,2,4)}
  // exterior canopy is physically tied to shopfront piers and upper slabs
  box(-8.7,5.48,z,3.8,.26,span-1.2,i%2?2:9);
  box(-9.0,4.95,z+span*.30,3,.25,span*.18,4);
  // upper elevations: recessed glazed rooms, integrated within thick building depth
  for(let lv=0;lv<2;lv++){
   const y=7.4+lv*5.85;
   box(-11.2,y+1.1,z,.22,3.0,span-2.2,i%2?3:11);
   box(-10.7,y-.68,z,.8,.25,span-1.3,9);
   box(-10.7,y+2.76,z,.7,.28,span-1.5,0);
   for(let j=0;j<3;j++)box(-10.67,y+1.05,start+(j+1)*span/4,.48,3.3,.5,8);
   // balconies in some homes that visually signal inhabited domestic scale
   if((i+lv)%3!==0){
     box(-9.2,y-.6,z,3.9,.3,span*.56,6);
     box(-7.32,y+.26,z,.18,1.4,span*.56,8);
   }
  }
 }
 // roof gardens not detached: terrace is directly on occupied roof structure
 for(let [z,span] of [[-28,20],[22,18],[57,18]]){
  box(-23,18.1,z,16,.55,span,5);
  for(let j=0;j<4;j++)cylindrical(-28+j*3.8,z,1.2,18.3,20.0,5,8);
 }
 // Right: less repetitive, more layered art workshop / market workshops with recessed shopfront and visible studio.
 group="east-culture-and-workshops";
 box(23,1.8,11,24,.58,121,6);box(33,8.8,11,1,17.4,121,10);
 box(22.5,6.2,11,24,.5,120,0);
 // asymmetry: two wings with different heights and a narrowing in the middle
 box(21,11.55,-22,22,.5,54,0);
 box(22,11.3,48,22,.5,46,0);
 box(20,16.1,9,25,.7,64,9);
 box(24,18.0,53,21,.6,36,9);
 const rb=[-48,-23,0,23,50,71];
 for(let i=0;i<rb.length;i++){let z=rb[i];box(10.6,3,z,.85,6.0,1.1,i%2?2:0)}
 for(let i=0;i<rb.length-1;i++){
  let a=rb[i],end=rb[i+1],z=(a+end)/2,w=end-a;
  box(32.0,3.2,z,.8,6.0,w-2.0,11);
  // workshop open window into public realm with real objects inside, not an opaque full facade
  for(let j=0;j<3;j++){let zz=a+4+j*(w-8)/2;
    box(21,1.08,zz,7,.25,2.3,2);
    box(21.5,2.25,zz,2.2,2.2,.85,4);
  }
  box(9.4,5.6,z,3.4,.3,w-1,2);
  box(10.9,8.2,z,.3,3.55,w-2,i%2===0?3:7);
  box(10.2,7.08,z,.4,.3,w-1,9);
  for(let j=0;j<4;j++)box(10.25,8.1,a+3+(w-6)*j/3,.34,3.0,.35,8);
  if(i>=3){box(8.8,11.4,z,3.8,.32,w*.7,6);box(6.95,12.15,z,.18,1.5,w*.67,8)}
 }
 // sweeping inhabited studio roof, not a roof blob hiding functions
 group="roof-and-landscape";
 const P=[[[11,16,-43],[11,15,-10]],[[11,15,-10],[12,17,31]],[[12,17,31],[11,19,70]]];
 for(let pp of P){polyline(pp,7,.65,9)}
 for(let z of [-33,-18,8,27,45,61])cylindrical(24,z,1.6,18.2,19.7,5,8);
 // end civic library with fully open entrance passage plus sheltered reading area (no sealed dark arch)
 group="visible-public-destination";
 box(0,.12,87,54,.3,50,6);
 box(-24,8.7,89,3,17,45,0);box(24,8.7,89,3,17,45,0);
 box(0,17.0,91,53,1.4,45,9);box(0,17.85,91,45,1.2,37,0);
 box(0,6,111,51,12,1.0,1); // only rear wall; front at z 72 open except portal piers
 for(let x of [-22,-11,11,22])box(x,5.9,69.8,1.6,11.8,2.4,0);
 box(0,12.4,70.1,49,1.1,3.1,9);
 for(let x of [-18,0,18]){box(x,14.3,72,12,3.2,.2,3);box(x,10.2,73.7,1.3,3.1,.9,4);}
 // room-depth visible book display, inviting lit destination
 for(let x of [-15,-4,7,18])for(let z of [92,103]){
 box(x,1.5,z,7.5,2.75,1.45,7);
 for(let j=0;j<3;j++)box(x,1.9+j*.75,z-.2,6,.16,1.7,2);
 }
 for(let k=0;k<3;k++){box(0,k*1.0+.2,77+k*5.5,24-3*k,.35,4.7,2);}
 box(0,9.8,100,29,.75,7.5,0);box(0,10.65,100,23,.35,7,5);
 for(let z of [83,95])for(let x of [-21,21])box(x,3,z,1.2,6,1.2,8);
 // wayfinding routes terminate in civic gateway: ensure image reads entrance + shops + distant destination
 group="street-scale-activity";
 const shopSeats=[[-8,-34],[-8,-6],[-8,19],[-8,48],[8,-39],[8,-7],[8,26],[8,56]];
 for(let [x,z]of shopSeats){cylindrical(x,z,.85,.2,.54,2,8);box(x,1.08,z,2.8,.2,1.2,7);box(x,1.42,z-.4,1.8,.5,.2,2);}
 for(let [x,z] of [[-6,-18],[6,0],[-7,36],[6,50]]){box(x,.66,z,1.8,1.1,1.8,10);cylindrical(x,z,1.25,1.2,2.7,5,9);}
 for(let z of [-42,-13,21,46,66]){
  // grounded street lights: base, pole and downward shade
  const x=z%2===0?7.6:-7.4;
  cylindrical(x,z,.13,0,4.9,8,8);box(x,4.9,z,2.8,.23,1.2,4);
 }
 for(let [x,z] of [[-3,-18],[3,3],[0,29],[-2,53],[8,79]])silhouette(x,z);
 return {V,F,M,groups,metresApprox:true,artifact:"not a city, no user traffic simulation"};
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

import fs from "node:fs"; import path from "node:path";
if(process.argv.includes("--write")){
  const root="artifacts/g4c7-a41-street-first/";
  const save=(name,contents,b64=false)=>{let dest=root+name;fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,b64?Buffer.from(contents,"base64"):contents)};
  const scene=buildA41(),glb=glbA39(scene);
  save("a41_street_first.obj",objA39(scene));save("a41_street_first.glb",glb.b64,true);
  save("materials.mtl",scene.M.map(x=>"newmtl "+x[0]+"\nKd "+x[1].map(c=>(c/255).toFixed(6)).join(" ")+"\n").join("\n"));
  const cameras={
    street_arrival:[[0,2.2,-66],[0,5.8,64],true],
    street_inner:[[0,2.2,-8],[0,5,85],true],
    side_shops:[[-5,2.2,-44],[-19,4,22],true],
    library_destination:[[0,2.2,24],[0,7,94],true],
    front:[[0,54,-140],[0,8,20],false],
    oblique:[[95,64,-86],[0,8,20],false],
    side:[[106,48,22],[0,8,20],false],
    aerial:[[81,126,-69],[0,8,20],false]
  };
  for(let [name,[eye,look,p]] of Object.entries(cameras)){
    save("verified-png/"+name+".png",pngA39(scene,eye,look,800,620,p?1.03:3.0,p).b64,true);
  }
  console.log("A41 ART HOLD. Not certified walkable. Geometry:",scene.V.length,scene.F.length);
}
