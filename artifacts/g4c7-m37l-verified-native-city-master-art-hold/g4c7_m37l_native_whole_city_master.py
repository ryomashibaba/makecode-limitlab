#!/usr/bin/env python3
"""M37-L: single native whole-city master; room void/capacity jointly determines skyline.
G4-C7 research only. No original scene modifications, no Minecraft writes.
This is an artistically unapproved design study, NOT manual Blender GUI authoring.
"""
import bpy, math, hashlib, json
from pathlib import Path
from mathutils import Vector

OUT=Path("artifacts/g4c7-m37l-native-master-build")
OUT.mkdir(parents=True,exist_ok=True)
S=[
 ("GATE", "PUBLIC",-7,-210,0,19,22,9),
 ("COMMONS","CIVIC",11,-161,4,34,44,22),
 ("CULTURE","CULTURE",-24,-108,13,39,66,30),
 ("MAKER_VIEW","PUBLIC_MAKER",9,-59,15,51,79,29),
 ("ASSEMBLY","STAFF_ONLY",48,-9,17,63,92,39),
 ("RESEARCH","RESEARCH",11,47,34,46,103,36),
 ("HABITAT","HABITAT",-38,104,54,52,114,49),
 ("UPPER_CULTURE","CULTURE",-43,166,68,42,98,43),
 ("BELVEDERE","PUBLIC",-9,224,81,22,69,23)
]
def section_shape(s):
 return (s[5]+12.5+.58*s[7],s[6]+11+.95*s[7])
assert len(S)==9 and all(S[i+1][3]-S[i][3]>=39 for i in range(8))
assert all(s[5]>=16 and s[6]>=20 and s[7]>=6 for s in S)
assert all(section_shape(s)[0]>s[5]+15 for s in S)
assert [x[1] for x in S].count("STAFF_ONLY")==1
def author_transaction(i,key,amount):
 assert key in ("void_w","void_h","capacity") and -10<=amount<=10
 j={"void_w":5,"void_h":6,"capacity":7}[key]
 a=list(S[i]);a[j]+=amount
 assert a[5]>=16 and a[6]>=20 and a[7]>=6
 ss=list(S);ss[i]=tuple(a)
 return ss
moved=author_transaction(5,"void_h",7)
assert section_shape(moved[5])[1]-section_shape(S[5])[1]==7
moved2=author_transaction(6,"capacity",8)
assert section_shape(moved2[6])[0]>section_shape(S[6])[0]
assert section_shape(moved2[6])[1]>section_shape(S[6])[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.name="M37L_SINGLE_CITY_MASTER_AUTHOR_ART_HOLD"
scene["M37L_ART"]="HOLD_UNREVIEWED"
scene["M37L_FORMAL_331_993"]="NOT_RUN"
scene["M37L_MINECRAFT"]="FORBIDDEN"
scene["M37L_ADOPTION"]=0
scene["M37L_RESEARCH_UNITS"]="ABSTRACT_NOT_BLOCKS"
groups={}
for name in ("SHELL","ROOMS","ROUTE","MAKER","BARRIER","CAMERAS","LIGHTS"):
 c=bpy.data.collections.new("M37L_"+name);scene.collection.children.link(c);groups[name]=c
mats={}
for k,color in {
 "concrete":(.46,.49,.46),"metal":(.34,.46,.55),"bronze":(.55,.42,.28),
 "stone":(.71,.70,.61),"deck":(.23,.31,.35),"work":(.5,.36,.26),
 "glass":(.16,.41,.47),"garden":(.2,.46,.32)}.items():
 m=bpy.data.materials.new("M37L_"+k);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get("Principled BSDF");p.inputs["Base Color"].default_value=(*color,1)
 p.inputs["Roughness"].default_value=.3 if k in ("metal","glass") else .73
 if k=="glass":p.inputs["Transmission Weight"].default_value=.65
 mats[k]=m
counts={x:0 for x in groups}
def obj(name,v,f,category,material,role):
 mesh=bpy.data.meshes.new("M37L_"+name+"_DATA")
 mesh.from_pydata(v,[],f);mesh.update()
 o=bpy.data.objects.new("M37L_"+name,mesh);groups[category].objects.link(o)
 mesh.materials.append(mats[material]);o["M37L_ROLE"]=role;counts[category]+=1
 return o
def prism(name,quad,z0,z1,cat,material,role):
 assert len(quad)==4 and z1>z0
 v=[(x,y,z) for z in (z0,z1) for x,y in quad]
 return obj(name,v,[(3,2,1,0),(4,5,6,7)]+[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)],cat,material,role)
