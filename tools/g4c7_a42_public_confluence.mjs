// MakeCode LimitLab / G4-C7 A42 - PUBLIC CONFLUENCE civic node research.
// Non-build real triangle mesh: no Minecraft Education, MakeCode, world, ZIP, USED, CSV, or external I/O.
function buildA42(){
 const V=[],F=[],labels={};
 const M=[
 ["ivory_structural",[221,227,217]],["deep_shadow",[42,64,75]],["warm_market_wood",[186,132,90]],
 ["civic_stone",[176,186,179]],["library_glass",[103,176,186]],["urban_plants",[95,156,111]],
 ["brass_signage",[235,192,109]],["public_terracotta",[191,125,98]],["steel_grid",[64,97,115]],
 ["warm_interior",[246,209,154]],["roof_ceramic",[198,210,198]],["theatre_blue",[85,135,148]],
 ["library_paper",[240,219,183]],["stage_light",[246,179,109]]
 ];
 let label="site";
 const id=p=>(V.push(p),V.length-1);
 const tri=(a,b,c,m)=>{F.push([id(a),id(b),id(c),m]);labels[label]=(labels[label]||0)+1};
 const quad=(a,b,c,d,m)=>{const j=[id(a),id(b),id(c),id(d)];F.push([j[0],j[1],j[2],m],[j[0],j[2],j[3],m]);labels[label]=(labels[label]||0)+2};
 function extrude(poly,lo,hi,m){
 for(let k=1;k<poly.length-1;k++){tri([poly[0][0],lo,poly[0][1]],[poly[k+1][0],lo,poly[k+1][1]],[poly[k][0],lo,poly[k][1]],m);tri([poly[0][0],hi,poly[0][1]],[poly[k][0],hi,poly[k][1]],[poly[k+1][0],hi,poly[k+1][1]],m)}
 for(let k=0;k<poly.length;k++){let j=(k+1)%poly.length;quad([poly[k][0],lo,poly[k][1]],[poly[j][0],lo,poly[j][1]],[poly[j][0],hi,poly[j][1]],[poly[k][0],hi,poly[k][1]],m)}
 }
 function box(x,y,z,w,h,d,m){extrude([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m)}
 function rotBox(x,y,z,w,h,d,m,a){
 let c=Math.cos(a),s=Math.sin(a);extrude([[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([u,v])=>[x+c*u-s*v,z+s*u+c*v]),y-h/2,y+h/2,m)}
 function beam(p,q,w,h,m){
  let dx=q[0]-p[0],dz=q[2]-p[2],len=Math.hypot(dx,dz)||1,s=[-dz/len*w/2,dx/len*w/2];
  let pts=o=>[[o[0]+s[0],o[1]-h/2,o[2]+s[1]],[o[0]-s[0],o[1]-h/2,o[2]-s[1]],[o[0]-s[0],o[1]+h/2,o[2]-s[1]],[o[0]+s[0],o[1]+h/2,o[2]+s[1]]];
  let a=pts(p),b=pts(q);for(let k=0;k<4;k++)quad(a[k],b[k],b[(k+1)%4],a[(k+1)%4],m);quad(a[3],a[2],a[1],a[0],m);quad(b[0],b[1],b[2],b[3],m);
 }
 function path(pts,w,h,m){for(let k=0;k<pts.length-1;k++)beam(pts[k],pts[k+1],w,h,m)}
 function column(x,z,y0,y1,r,m){const p=[];let n=10;for(let i=0;i<n;i++){let a=2*Math.PI*i/n;p.push([x+r*Math.cos(a),z+r*Math.sin(a)])}extrude(p,y0,y1,m)}
 function sphereProxy(x,z,y){column(x,z,y,y+1.2,.21,8);column(x,z,y+1.22,y+1.65,.36,6)}
 function slopedRoof4(x0,x1,z0,z1,yEdge,yRidge,m,thick=.42){
   // Real sloped roof leaves south + east entrances open and sits on piers.
   const mid=(x0+x1)/2;
   quad([x0,yEdge,z0],[mid,yRidge,z0],[mid,yRidge,z1],[x0,yEdge,z1],m);
   quad([mid,yRidge,z0],[x1,yEdge,z0],[x1,yEdge,z1],[mid,yRidge,z1],m);
   beam([x0,yEdge,z0],[x0,yEdge,z1],thick,thick,0);
   beam([x1,yEdge,z0],[x1,yEdge,z1],thick,thick,0);
   beam([mid,yRidge,z0],[mid,yRidge,z1],thick,thick,0);
 }
 function halfRing(cx,cz,r0,r1,a0,a1,y0,y1,m,n=20){
   for(let k=0;k<n;k++){let a=a0+(a1-a0)*k/n,b=a0+(a1-a0)*(k+1)/n,pt=(r,t)=>[cx+Math.cos(t)*r,cz+Math.sin(t)*r];extrude([pt(r0,a),pt(r1,a),pt(r1,b),pt(r0,b)],y0,y1,m)}
 }
 // Distinct non-parallel street arrival and crossing arms. Avoid a single rectilinear mall strip.
 label="public-ground";
 extrude([[-104,-50],[-62,-77],[13,-80],[70,-66],[113,-34],[115,39],[73,102],[-11,106],[-77,71],[-111,10]],-.8,0,3);
 // Three actual branches: SOUTH -> CENTER -> NORTH, WEST MARKET, EAST THEATER.
 path([[0,.04,-77],[0,.05,-45],[2,.06,-12],[0,.06,16],[3,.07,67]],14,.1,10);
 path([[-96,.08,7],[-60,.08,8],[-27,.08,4],[0,.06,0],[35,.08,-4],[84,.08,-10]],14,.11,10);
 path([[-10,.08,53],[9,.08,54],[37,.09,52],[87,.08,41]],9,.11,10);
 // Broad genuine urban plaza, NOT blank void; pavement hierarchy with contrasting civic surface.
 extrude([[-23,-25],[18,-24],[30,11],[12,29],[-17,25],[-32,0]],.01,.13,7);
 for(let x of [-17,-8,0,8,18]){box(x,.14,-10,1,.04,9,3);}
 for(let [x,z] of [[-18,-38],[22,-42],[-22,30],[28,19],[-9,38],[15,39]]){
   box(x,.37,z,7,.55,5,3);box(x,.8,z,4,.5,4,5);
 }
 label="west-covered-market";
 // MARKETHALL front looks EAST toward plaza: civic-gabled roof on actual piers.
 // footprint x -100 to -37 and z -40..32, walkway enters from east at x -38
 box(-76,.41,-4,46,.7,69,7);
 for(let z of [-38,-17,7,31]){
   column(-46,z,0,13,.66,0);column(-96,z,0,13,.68,0);
   beam([-96,13,z],[-46,13,z],.95,.9,0);
 }
 slopedRoof4(-104,-38,-43,35,13,24,10,.75);
 // open facade EAST: no wall across entrance, visibility into market rows
 // deep west stall wall segmented by genuine glazed openings.
 for(let z=-40;z<33;z+=12){box(-103,6,z,.8,12,3,7);box(-102,4.5,z+5,1.2,7,4,4)}
 // Market inner raised gallery occupies upper mezzanine portion, not obstructing whole void.
 box(-89,10,-3,15,.6,48,2);
 for(let z of [-22,-8,6,19]){beam([-84,10,z],[-75,10,z],1.2,.45,6);}
 // Commodity displays, stalls and striped roof rhythm as integral function
 for(let z of [-28,-9,13,27]){
  for(let x of [-84,-65]){
   box(x,1.2,z,10,2,5,2);box(x,2.45,z,8,.45,4,9);
   for(let i=0;i<3;i++)box(x-3+i*3,.85,z+1.2,1.5,.8,1.5,i%2?5:13);
   for(let side of [-4.5,4.5])column(x+side,z,0,5.1,.26,0);
   box(x,5.1,z,11,.6,8,(x===-84?6:9));
  }
 }
 // explicit market portal: tall piers, colored projecting canopy, entry platform
 for(let z of [-16,8]){column(-39,z,0,10,.75,0);}
 box(-38,10,-4,3,.9,31,6);box(-36,8.6,-4,5,.42,30,9);
 // People proxies only, not agents, visible near market entrance
 for(let [x,z] of [[-28,-6],[-40,14],[-52,-20]])sphereProxy(x,z,0);
 label="east-culture-workshop";
 // CULTURAL MAKER HALL faces WEST, rotated off east-west axis for a genuinely different spatial grammar
 // asymmetric glazed high hall with publicly visible exhibit and workshop
 const angle=-.23;rotBox(71,.44,-13,65,.7,57,3,angle);
 // One perforated courtyard-front rather than enclosed opaque facade
 for(let z of [-43,-18,7,30]){
    column(37,z,0,17,.76,0);
    column(105,z+8,0,17,.7,0);
    beam([37,17,z],[105,17,z+8],.8,.8,0);
 }
 // staggered roof with large diagonal profile, not a tall rectangular cap
 path([[34,17,-49],[55,22,-39],[76,24,-27],[105,18,-14]],7,.95,10);
 path([[39,17,18],[66,25,28],[108,18,36]],7,.95,10);
 rotBox(83,11,-17,1.3,20,55,8,angle); // glazed back frame, not entrance
 for(let z of [-35,-5,23]){
   rotBox(92,10,z,2.0,13,9,4,angle);
 }
 // Two workshop stages, publicly visible from west. Large vertical central void remains open.
 for(let z of [-28,9]){
  rotBox(71,1.0,z,28,1.4,12,2,angle);
  for(let k=0;k<3;k++){rotBox(65+k*7,2.3,z,4,1,5,9,angle);}
  rotBox(71,4.7,z,27,.6,10,11,angle);
 }
 // distinguish CULTURE/STAGE from markets with semicircular seating opening to the plaza
 halfRing(47,-6,11,16,-1.56,1.56,.0,.52,11,16);
 halfRing(47,-6,17,22,-1.56,1.56,.52,1.05,2,16);
 halfRing(47,-6,23,28,-1.56,1.56,1.05,1.52,7,16);
 box(51,.73,-6,9,1,18,13);
 for(let z of [-27,-6,15]){column(32,z,0,6,.7,0);}
 box(34,6,-7,2,1.3,50,6); // maker-hall portal in front, connected to floor columns
 for(let [x,z] of [[31,-17],[34,16],[51,-36]])sphereProxy(x,z,0);
 label="north-library-and-research";
 // LIBRARY becomes the third clearly different destination facing south.
 // Portal and glazed shelves are genuinely open towards public square (south).
 extrude([[-28,49],[23,49],[35,62],[26,103],[-26,101],[-37,76]],.0,.8,3);
 box(-27,11,69,1.8,22,51,0);box(27,11,71,1.8,22,50,0);
 box(0,22,76,59,1.5,58,10);
 box(0,23.4,76,49,.6,47,6);
 // Broad entry visible through plaza, no opaque entry wall at z ~ 51
 for(let x of [-25,-9,9,25]){column(x,51,0,16,.65,0);}
 beam([-28,16,51],[28,16,51],1.6,1.15,0);
 // Deep shelves at back are visible from main street as real volumes and colored spines
 for(let x of [-19,-9,2,13,23]){
   for(let z of [75,90]){
     box(x,2.8,z,7,5,2.2,2);
     for(let j=0;j<4;j++){box(x,1.1+j*1.15,z-.5,6.7,.24,2.3,12);}
     for(let j=0;j<4;j++){box(x-2.5+j*1.5,3.05,z-1.45,.65,3.5,.35,j%2?6:4);}
   }
 }
 // reading table group physically anchored within hall
 for(let z of [65,82])for(let x of [-12,10]){box(x,1.25,z,7,.22,3,2);box(x,.62,z,1.1,1.1,1.2,8);}
 // inhabitable reading mezzanine, asym but fixed to outer structural frame
 box(-20,11,79,10,.5,42,0);
 for(let z of [59,73,86,98]){column(-26,z,0,12,.5,0);box(-16,12,z,6,.4,1.2,8);}
 // skylight roof with supported angled structural wings, but no huge isolated arc
 path([[-29,22,55],[-18,29,65],[0,34,74],[20,29,82],[32,22,92]],4.8,.9,0);
 for(let [x,z] of [[-23,57],[-9,68],[12,78],[24,88]])beam([x,18,z],[x,29,z],.65,.65,0);
 // small light blocks emphasize entry without fabricated typography
 box(0,18,50.1,26,1.0,1.5,6);
 box(0,20,49.5,12,3,1.0,9);
 for(let [x,z] of [[-7,51],[7,51],[0,60]])sphereProxy(x,z,0);
 label="crossroads-and-human-scale";
 // Structured civic plaza, small cafe tables and trees are SECONDARY to urban legibility.
 for(let [x,z] of [[-19,-20],[16,12],[12,-29],[-13,28],[-11,9]]){
  column(x,z,.2,1.02,.73,2);box(x,1.12,z,3.7,.24,1.6,9);
  column(x-1.6,z+.4,.16,.72,.28,8);column(x+1.6,z-.4,.16,.72,.28,8);
 }
 for(let [x,z] of [[-12,-44],[24,27],[-28,30],[28,-41],[-2,33],[-35,42]]){
   box(x,.55,z,3.2,.9,3.3,7);column(x,z,1.0,3.65,.45,0);column(x,z,3.6,5.9,2.15,5); 
 }
 // lighting in route intersections
 for(let [x,z] of [[-15,-51],[20,-50],[-22,-6],[23,2],[0,34]]){
   column(x,z,0,6.1,.16,8);box(x,6.2,z,3,.35,1.3,6);
 }
 for(let [x,z] of [[-5,-32],[9,-16],[-14,2],[9,18],[2,39]])sphereProxy(x,z,.1);
 const anchors={
  arrival:[0,2.2,-61],junction:[0,2.2,-22],
  entrances:{market:[-37,0,-4],culture:[34,0,-6],library:[0,0,51]},
  streetBranches:{south:[0,-70],west:[-95,7],east:[84,-10],north:[3,67]}
 };
 return {V,F,M,labels,anchors,scope:"S1 civic junction scout; not full city"};
}

function objA39(m){
 let s="# G4-C7 A42 PUBLIC CONFLUENCE REAL MESH - ART HOLD - NO CONSTRUCTION\nmtllib materials.mtl\n";
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
 let g={asset:{version:"2.0",generator:"MakeCode LimitLab G4C7 A42 nonbuild civic art study"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:m.M.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:[...x[1].map(y=>y/255),1],metallicFactor:.06,roughnessFactor:.74},doubleSided:true})),buffers:[{byteLength:bin.length}],bufferViews:bv,accessors:ac};
 let json=Array.from(JSON.stringify(g)).map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
 let all=new Uint8Array(28+json.length+bin.length),dv=new DataView(all.buffer);dv.setUint32(0,0x46546c67,true);dv.setUint32(4,2,true);dv.setUint32(8,all.length,true);dv.setUint32(12,json.length,true);dv.setUint32(16,0x4e4f534a,true);all.set(json,20);let off=20+json.length;dv.setUint32(off,bin.length,true);dv.setUint32(off+4,0x004e4942,true);all.set(bin,off+8);
 return {b64:base64A39(all),bytes:all.length,object:g};
}
function pngA39(m,eye,target,W=900,H=720,scale=1.03,perspective=false){
 const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),norm=a=>{let l=Math.hypot(...a)||1;return a.map(x=>x/l)};
 let fw=norm(sub(target,eye)),right=norm(cross([0,1,0],fw)),up=norm(cross(fw,right)),light=norm([-.42,.88,-.25]);
 const P=m.V.map(p=>{let v=sub(p,target),re=sub(p,eye),z=dot(re,fw);return[W/2+(perspective?Math.min(850,Math.max(-850,480*dot(re,right)/Math.max(1,z))):scale*dot(v,right)),H/2-(perspective?Math.min(650,Math.max(-650,480*dot(re,up)/Math.max(1,z))):scale*dot(v,up)),z]});
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

