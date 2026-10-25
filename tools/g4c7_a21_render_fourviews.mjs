// G4-C7 A21 saved OBJ three-way four-view PNG review. Run: node tools/g4c7_a21_render_fourviews.mjs
import fs from 'node:fs';
const CONF={"cameras":{"front":[0,156,-370],"oblique":[275,218,-270],"side":[385,180,0],"aerial":[180,455,-195]},"target":[0,71,0],"scale":1.26,"pane":408,"height":355};
function render(ms,view){
 const W=CONF.pane*3,H=CONF.height,P=CONF.pane;
 const pix=new Uint8Array(W*H*3),depth=new Float32Array(W*H).fill(Infinity);
 const sub=(a,b)=>a.map((x,i)=>x-b[i]),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],unit=a=>a.map(x=>x/Math.hypot(...a));
 const cam=CONF.cameras[view],fw=unit(sub(CONF.target,cam)),right=unit(cross([0,1,0],fw)),up=unit(cross(fw,right));
 for(let j=0;j<W*H;j++){pix[j*3]=20;pix[j*3+1]=35;pix[j*3+2]=49}
 let pixels=[0,0,0];
 for(let i=0;i<3;i++){
  const {V,F}=ms[i],projected=V.map(v=>{let p=sub(v,CONF.target);return [i*P+P/2+dot(p,right)*CONF.scale,H*.57-dot(p,up)*CONF.scale,dot(sub(v,cam),fw)]});
  for(let [a,b,c] of F){
   const va=V[a],vb=V[b],vc=V[c],n=unit(cross(sub(vb,va),sub(vc,va))),center=va.map((x,k)=>(x+vb[k]+vc[k])/3);
   if(dot(n,sub(cam,center))<=0)continue;
   const A=projected[a],B=projected[b],C=projected[c],area=(B[0]-A[0])*(C[1]-A[1])-(B[1]-A[1])*(C[0]-A[0]);if(Math.abs(area)<1e-8)continue;
   const xlo=Math.max(i*P,Math.floor(Math.min(A[0],B[0],C[0]))),xhi=Math.min((i+1)*P-1,Math.ceil(Math.max(A[0],B[0],C[0]))),ylo=Math.max(0,Math.floor(Math.min(A[1],B[1],C[1]))),yhi=Math.min(H-1,Math.ceil(Math.max(A[1],B[1],C[1])));
   if(xlo>xhi||ylo>yhi)continue;
   const base=n[1]>.70&&center[1]>22&&Math.sin(center[1]*.19)>.38?[225,182,126]:Math.abs(n[1])<.55&&center[1]>29&&Math.abs(center[0])<87&&Math.sin(center[1]*.12+center[2]*.02)>.2?[73,177,186]:n[1]<-.18?[88,111,125]:[210,218,216];
   const light=Math.max(.42,Math.min(1.15,.71+.36*dot(n,unit([-.42,.8,-.32])))),color=base.map(v=>Math.round(Math.max(0,Math.min(255,v*light))));
   for(let y=ylo;y<=yhi;y++)for(let x=xlo;x<=xhi;x++){
    let px=x+.5,py=y+.5,q=((B[0]-px)*(C[1]-py)-(B[1]-py)*(C[0]-px))/area,w=((C[0]-px)*(A[1]-py)-(C[1]-py)*(A[0]-px))/area,u=1-q-w;if(q<-.000001||w<-.000001||u<-.000001)continue;
    const z=q*A[2]+w*B[2]+u*C[2],p=y*W+x;if(z>=depth[p])continue;
    if(depth[p]===Infinity)pixels[i]++;
    depth[p]=z;pix[p*3]=color[0];pix[p*3+1]=color[1];pix[p*3+2]=color[2];
   }
  }
 }
 return{pix,W,H,pixels};
}
function makePng(rgb,W,H){
 function u32(x){return[x>>>24&255,x>>>16&255,x>>>8&255,x&255]}
 const crcTable=new Uint32Array(256);for(let i=0;i<256;i++){let c=i;for(let j=0;j<8;j++)c=c&1?0xedb88320^(c>>>1):c>>>1;crcTable[i]=c>>>0}
 function chunk(name,data){let body=[...name.split("").map(x=>x.charCodeAt(0)),...data],v=0xffffffff;for(const byte of body)v=crcTable[(v^byte)&255]^(v>>>8);return [...u32(data.length),...body,...u32((v^0xffffffff)>>>0)]}
 const raw=new Uint8Array(H*(W*3+1));for(let y=0;y<H;y++)raw.set(rgb.subarray(y*W*3,(y+1)*W*3),y*(W*3+1)+1);
 let x=1,y=0;for(let byte of raw){x=(x+byte)%65521;y=(y+x)%65521}
 const zlib=[120,1];for(let off=0;off<raw.length;off+=65535){let len=Math.min(65535,raw.length-off);zlib.push(off+len===raw.length?1:0,len&255,len>>>8,(~len)&255,((~len)>>>8)&255);for(let i=0;i<len;i++)zlib.push(raw[off+i])}zlib.push(...u32(((y<<16)|x)>>>0));
 return new Uint8Array([137,80,78,71,13,10,26,10,...chunk("IHDR",[...u32(W),...u32(H),8,2,0,0,0]),...chunk("IDAT",zlib),...chunk("IEND",[])]);
}
const models=['a','b','c'].map(k=>{
 const content=fs.readFileSync('artifacts/g4c7-a21-scout/a21_'+k+'.obj','utf8'),V=[],F=[];
 for(const line of content.split('\n')){if(line.startsWith('v '))V.push(line.trim().split(/\s+/).slice(1).map(Number));else if(line.startsWith('f '))F.push(line.trim().split(/\s+/).slice(1).map(x=>parseInt(x)-1))}
 return {V,F};
});
fs.mkdirSync('build/g4c7_a21_fourview',{recursive:true});
for(const view of Object.keys(CONF.cameras)){const im=render(models,view);fs.writeFileSync('build/g4c7_a21_fourview/'+view+'.png',Buffer.from(makePng(im.pix,im.W,im.H)));}
console.log('A21 actual mesh projections ready; ART HOLD / NO MINECRAFT');
