#!/usr/bin/env python3
"""M28: real art-direct edit to M27 public visitor gallery.
Remove occluding entrance plinth, make an actually readable orbital-science
exhibit off the 7m-public route, preserve original M27 fixed eye cameras.
Editable native .blend + two fixed Cycles views, never ART PASS by script.
"""
from pathlib import Path
import os,sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m28_immutable_m27"
OUT=ROOT/"artifacts/g4c7-m28-gallery-visual-art-edit"/("run_"+os.getenv("GITHUB_SHA","local")[:12])
PIN="b39af3481a003ad6eef0e844310be8d7abce0af5616489f8514d1db3d3860efb"
ORIGIN=(-43.,37.,9.6)
VIEWS=("gallery_arrival_eye","controlled_threshold_eye")
HIDDEN=("M27_exhibition_real_demonstration_plinth_0",
        "M27_exhibition_label_readable_screen_0",
        "M27_exhibition_instrument_0",
        "M27_exhibition_lab_data_model_0")
FLOOR="M27_ONE_CONNECTED_U0_TO_U1_OBSERVATION_DECK"
THRESHOLD="M27_REAL_EAST_CONTROLLED_DOORWAY_THRESHOLD"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 found=list(SEED.rglob("M27_EDITABLE_RESEARCH_VISITOR_GALLERY.blend"))
 assert len(found)==1,("M27 source not uniquely recoverable",len(found))
 assert sha(found[0])==PIN,"M27 original SHA mismatch; no unpinned art edit"
 return found[0]
def preflight():
 assert len(HIDDEN)==4 and len(VIEWS)==2
 assert not OUT.exists(),"Append only; no overwrites"
 return {"source":str(original()),"art":"HOLD_NOT_APPROVED","same_cameras":True}