import fs from "node:fs";import path from "node:path";
if(process.argv.includes("--write")){
 const root="artifacts/g4c7-a42-public-confluence/";
 const save=(name,data,b64=false)=>{const to=root+name;fs.mkdirSync(path.dirname(to),{recursive:true});fs.writeFileSync(to,b64?Buffer.from(data,"base64"):data)};
 const m=buildA42(),g=glbA39(m);
 save("a42_public_confluence.obj",objA39(m));save("a42_public_confluence.glb",g.b64,true);
 save("materials.mtl",m.M.map(x=>"newmtl "+x[0]+"\nKd "+x[1].map(c=>(c/255).toFixed(6)).join(" ")+"\n").join("\n"));
 const cameras={
  junction_arrival:[[0,2.2,-61],[0,6,25],true,1.03],
  junction_center:[[0,2.2,-23],[0,5,21],true,1.03],
  market_portal:[[-9,2.2,-17],[-74,6,-5],true,1.03],
  culture_portal:[[10,2.2,-18],[66,7,-9],true,1.03],
  library_portal:[[0,2.2,-14],[0,8,78],true,1.03],
  front:[[0,89,-172],[0,14,10],false,2.20],
  oblique:[[136,112,-130],[0,14,10],false,2.20],
  side:[[168,90,5],[0,14,10],false,2.20],
  aerial:[[122,193,-104],[0,14,10],false,2.20]
 };
 for(let [name,[eye,target,p,s]] of Object.entries(cameras))save("verified-png/"+name+".png",pngA39(m,eye,target,900,720,s,p).b64,true);
 console.log("A42 ART HOLD initial S1 complete; NOT certified for walking or Minecraft");
}