def point(s,t,outer):
 idx=S.index(s);a=S[max(0,idx-1)];b=S[min(8,idx+1)]
 dx=b[2]-a[2];dy=b[3]-a[3];L=math.hypot(dx,dy);nx=dy/L;ny=-dx/L
 w,h=section_shape(s) if outer else (s[5],s[6])
 return (s[2]+nx*w*math.cos(t),s[3]+ny*w*math.cos(t),s[4]+h*math.sin(t))
# 9 different physical cross sections form one continuous hollow vault.
# Absence of real roof geometry at authored skylights, no surface paint.
skylights={(2,7),(2,8),(3,6),(3,7),(4,8),(5,7),(6,7),(6,8)}
for i,(a,b) in enumerate(zip(S,S[1:])):
 for j in range(16):
  if (i,j) in skylights:continue
  u=math.pi*j/16;v=math.pi*(j+1)/16
  v0=[point(a,u,True),point(a,v,True),point(a,v,False),point(a,u,False)]
  v1=[point(b,u,True),point(b,v,True),point(b,v,False),point(b,u,False)]
  verts=v0+v1
  obj(f"SHELL_{i:02d}_{j:02d}",verts,
      [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],
      "SHELL","bronze" if j in (0,1,14,15) else "metal" if j in (4,5,10,11) else "concrete",
      "ACTUAL_HOLLOW_SECTION_WALL_NOT_STRUCTURALLY_CERTIFIED")
# Rooms inside an authored *thick* cross-section, not 9 detached boxes.
roomspec={1:[("CIVIC","left",7,15)],2:[("CULTURE","left",17,21),("PUBLIC","right",34,13)],
 3:[("RESEARCH","left",18,17),("PUBLIC","right",37,17)],
 4:[("FABRICATION","right",7,29),("PUBLIC","left",35,18)],
 5:[("RESEARCH","left",40,22),("FABRICATION","right",23,24)],
 6:[("HABITAT","left",33,27),("RESEARCH","right",57,21)],
 7:[("HABITAT","right",35,21),("CULTURE","left",62,22)]}
rooms=[]
for i,plan in roomspec.items():
 s=S[i]
 for use,side,dz,span in plan:
  sign=-1 if side=="left" else 1
  inner=s[5];outer=section_shape(s)[0]
  x0=s[2]+sign*(inner+1.2);x1=s[2]+sign*(inner+.77*(outer-inner))
  y0=s[3]-span/2;y1=s[3]+span/2;z=s[4]+dz
  name=s[0]+"_"+use
  prism(name+"_FLOOR",[(x0,y0),(x1,y0),(x1,y1),(x0,y1)],z-.6,z,
        "ROOMS","stone" if use in ("CIVIC","PUBLIC","CULTURE") else "deck","REAL_ROOM_FLOOR_NOT_SAFETY_PASS")
  mid=(y0+y1)/2
  # Actual frontage opening is the absence of solid mesh between the side panels.
  for suffix,lo,hi,bot,top in [
   ("LEFT",y0,mid-2.3,z,z+4.5),("RIGHT",mid+2.3,y1,z,z+4.5),
   ("HEADER",mid-2.3,mid+2.3,z+4.5,z+6.6)]:
   prism(name+"_FRONT_"+suffix,[(x0-.25,lo),(x0+.25,lo),(x0+.25,hi),(x0-.25,hi)],
         bot,top,"ROOMS","bronze","REAL_WALL_WITH_DOOR_VOID")
  rooms.append({"name":name,"role":use,"station":s[0],"floor_z":z})
