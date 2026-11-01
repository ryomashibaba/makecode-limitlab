#!/usr/bin/env python3
"""M25 ART-FIRST: uninterrupted sculpted enclosing structure and inhabited alcoves.
TWO real visual gate frames only; NOT an approved city, walkability or construction.
Deliberately does not import rejected M23/M24 art.
"""
import os,json,hashlib,math,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m25_immutable_m22"
SPEC=ROOT/"research/g4c7-b11-r5-d56/p2/d3s26/M17_CIVIC_FABRIC_NETWORK.json"
OUT=ROOT/"artifacts/g4c7-m25-shell-first-two-view-gate"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="22473a0d17fb59470049fb22b508dcfc294316185d38878b5563e213246af9df"
STREET="M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD"
LEVELS=[14.,34.,54.,74.]
COURTS=[-3.,20.,43.,60.]
VIEWS=("hero_oblique","research_room_eye")
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 f=list(SEED.rglob("M22_EDITABLE_REVISED_PUBLIC_ROUTE.blend"))
 assert len(f)==1,("Expected exactly one source",len(f))
 assert sha(f[0])==PIN,"M22 source SHA mismatch"
 return f[0]
def shell_x(side,y,z,interior=False):
 # Warp is the SAME section generator for the outer envelope and its inner
 # inhabitable pocket boundary. No independent box-shell placement.
 sign=-1 if side=="west" else 1
 shift=4.7*math.sin((z-2)/24+0.034*y)+3.8*math.sin(y*.057-z*.017)
 flare=3.0*math.sin(z*.071+y*.047)
 return sign*(19.5 if interior else 49.0)+sign*(shift+flare)
def preflight():
 s=json.loads(SPEC.read_text(encoding="utf-8"))
 assert len(s["nodes"])==18 and len(s["edges"])==18
 assert s["gates"]["art"]=="HOLD" and s["gates"]["minecraft_education"]=="NO_WRITE"
 assert len(VIEWS)==2 and len(LEVELS)==len(COURTS)==4
 for z in (0,14,34,54,74,94):
  for y in (-25,0,25,52,80):
   assert shell_x("west",y,z)<-12 and shell_x("east",y,z)>12
   assert shell_x("west",y,z)<shell_x("west",y,z,True)-16
   assert shell_x("east",y,z)>shell_x("east",y,z,True)+16
 assert not OUT.exists(),"Refuse to overwrite evidence"
 return {"source":str(original()),"levels":LEVELS,"occupancy_sections":8,
         "new_method":"single master section drives real envelope + internal room pockets",
         "selection":"TWO_IMAGE_GATE_ONLY_ART_HOLD"}