def run():
 import bpy
 from mathutils import Vector
 preflight()
 bpy.ops.wm.open_mainfile(filepath=str(original().resolve()))
 scene=bpy.context.scene
 oldobjs=set(bpy.data.objects.keys())
 floor=bpy.data.objects.get(FLOOR)
 threshold=bpy.data.objects.get(THRESHOLD)
 assert floor and threshold and floor.type==threshold.type=="MESH"
 originalroad=bpy.data.objects.get("M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD")
 assert originalroad and originalroad.type=="MESH"
 oldgeo={n:sorted(tuple(round(float(w),5) for w in o.matrix_world@v.co) for v in o.data.vertices)
    for n,o in ((FLOOR,floor),(THRESHOLD,threshold),
                ("M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD",originalroad))}
 cameras={}
 for n in VIEWS:
  o=bpy.data.objects.get("M27_CAMERA_"+n)
  assert o and o.type=="CAMERA"
  cameras[n]=o
 campin={n:(tuple(o.location),tuple(o.rotation_euler),float(o.data.lens)) for n,o in cameras.items()}
 for n in HIDDEN:
  ob=bpy.data.objects.get(n)
  assert ob and ob.type=="MESH" and not ob.hide_render,n
  ob.hide_render=True
 # Keep actual accessible aisle and first location clear; retired exhibit
 # remains inside native blend (hidden), NOT destroyed.
 col=bpy.data.collections.new("M28_READABLE_ORBITAL_GALLERY_ART_HOLD")
 scene.collection.children.link(col)
 built=[]
 def xyz(p):return tuple(ORIGIN[i]+float(p[i]) for i in range(3))
 def mm(n,rgb,metal=0,rough=.4,emit=0,trans=0):
  m=bpy.data.materials.new("M28_"+n)
  m.use_nodes=True
  q=m.node_tree.nodes["Principled BSDF"]
  q.inputs["Base Color"].default_value=(*rgb,1)
  q.inputs["Metallic"].default_value=metal
  q.inputs["Roughness"].default_value=rough
  q.inputs["Transmission Weight"].default_value=trans
  if emit:
   q.inputs["Emission Color"].default_value=(*rgb,1)
   q.inputs["Emission Strength"].default_value=emit
  return m
 M={
  "deep":mm("bluegreen_enamel_matte",(.055,.15,.20),metal=.3),
  "brass":mm("satin_warm_brass",(.66,.41,.19),metal=.75),
  "light":mm("warm_guide_light",(.97,.69,.34),emit=1.4),
  "cyan":mm("marine_telematics",(.17,.75,.76),emit=.7),
  "glass":mm("clear_optics",(.34,.64,.65),trans=.69,rough=.08),
  "ash":mm("finished_warm_ash",(.56,.40,.27)),
  "navy":mm("carbon_control_surface",(.12,.19,.24),metal=.34),
  "pale":mm("accessible_embossed_letter",(.94,.85,.68),emit=.55)
 }
 def take(o,name,m):
  o.name="M28_"+name
  for c in list(o.users_collection):c.objects.unlink(o)
  col.objects.link(o);o.data.materials.append(M[m]);built.append(o)
  return o
 def cube(n,local,dim,mat,bev=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz(local))
  o=bpy.context.object;o.dimensions=dim
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  take(o,n,mat)
  if bev:
   mod=o.modifiers.new("Hand_finished_edges","BEVEL");mod.width=bev;mod.segments=3
   o.modifiers.new("Weighted_normals","WEIGHTED_NORMAL")
  return o
 def cylinder(n,center,r,depth,mat,vertices=20):
  bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=r,depth=depth,location=xyz(center))
  return take(bpy.context.object,n,mat)
 def beam(n,a,b,r,m):
  a,b=Vector(xyz(a)),Vector(xyz(b));dv=b-a
  assert dv.length>1e-6
  bpy.ops.mesh.primitive_cylinder_add(vertices=14,radius=r,depth=dv.length,location=(a+b)/2)
  o=bpy.context.object;o.rotation_euler=dv.to_track_quat("Z","Y").to_euler()
  return take(o,n,m)
 def ring(n,center,r,minor,mat,rot=(0,0,0)):
  bpy.ops.mesh.primitive_torus_add(major_segments=72,minor_segments=10,
       location=xyz(center),rotation=rot,major_radius=r,minor_radius=minor)
  return take(bpy.context.object,n,mat)
 def textobj(n,label,pos,size,color):
  font=bpy.data.curves.new("M28_"+n+"_letters","FONT")
  font.body=label;font.size=size;font.extrude=.009
  font.align_x="LEFT"
  o=bpy.data.objects.new("M28_"+n,font);col.objects.link(o)
  o.location=xyz(pos)
  o.rotation_euler=(math.pi/2,0,0) # face -Y for visitor
  font.materials.append(M[color])
  # Convert text to triangles so GLB independent preview sees real letters.
  bpy.ops.object.select_all(action="DESELECT")
  o.select_set(True);bpy.context.view_layer.objects.active=o
  bpy.ops.object.convert(target="MESH")
  o=bpy.context.view_layer.objects.active
  built.append(o);return o
 # A gallery-wide storyline, not small identical museum plinths. It is
 # situated against the LAB side (x<=12) and keeps the middle aisle clear.
 # Height is gallery floor local ~.043, z>0.15 for active exhibits.
 cube("ORBITAL_CHAMBER_MAIN_NARRATIVE_PANEL",(10.15,-13.8,2.60),
      (.28,5.25,3.12),"deep",.13)
 cube("ORBITAL_CHAMBER_FRONT_DATA_PLANE",(10.31,-13.8,2.61),
      (.034,4.70,2.65),"navy",.035)
 # Text on visitor-facing Y-normal display (x side panel will be visible
 # obliquely from arrival, with a second upright wall facing the camera).
 cube("CINEMATIC_WELCOME_SIGN",(13.7,-16.0,3.64),
      (5.4,.17,1.36),"deep",.13)
 textobj("CENTRAL_SIGN_HEAD","ORBITAL RESEARCH",
         (11.30,-16.13,3.55),.43,"pale")
 textobj("CENTRAL_SIGN_SUB","LIVE  /  SPACE SYSTEMS",
         (11.60,-16.14,3.14),.205,"cyan")
 # Interactive science instrument in an intentionally inhabitable bay,
 # centered x~11.7 and gallery y~-11, away from 14-19 walking axis.
 cylinder("ORBIT_DISPLAY_STAND",(11.38,-11.15,.57),.93,1.09,"deep")
 cylinder("ORBIT_DISPLAY_LIT_PODIUM_RIM",(11.38,-11.15,1.15),1.02,.10,"brass")
 beam("ORBIT_INTERNAL_BEARING",(11.38,-11.15,1.20),
      (11.38,-11.15,3.70),.10,"brass")
 ring("MEAN_SOLAR_ORBIT",(11.38,-11.15,2.86),1.34,.043,"cyan",(.41,.53,0))
 ring("ALTITUDE_SCIENCE_ORBIT",(11.38,-11.15,2.86),1.07,.035,"brass",(.66,-.33,0))
 ring("ORBIT_TRACK_ACTIVE_ARC",(11.38,-11.15,2.86),1.18,.021,"light",(.15,.8,0))
 cylinder("MICROSATELLITE_ACTUAL_CORE",(11.38,-11.15,2.86),.27,.56,"deep")
 for sign in (-1,1):
  cube("PROBE_SOLAR_ARRAY_%d"%sign,(11.38+sign*.74,-11.15,2.86),
       (.95,.10,.44),"glass",.018)
 # Trace data along a near-facing panel with genuine 3D curves.
 for i in range(10):
  z=1.75+i*.175
  cube("LIVE_LINEAR_TELEMETRY_%02d"%i,(10.39,-15.58+i*.39,z),
       (.04,.32,.075),"cyan" if i%3 else "light")
 for i in range(3):
  cube("TELEMETRY_LARGE_HISTOGRAM_%d"%i,(10.38,-14.75+i*.7,1.31),
       (.055,.31,.32+.1*i),"cyan",.02)
 # Smaller interactive visitor tactile console by lab-side wall.
 cube("PUBLIC_TOUCH_PANEL_OAK_TABLE",(11.23,-20.05,.93),
      (2.10,1.05,.16),"ash",.07)
 cube("PUBLIC_TOUCH_PANEL",(11.23,-20.05,1.067),
      (1.73,.74,.065),"deep",.04)
 for i in range(5):
  cube("PUBLIC_TACTILE_CONTROL_%d"%i,(10.62+i*.26,-20.07,1.115),
       (.16,.24,.04),"light" if i==2 else "cyan",.019)
 for x in (10.45,12.0):
  beam("PUBLIC_CONSOLE_REAL_SUPPORT_%d"%int(x*100),
       (x,-20.04,.04),(x,-20.04,.84),.075,"brass")
 # Restrained depth cues and human-scale waiting niche.
 cube("VIEWING_SEAT_WARM_LOW_BENCH",(10.44,-5.2,.50),
      (2.2,1.25,.85),"ash",.15)
 cube("VIEWING_SEAT_CUSHION",(10.44,-5.2,.96),
      (1.98,1.08,.13),"deep",.14)
 cube("VIEWING_SEAT_BACK",(10.17,-4.68,1.38),
      (2.18,.24,.80),"ash",.10)
 # An overhead light-painting strip along the actual gallery roof.
 for i,y in enumerate((-23.5,-17.5,-11.5,-5.5)):
  beam("SHIELD_DAYLIGHT_GRAZER_%d"%i,
      (10.4,y,5.12),(17.2,y,5.22),.095,"brass")
  beam("NEAR_TRANSPARENT_LIGHT_STRIP_%d"%i,
      (10.4,y+.18,5.08),(17.2,y+.18,5.17),.027,"light")
 # Direct contribution of new specific display lighting, avoiding hard
 # black caustics and huge washout; keep original cameras strictly fixed.
 def area(n,pos,energy,size):
  l=bpy.data.lights.new("M28_"+n,"AREA")
  l.energy=energy;l.shape="DISK";l.size=size
  o=bpy.data.objects.new("M28_"+n,l);col.objects.link(o)
  o.location=xyz(pos)
  o.rotation_euler=(Vector(xyz((11.3,-12.0,2.3)))-o.location).to_track_quat("-Z","Y").to_euler()
 area("ORBITAL_DISPLAY_WARM_KEY",(14,-17,5.1),480,6)
 area("ADJACENT_GALLERY_CYAN_FILL",(15,-7,4.8),220,5)
 # Retain prior lighting rather than scrapping M26B room art.
 scene.cycles.samples=40
 assert all(o.name in bpy.data.objects for o in built)
 assert oldobjs.issubset(set(bpy.data.objects.keys()))
 assert len(built)>=35,(len(built),"not enough meaningful edit")
 assert all(o.hide_render for o in (bpy.data.objects.get(n) for n in HIDDEN))
 for name,ob in cameras.items():
  assert (tuple(ob.location),tuple(ob.rotation_euler),float(ob.data.lens))==campin[name],name
 for name,ob in ((FLOOR,floor),(THRESHOLD,threshold),
                ("M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD",originalroad)):
  assert sorted(tuple(round(float(w),5) for w in ob.matrix_world@v.co) for v in ob.data.vertices)==oldgeo[name],name
 # M27 has some other cameras; don't remove or move them.
 scene["M28"]="IMAGE_GUIDED_VISITOR_GALLERY_ART_HOLD"
 scene["ART"]="HOLD_NOT_APPROVED";scene["ADOPTED"]=0
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["G0_S1_G1_G2_G3"]="NOT_RUN";scene["331_BODY_993_FEET"]="NOT_RUN"
 scene.render.engine="CYCLES"
 scene.render.resolution_x=1080;scene.render.resolution_y=680
 scene.render.resolution_percentage=100;scene.render.image_settings.file_format="PNG"
 OUT.mkdir(parents=True)
 blend=OUT/"M28_EDITABLE_ORBITAL_GALLERY.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 views={}
 for name in VIEWS:
  scene.camera=cameras[name]
  img=OUT/("M28_"+name+".png");scene.render.filepath=str(img)
  bpy.ops.render.render(write_still=True)
  assert img.stat().st_size>2500
  views[name]={"sha256":sha(img),"bytes":img.stat().st_size}
 bpy.ops.object.select_all(action="DESELECT")
 for o in bpy.data.objects:
  if o.type=="MESH" and not o.hide_render:o.select_set(True)
 glb=OUT/"M28_VISITOR_GALLERY_ART_REVIEW_NOT_APPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 record={"stage":"M28_FIXED_CAMERA_GALLERY_EXPERIENTIAL_EDIT",
  "original_SHA256":PIN,
  "original_cameras_frozen":True,"camera_names":list(VIEWS),
  "hidden_old_foreground_objects":list(HIDDEN),"new_objects":len(built),
  "unchanged_M27_road_and_threshold":True,
  "design":"Image guided real orbital exhibit, public tactile display and illuminated human seating",
  "new_display_location_local":[11.38,-11.15,2.86],
  "new_touch_console_local":[11.23,-20.05,1.067],
  "display_lighting_changed":True,
  "art":"HOLD_NOT_APPROVED","adopted":0,
  "official_331_993":"NOT_RUN","formal_G0_S1_G2_G3":"NOT_RUN",
  "minecraft":"FORBIDDEN",
  "blend_sha256":sha(blend),"glb_sha256":sha(glb),"views":views,
  "caveat":"Same camera but different lighting AND geometry: pixel differences are not a single-factor causal estimate."}
 (OUT/"manifest.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding="utf-8")
 print("M28_NATIVE_M27_EDIT_AND_TWO_FIXED_EYES_COMPLETE_ART_HOLD",len(built))
if __name__=="__main__":
 if "--preflight" in sys.argv:print(json.dumps(preflight()))
 else:run()