# A throughgoing, physically modeled public route within the hollow void;
# steep slopes, obstacles and true room reachability remain NOT RUN.
for i,(a,b) in enumerate(zip(S,S[1:])):
 pa=(a[2]-.62*a[5],a[3],a[4]+1.4)
 pb=(b[2]-.62*b[5],b[3],b[4]+1.4)
 dx=pb[0]-pa[0];dy=pb[1]-pa[1];L=math.hypot(dx,dy)
 nx=-dy/L*3.5;ny=dx/L*3.5
 v=[(pa[0]-nx,pa[1]-ny,pa[2]-.4),(pa[0]+nx,pa[1]+ny,pa[2]-.4),
    (pb[0]+nx,pb[1]+ny,pb[2]-.4),(pb[0]-nx,pb[1]-ny,pb[2]-.4),
    (pa[0]-nx,pa[1]-ny,pa[2]),(pa[0]+nx,pa[1]+ny,pa[2]),
    (pb[0]+nx,pb[1]+ny,pb[2]),(pb[0]-nx,pb[1]-ny,pb[2])]
 obj(f"PUBLIC_ROUTE_{i:02d}",v,
   [(3,2,1,0),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],
   "ROUTE","stone","PUBLIC_FLOOR_NOT_BODY_SWEEP_CERTIFIED")
for j,off in enumerate((-7,14,32)):
 s=S[4];x=s[2]+off;y=s[3]+(j-1)*10;w=6;l=24;z=s[4]+2
 prism(f"ACTUAL_WORKPAD_{j}",[(x-w,y-l/2),(x+w,y-l/2),(x+w,y+l/2),(x-w,y+l/2)],
       z-.6,z,"MAKER","deck","STAFF_ONLY_WORKPAD")
 prism(f"ASSEMBLY_JIG_{j}",[(x-2,y-l/2),(x+2,y-l/2),(x+2,y+l/2),(x-2,y+l/2)],
       z,z+5+j,"MAKER","bronze","FABRICATION_EQUIPMENT_STUDY")
s=S[4];x=s[2]-.38*s[5]
prism("MAKER_BOUNDARY_ACTUAL_MEMBRANE",[(x,-53),(x+1,-53),(x+1,23),(x,23)],
      s[4]+1,s[4]+38,"BARRIER","glass","ACTUAL_SOLID_MEMBRANE_NOT_FULL_SECURITY_PERIMETER")
for i in range(12):
 s=S[1];x=s[2]-.4*s[5];y=-173+(i+.5)*2;z=s[4]+1.4+(i+1)*7/12
 prism(f"CIVIC_TREAD_{i:02d}",[(x-3,y-1.1),(x+3,y-1.1),(x+3,y+1.1),(x-3,y+1.1)],
       z-.25,z,"ROUTE","bronze","TREAD_NOT_SAFE_VERTICAL_ACCESS")
def cam(key,pos,target,lens):
 d=bpy.data.cameras.new("M37L_"+key);o=bpy.data.objects.new("M37L_CAMERA_"+key,d)
 groups["CAMERAS"].objects.link(o);o.location=pos
 o.rotation_euler=(Vector(target)-o.location).to_track_quat("-Z","Y").to_euler()
 d.lens=lens
 return o
