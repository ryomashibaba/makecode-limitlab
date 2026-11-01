#!/usr/bin/env python3
"""M26B genuine native eye-informed interior art edit.
Preserve M26 source and the underlying M22 road. One camera only.
Changes: visual work information, optics, craft detail, graded daylight.
"""
import os,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEED=ROOT/"artifacts/m26b_pinned_M26_original"
OUT=ROOT/"artifacts/g4c7-m26b-occupied-work-visual-refinement"/("run_"+os.environ.get("GITHUB_SHA","local")[:12])
PIN="315581b06005436aeff6426c29b9d53dc539d8accd962cc87a0a8ceb2b69649a"
ORIGIN=(-43,37,9.6)
STREET="M22_ONE_CONNECTED_ARRIVAL_STAIR_BYPASS_ROAD"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def original():
 f=list(SEED.rglob("M26_EDITABLE_ROOM_FIRST_RESEARCH_ATELIER.blend"))
 assert len(f)==1,("pinned source uniqueness",len(f))
 assert sha(f[0])==PIN,"STOP: original source SHA mismatch"
 return f[0]
def do():
 import bpy
 from mathutils import Vector
 assert not OUT.exists(),"Append-only research evidence"
 bpy.ops.wm.open_mainfile(filepath=str(original().resolve()))
 scene=bpy.context.scene
 road=bpy.data.objects.get(STREET)
 assert road is not None
 road_before=sorted(tuple(round(float(c),5) for c in road.matrix_world@v.co) for v in road.data.vertices)
 old=set(bpy.data.objects.keys())
 cameras={o.name:(tuple(o.location),tuple(o.rotation_euler),o.data.lens)
          for o in bpy.data.objects if o.type=="CAMERA"}
 cam=bpy.data.objects.get("M26_HUMAN_EYE_CAMERA")
 assert cam and cam.type=="CAMERA" and abs(cam.data.lens-23.5)<.01
 col=bpy.data.collections.new("M26B_DIRECT_VIEW_EDIT_ADDED_ACTIVITY_NOT_CITY")
 scene.collection.children.link(col)
 changed=[]
 def xyz(v):return Vector((v[0]+ORIGIN[0],v[1]+ORIGIN[1],v[2]+ORIGIN[2]))
 def mm(n,rgb,metal=0,rough=.4,emission=0):
  m=bpy.data.materials.new("M26B_"+n)
  m.use_nodes=True
  p=m.node_tree.nodes["Principled BSDF"]
  p.inputs["Base Color"].default_value=(*rgb,1)
  p.inputs["Metallic"].default_value=metal
  p.inputs["Roughness"].default_value=rough
  if emission:
   p.inputs["Emission Color"].default_value=(*rgb,1)
   p.inputs["Emission Strength"].default_value=emission
  return m
 mats={
  "screen_ink":mm("data_chart_deep_blue",(.055,.18,.23)),
  "annotation":mm("lab_screen_turquoise",(.40,.92,.83),emission=.65),
  "copper":mm("satin_copper_orbit",(.53,.30,.17),metal=.64),
  "brass":mm("etched_brass",(.68,.49,.25),metal=.64),
  "glass":mm("optic_glass",(.45,.70,.69),rough=.16),
  "botanical":mm("fern_deep_green",(.16,.34,.23)),
  "warm":mm("golden_screen_indicator",(.95,.66,.33),emission=1.2)
 }
 def mesh_obj(o,n,material):
  o.name="M26B_"+n
  for c in list(o.users_collection):c.objects.unlink(o)
  col.objects.link(o)
  o.data.materials.append(mats[material])
  changed.append(o.name)
  return o
 def bar(n,center,dims,material,bevel=0):
  bpy.ops.mesh.primitive_cube_add(size=1,location=xyz(center))
  ob=bpy.context.object;ob.dimensions=dims
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  mesh_obj(ob,n,material)
  if bevel:
   m=ob.modifiers.new("Crafted_edge","BEVEL");m.width=bevel;m.segments=2
   ob.modifiers.new("Normal","WEIGHTED_NORMAL")
  return ob
 def pipe(n,a,b,r,material):
  a,b=xyz(a),xyz(b);v=b-a
  assert v.length>.0001
  bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=r,depth=v.length,location=(a+b)*.5)
  o=bpy.context.object;o.rotation_euler=v.to_track_quat("Z","Y").to_euler()
  return mesh_obj(o,n,material)
 def torus(n,center,major,minor,material,rotation=(0,0,0)):
  bpy.ops.mesh.primitive_torus_add(major_segments=56,minor_segments=8,
        location=xyz(center),rotation=rotation,
        major_radius=major,minor_radius=minor)
  return mesh_obj(bpy.context.object,n,material)
 # 1) Repair blank-screen perception: a real illuminated scientific orbit
 # interface on the VIEWER-facing screen, not a single flat colored block.
 # Front is negative Y; base display's front is Y≈-1.525.
 bar("left_screen_dark_instrument_ground",(-4.65,-1.559,1.68),
     (2.49,.035,1.21),"screen_ink",.025)
 torus("primary_orbital_plot",(-4.85,-1.596,1.72),.38,.016,"annotation",(math.pi/2,0,0))
 torus("secondary_orbit_confidence",(-4.85,-1.598,1.72),.28,.010,"warm",(math.pi/2,.32,0))
 for i in range(7):
  yy=-1.599
  x=-5.68+i*.26
  bar("small_hyperspectral_trace_%02d"%i,(x,yy,1.17+.027*(i%3)),
      (.17,.016,.07),"annotation")
 for i in range(5):
  z=2.07-i*.18
  bar("side_data_readout_%02d"%i,(-3.81,-1.599,z),
      (.50-.045*i,.017,.035),"annotation")
 for i in range(3):
  bar("warm_miniscreen_locator_%d"%i,(-5.69+i*.14,-1.60,2.23),
      (.07,.02,.045),"warm")
 # 2) Active science instrument: small articulated arm actually reaching
 # close to satellite demonstrator rather than anonymous detached tubes.
 pipe("optics_arm_lower_joint",(-2.6,3.6,1.12),(-2.6,3.6,2.45),.09,"copper")
 pipe("optics_arm_articulated_forearm",(-2.6,3.6,2.45),(-1.25,2.8,3.13),.08,"copper")
 pipe("optics_arm_precise_probe",(-1.25,2.8,3.13),(-.70,2.46,3.18),.055,"brass")
 for j,(x,y,z) in enumerate(((-2.6,3.6,2.45),(-1.25,2.8,3.13))):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.17,
      location=xyz((x,y,z)))
  mesh_obj(bpy.context.object,"articulated_copper_joint_%d"%j,"brass")
 pipe("light_grazing_optical_test_line",(-1.00,2.40,3.17),
      (-.44,2.19,3.02),.014,"annotation")
 # 3) Trace the real experiment's relation to human-scale floor to give
 # the object spatial legibility, not to fake physical safety.
 torus("floor_inlaid_symmetric_orbital_mark",(0,2.12,.075),3.05,.026,"brass")
 for j,angle in enumerate((.4,1.4,2.6,4.1,5.2)):
  x=3.17*math.cos(angle);y=2.12+3.17*math.sin(angle)
  bar("floor_embedded_wayfinder_%d"%j,(x,y,.08),(.36,.10,.025),"brass",.01)
 # 4) Real work artifacts and directional details on wetlab and lounge.
 for i in range(5):
  x=3.7+i*.49
  bar("wetlab_data_sample_tray_%d"%i,(x,3.18,1.09),(.34,.31,.065),"screen_ink",.035)
  bar("wetlab_sample_status_%d"%i,(x,3.15,1.135),(.12,.055,.03),"warm")
 bar("lounge_open_book_left_page",(2.22,-6.33,1.07),(.55,.50,.045),"glass",.025)
 bar("lounge_open_book_right_page",(2.72,-6.33,1.07),(.48,.50,.045),"glass",.025)
 # 5) Deliberately refine over-flat original exposure while preserving
 # the M26 camera, geometry, and painted room surfaces.
 sun=bpy.data.objects.get("M26_room_sun")
 assert sun and sun.type=="LIGHT"
 sun.data.energy=1.23
 daylight=bpy.data.objects.get("M26_wide_window_daylight")
 assert daylight and daylight.type=="LIGHT"
 daylight.data.energy=1150
 assert scene.world and scene.world.use_nodes
 scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value=.61
 scene.cycles.samples=44
 # The original camera is fixed; no fabricated comparison angle.
 assert cameras=={o.name:(tuple(o.location),tuple(o.rotation_euler),o.data.lens)
                for o in bpy.data.objects if o.type=="CAMERA"}
 assert old.issubset(set(bpy.data.objects.keys())) and len(changed)>=30
 assert road_before==sorted(tuple(round(float(c),5) for c in road.matrix_world@v.co)
                           for v in road.data.vertices)
 scene.camera=cam
 scene["M26B"]="REAL_IMAGE_GUIDED_INTERIOR_REFINEMENT_ART_HOLD"
 scene["MINECRAFT_EDUCATION_WRITES"]=0
 scene["FORMAL_G0_S1_G1_G2_G3"]="NOT_RUN"
 scene["FORMAL_BODY331_FEET993"]="NOT_RUN"
 OUT.mkdir(parents=True)
 blend=OUT/"M26B_EDITED_HUMAN_RESEARCH_ROOM.blend"
 bpy.ops.wm.save_as_mainfile(filepath=str(blend),check_existing=False)
 img=OUT/"M26B_SAME_HUMAN_EYE.png"
 scene.render.filepath=str(img)
 bpy.ops.render.render(write_still=True)
 assert img.stat().st_size>4000
 bpy.ops.object.select_all(action="DESELECT")
 for ob in bpy.data.objects:
  if ob.type=="MESH" and not ob.hide_render:ob.select_set(True)
 glb=OUT/"M26B_INTERIOR_ART_REVIEW_UNAPPROVED.glb"
 bpy.ops.export_scene.gltf(filepath=str(glb),export_format="GLB",use_selection=True)
 manifest={"stage":"M26B_NATIVE_DIRECT_ROOM_VISUAL_EDIT",
  "source_sha256":PIN,"source_objects_untouched":True,
  "new_detail_objects":len(changed),"new_detail_names":changed,
  "camera_frozen":True,
  "material_changes":"New overlay materials only, existing materials unchanged",
  "lighting_changes":{"sun_energy_before":1.65,"sun_energy_after":1.23,
     "daylight_energy_before":1600,"daylight_energy_after":1150,
     "world_strength_before":.75,"world_strength_after":.61},
  "road_unchanged":True,
  "png_sha256":sha(img),"blend_sha256":sha(blend),"glb_sha256":sha(glb),
  "art":"HOLD_NOT_APPROVED","adopted":0,
  "minecraft":"FORBIDDEN","formal_331_993":"NOT_RUN",
  "limitations":"Only one fixed human eye viewpoint. Lighting AND detail added, no controlled single-factor causal attribution."}
 (OUT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print("M26B_NATIVE_IMAGE_GUIDED_ROOM_EDIT_COMPLETE_ART_HOLD",len(changed))
if __name__=="__main__":
 if "--preflight" in os.sys.argv:print("M26B_PINNED_NATIVE_SOURCE",original())
 else:do()
