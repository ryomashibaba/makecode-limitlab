import fs from 'node:fs'; import path from 'node:path';
const C={"start":[-135,-10,-125],"step":12.5,"count":[23,19,21],"modes":[["a","TIDAL FJORD"],["b","POROUS CONTINENT"],["c","ASCENDING ESTUARY"]]};
function ell(x,y,z,p){const[a,b,c,d,e,f]=p;return(1-Math.pow((x-a)/d,2)-Math.pow((y-b)/e,2)-Math.pow((z-c)/f,2))*32}
function deck(x,y,z,p){const[a,b,c,d,e]=p;return Math.min(y-b+3,b+3-y,(1-Math.pow((x-a)/d,2)-Math.pow((z-c)/e,2))*17)}
function val(t,x,y,z){
 const base=(1-Math.pow(Math.abs(x/126),4)-Math.pow(Math.abs(z/114),4))*43;let h,s;
 if(t==="a"){
 h=104+29*Math.sin(.024*x+.012*z)+30*Math.exp(-(Math.pow((x-49)/65,2)+Math.pow((z+7)/58,2)))+18*x/128+9*Math.cos(.05*z);s=Math.min(y+4,h-y,base);
 let g=-10+18*Math.sin((z+38)*.027);s=Math.min(s,-Math.min(22-Math.abs(x-g),y-17,44-z,z+135));
 for(const p of [[-43,64,-7,52,34,51],[29,98,5,55,33,61],[-19,128,24,48,29,48]])s=Math.min(s,-ell(x,y,z,p));
 for(const p of [[-35,40,-9,66,59],[35,75,7,65,57],[-28,109,17,61,51]])s=Math.max(s,deck(x,y,z,p));
 }else if(t==="b"){
 h=78+72*Math.exp(-Math.pow((x+.32*z)/94,2))*(.65+.35*Math.sin((z+120)*.018))+23*Math.cos(x*.029+z*.018);
 s=Math.min(y+4,h-y,base);
 for(const p of [[-25,69,-22,57,38,62],[28,111,14,56,35,55],[-40,131,35,42,30,45],[55,65,35,42,27,39],[-1,99,-61,46,29,46]])s=Math.min(s,-ell(x,y,z,p));
 for(const p of [[-22,43.7,-24,75,66],[27,80.7,8,74,61],[-30,114.7,26,59,56]])s=Math.max(s,deck(x,y,z,p));
 }else{
 h=59+103/(1+Math.exp(-(x+15)/35))+27*Math.sin(.028*z-.013*x)+12*Math.cos((x+z)*.02);s=Math.min(y+4,h-y,base);
 let g=-18+28*Math.sin((z+28)*.026);s=Math.min(s,-Math.min(19-Math.abs(x-g),y-24,68-z,z+129));
 for(const p of [[-26,61,-39,58,32,45],[23,98,-5,58,39,62],[64,137,41,46,36,49]])s=Math.min(s,-ell(x,y,z,p));
 for(const p of [[-28,39.7,-28,71,65],[24,77.7,-8,66,59],[55,113.7,27,58,54]])s=Math.max(s,deck(x,y,z,p));
 }
 return s;
}
function gen(type){
 const [NX,NY,NZ]=C.count,[x0,y0,z0]=C.start,s=C.step,I=(i,j,k)=>(i*NY+j)*NZ+k,F=new Float32Array(NX*NY*NZ);
 for(let i=0;i<NX;i++)for(let j=0;j<NY;j++)for(let k=0;k<NZ;k++){let x=val(type,x0+i*s,y0+j*s,z0+k*s);F[I(i,j,k)]=Math.abs(x)<.0001?-.0001:x}
 const O=[[0,0,0],[1,0,0],[1,1,0],[0,1,0],[0,0,1],[1,0,1],[1,1,1],[0,1,1]],
 TE=[[0,5,1,6],[0,1,2,6],[0,2,3,6],[0,3,7,6],[0,7,4,6],[0,4,5,6]],V=[],faces=[],cache=new Map();
 const pos=t=>[Math.floor(t/(NY*NZ)),Math.floor(t/NZ)%NY,t%NZ],sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((v,x,i)=>v+x*b[i],0);
 function point(a,b){let key=a<b?a+","+b:b+","+a;if(cache.has(key))return cache.get(key);let p=pos(a),q=pos(b),t=F[a]/(F[a]-F[b]),v=[x0+(p[0]+(q[0]-p[0])*t)*s,y0+(p[1]+(q[1]-p[1])*t)*s,z0+(p[2]+(q[2]-p[2])*t)*s],id=V.length;V.push(v);cache.set(key,id);return id}
 function tri(f,inside,outside){let[a,b,c]=f.map(i=>V[i]),n=cross(sub(b,a),sub(c,a));if(Math.hypot(...n)<1e-9)return;let mean=q=>q.reduce((v,t)=>v.map((x,i)=>x+pos(t)[i]/q.length),[0,0,0]);if(dot(n,sub(mean(outside),mean(inside)))<0)[f[1],f[2]]=[f[2],f[1]];faces.push(f)}
 for(let i=0;i<NX-1;i++)for(let j=0;j<NY-1;j++)for(let k=0;k<NZ-1;k++){const c=O.map(([a,b,d])=>I(i+a,j+b,k+d)),n=c.filter(q=>F[q]>0).length;if(n===0||n===8)continue;
  for(let t of TE){let q=t.map(v=>c[v]),a=q.filter(v=>F[v]>0),b=q.filter(v=>F[v]<=0);if(!a.length||!b.length)continue;
   if(a.length===1)tri(b.map(v=>point(a[0],v)),a,b);
   else if(b.length===1)tri(a.map(v=>point(b[0],v)),a,b);
   else{let p=point(a[0],b[0]),q=point(a[0],b[1]),r=point(a[1],b[1]),u=point(a[1],b[0]);tri([p,q,r],a,b);tri([p,r,u],a,b)}
  }
 }
 let uf=Array.from({length:V.length},(_,i)=>i);
 function root(i){while(uf[i]!==i){uf[i]=uf[uf[i]];i=uf[i]}return i}
 for(let f of faces){let a=root(f[0]);for(let i=1;i<3;i++){let b=root(f[i]);if(a!==b)uf[b]=a}}
 let comp=new Map();for(let f of faces){let k=root(f[0]);comp.set(k,(comp.get(k)||0)+1)}
 let best=[...comp].sort((a,b)=>b[1]-a[1])[0],dropped=faces.length-best[1];
 if(dropped>faces.length*.025)throw Error("Disconnected geometry too large: "+type+" "+dropped+"/"+faces.length);
 const chosen=faces.filter(f=>root(f[0])===best[0]),map=new Map(),verts=[];
 const tris=chosen.map(f=>f.map(i=>{if(!map.has(i)){map.set(i,verts.length);verts.push(V[i])}return map.get(i)}));
 let edge=new Map(),volume=0;
 for(let [a,b,c] of tris){volume+=dot(verts[a],cross(verts[b],verts[c]))/6;for(let [p,q] of [[a,b],[b,c],[c,a]]){let key=p<q?p+","+q:q+","+p,entry=edge.get(key)||[0,0];entry[0]++;entry[1]+=p<q?1:-1;edge.set(key,entry)}}
 const qa={variant:type,original_connected_pieces:comp.size,detached_faces_explicitly_removed:dropped,removed_ratio:+(dropped/faces.length).toFixed(6),vertices:verts.length,triangles:tris.length,edge_boundary_failures:[...edge.values()].filter(v=>v[0]!==2).length,edge_orientation_failures:[...edge.values()].filter(v=>v[1]!==0).length,signed_volume:Math.round(volume),art:"HOLD",legacy_route_331_993:"NOT TESTED",structure:"NOT VERIFIED"};
 return {type,verts,tris,qa};
}
function obj(m){let o="# A21 ART HOLD / Y-up / real iso-surface / no Minecraft\n";for(let p of m.verts)o+="v "+p.map(x=>x.toFixed(4)).join(" ")+"\n";for(let f of m.tris)o+="f "+f.map(i=>i+1).join(" ")+"\n";return o}
function b64(b){const a="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",r=[];for(let i=0;i<b.length;i+=3){let x=(b[i]<<16)|((b[i+1]||0)<<8)|(b[i+2]||0);r.push(a[x>>>18&63]+a[x>>>12&63]+(i+1<b.length?a[x>>>6&63]:"=")+(i+2<b.length?a[x&63]:"="))}return r.join("")}
function glb(m){
 const vbytes=m.verts.length*12,bytes=new Uint8Array(vbytes+m.tris.length*12),d=new DataView(bytes.buffer);
 const mn=[Infinity,Infinity,Infinity],mx=[-Infinity,-Infinity,-Infinity];
 m.verts.forEach((v,i)=>v.forEach((x,k)=>{d.setFloat32(i*12+k*4,x,true);mn[k]=Math.min(mn[k],x);mx[k]=Math.max(mx[k],x)}));
 let p=vbytes;for(let f of m.tris)for(let i of f){d.setUint32(p,i,true);p+=4}
 const j={asset:{version:"2.0",generator:"G4-C7 A21 continuous void city ART HOLD"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:[{attributes:{POSITION:0},indices:1,material:0}]}],materials:[{name:"limestone megastructure",doubleSided:true,pbrMetallicRoughness:{baseColorFactor:[.79,.85,.87,1],roughnessFactor:.65,metallicFactor:.08}}],buffers:[{byteLength:bytes.length}],bufferViews:[{buffer:0,byteOffset:0,byteLength:vbytes,target:34962},{buffer:0,byteOffset:vbytes,byteLength:m.tris.length*12,target:34963}],accessors:[{bufferView:0,componentType:5126,count:m.verts.length,type:"VEC3",min:mn,max:mx},{bufferView:1,componentType:5125,count:m.tris.length*3,type:"SCALAR"}]};
 let src=JSON.stringify(j),txt=new Uint8Array(src.length);for(let i=0;i<src.length;i++)txt[i]=src.charCodeAt(i);
 let jp=(4-txt.length%4)%4,bp=(4-bytes.length%4)%4,out=new Uint8Array(12+8+txt.length+jp+8+bytes.length+bp),dv=new DataView(out.buffer);
 dv.setUint32(0,0x46546c67,true);dv.setUint32(4,2,true);dv.setUint32(8,out.length,true);dv.setUint32(12,txt.length+jp,true);dv.setUint32(16,0x4e4f534a,true);out.set(txt,20);out.fill(32,20+txt.length,20+txt.length+jp);let o=20+txt.length+jp;dv.setUint32(o,bytes.length+bp,true);dv.setUint32(o+4,0x004e4942,true);out.set(bytes,o+8);
 return b64(out);
}
const ms=C.modes.map(([t])=>gen(t));
for(let m of ms){if(m.qa.edge_boundary_failures||m.qa.edge_orientation_failures||m.qa.signed_volume<=0)throw Error('Geometry gate failed');}
fs.mkdirSync('build/g4c7_a21',{recursive:true});
for(let m of ms){fs.writeFileSync('build/g4c7_a21/'+m.type+'.obj',obj(m));fs.writeFileSync('build/g4c7_a21/'+m.type+'.glb',Buffer.from(glb(m),'base64'));}
fs.writeFileSync('build/g4c7_a21/qa.json',JSON.stringify(ms.map(m=>m.qa),null,2));
console.log('A21 ART HOLD / NO MINECRAFT',ms.map(m=>m.qa));