cams={
 "SOUTH":cam("SOUTH",(-70,-400,180),(-1,3,90),35),
 "NORTH":cam("NORTH",(65,425,185),(-4,4,92),36),
 "AERIAL":cam("AERIAL",(-310,-255,335),(0,4,105),32),
 "PUBLIC_EYE":cam("PUBLIC_EYE",(-17,-190,3.1),(-12,-128,37),23),
 "MAKER_EYE":cam("MAKER_EYE",(9,-62,22),(64,-4,57),23),
 "RESEARCH_EYE":cam("RESEARCH_EYE",(-17,43,45),(20,105,96),22),
 "HABITAT_EYE":cam("HABITAT_EYE",(-45,122,63),(-28,165,100),22),
 "UPPER_EYE":cam("UPPER_EYE",(-13,183,124),(7,8,102),25),
 "SKYLINE_SIDE":cam("SKYLINE_SIDE",(300,-35,190),(-10,10,85),36)}
world=bpy.data.worlds.new("M37L_SKY");world.use_nodes=True
world.node_tree.nodes["Background"].inputs["Color"].default_value=(.36,.46,.56,1)
world.node_tree.nodes["Background"].inputs["Strength"].default_value=.82
scene.world=world
for i,(location,energy,size) in enumerate([
 ((-190,-130,290),57000,120),((140,175,300),51000,130),((25,-110,230),27000,90)]):
 d=bpy.data.lights.new("M37L_AREA_"+str(i),"AREA");d.energy=energy;d.shape="DISK";d.size=size
 o=bpy.data.objects.new("M37L_LIGHT_"+str(i),d);groups["LIGHTS"].objects.link(o)
 o.location=location;o.rotation_euler=(Vector((0,0,75))-o.location).to_track_quat("-Z","Y").to_euler()
scene.render.engine="CYCLES";scene.cycles.samples=8
scene.render.resolution_x=850;scene.render.resolution_y=532
scene.render.resolution_percentage=100;scene.render.image_settings.file_format="PNG"
scene.camera=cams["SOUTH"]
saved=OUT/"M37L_SINGLE_CITY_AUTHOR_MASTER_ART_HOLD.blend"
bpy.ops.wm.save_as_mainfile(filepath=str(saved.resolve()))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
images={}
for k,c in cams.items():
 scene.camera=c;dest=OUT/("M37L_"+k+".png");scene.render.filepath=str(dest.resolve())
 bpy.ops.render.render(write_still=True,scene=scene.name)
 assert dest.stat().st_size>1500
 images[k]={"name":dest.name,"sha256":sha(dest)}
 print("M37L_RENDER",k,flush=True)
manifest={"schema":"g4c7-m37l-native-whole-city-coupled-section-v1",
 "art":"HOLD_UNREVIEWED","formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN","adoption":0,
 "scope":"COARSE_WHOLE_CITY_AND_REAL_LIVED_SECTION_IN_ONE_NATIVE_SCENE_NOT_ADOPTED",
 "units":"ABSTRACT_RESEARCH_NOT_BLOCKS","blender_gui":"NOT_USED",
 "author_stations":[{"name":s[0],"role":s[1],"x":s[2],"y":s[3],"z":s[4],
    "void_w":s[5],"void_h":s[6],"capacity":s[7],
    "outer_w":section_shape(s)[0],"outer_h":section_shape(s)[1]} for s in S],
 "actual_rooms":rooms,"mesh_counts":counts,
 "mesh_total":sum(counts.values()),"rendered_fixed_cameras":images,
 "native_blend":{"file":saved.name,"bytes":saved.stat().st_size,"sha256":sha(saved)},
 "limitations":{"complete_human_walk":"NOT_RUN","room_to_route_reachability":"NOT_RUN",
   "fabrication_access_control":"NOT_CERTIFIED","roof_support":"NOT_TESTED",
   "authoring":"bpy real native loft geometry; exterior and interior derived from one station dataset; not manually hand-sculpted"}}
(OUT/"M37L_NATIVE_MASTER_MANIFEST.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf8")
print("M37L_NATIVE_MASTER_SAVED",json.dumps({"meshes":sum(counts.values()),"rooms":len(rooms),"blend_sha":sha(saved)}),flush=True)
