#!/usr/bin/env node
// G4-C7 A23 isolated ART HOLD actual 3D massing. NEVER modifies Minecraft Education.
import fs from 'node:fs';import path from 'node:path';
const build=function build(){
const R="artifacts/g4c7-a23-skyline-scout/",C={front:[0,178,-392],oblique:[290,228,-305],side:[403,196,0],aerial:[188,456,-208]},T=[0,70,0],S=1.27;
const MAT=[["ivory","#cddce1",[.8,.863,.882,1]],["structure","#567186",[.337,.443,.525,1]],["glass","#58b5c0",[.345,.71,.75,1]],["public","#efbb82",[.937,.733,.51,1]],["garden","#82a58a",[.51,.647,.54,1]]];
const VAR=[["a","MERIDIAN ASCENT",.1,11,1,1,.2],["b","DIAGONAL FAULT CITY",.23,28,.84,1.24,1.1],["c","SINGLE CIVIC ESCARPMENT",-.07,8,1.38,.60,-.3]];
function mk(v){
let m={name:v[1],id:v[0],V:[],F:[],solids:[],frontages:0};
function add(st,mat,label){if(st.length<2)throw Error(label);const pts=[],face=[];
for(let s of st){if(s.h<=s.l||s.w<=0)throw Error(label);pts.push([s.x-s.w/2,s.l,s.z],[s.x+s.w/2,s.l,s.z],[s.x+s.w/2,s.h,s.z],[s.x-s.w/2,s.h,s.z]);}
for(let k=0;k<st.length-1;k++)for(let j=0;j<4;j++){let a=4*k+j,b=4*k+(j+1)%4,c=4*(k+1)+(j+1)%4,d=4*(k+1)+j;face.push([a,b,c],[a,c,d]);}
face.push([0,2,1],[0,3,2]);let i=(st.length-1)*4;face.push([i,i+1,i+2],[i,i+2,i+3]);
let vol=0;for(let f of face){let a=pts[f[0]],b=pts[f[1]],c=pts[f[2]];
vol+=(a[0]*(b[1]*c[2]-b[2]*c[1])+a[1]*(b[2]*c[0]-b[0]*c[2])+a[2]*(b[0]*c[1]-b[1]*c[0]))/6;}
if(vol<0){face=face.map(f=>[f[0],f[2],f[1]]);vol=-vol;}
if(vol<=.0001)throw Error(label+" volume");
let edge=new Map(),or=new Map(),deg=0;
for(let f of face){let a=pts[f[0]],b=pts[f[1]],c=pts[f[2]],u=b.map((x,j)=>x-a[j]),w=c.map((x,j)=>x-a[j]);
if(Math.hypot(u[1]*w[2]-u[2]*w[1],u[2]*w[0]-u[0]*w[2],u[0]*w[1]-u[1]*w[0])<.000001)deg++;
for(let j=0;j<3;j++){let x=f[j],y=f[(j+1)%3],key=Math.min(x,y)+":"+Math.max(x,y);edge.set(key,(edge.get(key)||0)+1);let key2=x+":"+y;or.set(key2,(or.get(key2)||0)+1);}}
let bad=[...edge].filter(([k,n])=>{let [a,b]=k.split(":");return n!==2||(or.get(a+":"+b)||0)!==1||(or.get(b+":"+a)||0)!==1}).length;
if(bad||deg)throw Error(label+" invalid surface "+bad+" "+deg);
let base=m.V.length;m.V.push(...pts);m.F.push(...face.map(f=>[base+f[0],base+f[1],base+f[2],mat]));m.solids.push({name:label,triangles:face.length,volume:+vol.toFixed(3)});
}
function box(x,z,w,d,y,h,mat,name){add([{x,z:z-d/2,w,l:y,h},{x,z:z+d/2,w,l:y,h}],mat,name);}
const axis=z=>v[2]*z+v[3]*Math.sin(z/62+v[6]),Z=[-151,-115,-75,-38,0,37,76,115,151];
let path=Z.map((z,i)=>({z,x:axis(z),left:Math.max(36,(44+(z+151)*.4+9*Math.sin(i*.74+v[6]))*v[4]),right:Math.max(36,(118-(z+151)*.16+8*Math.cos(i*.8+v[6]))*v[5])}));
for(let side of [-1,1]){let key=side<0?"left":"right",root=side<0?"left":"right";
add(path.map(p=>({z:p.z,x:p.x+side*81,w:23,l:10,h:p[root]})),0,key+"_entire_inhabited_wall");
add(path.map(p=>({z:p.z,x:p.x+side*70,w:40,l:-4,h:13})),1,key+"_connected_ground_footprint");
add(path.map((p,i)=>({z:p.z,x:p.x+side*(106+7*Math.sin(i*.8)),w:15,l:-4,h:Math.max(23,p[root]*.76)})),1,key+"_sculpted_exterior_ridge");
for(let j=0;j<Z.length-1;j++){let z=(Z[j]+Z[j+1])/2,central=axis(z),max=(path[j][root]+path[j+1][root])/2,d=(Z[j+1]-Z[j])*.82;
for(let h of [19,42,69,100,130]){if(h+16>=max)continue;let x=central+side*(39+(h%3)*2);
box(x,z,31,d,h,h+3.5,3,key+"_public_terrace_"+j+"_"+h);
box(x+side*12,z+((j%2)*3),13,d*.8,h+3.5,h+16,2,key+"_inhabited_facade_"+j+"_"+h);
if(j%3===0)box(x-side*7,z+3,10,10,h+3.5,h+5.2,4,key+"_sky_garden_"+j+"_"+h);
m.frontages++;}
box(central+side*77,z,4,d*.6,Math.max(16,max-21),max-4,0,key+"_finned_crest_"+j);
}}
add(path.map((p,i)=>({z:p.z,x:p.x,w:23+(i%3)*2,l:2+i*.75,h:5+i*.75})),3,"continuous_asymmetrical_main_boulevard");
for(let j=1;j<=6;j++){let z=Z[j],c=axis(z),y=5+j*.75;box(c,z,14,15,y,y+7,2,"active_civic_centre_"+j);}
for(let j=0;j<3;j++){let z=[-98,5,116][j],c=axis(z),y=[22,50,78][j];add([{z:z-6,x:c,w:145,l:y,h:y+4},{z:z+7,x:c+6,w:146,l:y,h:y+4}],3,"large_civic_cross_boulevard_"+j);box(c+19,z,13,12,y+4,y+13,2,"bridged_urban_hall_"+j);}
for(let j=0;j<3;j++){let z0=[-93,-9,78][j],side=j%2?1:-1;
add(Array.from({length:5},(_,k)=>{let z=z0+k*12,y=75+j*7+k*6;return {z,x:axis(z)+side*(91+k*1.7),w:16-k,l:y-13,h:y+6}}),0,"folded_urban_roof_wing_"+j);}
return m;}
const mods=VAR.map(mk),stats=mods.map(m=>{let mn=[Infinity,Infinity,Infinity],mx=[-Infinity,-Infinity,-Infinity];for(let p of m.V)for(let k=0;k<3;k++){mn[k]=Math.min(mn[k],p[k]);mx[k]=Math.max(mx[k],p[k]);}
return {name:m.name,vertices:m.V.length,triangles:m.F.length,isolated_closed_solids:m.solids.length,positive_individual_volumes:true,paired_oriented_edges:true,no_degenerate_faces:true,bounds:[mn,mx],inhabited_frontages:m.frontages,whole_boolean_union:"NOT DONE",walk_331_993:"NOT RUN",art:"ART HOLD"};});
let files=[],out=(name,content,encoding="utf-8")=>files.push({path:R+name,content,encoding});
const b64=u=>{let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",r=[];for(let i=0;i<u.length;i+=3){let a=u[i],b=u[i+1]??0,c=u[i+2]??0;r.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<u.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<u.length?abc[c&63]:"=");}return r.join("");};
function glb(m){let pos=new Uint8Array(m.V.length*12),p=new DataView(pos.buffer);for(let i=0;i<m.V.length;i++)for(let j=0;j<3;j++)p.setFloat32(i*12+j*4,m.V[i][j],true);
let buf=[...pos],views=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],acc=[{bufferView:0,componentType:5126,count:m.V.length,type:"VEC3",min:[0,1,2].map(j=>Math.min(...m.V.map(p=>p[j]))),max:[0,1,2].map(j=>Math.max(...m.V.map(p=>p[j])))}],pr=[];
for(let k=0;k<MAT.length;k++){let id=m.F.filter(f=>f[3]===k).flatMap(f=>f.slice(0,3));if(!id.length)continue;let bb=new Uint8Array(id.length*4),dv=new DataView(bb.buffer);id.forEach((x,i)=>dv.setUint32(i*4,x,true));let offset=buf.length;buf.push(...bb);views.push({buffer:0,byteOffset:offset,byteLength:bb.length,target:34963});acc.push({bufferView:views.length-1,componentType:5125,count:id.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:acc.length-1,material:k,mode:4});}
let j={asset:{version:"2.0",generator:"G4C7_A23_ART_HOLD"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:MAT.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:x[2],roughnessFactor:.74,metallicFactor:.12},doubleSided:true})),buffers:[{byteLength:buf.length}],bufferViews:views,accessors:acc};
let str=JSON.stringify(j),json=Array.from(str,c=>c.charCodeAt(0));while(json.length%4)json.push(32);while(buf.length%4)buf.push(0);let a=new Uint8Array(28+json.length+buf.length),d=new DataView(a.buffer);
d.setUint32(0,0x46546c67,true);d.setUint32(4,2,true);d.setUint32(8,a.length,true);d.setUint32(12,json.length,true);d.setUint32(16,0x4e4f534a,true);a.set(json,20);let off=20+json.length;d.setUint32(off,buf.length,true);d.setUint32(off+4,0x004e4942,true);a.set(buf,off+8);return b64(a);}
function obj(m){let s=`# G4-C7 A23 ${m.name} ART HOLD\nmtllib a23_materials.mtl\n`;for(let p of m.V)s+=`v ${p.map(x=>x.toFixed(4)).join(" ")}\n`;let prev=-1;for(let f of m.F){if(prev!==f[3])s+=`usemtl ${MAT[f[3]][0]}\n`;prev=f[3];s+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}return s;}
const sub=(a,b)=>a.map((x,k)=>x-b[k]),dot=(a,b)=>a.reduce((s,x,k)=>s+x*b[k],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],norm=a=>a.map(x=>x/Math.hypot(...a));
function svg(view){let eye=C[view],fwd=norm(sub(T,eye)),right=norm(cross([0,1,0],fwd)),up=norm(cross(fwd,right)),W=1470,H=536,P=490;
let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#0c1c2e"/><defs>`;
for(let i=0;i<3;i++)s+=`<clipPath id="v${i}"><rect x="${i*P+6}" y="56" width="478" height="430"/></clipPath>`;
s+=`</defs><text x="1454" y="17" font-size="12" font-family="sans-serif" text-anchor="end" fill="#e1e9f2">A23 ${view.toUpperCase()} · A22 IDENTICAL CAMERA/TARGET/SCALE · ART HOLD</text>`;
for(let i=0;i<3;i++){let m=mods[i],points=m.V.map(v=>{let p=sub(v,T);return [P*i+245+dot(p,right)*S,270-dot(p,up)*S]});
s+=`<rect x="${i*P+6}" y="56" width="478" height="430" fill="#192d3f" stroke="#54778d"/><g clip-path="url(#v${i})">`;
let tris=[];for(let t of m.F){let A=m.V[t[0]],B=m.V[t[1]],D=m.V[t[2]],n=norm(cross(sub(B,A),sub(D,A))),centre=A.map((x,k)=>(x+B[k]+D[k])/3);if(dot(n,sub(eye,centre))<=0)continue;
let orig=MAT[t[3]][1].slice(1),light=Math.max(.39,Math.min(1.23,.77+.34*dot(n,norm([-.45,.83,-.29])))),hex="#"+[0,2,4].map(k=>Math.max(0,Math.min(255,Math.round(parseInt(orig.slice(k,k+2),16)*light))).toString(16).padStart(2,"0")).join("");
tris.push({depth:dot(sub(centre,eye),fwd),hex,xyz:t.slice(0,3).map(k=>points[k].map(x=>x.toFixed(2)).join(",")).join(" ")});}
tris.sort((a,b)=>b.depth-a.depth);for(let t of tris)s+=`<polygon points="${t.xyz}" fill="${t.hex}" stroke="#293d51" stroke-width=".34"/>`;
s+=`</g><text x="${i*P+16}" y="38" font-size="17" font-weight="bold" font-family="sans-serif" fill="white">A23-${"ABC"[i]} ${m.name}</text><text x="${i*P+16}" y="510" font-size="12" font-family="sans-serif" fill="#b8cddc">${m.F.length} triangles / CONSTRUCTION PROHIBITED</text>`;}
return s+"</svg>";}
mods.forEach((m,i)=>{out("a23_"+"abc"[i]+".obj",obj(m));out("a23_"+"abc"[i]+".glb",glb(m),"base64");});
out("a23_materials.mtl",MAT.map(x=>`newmtl ${x[0]}\nKd ${x[2].slice(0,3).join(" ")}\n`).join("\n"));
Object.keys(C).forEach(v=>out("fourview/"+v+"_a23_abc.svg",svg(v)));
out("a23_manifest.json",JSON.stringify({project:"G4-C7 A23",base:"9d14d2bc2232510440d2a4741f2ea2d2c0be729e",camera:C,target:T,scale:S,results:stats,verified:["genuine GLB binary and OBJ geometry constructed","positive independent solid volumes","two incident correctly oriented edges per solid edge","zero degenerate triangles","same four A22 cameras"],unverified:["independent GLB importer","Boolean merging and cross-solid self-intersections","load support and egress","legacy 331/993 route QA","independent four-view human art judgment"],state:"ART HOLD",minecraft_education:"NO CONSTRUCTION",city_integration:"PROHIBITED",historical_assets:"PROTECTED",legacy_limits:{bodies:331,feet:993,halfwidth:.65,foot_relative:[.15,3.25],old_collision_max:45,unsupported_foot_max:0}},null,2));
return{files,stats};};
const r=build();for(let f of r.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==='base64'?Buffer.from(f.content,'base64'):f.content);}
console.log(JSON.stringify(r.stats,null,2));
