// A49 independent semantic-visibility preflight for existing research meshes.
// It reports pixels actually nearest to the camera; NOT an architectural/aesthetic safety certification.
// Use Node: node tools/g4c7_a49_visibility_gate.mjs --baseline
import fs from "node:fs";
import vm from "node:vm";
const BASE="tools/g4c7_a48_inhabited_civic_forum.mjs";
const CAMERAS={
 atrium_arrival:[[0,2.1,-35],[0,9,47],"perspective",0],
 civic_forum:[[0,2.4,1],[0,13,51],"perspective",0],
 market_room:[[8,2,1],[28,8,26],"perspective",0],
 reading_room:[[-8,2,0],[-28,12,28],"perspective",0],
 front:[[0,96,-191],[0,22,20],"ortho",2.26],
 oblique:[[141,119,-146],[0,22,20],"ortho",2.26],
 side:[[193,116,20],[0,22,20],"ortho",2.26],
 aerial:[[131,194,-115],[0,19,20],"ortho",2.26]
};
const ACTIVITY=["market-niches-attached-to-band","culture-performance-center","library-reading-gallery","upper-residential-visible-occupation"];
function analyze(mesh,params,W=560,H=420){
 const [eye,target,mode,scale]=params;
 const sub=(a,b)=>a.map((x,i)=>x-b[i]),dot=(a,b)=>a.reduce((n,x,i)=>n+x*b[i],0);
 const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
 const norm=a=>{let l=Math.hypot(...a)||1;return a.map(x=>x/l);};
 const fw=norm(sub(target,eye)),right=norm(cross([0,1,0],fw)),up=norm(cross(fw,right)),near=2;
 const depth=p=>dot(sub(p,eye),fw),point=p=>{let d=sub(p,eye),t=sub(p,target),z=depth(p);return [W/2+(mode==="perspective"?305*dot(d,right)/z:scale*dot(t,right)),H/2-(mode==="perspective"?305*dot(d,up)/z:scale*dot(t,up)),z];};
 const group=Object.entries(mesh.tags),gid=new Uint8Array(mesh.F.length);
 let start=0;for(let i=0;i<group.length;i++){gid.fill(i+1,start,start+group[i][1]);start+=group[i][1];}
 if(start!==mesh.F.length)throw Error("Semantic group length mismatch: cannot label faces");
 const winner=new Uint8Array(W*H),zbuf=new Float32Array(W*H);zbuf.fill(Infinity);
 function clip(poly){let out=[];for(let k=0;k<poly.length;k++){let a=poly[k],b=poly[(k+1)%poly.length],za=depth(a)-near,zb=depth(b)-near;if(za>=0)out.push(a);if((za<0&&zb>0)||(za>0&&zb<0)){const t=za/(za-zb);out.push(a.map((v,i)=>v+(b[i]-v)*t));}}return out;}
 let clipped=0,discarded=0;
 for(let id=0;id<mesh.F.length;id++){
  const f=mesh.F[id],original=f.slice(0,3).map(i=>mesh.V[i]),behind=original.filter(p=>depth(p)<near).length;
  if(behind===3){discarded++;continue;}
  if(behind)clipped++;
  const poly=behind?clip(original):original;
  for(let k=1;k<poly.length-1;k++){
   const a=point(poly[0]),b=point(poly[k]),c=point(poly[k+1]);
   const area=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);
   if(Math.abs(area)<1e-9)continue;
   const x0=Math.max(0,Math.floor(Math.min(a[0],b[0],c[0]))),x1=Math.min(W-1,Math.ceil(Math.max(a[0],b[0],c[0])));
   const y0=Math.max(0,Math.floor(Math.min(a[1],b[1],c[1]))),y1=Math.min(H-1,Math.ceil(Math.max(a[1],b[1],c[1])));
   for(let y=y0;y<=y1;y++)for(let x=x0;x<=x1;x++){
    const xx=x+.5,yy=y+.5;
    const w1=((xx-a[0])*(c[1]-a[1])-(yy-a[1])*(c[0]-a[0]))/area;
    const w2=((b[0]-a[0])*(yy-a[1])-(b[1]-a[1])*(xx-a[0]))/area;
    const w0=1-w1-w2;
    if(w0<-.00001||w1<-.00001||w2<-.00001)continue;
    const z=mode==="perspective"?1/(w0/a[2]+w1/b[2]+w2/c[2]):(w0*a[2]+w1*b[2]+w2*c[2]),pixel=y*W+x;
    if(z<zbuf[pixel]){zbuf[pixel]=z;winner[pixel]=gid[id];}
   }
  }
 }
 const count=Array(group.length+1).fill(0);for(const id of winner)count[id]++;
 const visible=W*H-count[0];
 const counts=Object.fromEntries(group.map(([name],i)=>[name,count[i+1]]));
 const active=ACTIVITY.reduce((n,k)=>n+(counts[k]||0),0),share=visible?(100*active/visible):0;
 const visibleActivityGroups=ACTIVITY.filter(k=>(counts[k]||0)>0);
 return {size:[W,H],backgroundPixels:count[0],modelPixels:visible,activityPixels:active,activityOfModelPercent:Math.round(share*100)/100,groupPixels:counts,visibleActivityGroups,nearClippedTriangles:clipped,discardedTriangles:discarded};
}
function testOcclusion(){
 function quadAt(z){return [[-1,-1,z],[1,-1,z],[1,1,z],[-1,1,z]];}
 let vertices=[],faces=[];const add=(z,group)=>{const n=vertices.length;vertices.push(...quadAt(z));faces.push([n,n+1,n+2,0],[n,n+2,n+3,0]);};
 add(11,"near");add(20,"far");
 const mesh={V:vertices,F:faces,tags:{near:2,far:2}},camera=[[0,0,0],[0,0,1],"perspective",0];
 let a=analyze(mesh,camera,180,120);
 if(!(a.groupPixels.near>0&&a.groupPixels.far===0))throw Error("Negative control: occluded far face should not be visible");
 // Move both quads past the eye: nothing should be visible.
 const mirrored={...mesh,V:mesh.V.map(([x,y,z])=>[x,y,-z])},b=analyze(mirrored,camera,180,120);
 if(b.modelPixels!==0)throw Error("Negative control: behind-camera polygons should be absent");
 return {frontBlocksFar:true,behindCameraHidden:true,frontPixels:a.groupPixels.near};
}
function main(){
 let base=fs.readFileSync(BASE,"utf8");
 if(!base.includes("function build(){")||!base.includes("import fs from"))throw Error("Unexpected A48 code revision; do not evaluate");
 base=base.slice(0,base.indexOf("import fs from"));
 // Controlled, pinned local first-party source; no inputs or network.
 const built=vm.runInNewContext(base+"\n({build});",{}, {timeout:15000});
 const mesh=built.build();
 const views=Object.fromEntries(Object.entries(CAMERAS).map(([name,params])=>[name,analyze(mesh,params)]));
 const negativeControls=testOcclusion();
 const out={stage:"A49",source:"A48 original real triangle scene",method:"depth-tested nearest-face pixel attribution; camera and semantics reused, no aesthetic certification",width:560,height:420,semanticFaceCounts:mesh.tags,activityKeys:ACTIVITY,views,negativeControls,interpretation:"Screen share is not function readability, does not establish room depth, walkability, construction or visual quality"};
 if(process.argv.includes("--write")){
  const p="artifacts/g4c7-a49-preflight/a48_semantic_visibility_baseline.json";
  if(fs.existsSync(p))throw Error("Refusing to overwrite existing evidence: "+p);
  fs.mkdirSync("artifacts/g4c7-a49-preflight",{recursive:true});
  fs.writeFileSync(p,JSON.stringify(out,null,2)+"\n");
 }
 console.log(JSON.stringify(out,null,2));
}
if(process.argv.includes("--baseline")||process.argv.includes("--write"))main();
export {analyze,testOcclusion,CAMERAS,ACTIVITY};
