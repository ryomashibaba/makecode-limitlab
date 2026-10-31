#!/usr/bin/env python3
"""D3S26 M15C: one edited inhabited interior, not a future-city massing generator.
Actual Blender renders are a visual review gate; never approval or Minecraft construction.
"""
import hashlib,json,math,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"artifacts/g4c7-d3s26-m15c-occupied-room"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
CAMERAS={
 "south":((0,-104,53),(0,3,10)),
 "north":((0,95,46),(0,3,9)),
 "oblique":((-88,-69,50),(0,2,9)),
 "district":((83,-58,38),(0,5,9)),
 "street_eye":((0,-29,1.7),(0,6,5.0)),
 "maker_eye":((-24,1,1.7),(-8,8,4.5)),
 "research_eye":((2,18,8.9),(-17,0,6)),
 "resident_eye":((17,18,8.9),(0,-1,7))}
def preflight():
 assert list(CAMERAS)==["south","north","oblique","district",
                        "street_eye","maker_eye","research_eye","resident_eye"]
 return {"status":"NATIVE_EDITABLE_ART_STUDY","art":"HOLD_NOT_APPROVED",
         "construction":"FORBIDDEN","integration":"FORBIDDEN",
         "formal_G0_S1_G1_G2_G3":"NOT_RUN","formal_331_993":"NOT_RUN",
         "stage":"M15C","scale":"architectural interior prototype, not city"}
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def create():
 import bpy
 from mathutils import Vector
 preflight()
 assert not OUT.exists(), "append-only path already exists"
 OUT.mkdir(parents=True)
 bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene
 C={}
 for label in ("01_PUBLIC_FLOOR","02_INHABITED_MAKER_MARKET","03_UPPER_RESEARCH",
               "04_STRUCTURE_DAYLIGHT","05_WAYFINDING_AND_PEOPLE","06_CAMERAS_LIGHTS"):
  coll=bpy.data.collections.new(label);scene.collection.children.link(coll);C[label]=coll
 def material(n,c,metal=0,rough=.55,trans=0,emission=0):
  m=bpy.data.materials.new(n);m.use_nodes=True
  p=m.node_tree.nodes.get("Principled BSDF")
  p.inputs["Base Color"].default_value=(*c,1)
  p.inputs["Metallic"].default_value=metal
  p.inputs["Roughness"].default_value=rough
  if trans:p.inputs["Transmission Weight"].default_value=trans
  if emission:
   p.inputs["Emission Color"].default_value=(*c,1)
   p.inputs["Emission Strength"].default_value=emission
  return m
 M={
 "ground":material("warm cast stone",(.41,.46,.45),.08),
 "walk":material("sunlit pale limestone",(.69,.65,.55),.03),
 "dark":material("structural charcoal bronze",(.12,.19,.22),.5,.32),
 "copper":material("ceramic oxidized copper",(.34,.57,.52),.4,.31),
 "warm":material("warm terracotta public furniture",(.70,.38,.21),.12),
 "glass":material("clear cyan daylight glazing",(.30,.58,.64),.03,.15,.56),
 "glassrail":material("frosted balcony glass",(.36,.68,.69),.08,.24,.42),
 "canopy":material("light ceramic roof",(.75,.80,.76),.12),
 "green":material("inhabited tree foliage",(.12,.33,.21)),
 "wood":material("touch surface hardwood",(.45,.28,.15)),
 "light":material("architectural practical light",(.96,.80,.54),.0,.34,0,1.0),
 "fabric":material("clothing pale indigo",(.25,.30,.51)),
 "floor":material("active gallery flooring",(.59,.54,.43))
 }
 def move(ob,collection):
  for c in list(ob.users_collection):c.objects.unlink(ob)
  C[collection].objects.link(ob)
  return ob
 def cube(n,p,size,k,collection="02_INHABITED_MAKER_MARKET",bevel=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=p)
  ob=bpy.context.object;ob.name=n
  ob.dimensions=size
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  move(ob,collection);ob.data.materials.append(M[k])
  if bevel:
   mod=ob.modifiers.new("Soft physical edges","BEVEL")
   mod.width=bevel;mod.segments=2
   ob.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
  return ob
 def panel(n,pts,k,collection="04_STRUCTURE_DAYLIGHT",thick=.30):
  data=bpy.data.meshes.new(n+"_MESH");data.from_pydata(pts,[],[tuple(range(len(pts)))])
  data.update()
  ob=bpy.data.objects.new(n,data);C[collection].objects.link(ob)
  data.materials.append(M[k])
  if thick:
   mod=ob.modifiers.new("Real material thickness","SOLIDIFY");mod.thickness=thick
  return ob
 def post(n,xy,z,height,r,k,collection="04_STRUCTURE_DAYLIGHT"):
  bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=height,location=(xy[0],xy[1],z+height/2))
  ob=bpy.context.object;ob.name=n;move(ob,collection);ob.data.materials.append(M[k])
  return ob
 def beam(n,a,b,thick,k):
  a,b=Vector(a),Vector(b);v=b-a
  ob=cube(n,tuple((a+b)/2),(thick,thick,v.length),k,"04_STRUCTURE_DAYLIGHT",.12)
  ob.rotation_euler=v.to_track_quat("Z","Y").to_euler()
  return ob
 # An actual, visibly continuous public surface. No city plates or towers.
 cube("PUBLIC_PROMENADE_TRUE_GROUND",(0,-4,-.38),(75,64,.76),"ground","01_PUBLIC_FLOOR")
 cube("PUBLIC_STONE_ARRIVAL",(0,-19,.06),(17,21,.16),"walk","01_PUBLIC_FLOOR")
 cube("PUBLIC_COURT_INSIDE",(0,5,.06),(21,22,.16),"walk","01_PUBLIC_FLOOR")
 # One partial double-height maker hall, with real shop openings facing the public court.
 cube("MAKER_INTERIOR_FLOOR",(-23,4,.12),(27,34,.24),"walk","01_PUBLIC_FLOOR")
 cube("MAKER_BACK_THICK_WALL",(-36,4,7.7),(1.3,33,15.4),"dark")
 cube("MAKER_NORTH_THICK_WALL",(-23,20,7.7),(27,1.4,15.4),"dark")
 cube("MAKER_SOUTH_THICK_WALL",(-23,-12,7.7),(27,1.4,15.4),"dark")
 for y in (-11,2,18):
  post("MAKER_OPEN_FRONT_POST_%02d"%int(y+12),(-10.2,y),0,13,.48,"copper")
 beam("MAKER_GLAZED_HEADER",(-10.2,-12,13),(-10.2,20,13),.7,"copper")
 for ya,yb in ((-11.2,-4.2),(5.4,12.4)):
  panel("MAKER_INSET_GLAZING_%s"%str(ya),
        [(-10.4,ya,4.6),(-10.4,yb,4.6),(-10.4,yb,12.4),(-10.4,ya,12.4)],"glass")
 # Substantial maker activity: visible fabrication tables and hanging overhead tooling.
 for i,(x,y) in enumerate(((-30,-4),(-23,7),(-30,13),(-17,0))):
  cube("MAKER_STATION_%02d"%(i+1),(x,y,.86),(5.1,2.7,1.55),"wood",bevel=.14)
  cube("MAKER_WORKPIECE_%02d"%(i+1),(x,y,1.76),(1.7,1.0,.24),"copper",bevel=.08)
  post("MAKER_TASK_LIGHT_%02d"%(i+1),(x+1.6,y),3.3,3,.10,"dark")
  cube("MAKER_TASK_LAMP_%02d"%(i+1),(x+1.6,y,6.18),(2.5,.7,.17),"light",bevel=.06)
 beam("MAKER_TRUE_OVERHEAD_RAIL",(-32,-9,11.4),(-15,17,11.4),.52,"copper")
 # Open civic market to the east, populated by unlike workstations and seating.
 cube("MARKET_MARKETFLOOR",(25,-6,.12),(25,42,.24),"walk","01_PUBLIC_FLOOR")
 cube("MARKET_EAST_END_WALL",(38,-6,6),(1.2,42,12),"dark")
 cube("MARKET_SOUTH_DARK_WALL",(25,-27,5),(25,1.0,10),"dark")
 for label,x,y,sz in (("INFORMATION",28,-17,(6,3,1.3)),
                       ("MARKET_CRAFT",22,-7,(5,3.7,1.15)),
                       ("PUBLIC_REPAIR",31,6,(7,3.2,1.25))):
  cube(label+"_SERVICE_COUNTER",(x,y,.78),sz,"warm",bevel=.26)
  cube(label+"_ILLUMINATED_WORKTOP",(x,y,1.54),(sz[0]-.35,sz[1]-.3,.12),"light")
 cube("PUBLIC_CIVIC_SEATING_A",(7,-12,.44),(5,1.1,.88),"wood",bevel=.28)
 cube("PUBLIC_CIVIC_SEATING_B",(-5,13,.44),(3.3,1.0,.88),"wood",bevel=.23)
 # Double-height central garden: a tall living focal point with a genuine open void.
 cube("CENTRAL_RAIN_GARDEN_BED",(-1,5,.40),(9,7,.72),"dark","01_PUBLIC_FLOOR",.44)
 for j,(x,y,h,r) in enumerate(((-2.2,4.7,8,.57),(1.7,6.2,6,.40))):
  post("COURT_TRUE_TREE_TRUNK_%d"%j,(x,y),.78,h,r,"wood","05_WAYFINDING_AND_PEOPLE")
  for t,dx,dy in ((0,-1.8,.5),(1,1.0,1.0),(2,.6,-1.7)):
   bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=1,
                                       location=(x+dx,y+dy,.9+h-(t%2)*1.1))
   o=bpy.context.object;o.name="COURT_FOLIAGE_%d_%d"%(j,t)
   o.scale=(2.8,2.4,2.0);move(o,"05_WAYFINDING_AND_PEOPLE");o.data.materials.append(M["green"])
 # Research gallery is a true upper destination, not a flat facade decoration.
 cube("RESEARCH_UPPER_GALLERY_TRUE_FLOOR",(0,24,7.2),(46,13,.50),"floor","03_UPPER_RESEARCH",.25)
 cube("RESEARCH_WORK_ROOM_TRUE_FLOOR",(-16,31,7.2),(18,12,.50),"walk","03_UPPER_RESEARCH")
 cube("RESEARCH_NORTH_WALL",(0,37,13.1),(46,1,11.8),"dark","03_UPPER_RESEARCH")
 for x in (-20,0,20):
  post("RESEARCH_GALLERY_COLUMN_%s"%str(x),(x,18),7.4,9,.36,"copper")
 # Gallery has see-through parapets and human-scaled workbenches.
 panel("RESEARCH_OPEN_GALLERY_RAIL",
       [(-22,17.6,7.6),(22,17.6,7.6),(22,17.6,8.75),(-22,17.6,8.75)],
       "glassrail","03_UPPER_RESEARCH",.07)
 for i,(x,y) in enumerate(((-15,27),(-7,31),(9,27))):
  cube("RESEARCH_OCCUPIED_DESK_%02d"%i,(x,y,8.0),(3.5,1.7,1.3),
       "wood","03_UPPER_RESEARCH",.14)
  cube("RESEARCH_ANALYSIS_SURFACE_%02d"%i,(x,y,8.73),(2.5,1.1,.14),
       "glass","03_UPPER_RESEARCH")
 # A connected switchback staircase is represented by 40 actual treads, not a ramp label.
 # Foot dimensions are visual-scale hypotheses only; full collision QA NOT RUN.
 for flight,(x,ystart,zstart,direction) in enumerate(((23,-17,0,1),(16,-6,3.6,1)),1):
  for j in range(20):
   zz=zstart+(j+1)*.18
   yy=ystart+direction*(j+.5)*.46
   cube("TRUE_STAIR_%d_TREAD_%02d"%(flight,j+1),
        (x,yy,zz-.09),(5.8,.46,.18),"walk","03_UPPER_RESEARCH",.02)
 cube("TRUE_MID_LANDING",(19.5,-7.8,3.50),(13.0,4.4,.22),
      "walk","03_UPPER_RESEARCH")
 cube("TRUE_UPPER_LANDING",(16,4.5,7.10),(9,6,.22),"floor","03_UPPER_RESEARCH")
 cube("TRUE_RESEARCH_CONNECTING_BRIDGE",(12,11.4,7.12),(9,15,.22),"walk","03_UPPER_RESEARCH")
 # Separate residential approach is legible but not certified a complete room or city.
 cube("RESIDENTIAL_APPROACH_TRUE_FLOOR",(27,25,7.2),(9,12,.5),
      "floor","03_UPPER_RESEARCH")
 cube("RESIDENTIAL_APPROACH_BACK_WALL",(31.5,26,11),(1.2,10,7.5),
      "warm","03_UPPER_RESEARCH")
 beam("RESEARCH_HIGH_DAYLIGHT_FRAME_A",(-32,19,16),(5,17,23),.76,"copper")
 beam("RESEARCH_HIGH_DAYLIGHT_FRAME_B",(5,17,23),(33,26,17),.84,"copper")
 beam("MAKER_TALL_ATRIUM_FRAME",(-33,-15,16),(-6,13,22),.72,"copper")
 # Partial separate roof pieces above occupied workspaces, leaving central daylight void.
 panel("MAKER_PARTIAL_DAYLIGHT_ROOF",
       [(-37,-14,16),(-9,-14,17),(-7,13,21),(-37,21,18)],
       "canopy",thick=.58)
 panel("RESEARCH_SAWTOOTH_SKYLIGHT",
       [(-24,31,17),(-4,31,22),(20,32,17),(22,37,17)],
       "glass",thick=.14)
 for a,b,n in [((-37,-14,16),(-9,-14,17),"ROOF_EDGE_A"),
               ((-7,13,21),(-37,21,18),"ROOF_EDGE_B"),
               ((-24,31,17),(-4,31,22),"ROOF_EDGE_C")]:
  beam(n,a,b,.55,"copper")
 # Human scale figures, each 1.75m, clearly separate from safety samples.
 for i,(x,y) in enumerate(((-1,-20),(-18,-1),(21,-18),(2,22),(17,19))):
  post("SCALE_FIGURE_BODY_%02d"%i,(x,y),.25,1.22,.19,"fabric","05_WAYFINDING_AND_PEOPLE")
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.24,
                                       location=(x,y,1.64))
  o=bpy.context.object;o.name="SCALE_FIGURE_HEAD_%02d"%i
  move(o,"05_WAYFINDING_AND_PEOPLE");o.data.materials.append(M["warm"])
 # A neutral context; do not fake a city skyline.
 world=bpy.data.worlds.new("Bright neutral day world") if not scene.world else scene.world
 scene.world=world;world.use_nodes=True
 bg=world.node_tree.nodes.get("Background")
 bg.inputs["Color"].default_value=(.59,.69,.76,1)
 bg.inputs["Strength"].default_value=.75
 def area(n,loc,target,energy,size):
  data=bpy.data.lights.new(n,"AREA");data.energy=energy;data.shape="DISK";data.size=size
  ob=bpy.data.objects.new(n,data);C["06_CAMERAS_LIGHTS"].objects.link(ob)
  ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
 for n,p,t,e,z in (
  ("Main daylight",(-25,-5,30),(-6,0,4),8000,31),
  ("Atrium softbox",(15,4,34),(0,3,4),8500,28),
  ("Upper gallery",(0,32,27),(0,20,9),6500,24),
  ("Public plaza",(12,-28,24),(0,-12,3),4800,23)):
  area(n,p,t,e,z)
 for name,(eye,target) in CAMERAS.items():
  cam=bpy.data.cameras.new("M15C_CAMERA_"+name)
  ob=bpy.data.objects.new("M15C_CAMERA_"+name,cam)
  C["06_CAMERAS_LIGHTS"].objects.link(ob)
  ob.location=eye
  ob.rotation_euler=(Vector(target)-ob.location).to_track_quat("-Z","Y").to_euler()
  cam.lens=29 if "eye" in name else 39
 scene.render.engine="CYCLES";scene.cycles.samples=12
 scene.render.resolution_x=960;scene.render.resolution_y=540
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 scene.view_settings.view_transform="AgX"
 scene.camera=bpy.data.objects["M15C_CAMERA_oblique"]
 scene["DESIGN_SCOPE"]="ONE INHABITED INTERIOR, NOT CITY"
 scene["ART"]="HOLD_NOT_APPROVED"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["FORMAL_331_993_AND_GATES"]="NOT_RUN"
 blend=OUT/"M15C_EDITABLE_PUBLIC_INTERIOR.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in CAMERAS:
  scene.camera=bpy.data.objects["M15C_CAMERA_"+name]
  image_path=OUT/("M15C_"+name+".png")
  scene.render.filepath=str(image_path)
  bpy.ops.render.render(write_still=True)
  assert image_path.stat().st_size>1500
  views[name]={"sha256":digest(image_path),"bytes":image_path.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M15C_PUBLIC_INTERIOR_NOT_ART_APPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 assert glb.stat().st_size>5000
 manifest={"status":preflight(),"blender":bpy.app.version_string,
  "blend_sha256":digest(blend),"glb_sha256":digest(glb),
  "views":views,"stair_treads":40,
  "disclaimer":"Render and named objects do not certify walkability, art or Minecraft safety."}
 (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
 print("M15C_NATIVE_INTERIOR_EVIDENCE_CREATED_NOT_ART_APPROVED",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print(json.dumps(preflight(),indent=2))
 else:create()