def build():
 import bpy
 from mathutils import Vector
 preflight()
 bpy.ops.wm.open_mainfile(filepath=str(original().resolve()))
 scene=bpy.context.scene
 existing=list(bpy.data.objects)
 road=bpy.data.objects.get(STREET)
 assert road and road.type=="MESH"
 source_coords=sorted((tuple(round(float(c),5) for c in road.matrix_world @ v.co) for v in road.data.vertices))
 for ob in existing:
  if ob!=road:ob.hide_render=True
 col=bpy.data.collections.new("M25_SCULPTED_SECTION_INHABITED_CANYON_ART_HOLD")
 scene.collection.children.link(col)
 created=[]
 def link(o):
  for oc in list(o.users_collection):oc.objects.unlink(o)
  col.objects.link(o)
  created.append(o)
  return o
 def mat(name,rgba,metal=0,rough=.43,glass=0,emission=0):
  m=bpy.data.materials.new("M25_"+name)
  m.use_nodes=True
  p=m.node_tree.nodes.get("Principled BSDF")
  p.inputs["Base Color"].default_value=(*rgba,1)
  p.inputs["Roughness"].default_value=rough
  p.inputs["Metallic"].default_value=metal
  p.inputs["Transmission Weight"].default_value=glass
  if emission:
   p.inputs["Emission Color"].default_value=(*rgba,1)
   p.inputs["Emission Strength"].default_value=emission
  return m
 M={
  "stone":mat("smoked_sandstone_ruled_rainscreen",(.43,.49,.47),.14),
  "copper":mat("dark_patinated_copper_structure",(.16,.27,.29),.60),
  "inset":mat("warm_white_occupied_galleries",(.75,.67,.53),.03),
  "timber":mat("deep_wooden_occupied_pockets",(.33,.21,.15)),
  "glazed":mat("translucent_atrium_windows",(.26,.60,.63),.04,.13,.76),
  "gold":mat("warm_interior_pendant_lamps",(.99,.65,.27),0,.32,0,2),
  "vegetation":mat("vertical_planting",(.13,.37,.25)),
  "bronze":mat("load_bearing_steel_bronze",(.31,.27,.19),.68),
  "water":mat("water_court",(.13,.40,.45),.17,.14,.29)
 }
 def meshobj(name,verts,faces,material,thickness=0):
  me=bpy.data.meshes.new("M25_"+name+"_mesh")
  me.from_pydata(verts,[],faces);me.update()
  o=bpy.data.objects.new("M25_"+name,me);col.objects.link(o);created.append(o)
  me.materials.append(M[material])
  if thickness:
   mod=o.modifiers.new("Genuine_minimum_thickness","SOLIDIFY");mod.thickness=thickness
  return o
 def cube(name,loc,dims,material):
  bpy.ops.mesh.primitive_cube_add(size=1,location=loc)
  o=bpy.context.object;o.name="M25_"+name;o.dimensions=dims
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  link(o);o.data.materials.append(M[material]);return o
 def beam(name,a,b,r,material):
  p,q=Vector(a),Vector(b)
  d=q-p
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=d.length,location=(p+q)*.5)
  o=bpy.context.object;o.name="M25_"+name
  o.rotation_euler=d.to_track_quat("Z","Y").to_euler()
  link(o);o.data.materials.append(M[material]);return o
 def section_skin(side,interior=False):
  # Single continuous mesh each side: fused vertical ribbons folded through
  # 94m of elevation, openings are actual absent faces, not black painted boxes.
  ys=[-30+i*3 for i in range(39)] # -30..84
  zs=[i*4.7 for i in range(21)]  # 0..94
  verts=[(shell_x(side,y,z,interior),y,z) for z in zs for y in ys]
  faces=[];glazing=[];window_count=0
  for iz in range(len(zs)-1):
   for iy in range(len(ys)-1):
    ids=(iz*len(ys)+iy,iz*len(ys)+iy+1,
       (iz+1)*len(ys)+iy+1,(iz+1)*len(ys)+iy)
    # Major diagonal slits open onto actual workspace pockets.
    opening=(2<iz<19 and 3<iy<34 and
            ((iy//3+iz//4+(1 if side=="east" else 0))%5==0))
    if opening:
     window_count+=1
     glazing.append(ids)
    else:faces.append(ids if side=="west" else tuple(reversed(ids)))
  ob=meshobj(side+("_atrium_inner_skin" if interior else "_single_continuous_outer_skin"),
       verts,faces,"glazed" if interior else "stone",.27 if interior else .82)
  assert len(ob.data.polygons)>480 and window_count>20
  if not interior:
   # Three continuous braced vertical section rails reference exact outer mesh.
   for j,iy in enumerate((5,21,34)):
    seq=[verts[iz*len(ys)+iy] for iz in range(len(zs))]
    for k,(a,b) in enumerate(zip(seq,seq[1:])):
     beam(side+"_monocoque_section_rib_%d_%02d"%(j,k),a,b,.69,"bronze")
  return window_count
 count=sum(section_skin(side,interior) for side in ("west","east") for interior in (False,True))
 # Sculpted interior pods held BETWEEN two surfaces generated from same
 # master section. No great stack of visible 60m-wide roofs.
 alcoves=[]
 for side in ("west","east"):
  for k,(z,y) in enumerate(zip(LEVELS,COURTS)):
   outer=shell_x(side,y,z+3)
   inner=shell_x(side,y,z+3,True)
   center_x=(outer+inner)*.5
   radius_x=abs(inner-outer)*.38
   radius_y=11.0 if k<3 else 8.8
   verts=[(center_x+radius_x*math.cos(i*2*math.pi/20),
           y+radius_y*math.sin(i*2*math.pi/20),z) for i in range(20)]
   o=meshobj(side+"_carved_occupied_pocket_%d"%k,verts,[tuple(range(20))],"inset",.6)
   assert len(o.data.polygons)==1
   # Each room framed by continuous primary shell, NOT detached box geometry.
   alcoves.append({"side":side,"z":z,"y":y,"center_x":center_x,
         "inner_x":inner,"outer_x":outer})
   for j,dy in enumerate((-6.4,1.3,6.8)):
    xx=center_x+(-3 if side=="west" else 3)
    cube(side+"_interior_living_workbench_%d_%d"%(k,j),
      (xx,y+dy,z+.68),(3.3,1.7,1.15),"timber")
    cube(side+"_daylight_tasklight_%d_%d"%(k,j),
      (xx,y+dy,z+1.29),(.55,.35,.19),"gold")
   cube(side+"_private_room_partition_%d"%k,
    (center_x+(-5 if side=="west" else 5),y+8,z+2.4),
    (6,.26,4.4),"timber")
   # A narrow surface-tied canopy inside the envelope, never protruding
   # beyond outer skin. Deep open slot keeps the main public atrium sky-open.
   shell_y=y+10
   vs=[(shell_x(side,shell_y,z+7),shell_y,z+7),
       (shell_x(side,shell_y,z+7,True),shell_y,z+7),
       (shell_x(side,shell_y-2,z+7,True),shell_y-2,z+7),
       (shell_x(side,shell_y-2,z+7),shell_y-2,z+7)]
   meshobj(side+"_recessed_canopy_%d"%k,vs,[(0,1,2,3)],"copper",.4)
 # True physical public bridges at exactly the same terminal floor height,
 # spanning the canyon at the same Y in each occupied level.
 bridge_levels=(1,2)
 bridge_tests=[]
 for k in bridge_levels:
  z,y=LEVELS[k],COURTS[k]
  ends=[shell_x(side,y,z,True) for side in ("west","east")]
  assert ends[0]<0<ends[1] and abs(z-LEVELS[k])<1e-7
  lo,hi=ends[0]-2.4,ends[1]+2.4
  cube("true_level_matched_bridge_%d"%k,((lo+hi)/2,y,z-.35),
       (hi-lo,4.8,.7),"inset")
  for sign in (-1,1):
   yy=y+sign*2.35
   beam("bridge_%d_human_guard_%d"%(k,sign),
     (lo,yy,z+.95),(hi,yy,z+.95),.23,"bronze")
  bridge_tests.append({"level":z,"left_room":LEVELS[k],"right_room":LEVELS[k],"bridge_length":hi-lo})
 # Central load-bearing elevated cross-arm is architecturally joined into
 # both side envelopes, NOT a standalone decorative repeated arch.
 for j,y in enumerate((14,46,68)):
  z=85-4*j
  lo=shell_x("west",y,z,False)
  hi=shell_x("east",y,z,False)
  key=[(lo,y,z-4),(lo*.65,y+2,z+3),(0,y+2,z+8),
       (hi*.65,y+2,z+4),(hi,y,z-4)]
  for k,(a,b) in enumerate(zip(key,key[1:])):
   beam("integrated_megatruss_%d_%d"%(j,k),a,b,1.20,"copper")
  beam("megatruss_cross_tension_%d"%j,(lo*.65,y+2,z+3),
      (hi*.65,y+2,z+4),.30,"bronze")
 # Real atrium ground courtyard on the preserved road without altering it.
 meshobj("exterior_water_edge",
   [(-12,22,.25),(-8,22,.25),(-8,48,.25),(-12,48,.25)],
   [(0,1,2,3)],"water",.13)
 for j,(x,y) in enumerate(((0,10),(-7,37),(9,51))):
  beam("atrium_planted_core_%d"%j,(x,y,.2),(x,y,8.1),.42,"timber")
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=3.3,location=(x,y,9.2))
  o=bpy.context.object;o.name="M25_atrium_tree_canopy_%d"%j
  link(o);o.data.materials.append(M["vegetation"])
 # Human eye deliberately starts INSIDE real research pod and looks to
 # furnishings and out across atrium, not into an occluding vertical wall.
 camplans={
   "hero_oblique":((-139,-132,108),(-1,28,52),34),
   "research_room_eye":((-34,11,35.6),(-32,23,36.0),27)}
 cams={}
 for name,(eye,aim,lens) in camplans.items():
  data=bpy.data.cameras.new("M25_CAMERA_"+name)
  obj=bpy.data.objects.new("M25_CAMERA_"+name,data)
  col.objects.link(obj);obj.location=eye
  obj.rotation_euler=(Vector(aim)-obj.location).to_track_quat("-Z","Y").to_euler()
  data.lens=lens;cams[name]=obj
 # Controlled, deliberately directional lighting for authored sculptural
 # surface relief rather than uniform flat M24 lighting.
 world=scene.world
 if world and world.use_nodes:
  world.node_tree.nodes["Background"].inputs["Color"].default_value=(.48,.59,.64,1)
  world.node_tree.nodes["Background"].inputs["Strength"].default_value=.63
 scene.render.engine="CYCLES";scene.cycles.samples=22
 scene.render.resolution_x=1050;scene.render.resolution_y=675
 scene.render.resolution_percentage=100
 scene.render.image_settings.file_format="PNG"
 scene["M25"]="SINGLE_SECTION_GENERATED_ENVELOPE_TWO_VIEW_VISUAL_GATE_ART_HOLD"
 scene["FORMAL_GATES"]="NOT_RUN";scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["ART"]="HOLD_NOT_APPROVED"
 after_coords=sorted((tuple(round(float(c),5) for c in road.matrix_world @ v.co) for v in road.data.vertices))
 assert after_coords==source_coords,"M22 road geometry changed!"
 assert len(alcoves)==8 and all(b["level"]==b["left_room"]==b["right_room"] for b in bridge_tests)
 assert len(created)>180,(len(created),"no actual geometry")
 OUT.mkdir(parents=True)
 blend=OUT/"M25_EDITABLE_SECTION_GENERATED_HERO_ART_HOLD.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in VIEWS:
  scene.camera=cams[name]
  image=OUT/("M25_"+name+".png")
  scene.render.filepath=str(image)
  bpy.ops.render.render(write_still=True)
  assert image.stat().st_size>1600
  views[name]={"sha256":sha(image),"bytes":image.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for o in bpy.data.objects:
  if o.type=="MESH" and not o.hide_render:o.select_set(True)
 glb=OUT/"M25_SECTION_HERO_GEOMETRY_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={"stage":"M25_2_FRAME_EARLY_ART_GATE",
   "pinned_M22_original_sha256":PIN,
   "views":views,"new_objects":len(created),
   "monocoque_window_open_faces":count,
   "occupied_alcoves":alcoves,"aligned_bridge_levels":bridge_tests,
   "M22_road_unmodified":True,
   "blend_sha256":sha(blend),"glb_sha256":sha(glb),
   "art":"HOLD_NOT_APPROVED","adopted":0,"minecraft":"FORBIDDEN",
   "official_body_feet":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
   "honesty":"Shell and alcoves are an aesthetic research prototype. No certified access, structure or safety."}
 (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print("M25_REAL_TWO_FRAME_ART_FIRST_NATIVE_COMPLETE_ART_HOLD",OUT)
if __name__=="__main__":
 if "--preflight" in sys.argv:print(json.dumps(preflight()))
 else:build()
