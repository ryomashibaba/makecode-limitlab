// G4-C7 A40 - POROUS INHABITED BLOCK SECTION - RESEARCH ONLY
function buildA40(){
 const V=[],F=[],materials=[["porcelain",[220,229,221]],["recess",[43,72,89]],["stone",[181,168,145]],["civic_clay",[215,159,114]],["glazing",[83,160,171]],["plants",[94,151,106]],["reading_light",[241,206,132]],["deep_glass",[72,110,128]],["pale_bridge",[203,217,208]]],groups={};
 let group="ground";const vertex=p=>(V.push(p),V.length-1);
 function q(a,b,c,d,m){let ids=[vertex(a),vertex(b),vertex(c),vertex(d)];F.push([ids[0],ids[1],ids[2],m],[ids[0],ids[2],ids[3],m]);groups[group]=(groups[group]||0)+2}
 function t(a,b,c,m){F.push([vertex(a),vertex(b),vertex(c),m]);groups[group]=(groups[group]||0)+1}
 function prism(P,y0,y1,m){for(let i=1;i<P.length-1;i++){t([P[0][0],y0,P[0][1]],[P[i+1][0],y0,P[i+1][1]],[P[i][0],y0,P[i][1]],m);t([P[0][0],y1,P[0][1]],[P[i][0],y1,P[i][1]],[P[i+1][0],y1,P[i+1][1]],m)}for(let i=0;i<P.length;i++){let j=(i+1)%P.length;q([P[i][0],y0,P[i][1]],[P[j][0],y0,P[j][1]],[P[j][0],y1,P[j][1]],[P[i][0],y1,P[i][1]],m)}}
 function box(x,y,z,w,h,d,m){prism([[x-w/2,z-d/2],[x+w/2,z-d/2],[x+w/2,z+d/2],[x-w/2,z+d/2]],y-h/2,y+h/2,m)}
 function beam(p,b,w,h,m){let dx=b[0]-p[0],dz=b[2]-p[2],r=Math.hypot(dx,dz)||1,s=[-dz/r*w/2,dx/r*w/2],a=[[p[0]+s[0],p[1]-h/2,p[2]+s[1]],[p[0]-s[0],p[1]-h/2,p[2]-s[1]],[p[0]-s[0],p[1]+h/2,p[2]-s[1]],[p[0]+s[0],p[1]+h/2,p[2]+s[1]]],c=a.map(v=>[v[0]+dx,v[1]+b[1]-p[1],v[2]+dz]);for(let i=0;i<4;i++)q(a[i],c[i],c[(i+1)%4],a[(i+1)%4],m);q(a[3],a[2],a[1],a[0],m);q(c[0],c[1],c[2],c[3],m)}
 function route(P,w,h,m){for(let i=0;i<P.length-1;i++)beam(P[i],P[i+1],w,h,m)}
 function arch(cx,z,r,spring,thickness,depth,m){let n=12;
 for(let k=0;k<n;k++){let a=Math.PI*k/n,b=Math.PI*(k+1)/n,p=(r,t,j)=>[cx+r*Math.cos(t),spring+r*Math.sin(t),z+j*depth],ra=r+thickness;let A=p(ra,a,0),B=p(ra,b,0),C=p(r,b,0),D=p(r,a,0),E=p(ra,a,1),G=p(ra,b,1),H=p(r,b,1),I=p(r,a,1);
 q(A,B,C,D,m);q(I,H,G,E,m);q(A,E,G,B,m);q(D,C,H,I,m)}
 box(cx-r-thickness/2,spring/2,z+depth/2,thickness,spring,depth,m);box(cx+r+thickness/2,spring/2,z+depth/2,thickness,spring,depth,m)}
 function arc(cx,cz,r0,r1,a0,a1,y0,y1,m,n=18){for(let k=0;k<n;k++){let a=a0+(a1-a0)*k/n,b=a0+(a1-a0)*(k+1)/n;let pt=(r,s)=>[cx+r*Math.cos(s),cz+r*Math.sin(s)];prism([pt(r0,a),pt(r1,a),pt(r1,b),pt(r0,b)],y0,y1,m)}}
 // Irregular civic site and diagonal public route, not boxed platform.
 prism([[-215,-155],[-157,-190],[-28,-183],[61,-157],[182,-102],[222,35],[170,154],[51,191],[-100,175],[-203,112]],-2,9,2);
 route([[4,10,-189],[11,11,-123],[22,12,-42],[26,13,52],[35,14,164]],21,3,3);
 prism([[-91,-80],[15,-102],[82,-30],[73,65],[-11,109],[-99,57]],9,12,3);
 group="west-public-arcade";
 // Three deep arch bays. Interiors extend a full 94 units behind actual portal openings.
 for(let [cx,r] of [[-174,22],[-119,24],[-59,25]]){
 arch(cx,-44,r,25,8,17,0);
 for(let k=0;k<3;k++){let y=52+37*k;
 box(cx,y+1,32,2*r+14,6,92,k===1?8:2);
 box(cx,y+13,54,2*r-4,18,31,7);
 box(cx-11,y+6,-11,2*r*.72,4,25,3);
 box(cx+17,y+10,-20,9,22,5,0);
 if(k%2===0){box(cx+13,y+6,-14,21,3,16,5);box(cx+12,y+13,-10,11,12,10,5)}
 }
 box(cx-8,139,29,2*r+13,7,108,0);
 for(let k=0;k<3;k++)box(cx+r-8,62+37*k,30,5,20,82,8);
 }
 group="roof-crest";
 route([[-210,142,43],[-165,181,52],[-109,187,61],[-45,164,82],[2,153,114]],22,10,0);
 for(let [x,y,z] of [[-210,142,43],[-165,181,52],[-109,187,61],[-45,164,82]])beam([x,y,z],[x+20,y-34,z-24],7,6,0);
 for(let i=0;i<10;i++)box(-204+i*19,147,92+8*Math.sin(i*.3),14,5,17,5);
 group="east-civic-institute";
 // curved multifunctional halls visible from the central civic forecourt
 for(let level of [[13,20,3],[56,63,0],[104,111,8],[124,132,0],[141,147,5]])
 arc(107,25,level[0]>=104?67:63,level[0]>=104?94:99,-1.32,1.26,level[0],level[1],level[2],20);
 for(let k=0;k<=11;k++){let a=-1.32+2.58*k/11,x=107+91*Math.cos(a),z=25+91*Math.sin(a);
 beam([x,20,z],[x,113,z],5,5,k%3===0?0:8);
 if(k%2===0){let u=[107+66*Math.cos(a),64,25+66*Math.sin(a)];beam(u,[x,64,z],4,4,6)}}
 group="public-activity";
 for(let i=0;i<6;i++){box(113,22+i*4,0+i*16,56-4*i,5,10,6);box(113,27+i*4,5+i*16,39-3*i,6,3,7)}
 for(let i=0;i<7;i++)box(70+i*14,23,99,9,22,6,i%2?7:6);
 box(120,70,119,80,6,41,0);for(let i=0;i<5;i++)box(80+i*17,82,132,4,17,4,6);
 group="upper-civic-street";
 route([[-206,79,-17],[-154,82,-5],[-99,91,4],[-35,101,45],[35,106,65],[80,108,83],[126,124,122]],15,5,8);
 route([[-204,133,57],[-131,145,82],[-55,155,87],[-3,160,115]],12,5,0);
 box(-33,102,46,28,5,23,6);box(123,125,120,36,5,26,6);
 group="north-civic-library";
 let P=[[-43,119],[31,120],[80,158],[32,202],[-38,193]];
 prism(P,20,36,2);
 for(let j=0;j<4;j++){let y=43+j*26;prism([[-41,127],[30,128],[72,160],[28,195],[-33,187]],y,y+5,j===3?5:6);
 for(let [x,z] of [[-35,130],[29,130],[66,159],[-27,190]])box(x,y+13,z,4,24,4,j%2?8:0);
 for(let k=0;k<4;k++)box(-23+k*15,y+11,162,10,15,5,k%2?6:7);}
 for(let [x,z] of [[-41,129],[33,129],[79,160],[-32,193]])beam([x,36,z],[x,162,z],8,6,0);
 prism([[-49,118],[40,122],[86,159],[31,214],[-48,200]],160,169,0);
 group="human-scale-program";
 // Market stalls, public benches, tables, planted civic forecourt; all actual geometry.
 for(let i=0;i<8;i++){let x=-144+i*31,z=-111+(i%2)*10;box(x,14,z,15,4,10,3);box(x,22,z,3,12,3,0);box(x,29,z,21,4,18,i%3===0?5:6);box(x+12,13,z+8,5,6,5,7)}
 for(let [x,z] of [[-58,-75],[-23,16],[16,28],[58,-71],[-170,54],[-120,120],[59,113]]){box(x,16,z,4,12,4,1);box(x,25,z,17,8,18,5);box(x+10,12,z+5,8,4,6,3)}
 for(let i=0;i<8;i++){let x=-28+11*i;box(x,14,-38+i%2*10,6,3,6,6)}
 return {V,F,M:materials,groups,stage:"section-grammar-only"};
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
 const root="artifacts/g4c7-a40-inhabited-block-section/";
 const save=(name,content,binary=false)=>{let to=root+name;fs.mkdirSync(path.dirname(to),{recursive:true});fs.writeFileSync(to,binary?Buffer.from(content,"base64"):content)};
 const m=buildA40(),g=glbA39(m);
 save("a40_section.obj",objA39(m));save("a40_section.glb",g.b64,true);
 save("materials.mtl",m.M.map(x=>"newmtl "+x[0]+"\nKd "+x[1].map(c=>(c/255).toFixed(6)).join(" ")+"\n").join("\n"));
 const cams={front:[[0,195,-395],[0,83,0],false],oblique:[[305,230,-340],[0,83,0],false],side:[[380,187,0],[0,83,0],false],aerial:[[240,490,-240],[0,83,0],false],street_eye:[[15,28,-146],[22,63,123],true],gallery_eye:[[-112,74,4],[88,76,80],true]};
 for(let [name,[eye,target,p]] of Object.entries(cams))save("verified-png/"+name+".png",pngA39(m,eye,target,900,720,1.03,p).b64,true);
 console.log("A40 ART HOLD experimental section written, NOT A CITY APPROVAL");
}
