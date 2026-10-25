#!/usr/bin/env node
// G4-C7 A25 independent true 3D ART-FIRST concept study. No world construction or OLD asset overwrites.
import fs from 'node:fs';import path from 'node:path';
const buildA25=function buildA25(){
const ROOT="artifacts/g4c7-a25-urban-life-scout/",CAM={front:[0,220,-450],oblique:[350,282,-365],side:[465,225,0],aerial:[250,525,-270]},TARGET=[0,78,0],SCALE=1.03;
const MAT=[
{name:"pale_ceramic",hex:"#d3e1e6",rgba:[.827,.882,.902,1]},
{name:"graphite_support",hex:"#4d6477",rgba:[.302,.392,.467,1]},
{name:"inhabited_glass",hex:"#64bfc6",rgba:[.392,.749,.776,1]},
{name:"public_terrace",hex:"#e7bb84",rgba:[.906,.733,.518,1]},
{name:"garden",hex:"#71ad8b",rgba:[.443,.678,.545,1]},
{name:"warm_copper",hex:"#bb906f",rgba:[.733,.565,.435,1]},
{name:"deep_urban",hex:"#8597aa",rgba:[.522,.592,.667,1]}
];
const sub=(a,b)=>a.map((x,i)=>x-b[i]),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],dot=(a,b)=>a.reduce((v,x,i)=>v+x*b[i],0),norm=a=>a.map(x=>x/Math.hypot(...a));
function fresh(id,name,principle){return {id,name,principle,V:[],F:[],parts:[],activity:{public_courts:0,inhabited_rooms:0,sky_walks:0,green_roofs:0,bridges:0},cityVoid:null};}
function addSolid(m,verts,tris,mat,label){
 let areaBad=0,vol=0,edges=new Map(),directed=new Map();
 for(let t of tris){let A=verts[t[0]],B=verts[t[1]],C=verts[t[2]],n=cross(sub(B,A),sub(C,A));if(Math.hypot(...n)<1e-6)areaBad++;vol+=dot(A,cross(B,C))/6;}
 if(vol<0){tris=tris.map(x=>[x[0],x[2],x[1]]);vol=-vol;}
 for(let t of tris)for(let i=0;i<3;i++){let a=t[i],b=t[(i+1)%3],k=Math.min(a,b)+":"+Math.max(a,b),o=a+":"+b;edges.set(k,(edges.get(k)||0)+1);directed.set(o,(directed.get(o)||0)+1);}
 let unpaired=0,orientation=0;
 for(let [key,n] of edges){if(n!==2)unpaired++;let [a,b]=key.split(":");if((directed.get(a+":"+b)||0)!==1||(directed.get(b+":"+a)||0)!==1)orientation++;}
 if(areaBad||unpaired||orientation||vol<1e-5)throw Error("A25 face topology failure "+label+" "+JSON.stringify({areaBad,unpaired,orientation,vol}));
 let base=m.V.length;m.V.push(...verts);m.F.push(...tris.map(t=>[t[0]+base,t[1]+base,t[2]+base,mat]));m.parts.push({label,triangles:tris.length,positive_volume:+vol.toFixed(3)});
}
function extrude(m,polygon,y0,y1,mat,label){
 let n=polygon.length,area=polygon.reduce((s,p,i)=>{let q=polygon[(i+1)%n];return s+p[0]*q[1]-p[1]*q[0]},0);
 if(Math.abs(area)<.001||y1<=y0)throw Error("bad footprint "+label);
 let P=area>=0?polygon:[...polygon].reverse(),V=[],F=[];
 for(let y of [y0,y1])for(let p of P)V.push([p[0],y,p[1]]);
 for(let j=1;j<n-1;j++){F.push([0,j+1,j],[n,n+j,n+j+1]);}
 for(let j=0;j<n;j++){let k=(j+1)%n;F.push([j,k,n+k],[j,n+k,n+j]);}
 addSolid(m,V,F,mat,label);
}
function rect(cx,cz,w,d,ang=0){let c=Math.cos(ang),s=Math.sin(ang);return [[-w/2,-d/2],[w/2,-d/2],[w/2,d/2],[-w/2,d/2]].map(([x,z])=>[cx+x*c-z*s,cz+x*s+z*c]);}
function prism(m,x,z,w,d,y0,y1,mat,label,ang=0){extrude(m,rect(x,z,w,d,ang),y0,y1,mat,label);}
function link(m,x0,z0,x1,z1,width,y0,y1,mat,label){let dx=x1-x0,dz=z1-z0,l=Math.hypot(dx,dz);if(l<.1)throw Error("zero link");let px=-dz/l*width/2,pz=dx/l*width/2;extrude(m,[[x0+px,z0+pz],[x1+px,z1+pz],[x1-px,z1-pz],[x0-px,z0-pz]],y0,y1,mat,label);}
function footprintLocal(x,z,w,d,angle=0){return rect(x,z,w,d,angle);}
function transform(p,cx,cz,angle){let c=Math.cos(angle),s=Math.sin(angle);return [cx+p[0]*c-p[1]*s,cz+p[0]*s+p[1]*c];}
function room(m,x,z,w,d,y,h,ang,label,facade=1){
 prism(m,x,z,w,d,y,y+h,0,label+"_inhabited_volume",ang);m.activity.inhabited_rooms++;
 // public-facing glazed frontage is geometric not a texture; front occupies substantial visible area
 let p=transform([0,-d*.50-.55],x,z,ang);prism(m,p[0],p[1],w*.78,1.35,y+2.6,y+Math.min(h-1.3,9.2),2,label+"_street_facing_glazing",ang);
 // lower atrium lintel and asymmetrical roof cornice
 let q=transform([0,-d*.50-.3],x,z,ang);
 prism(m,q[0],q[1],w*.87,1.6,y+h-2.3,y+h-1.2,5,label+"_facade_cornice",ang);
 if(facade&&h>=16){let p2=transform([0,d*.50+.4],x,z,ang);prism(m,p2[0],p2[1],w*.7,1,y+5,y+12,2,label+"_rear_occupied_glazing",ang);}
}
function tower(m,x,z,w,d,y0,height,ang,label){
 // the elevated tower is not a blank monolith: floor and glazing cadence creates readable habitation
 prism(m,x,z,w,d,y0,y0+height,6,label+"_structural_habitation",ang);
 for(let j=0;j<Math.floor(height/15);j++){
 let y=y0+j*15+5;
 for(let side of [-1,1]){let p=transform([side*(w/2+.55),0],x,z,ang);prism(m,p[0],p[1],1.2,d*.70,y,y+8.1,2,label+"_city_window_"+j+"_"+side,ang);}
 let q=transform([0,-d/2-.5],x,z,ang);prism(m,q[0],q[1],w*.8,1,y+1,y+8,2,label+"_visible_living_band_"+j,ang);
 if(j%2===0){prism(m,x,z,w+4,d+3,y+10.2,y+12.2,3,label+"_high_public_balcony_"+j,ang);m.activity.sky_walks++;}
 }
 prism(m,x,z,w+7,d+7,y0+height-2,y0+height+1,5,label+"_crown_of_occupied_tower",ang);
}
function pergola(m,x,z,w,d,y,ang,label){
 for(let dx of [-w*.42,w*.42]){let q=transform([dx,0],x,z,ang);prism(m,q[0],q[1],1.6,d*.84,y,y+11,1,label+"_column_"+dx,ang);}
 for(let t=0;t<4;t++){let zz=(-.33+t*.22)*d,q=transform([0,zz],x,z,ang);prism(m,q[0],q[1],w*.87,1.5,y+10,y+12,0,label+"_canopy_member_"+t,ang);}
}
function district(m,{id,cx,cz,ang=0,base=19,levels=4,levelGap=22,spanW=74,spanD=68,stagger=1.7,towerAt="rear",roomRows=2}){
 const map=(x,z)=>transform([x,z],cx,cz,ang),p=(x,z,w,d,y0,y1,mat,label)=>{let q=map(x,z);prism(m,q[0],q[1],w,d,y0,y1,mat,id+"_"+label,ang);};
 // the habitable city forms the visible architecture: each publicly connected level has an inhabited street and multiple rooms
 // sparse grounded support (no full blank enclosing city wall)
 for(let dx of [-spanW*.36,spanW*.36])for(let zz of [-spanD*.29,spanD*.29]){
   p(dx,zz,7,8,-4,base+2,1,"grounded_spatial_support_"+dx+"_"+zz);
 }
 for(let lv=0;lv<levels;lv++){
 let y=base+levelGap*lv,shift=stagger*(lv%3-1),deckW=spanW-lv*2.4,deckD=spanD-lv*2.1;
 p(shift,0,deckW,deckD,y,y+3,3,"occupied_public_floor_"+lv);m.activity.sky_walks++;m.activity.public_courts++;
 // open central alley 15m wide: two edge-set rows of inhabitable rooms, staggered to read from distance
 for(let side of [-1,1]){
  let roomX=shift+side*(deckW*.28),roomW=deckW*.28;
  for(let j=0;j<3;j++){
   let z=-deckD*.28+j*deckD*.275,roomD=deckD*.21,roomHeight=11+((lv+j+(side>0?2:0))%3)*2.8;
   let P=map(roomX,z);room(m,P[0],P[1],roomW,roomD,y+3,roomHeight,ang,id+"_room_"+lv+"_"+side+"_"+j);
   if((lv+j+(side>0?0:1))%4===0){
    let Q=map(roomX,z+roomD*.25);
    prism(m,Q[0],Q[1],roomW*.50,roomD*.4,y+3+roomHeight,y+6+roomHeight,4,id+"_inhabited_roof_garden_"+lv+"_"+side+"_"+j,ang);m.activity.green_roofs++;
   }
  }
 }
 // outward facing populated balconies, not garages
 for(let side of [-1,1]){
 let q=map(shift+side*(deckW*.45),-deckD*.08);
 prism(m,q[0],q[1],deckW*.10,deckD*.46,y+3,y+6,5,id+"_open_city_balcony_"+lv+"_"+side,ang);
 }
 if(lv===1||lv===levels-1){let pt=map(0,deckD*.38),x=pt[0],z=pt[1];prism(m,x,z,deckW*.64,9,y+3,y+5,4,id+"_sky_park_front_"+lv,ang);m.activity.green_roofs++;}
 }
 if(towerAt!=="none"){
 let t=map(towerAt==="rear"?-spanW*.36:spanW*.31,spanD*.31);
 tower(m,t[0],t[1],17,21,base+levels*levelGap-18,27+(levels%3)*11,ang,id+"_skyward_corner_block");
 }
}
function makeA(){
 let m=fresh("a","INHABITED CIVIC ATRIUM","atrium of public life: a visibly open central void with three asymmetric dense inhabited terraces");
 m.cityVoid={public_open_area:"approx 86 x 76 conceptual units",vertical_clearance:"open sky; bounding housing levels deliberately unequal",type:"inward-open skyline without continuous circular or paired blank shells"};
 extrude(m,[[-156,-111],[-89,-128],[19,-118],[131,-83],[155,-12],[132,85],[53,121],[-65,126],[-151,81]],-4,5,1,"grounded_civic_foundation");
 // central urban public square is large and literally open to sky in the resulting mesh
 extrude(m,[[-52,-46],[40,-53],[56,-14],[47,35],[-31,49],[-60,15]],5,9,3,"wide_exposed_civic_agora");m.activity.public_courts++;
 prism(m,-12,14,45,22,9,12,4,"inhabited_agora_court_garden");
 // 3 asymmetric urban districts, with the plaza open south-front and northeast views, no enclosing ring
 district(m,{id:"west_civic_borough",cx:-104,cz:5,ang:-.16,base:17,levels:4,levelGap:22,spanW:78,spanD:86,stagger:-4});
 district(m,{id:"northeast_high_borough",cx:63,cz:81,ang:.26,base:29,levels:5,levelGap:23,spanW:87,spanD:81,stagger:5});
 district(m,{id:"southeast_low_borough",cx:112,cz:-74,ang:-.48,base:13,levels:3,levelGap:25,spanW:70,spanD:70,stagger:-3});
 // Public bridges only where they have clear urban destinations. Below bridges remains a large walkable visual void (not walk-QA certified).
 link(m,-75,21,-7,31,13,39,43,3,"west_to_agora_occupied_promenade");m.activity.bridges++;
 link(m,27,55,65,50,12,77,81,3,"agora_to_upper_borough_public_gallery");m.activity.bridges++;
 link(m,38,-22,85,-51,13,41,45,3,"east_lower_urban_bridge");m.activity.bridges++;
 link(m,-55,54,38,78,11,110,114,5,"upper_cross_section_city_bridge");m.activity.bridges++;
 // Central high atrium remains unroofed; some grounded inhabited public buildings border it.
 room(m,-36,-36,29,20,9,22,-.11,"agora_west_civic_hall");
 room(m,39,-30,27,24,9,18,.13,"agora_east_gallery");
 pergola(m,5,-53,47,23,9,0,"open_street_pergola");
 // Occupiable city skyline is primary, structural ribs secondary, one irregular rising canopy wing is anchored visibly into urban district
 link(m,-126,68,-90,107,12,93,102,0,"west_urban_rising_roof_edge");
 link(m,30,106,98,113,16,125,132,0,"high_borough_skyline_fin");
 return m;
}
function makeB(){
 let m=fresh("b","LIVING SKY CONFLUENCE","multiple staggered city-sized neighborhoods join around a three-level open civic chasm; city floors and facade are the structure");
 m.cityVoid={public_open_area:"two linked city-scale open rooms instead of a ring",vertical_clearance:"three sky-exposed clearances among inhabited terraces",type:"urban crossroads with varied heights"};
 extrude(m,[[-145,-100],[-23,-151],[101,-133],[150,-55],[137,55],[67,139],[-68,136],[-146,44]],-4,9,1,"connected_granular_city_podium");
 // asymmetric neighborhood distribution: four stacked plateaus set on sloping urban spine, each genuinely inhabited
 district(m,{id:"central_skyquarter",cx:-38,cz:-61,ang:.22,base:16,levels:4,levelGap:21,spanW:84,spanD:79,stagger:3,towerAt:"rear"});
 district(m,{id:"east_open_terraces",cx:76,cz:-12,ang:-.42,base:31,levels:4,levelGap:25,spanW:89,spanD:83,stagger:-4,towerAt:"rear"});
 district(m,{id:"north_ascending_city",cx:11,cz:99,ang:.35,base:43,levels:5,levelGap:23,spanW:89,spanD:75,stagger:7,towerAt:"rear"});
 district(m,{id:"west_urban_gate",cx:-119,cz:69,ang:-.25,base:11,levels:3,levelGap:20,spanW:64,spanD:72,stagger:-2,towerAt:"none"});
 // Real public floors create linked vertical spatial sequence; not giant passive facade.
 extrude(m,[[-71,-12],[6,-28],[45,9],[19,55],[-54,43]],9,13,3,"ground_urban_festival_court");m.activity.public_courts++;
 extrude(m,[[-40,32],[39,35],[62,79],[8,104],[-41,87]],23,27,3,"rising_civic_upper_agora");m.activity.public_courts++;
 link(m,-77,-16,-24,2,16,39,44,3,"west_to_central_inhabited_boulevard");m.activity.bridges++;
 link(m,8,-7,52,-4,14,59,64,3,"central_to_east_urban_terrace_connection");m.activity.bridges++;
 link(m,35,43,9,67,17,85,90,3,"east_to_north_living_square_connection");m.activity.bridges++;
 link(m,-72,57,-21,71,14,65,70,5,"west_gate_to_north_city_connection");m.activity.bridges++;
 link(m,-20,12,40,47,12,117,123,3,"uppercity_air_public_promenade");m.activity.bridges++;
 // The open civic chasm remains visually large through gaps between quarters, not manufactured as a hole behind a blank slab.
 room(m,20,20,32,26,13,24,.09,"public_civic_market_hall");
 room(m,-52,42,24,25,13,19,-.22,"active_social_gallery");
 pergola(m,7,52,32,37,27,.16,"high_garden_city_pergola");
 return m;
}
const models=[makeA(),makeB()];
function report(m){
 let min=[Infinity,Infinity,Infinity],max=[-Infinity,-Infinity,-Infinity];
 for(let p of m.V)for(let i=0;i<3;i++){min[i]=Math.min(min[i],p[i]);max[i]=Math.max(max[i],p[i]);}
 return {id:m.id,name:m.name,design:m.principle,vertices:m.V.length,triangles:m.F.length,individually_closed_solids:m.parts.length,bounds:[min,max],program_parts:m.activity,public_void:m.cityVoid,isolated_topology:{degenerate_triangles:0,positive_volume_violations:0,unpaired_edges:0,orientation_mismatches:0},whole_model_boolean:"NOT DONE",route_331_993:"NOT RUN",global_access:"UNPROVEN",aesthetic:"PENDING INDEPENDENT IMAGE REVIEW"};
}
const stats=models.map(report);
function obj(m){let s=`# ${m.name} | G4-C7 A25 CITY-FIRST true 3D | ART HOLD\nmtllib materials.mtl\n`;
 for(let v of m.V)s+=`v ${v.map(x=>x.toFixed(5)).join(" ")}\n`;
 let last=-1;for(let f of m.F){if(last!==f[3]){s+=`usemtl ${MAT[f[3]].name}\n`;last=f[3];}s+=`f ${f[0]+1} ${f[1]+1} ${f[2]+1}\n`;}
 return s;}
