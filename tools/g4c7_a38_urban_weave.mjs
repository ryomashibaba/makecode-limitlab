// A38 reproducible research-only generator; NO MINECRAFT command or world modifications.
import fs from "node:fs"; import path from "node:path";
function modelA38(){
const V=[],F=[],M=[["ivory_frame",[218,229,225]],["shadow_recess",[38,64,82]],["civic_floors",[221,170,114]],["cyan_glass",[79,177,191]],["public_green",[94,157,119]],["library_landmark",[242,225,181]],["promenade",[177,195,194]],["warm_public_lights",[248,196,102]]];
const add=v=>(V.push(v),V.length-1);
const quad=(a,b,c,d,m)=>{let i=add(a),j=add(b),k=add(c),l=add(d);F.push([i,j,k,m],[i,k,l,m])};
function prism(P,lo,hi,m){let b=P.map(p=>[p[0],lo,p[1]]),t=P.map(p=>[p[0],hi,p[1]]);
 for(let k=1;k<P.length-1;k++){F.push([add(b[0]),add(b[k+1]),add(b[k]),m],[add(t[0]),add(t[k]),add(t[k+1]),m]);}
 for(let k=0;k<P.length;k++){let j=(k+1)%P.length;quad(b[k],b[j],t[j],t[k],m);}}
const box=(x,y,z,sx,sy,sz,m)=>prism([[x-sx/2,z-sz/2],[x+sx/2,z-sz/2],[x+sx/2,z+sz/2],[x-sx/2,z+sz/2]],y-sy/2,y+sy/2,m);
function shaft(p,q,w,h,m){let dx=q[0]-p[0],dz=q[2]-p[2],d=Math.hypot(dx,dz)||1,nx=-dz/d*w/2,nz=dx/d*w/2;prism([[p[0]+nx,p[2]+nz],[q[0]+nx,q[2]+nz],[q[0]-nx,q[2]-nz],[p[0]-nx,p[2]-nz]],(p[1]+q[1])/2-h/2,(p[1]+q[1])/2+h/2,m)}
function bent(points,width,height,m){for(let k=0;k<points.length-1;k++){
let p=points[k],q=points[k+1],d=[q[0]-p[0],q[1]-p[1],q[2]-p[2]],l=Math.hypot(...d),t=d.map(v=>v/l),side=[-t[2]*width/2,0,t[0]*width/2],up=[-t[0]*t[1]*height/2,(1-t[1]*t[1])*height/2,-t[2]*t[1]*height/2];
let four=o=>[[o[0]+side[0]+up[0],o[1]+up[1],o[2]+side[2]+up[2]],[o[0]-side[0]+up[0],o[1]+up[1],o[2]-side[2]+up[2]],[o[0]-side[0]-up[0],o[1]-up[1],o[2]-side[2]-up[2]],[o[0]+side[0]-up[0],o[1]-up[1],o[2]+side[2]-up[2]]],a=four(p),b=four(q);
for(let j=0;j<4;j++)quad(a[j],b[j],b[(j+1)%4],a[(j+1)%4],m);
quad(a[3],a[2],a[1],a[0],m);quad(b[0],b[1],b[2],b[3],m);}}
function ring(x,z,r,lo,hi,m,n=12,s=1){prism(Array.from({length:n},(_,k)=>{let a=2*Math.PI*k/n;return[x+r*Math.cos(a),z+s*r*Math.sin(a)]}),lo,hi,m)}
// Spatial grammar: interlocking precincts, occupied urban elevations, the active civic forum and a visible northern destination.
prism([[-194,-170],[-120,-219],[22,-214],[85,-172],[80,-102],[-36,-75],[-147,-94]],0,10,6);
prism([[-197,-169],[-195,47],[-131,133],[-56,80],[-56,-105],[-128,-176]],5,24,0);
prism([[60,-162],[171,-151],[200,-49],[171,106],[104,143],[42,45]],5,24,0);
prism([[-70,55],[43,65],[122,125],[76,203],[-51,202],[-123,118]],7,28,6);
prism([[-102,-110],[85,-110],[105,29],[52,94],[-92,66]],10,18,2);
shaft([0,19,-204],[0,19,20],22,3,6);
for(let z=-167;z<=-35;z+=33){box(-24,21,z,5,6,6,4);box(24,21,z,5,6,6,4);}
for(let k=0;k<6;k++){let z=-150+k*26;box(-40,23,z,5,4,5,4);box(40,23,z+8,5,4,5,4);}
ring(5,-9,29,19,22,2,20,.84);ring(5,-9,17,22,24,4,16,.83);
for(let k=0;k<12;k++){let a=k*Math.PI/6;box(5+Math.cos(a)*27,30,-9+Math.sin(a)*22,3,17,3,0);}
let wp=[[-159,-132],[-151,-67],[-155,-1],[-135,62],[-87,120]];
for(let l=0;l<5;l++){let y=29+l*21;for(let k=0;k<wp.length-1;k++){
let p=wp[k],q=wp[k+1],a=[p[0],y,p[1]],b=[q[0],y,q[1]];
shaft(a,b,37,4,l%2?2:6);shaft([a[0]+14,y+4,a[2]],[b[0]+14,y+4,b[2]],3,12,3);
for(let j=1;j<=4;j++){let t=j/5;box(p[0]*(1-t)+q[0]*t+7,y+11,p[1]*(1-t)+q[1]*t,2.3,19,3,0);}}}
for(let p of wp)box(p[0]-10,82,p[1],9,123,9,0);
for(let k=0;k<4;k++){let p=wp[k],q=wp[k+1];box((p[0]+q[0])/2-12,135,(p[1]+q[1])/2,17,4,26,4);}
const cx=121,cz=-8;for(let l=0;l<4;l++){let y=28+l*26,rad=74-4*l,P=Array.from({length:10},(_,k)=>{let a=-1.25+2.5*k/9;return[cx+rad*Math.cos(a),cz+rad*Math.sin(a)]});
for(let k=0;k<P.length-1;k++){let a=P[k],b=P[k+1];shaft([a[0],y,a[1]],[b[0],y,b[1]],29,4,l%2?2:6);shaft([a[0],y+10,a[1]],[b[0],y+10,b[1]],3,17,3);
if(k%2===0)box(a[0]-14,y+14,a[1],3,21,3,0);}}
for(let a=-1.15;a<=1.2;a+=.41)box(cx+75*Math.cos(a),86,cz+75*Math.sin(a),7,103,7,0);
for(let l=0;l<9;l++){let y=27+l*22,r=48-l*2.7,rot=(l%2)*.12;
let P=Array.from({length:10},(_,k)=>{let a=2*Math.PI*k/10+rot;return[r*Math.cos(a),146+r*.78*Math.sin(a)]});prism(P,y,y+3,l%3===0?5:0);
let glass=Array.from({length:10},(_,k)=>{let a=2*Math.PI*k/10+rot;return[(r-4)*Math.cos(a),146+(r-4)*.78*Math.sin(a)]});
for(let k=0;k<10;k++){let p=glass[k],q=glass[(k+1)%10];shaft([p[0],y+9,p[1]],[q[0],y+9,q[1]],1.4,17,3);}}
ring(0,146,29,226,235,5,10,.72);bent([[0,235,146],[8,260,150]],7,9,5);
bent([[-147,75,12],[-91,82,20],[-21,96,25],[57,108,16],[125,119,-4]],18,7,0);
bent([[-120,118,88],[-51,128,79],[15,143,89],[60,164,117],[12,179,150]],15,8,2);
bent([[-190,28,-145],[-188,75,-105],[-169,130,-30],[-104,190,40],[-29,226,88],[15,232,140]],21,17,0);
bent([[176,27,-104],[183,65,-51],[169,111,13],[126,156,84],[43,210,137]],16,14,0);
bent([[-104,190,40],[-39,201,30],[35,190,54],[126,156,84]],10,8,5);
for(let k=0;k<4;k++){box(-151+23*k,14,-119+8*k,7,19,9,1);box(110+14*k,15,-120+7*k,7,19,9,1);}
bent([[0,26,10],[20,28,61],[18,31,112],[0,35,145]],19,5,6);
for(let k=0;k<9;k++)box(-23+k*6,21+k*.9,89+k*6,4,3,4,4);
for(let [x,z]of [[-49,-71],[49,-62],[-57,13],[66,40],[-65,75],[66,-95]]){box(x,33,z,3,26,3,0);box(x,47,z,23,3,16,5);box(x,26,z,11,3,5,2);}
for(let [x,z]of [[-96,-119],[-89,-79],[-83,25],[-61,74],[91,-106],[102,-67],[92,23],[88,64],[39,145],[-37,137]]){box(x,30,z,4,13,4,1);ring(x,z,9,37,44,4,6,.8);}
for(let z=-112;z<=67;z+=24)for(let y of[39,60,81,102])box(-92,y,z,5,8,15,3);
return{V,F,M};
}
function b64Bytes(a){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];for(let i=0;i<a.length;i+=3){let x=a[i],y=a[i+1]||0,z=a[i+2]||0;out.push(abc[x>>2],abc[((x&3)<<4)|(y>>4)],i+1<a.length?abc[((y&15)<<2)|(z>>6)]:"=",i+2<a.length?abc[z&63]:"=")}return out.join("")}
function objA38(m){let txt="# G4-C7 A38 real mesh / research only / ART HOLD / NO MINECRAFT\nmtllib materials.mtl\n";for(let p of m.V)txt+="v "+p.join(" ")+"\n";let old=-1;for(let f of m.F){if(old!==f[3]){old=f[3];txt+="usemtl "+m.M[old][0]+"\n";}txt+="f "+(f[0]+1)+" "+(f[1]+1)+" "+(f[2]+1)+"\n";}return txt}
function glbA38(m){let v=m.V,f=m.F,nb=v.length*12,indexGroups=m.M.map((_,i)=>f.filter(p=>p[3]===i).flatMap(p=>p.slice(0,3))),offset=nb;const buf=[],views=[{buffer:0,byteOffset:0,byteLength:nb,target:34962}],accessors=[{bufferView:0,componentType:5126,count:v.length,type:"VEC3",min:[0,1,2].map(k=>Math.min(...v.map(p=>p[k]))),max:[0,1,2].map(k=>Math.max(...v.map(p=>p[k])))}],pr=[];
let pos=new Uint8Array(nb),pd=new DataView(pos.buffer);for(let i=0;i<v.length;i++)for(let k=0;k<3;k++)pd.setFloat32(i*12+k*4,v[i][k],true);for(let x of pos)buf.push(x);
for(let i=0;i<indexGroups.length;i++){let ids=indexGroups[i];if(!ids.length)continue;let raw=new Uint8Array(ids.length*4),dv=new DataView(raw.buffer);ids.forEach((id,k)=>dv.setUint32(4*k,id,true));views.push({buffer:0,byteOffset:offset,byteLength:raw.length,target:34963});accessors.push({bufferView:views.length-1,componentType:5125,count:ids.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:accessors.length-1,material:i,mode:4});for(let x of raw)buf.push(x);offset+=raw.length;}
while(buf.length%4)buf.push(0);
let document={asset:{version:"2.0",generator:"G4-C7 A38 research mesh"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0}],meshes:[{primitives:pr}],materials:m.M.map(x=>({name:x[0],pbrMetallicRoughness:{baseColorFactor:[...x[1].map(a=>a/255),1],metallicFactor:0.05,roughnessFactor:0.77},doubleSided:true})),buffers:[{byteLength:buf.length}],bufferViews:views,accessors},s=JSON.stringify(document),js=Array.from(s).map(c=>c.charCodeAt(0));while(js.length%4)js.push(32);
let full=new Uint8Array(28+js.length+buf.length),dv=new DataView(full.buffer);dv.setUint32(0,0x46546c67,true);dv.setUint32(4,2,true);dv.setUint32(8,full.length,true);dv.setUint32(12,js.length,true);dv.setUint32(16,0x4e4f534a,true);full.set(js,20);let at=20+js.length;dv.setUint32(at,buf.length,true);dv.setUint32(at+4,0x004e4942,true);full.set(buf,at+8);
return{b64:b64Bytes(full),bytes:full.length,json:document,headerValid:dv.getUint32(8,true)===full.length,indicesValid:Math.max(...indexGroups.flat())<v.length};}
function pngA38(m,eye,target,W=650,H=540,scale=.95){
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),norm=a=>{let l=Math.hypot(...a)||1;return a.map(x=>x/l)};
let fw=norm(sub(target,eye)),rt=norm(cross([0,1,0],fw)),up=norm(cross(fw,rt)),light=norm([-.4,.88,-.25]),P=m.V.map(p=>{let v=sub(p,target);return[W/2+scale*dot(v,rt),H/2-scale*dot(v,up),dot(sub(p,eye),fw)]});
let palette=[[26,46,66]];for(let [name,col]of m.M)for(let s=0;s<8;s++){let c=.4+s*.105;palette.push(col.map(x=>Math.max(0,Math.min(255,Math.round(x*c)))))}
let pix=new Uint8Array(W*H),depth=new Float64Array(W*H);depth.fill(Infinity);
for(let a of m.F){let i=a[0],j=a[1],k=a[2],p=P[i],q=P[j],t=P[k];if(p[2]<=1||q[2]<=1||t[2]<=1)continue;
let normal=norm(cross(sub(m.V[j],m.V[i]),sub(m.V[k],m.V[i]))),shade=Math.max(0,Math.min(7,Math.round(2+5*Math.max(0,dot(normal,light))))),idx=1+a[3]*8+shade;
let x0=Math.max(0,Math.floor(Math.min(p[0],q[0],t[0]))),x1=Math.min(W-1,Math.ceil(Math.max(p[0],q[0],t[0]))),y0=Math.max(0,Math.floor(Math.min(p[1],q[1],t[1]))),y1=Math.min(H-1,Math.ceil(Math.max(p[1],q[1],t[1]))),area=(q[0]-p[0])*(t[1]-p[1])-(q[1]-p[1])*(t[0]-p[0]);if(Math.abs(area)<1e-8)continue;
for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){let sx=x+.5,sy=y+.5,b=((sx-p[0])*(t[1]-p[1])-(sy-p[1])*(t[0]-p[0]))/area,c=((q[0]-p[0])*(sy-p[1])-(q[1]-p[1])*(sx-p[0]))/area,aa=1-b-c;if(aa<-.00001||b<-.00001||c<-.00001)continue;let z=aa*p[2]+b*q[2]+c*t[2],ix=y*W+x;if(z<depth[ix]){depth[ix]=z;pix[ix]=idx;}}}
const u32=n=>[(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255],raw=[];for(let y=0;y<H;y++){raw.push(0);for(let x=0;x<W;x++)raw.push(pix[y*W+x]);}
let table=Array.from({length:256},(_,n)=>{let c=n;for(let i=0;i<8;i++)c=c&1?0xedb88320^(c>>>1):c>>>1;return c>>>0});
let crc=a=>{let c=0xffffffff;for(let b of a)c=table[(c^b)&255]^(c>>>8);return(c^0xffffffff)>>>0};
let chunk=(name,p)=>{let bytes=Array.from(name).map(x=>x.charCodeAt(0));return[...u32(p.length),...bytes,...p,...u32(crc([...bytes,...p]))]};
let ad1=1,ad2=0;for(let x of raw){ad1=(ad1+x)%65521;ad2=(ad2+ad1)%65521}
let zip=[120,1];for(let off=0;off<raw.length;){let n=Math.min(65535,raw.length-off),last=(off+n===raw.length)?1:0;zip.push(last,n&255,(n>>8)&255,(~n)&255,((~n)>>8)&255,...raw.slice(off,off+n));off+=n}zip.push(...u32(((ad2<<16)|ad1)>>>0));
let png=[137,80,78,71,13,10,26,10,...chunk("IHDR",[...u32(W),...u32(H),8,3,0,0,0]),...chunk("PLTE",palette.flat()),...chunk("IDAT",zip),...chunk("IEND",[])];
return{b64:b64Bytes(png),bytes:png.length,nonBg:pix.reduce((s,n)=>s+(n>0),0)};}
const root="artifacts/g4c7-a38-urban-weave-scout/"; const m=modelA38(); const g=glbA38(m); const save=(p,s,enc="utf8")=>{const to=root+p;fs.mkdirSync(path.dirname(to),{recursive:true});fs.writeFileSync(to,enc==="base64"?Buffer.from(s.replace(/\s/g,""),"base64"):s)};
save("a38_urban_weave.obj",objA38(m));save("a38_urban_weave.glb",g.b64,"base64");save("materials.mtl",m.M.map(v=>"newmtl "+v[0]+"\\nKd "+v[1].map(x=>x/255).join(" ")+"\\n").join(""));const cameras={"front":[[0,220,-450],[0,78,0]],"oblique":[[350,282,-365],[0,78,0]],"side":[[465,225,0],[0,78,0]],"aerial":[[250,525,-270],[0,78,0]],"interior_south":[[0,63,-151],[0,80,135]]};for(let [k,[eye,target]] of Object.entries(cameras))save("verified-png/"+k+".png",pngA38(m,eye,target).b64,"base64");console.log("A38 research 3D generated:",m.V.length,m.F.length,g.bytes);
