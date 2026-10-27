#!/usr/bin/env python3
"""A72 real Blender/Cycles author-edited civic section. G0 ONLY, never an ART pass."""
import argparse,copy,hashlib,json,math,struct,zlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts/g4c7-a72-authored-native/native-output"
ROOMS=[
 {"id":"MARKET","z":0,"height":6.2,"poly":[[-27,-3],[-9,-4],[-7,19],[-21,26],[-32,14]],"door":6,"color":"amber"},
 {"id":"MAKER","z":0,"height":6.7,"poly":[[10,-3],[29,3],[34,24],[13,22]],"door":6,"color":"teal"},
 {"id":"READING","z":7.2,"height":5.3,"poly":[[-14,27],[12,26],[20,44],[-17,49]],"door":6.4,"color":"warm"},
 {"id":"HOUSING","z":12.6,"height":5.7,"poly":[[24,27],[43,34],[41,53],[19,49]],"door":4.8,"color":"teal"}]
META={"stage":"A72","art":"NOT_APPROVED","gates":{"S1":"NOT_RUN","G1":"NOT_RUN","G2":"NOT_RUN","G3":"NOT_RUN"},"construction":"FORBIDDEN","integration":"FORBIDDEN","lens_count":2,"intended_stairs":40}
def polygon_area(p):
 return sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(p,p[1:]+p[:1]))/2
def validate(meta= META,rooms=ROOMS):
 problems=[]
 if meta["stage"]!="A72" or meta["art"]!="NOT_APPROVED":problems.append("FAKE_ART")
 if meta["gates"]!={k:"NOT_RUN" for k in ("S1","G1","G2","G3")}:problems.append("GATE")
 if meta["construction"]!="FORBIDDEN" or meta["integration"]!="FORBIDDEN":problems.append("CONSTRUCTION")
 if meta["lens_count"]!=2 or meta["intended_stairs"]!=40:problems.append("CAMERA_STAIR")
 if len(rooms)!=4 or {r["id"] for r in rooms}!={"MARKET","MAKER","READING","HOUSING"}:problems.append("ROOM_SET")
 for r in rooms:
  if polygon_area(r["poly"])<40 or r["height"]<4.5 or not 3.5<=r["door"]<=8:problems.append("ROOM_GEOMETRY_"+r["id"])
 if sorted(r["z"] for r in rooms)!=[0,0,7.2,12.6]:problems.append("ROOM_Z")
 if problems:raise ValueError(",".join(problems))
 return {"A72_AUTHOR_DATA":"PASS_ONLY_METADATA","art":"HOLD","S1_G1_G2_G3":"NOT_RUN"}
def negatives():
 cases=[
 ("art",lambda m,r:m.__setitem__("art","PASS")),
 ("g2",lambda m,r:m["gates"].__setitem__("G2","PASS")),
 ("construction",lambda m,r:m.__setitem__("construction","ALLOWED")),
 ("door",lambda m,r:r[0].__setitem__("door",30)),
 ("missing_room",lambda m,r:r.pop()),
 ("flipped_floor",lambda m,r:r[1]["poly"].reverse()),
 ("stair_count",lambda m,r:m.__setitem__("intended_stairs",0))]
 for name,fn in cases:
  m=copy.deepcopy(META);r=copy.deepcopy(ROOMS);fn(m,r)
  try:validate(m,r)
  except ValueError:print("NEGATIVE_DETECTED",name)
  else:raise AssertionError("UNCHECKED_"+name)
 print("A72_SEVEN_NEGATIVE_CASES_PASS_DATA_ONLY")