function b64(u){let abc="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",s=[];for(let i=0;i<u.length;i+=3){let a=u[i],b=u[i+1]??0,c=u[i+2]??0;s.push(abc[a>>2],abc[((a&3)<<4)|(b>>4)],i+1<u.length?abc[((b&15)<<2)|(c>>6)]:"=",i+2<u.length?abc[c&63]:"=");}return s.join("");}
function glb(m){
 let pos=new Uint8Array(12*m.V.length),dv=new DataView(pos.buffer);for(let i=0;i<m.V.length;i++)for(let j=0;j<3;j++)dv.setFloat32(i*12+j*4,m.V[i][j],true);
 let raw=[...pos],views=[{buffer:0,byteOffset:0,byteLength:pos.length,target:34962}],access=[{bufferView:0,componentType:5126,count:m.V.length,type:"VEC3",min:[0,1,2].map(j=>Math.min(...m.V.map(p=>p[j]))),max:[0,1,2].map(j=>Math.max(...m.V.map(p=>p[j])))}],pr=[];
 for(let i=0;i<MAT.length;i++){let ix=m.F.filter(f=>f[3]===i).flatMap(f=>f.slice(0,3));if(ix.length===0)continue;let chunk=new Uint8Array(4*ix.length),w=new DataView(chunk.buffer);ix.forEach((a,k)=>w.setUint32(k*4,a,true));let at=raw.length;raw.push(...chunk);views.push({buffer:0,byteOffset:at,byteLength:chunk.length,target:34963});access.push({bufferView:views.length-1,componentType:5125,count:ix.length,type:"SCALAR"});pr.push({attributes:{POSITION:0},indices:access.length-1,material:i,mode:4});}
 while(raw.length%4)raw.push(0);
 let asset={asset:{version:"2.0",generator:"G4C7_A25_cityfirst_ART_HOLD"},scene:0,scenes:[{nodes:[0]}],nodes:[{mesh:0,name:m.name}],meshes:[{primitives:pr}],materials:MAT.map(x=>({name:x.name,pbrMetallicRoughness:{baseColorFactor:x.rgba,metallicFactor:.14,roughnessFactor:.66},doubleSided:true})),buffers:[{byteLength:raw.length}],bufferViews:views,accessors:access};
 let json=[...JSON.stringify(asset)].map(x=>x.charCodeAt(0));while(json.length%4)json.push(32);
 let u=new Uint8Array(28+json.length+raw.length),h=new DataView(u.buffer);h.setUint32(0,0x46546c67,true);h.setUint32(4,2,true);h.setUint32(8,u.length,true);h.setUint32(12,json.length,true);h.setUint32(16,0x4e4f534a,true);u.set(json,20);
 let off=20+json.length;h.setUint32(off,raw.length,true);h.setUint32(off+4,0x004e4942,true);u.set(raw,off+8);
 // independent parse of generated GLB header and JSON metadata to detect exporter self errors; not external 3D import
 if(h.getUint32(8,true)!==u.length)throw Error("GLB length inconsistency");
 let metadata=JSON.parse(String.fromCharCode(...json).trim());
 if(metadata.accessors[0].count!==m.V.length||metadata.meshes[0].primitives.length<4)throw Error("GLB schema count mismatch");
 return {base64:b64(u),size:u.length};
}
function view(m,name){
 let eye=CAM[name],fw=norm(sub(TARGET,eye)),right=norm(cross([0,1,0],fw)),up=norm(cross(fw,right)),coord=m.V.map(p=>{let v=sub(p,TARGET);return[dot(v,right)*SCALE,-dot(v,up)*SCALE]});
 return{coord,eye,fw,right,up,bounds:[Math.min(...coord.map(p=>p[0])),Math.min(...coord.map(p=>p[1])),Math.max(...coord.map(p=>p[0])),Math.max(...coord.map(p=>p[1]))]};
}
const viewQA={};function svg(name){
 const W=1512,H=708,Pane=756,cy=358;
 let s=`<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><rect width="${W}" height="${H}" fill="#0e1b2a"/><defs><clipPath id="left"><rect x="8" y="56" width="740" height="608"/></clipPath><clipPath id="right"><rect x="764" y="56" width="740" height="608"/></clipPath></defs><text x="1495" y="16" fill="#cddbe8" font-size="13" font-family="sans-serif" text-anchor="end">G4-C7 A25 · ${name.toUpperCase()} · EQUAL CAMERA &amp; SCALE ${SCALE} · REAL TRIANGLE VIEW · ART HOLD</text>`;
 viewQA[name]=[];
 for(let i=0;i<2;i++){
   let m=models[i],v=view(m,name),cx=Pane*i+378;
   let box={left:cx+v.bounds[0],right:cx+v.bounds[2],top:cy+v.bounds[1],bottom:cy+v.bounds[3]};
   let clear=box.left>=Pane*i+12&&box.right<=(i+1)*Pane-12&&box.top>=59&&box.bottom<=658;
   viewQA[name].push({model:m.id,bounds:box,in_frame:clear});
   if(!clear)throw Error("A25 view clipping "+name+" "+m.id+" "+JSON.stringify(box));
   s+=`<rect x="${Pane*i+8}" y="56" width="740" height="608" fill="#192f42" stroke="#69859d"/><g clip-path="url(#${i===0?"left":"right"})">`;
   let draw=[];for(let f of m.F){
     let A=m.V[f[0]],B=m.V[f[1]],C=m.V[f[2]],N=norm(cross(sub(B,A),sub(C,A))),mid=A.map((x,j)=>(x+B[j]+C[j])/3);
     if(dot(N,sub(v.eye,mid))<=0)continue;
     let hex=MAT[f[3]].hex.slice(1),lighting=Math.max(.37,Math.min(1.17,.74+.36*dot(N,norm([-.45,.86,-.3]))));
     let color="#"+[0,2,4].map(j=>Math.max(0,Math.min(255,Math.round(parseInt(hex.slice(j,j+2),16)*lighting))).toString(16).padStart(2,"0")).join("");
     draw.push({depth:dot(sub(mid,v.eye),v.fw),color,points:f.slice(0,3).map(j=>(cx+v.coord[j][0]).toFixed(2)+","+(cy+v.coord[j][1]).toFixed(2)).join(" ")});
   }
   draw.sort((a,b)=>b.depth-a.depth);
   for(let tri of draw)s+=`<polygon points="${tri.points}" fill="${tri.color}" stroke="#243a4c" stroke-width=".2"/>`;
   s+=`</g><text x="${Pane*i+25}" y="36" font-size="23" font-family="sans-serif" fill="#ebf5fb" font-weight="bold">A25-${m.id.toUpperCase()} ${m.name}</text><text x="${Pane*i+25}" y="690" font-size="15" font-family="sans-serif" fill="#bacddd">${m.F.length.toLocaleString("en-US")} triangles | ${m.activity.inhabited_rooms} inhabited geometric volumes | NO MINECRAFT</text>`;
 }
 return s+"</svg>";
}
let files=[],put=(file,content,encoding="utf-8")=>files.push({path:ROOT+file,content,encoding}),sizes={};
for(let m of models){put(`a25_${m.id}.obj`,obj(m));let g=glb(m);put(`a25_${m.id}.glb`,g.base64,"base64");sizes[m.id]=g.size;}
put("materials.mtl",MAT.map(x=>`newmtl ${x.name}\nKd ${x.rgba.slice(0,3).join(" ")}\n`).join("\n"));
for(let n of Object.keys(CAM))put("fourview/"+n+"_a25_ab.svg",svg(n));
let manifest={stage:"G4-C7 A25 visibly inhabited public-void city-first art study",created_jst:"2026-10-25",previous_head:"d271ea98f57006b82d8e58754a43124113991d94",cameras:CAM,target:TARGET,scale:SCALE,do_not_compare_same_scale_to_A24:true,stats,files_bytes:sizes,view_frame_audit:viewQA,qa_verified:["every isolated mesh is positive-volume and directed-edge manifold","no zero-area triangles","same 4-view camera/scale and full silhouette in-frame","real OBJ/GLB geometry and projection from same mesh arrays","generated GLB header and JSON schema consistency"],qa_not_verified:["third-party GLB importer/independent binary re-read","inter-solid Boolean union and all-model self-intersections","load paths, joints, fire/egress/access, usable urban floors","candidate-specific 331 human envelopes and 993 foot samples","recovery of 45 legacy body-interference samples"],historical_protection:"NO CHANGES TO OLD GLB, world, USED, CSV, ZIP, hardware evidence",status:"ART HOLD; pending visual evaluation",minecraft_education:"CONSTRUCTION PROHIBITED",city_integration:"PROHIBITED",unchanged_legacy_gates:{bodies:331,feet:993,halfwidth:.65,feet_relative:[.15,3.25],body_collision_max:45,unsupported_feet:0,negative_blocker:"REQUIRED"}};
put("a25_manifest.json",JSON.stringify(manifest,null,2));
return {files,stats,viewQA,sizes};
};
const built=buildA25();
for (const f of built.files){fs.mkdirSync(path.dirname(f.path),{recursive:true});fs.writeFileSync(f.path,f.encoding==="base64"?Buffer.from(f.content,"base64"):f.content);}
console.log(JSON.stringify({stats:built.stats,viewQA:built.viewQA},null,2));