def png_info(path):
 data=path.read_bytes();assert data[:8]==b"\x89PNG\r\n\x1a\n"
 p=8;types=[]
 while p<len(data):
  n=struct.unpack_from(">I",data,p)[0];typ=data[p+4:p+8];c=data[p+8:p+8+n]
  assert zlib.crc32(typ+c)&0xffffffff==struct.unpack_from(">I",data,p+8+n)[0]
  if typ==b"IHDR":assert struct.unpack(">II",c[:8])==(960,720)
  types.append(typ);p+=n+12
  if typ==b"IEND":break
 assert p==len(data) and b"IDAT" in types and types[-1]==b"IEND"
 return {"sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
def render():
 import bpy
 from mathutils import Vector
 OUT.mkdir(parents=True,exist_ok=True)
 blend=OUT/"a72_authored_true_section.blend"
 if blend.exists() or (OUT/"render_public_heart.png").exists() or (OUT/"render_oblique.png").exists():raise FileExistsError("Append-only protected A72 output")
 bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
 s=bpy.context.scene;s.render.engine="CYCLES";s.cycles.samples=20
 s.render.resolution_x=960;s.render.resolution_y=720;s.render.resolution_percentage=100
 s.render.image_settings.file_format="PNG";s.view_settings.view_transform="AgX"
 C={}
 for n in ["01_AUTHORED_ROOM_SURFACES","02_OCCUPIED_ROOM_CONTENT","03_ACTUAL_STAIR_TREADS","04_LIGHTS_CAMERAS"]:
  q=bpy.data.collections.new(n);s.collection.children.link(q);C[n]=q
 def mat(n,c,metal=0,emit=0):
  m=bpy.data.materials.new(n);m.use_nodes=True
  node=m.node_tree.nodes.get("Principled BSDF")
  node.inputs["Base Color"].default_value=(*c,1);node.inputs["Metallic"].default_value=metal
  node.inputs["Roughness"].default_value=.54
  if emit:
   node.inputs["Emission Color"].default_value=(*c,1);node.inputs["Emission Strength"].default_value=emit
  return m
 M={"dark":mat("Load-bearing dark mineral",(.08,.18,.24),.25),
    "stone":mat("Weathered light stone",(.48,.62,.64),.2),
    "amber":mat("Market copper",(.75,.43,.25),.42),
    "teal":mat("Maker turquoise",(.17,.56,.56),.3),
    "warm":mat("Learning honey",(.81,.65,.37),.1),
    "floor":mat("Civic charcoal floor",(.31,.39,.42),.1),
    "plant":mat("Planter greens",(.12,.34,.25)),
    "glow":mat("Warm glowing touch surface",(.89,.71,.48),.1,.22)}
 def mesh(n,verts,faces,kind,col,thick=0):
  d=bpy.data.meshes.new(n+"_mesh");d.from_pydata(verts,[],faces);d.update()
  ob=bpy.data.objects.new(n,d);C[col].objects.link(ob);d.materials.append(M[kind])
  if thick:
   mod=ob.modifiers.new("Author_editable_thickness","SOLIDIFY");mod.thickness=thick
  return ob
 def panel(n,p,kind,thick=.35,col="01_AUTHORED_ROOM_SURFACES"):
  return mesh(n,p,[tuple(range(len(p)))],kind,col,thick)
 def solid_poly(n,pts,lo,hi,kind):
  assert hi>lo
  l=len(pts);vs=[(x,y,lo) for x,y in pts]+[(x,y,hi) for x,y in pts]
  faces=[tuple(reversed(range(l))),tuple(range(l,l*2))]
  faces.extend((i,(i+1)%l,(i+1)%l+l,i+l) for i in range(l))
  return mesh(n,vs,faces,kind,"01_AUTHORED_ROOM_SURFACES")
 def cube(n,xyz,dims,kind,col):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz)
  ob=bpy.context.object;ob.name=n;ob.dimensions=dims
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for c in list(ob.users_collection):c.objects.unlink(ob)
  C[col].objects.link(ob);ob.data.materials.append(M[kind])
  return ob
 def interpolate(a,b,t):return (a[0]+t*(b[0]-a[0]),a[1]+t*(b[1]-a[1]))
 court=[(-13,-18),(11,-18),(18,3),(4,11),(-11,10),(-18,-1)]
 solid_poly("REAL_CIVIC_COURT_GROUND_NOT_FULL_PATH_QA",court,-.9,0,"floor")
 for room in ROOMS:
  id=room["id"];p=room["poly"];z=room["z"];h=room["height"];typ=room["color"]
  solid_poly(id+"_TRUE_INTERIOR_FLOOR",p,z-.43,z,"floor")
  for i in range(1,len(p)):
   a,b=p[i],p[(i+1)%len(p)]
   panel(id+"_SIDE_WALL_"+str(i),[(a[0],a[1],z),(b[0],b[1],z),(b[0],b[1],z+h),(a[0],a[1],z+h)],
     "dark" if i%2 else "stone")
  a,b=p[0],p[1];half=.5*room["door"]/math.dist(a,b)
  L,R=interpolate(a,b,.5-half),interpolate(a,b,.5+half)
  for name,u,v in [("LEFT",a,L),("RIGHT",R,b)]:
   panel(id+"_ENTRANCE_WALL_"+name,[(u[0],u[1],z),(v[0],v[1],z),(v[0],v[1],z+h),(u[0],u[1],z+h)],"stone")
  panel(id+"_LINTEL_ABOVE_REAL_OPENING",[(L[0],L[1],z+4.1),(R[0],R[1],z+4.1),(R[0],R[1],z+h),(L[0],L[1],z+h)],typ,.35)
  # Each folded roof is a separate authored asymmetric facet, never a roof spanning the whole city.
  panel(id+"_INDIVIDUAL_FOLDED_ROOF",
   [(p[-2][0],p[-2][1],z+h+.3),(p[-1][0],p[-1][1],z+h+1.6),
    (p[0][0],p[0][1],z+h+.85),((p[0][0]+p[1][0])/2,(p[0][1]+p[1][1])/2,z+h+.15)],
    typ,.7)
  cx=sum(a[0] for a in p)/len(p);cy=sum(a[1] for a in p)/len(p)
  for i in range(2 if id=="HOUSING" else 3):
   yy=cy+(i-1)*2.5
   cube(id+"_REAL_FURNITURE_"+str(i),(cx,yy,z+.7),(2.1,1.4,1.4),typ,"02_OCCUPIED_ROOM_CONTENT")
   cube(id+"_REAL_TASK_SURFACE_"+str(i),(cx,yy,z+1.45),(1.4,.9,.08),"glow","02_OCCUPIED_ROOM_CONTENT")
 # Two individual 20-tread flights; dimensions are explicit, but no full route or G2 evidence.
 for name,start,dir in [("STAIR1",(1,5,0),(0,1)),("STAIR2",(1,15,3.6),(-1,0))]:
  x,y,z=start;ux,uy=dir
  for i in range(20):
   xp=x+ux*(i+.5)*.32;yp=y+uy*(i+.5)*.32;top=z+(i+1)*.18
   cube(name+"_TRUE_TREAD_"+str(i),(xp,yp,top-.1),
    (2.8,.32,.2) if uy else (.32,2.8,.2),"floor","03_ACTUAL_STAIR_TREADS")
   cube(name+"_TRUE_RISER_"+str(i),(xp-ux*.16,yp-uy*.16,top-.09),
    (2.8,.12,.18) if uy else (.12,2.8,.18),"stone","03_ACTUAL_STAIR_TREADS")
 cube("LANDING_1_ACTUAL_SURFACE",(1,13,3.48),(3.6,4.6,.24),"floor","03_ACTUAL_STAIR_TREADS")
 cube("LANDING_2_ACTUAL_SURFACE",(-5.5,16.8,7.08),(3.8,4.5,.24),"floor","03_ACTUAL_STAIR_TREADS")
 cube("LEARNING_APPROACH_FLOOR",(-7.5,22,7.08),(4,12,.24),"floor","03_ACTUAL_STAIR_TREADS")
 # The elevated room has candidate piers; never call them support PASS.
 for i,(x,y) in enumerate([(-12,28),(10,30),(15,42)]):
  panel("READING_UNVERIFIED_CANTILEVER_BRACE_"+str(i),
   [(x,y,0),(x+1.4,y,0),(x+3,y+1,7.2),(x+1.6,y+1,7.2)],"dark",.8)
 # The small green and public touch spaces define human scale without becoming decorative windows.
 for i,(x,y) in enumerate([(-13,-10),(15,-8),(-6,5),(8,20)]):
  cube("PLANTER_"+str(i),(x,y,.5),(1.7,1.6,1),"amber","02_OCCUPIED_ROOM_CONTENT")
  cube("FOLIAGE_"+str(i),(x,y,1.9),(2.5,2.1,1.8),"plant","02_OCCUPIED_ROOM_CONTENT")
 cube("SITE_CONTEXT_NOT_MINECRAFT",(0,22,-2),(150,150,2),"dark","04_LIGHTS_CAMERAS")
 world=bpy.data.worlds.new("A72_DIFFUSE_CITY_DAY");world.use_nodes=True
 bg=world.node_tree.nodes.get("Background");bg.inputs["Color"].default_value=(.51,.65,.72,1);bg.inputs["Strength"].default_value=.7;s.world=world
 sun=bpy.data.lights.new("SKYLIGHT","SUN");sun.energy=2.4
 light=bpy.data.objects.new("SKYLIGHT",sun);C["04_LIGHTS_CAMERAS"].objects.link(light);light.rotation_euler=(.45,-.48,.3)
 for label,position,energy,size in [("COURT",(0,-30,45),4800,30),("BACK",(45,65,85),7500,65)]:
  d=bpy.data.lights.new(label,"AREA");d.energy=energy;d.shape="DISK";d.size=size
  a=bpy.data.objects.new("AREA_"+label,d);C["04_LIGHTS_CAMERAS"].objects.link(a);a.location=position
  a.rotation_euler=(Vector((0,16,6))-a.location).to_track_quat("-Z","Y").to_euler()
 cams={}
 for key,pos,target in [("public_heart",(0,-14,1.7),(0,9,4.2)),("oblique",(88,-107,90),(1,18,15))]:
  d=bpy.data.cameras.new("CAM_"+key);d.lens=31 if key=="public_heart" else 36
  cam=bpy.data.objects.new("VIEW_"+key,d);C["04_LIGHTS_CAMERAS"].objects.link(cam);cam.location=pos
  cam.rotation_euler=(Vector(target)-cam.location).to_track_quat("-Z","Y").to_euler()
  cams[key]=cam
 s.camera=cams["oblique"];bpy.ops.wm.save_as_mainfile(filepath=str(blend))
 views={}
 for name,cam in cams.items():
  f=OUT/("render_"+name+".png");s.camera=cam;s.render.filepath=str(f)
  bpy.ops.render.render(write_still=True);views[name]=png_info(f)
 report={"stage":"A72","renderer":"BLENDER_CYCLES","art":"NOT_ASSESSED","gates":META["gates"],
         "construction":"FORBIDDEN","integration":"FORBIDDEN","true_rooms":4,"treads":40,
         "complete_walk_test":False,"body_collision_test":False,
         "blend_sha256":hashlib.sha256(blend.read_bytes()).hexdigest(),"views":views}
 (OUT/"a72_native_manifest.json").write_text(json.dumps(report,indent=2)+"\n")
 print("A72_NATIVE_REAL_BLEND_AND_TWO_CYCLES_VIEWS_EVIDENCE_ONLY_NO_ART_APPROVAL")
if __name__=="__main__":
 ap=argparse.ArgumentParser();ap.add_argument("--preflight",action="store_true");ap.add_argument("--negatives",action="store_true");ap.add_argument("--render",action="store_true")
 opt=ap.parse_args();print(validate())
 if opt.negatives:negatives()
 if opt.render:render()
