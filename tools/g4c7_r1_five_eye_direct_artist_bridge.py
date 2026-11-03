#!/usr/bin/env python3
"""G4-C7 R1: five-eye bridge for a HUMAN DIRECTLY AUTHORED Blender city.

This is an authoring UI + independent saved-native renderer, NOT a city maker.
It NEVER creates mesh geometry, declares artistic acceptance or runs MakeCode.
The archived M37-P2 editor and the two rejected R1 scenes stay immutable.

Install as Blender add-on, or execute from Blender Text Editor to register UI.
Five actual saved-native Cycles views are a REVIEW INPUT, never ART PASS.

CLI after a genuinely edited NEW source .blend:
 blender -b /path/to/NEW-ARTIST-SOURCE.blend --python this.py -- --render /new/review/folder
"""
bl_info = {
 "name":"G4-C7 R1 Five-Eye Direct Author Bridge (NOT ART)",
 "author":"G4-C7 research", "version":(0,1,0), "blender":(4,5,0),
 "location":"3D View > Sidebar > G4-C7 Artist",
 "category":"3D View",
}
from pathlib import Path
import hashlib
import json
import os
import sys

EYES=(
 ("AERIAL","P2_CAMERA_AERIAL"),
 ("PUBLIC_EYE","P2_CAMERA_PUBLIC_EYE"),
 ("HABITAT_EYE","P2_CAMERA_HABITAT_EYE"),
 ("FACTORY_EYE","P2_CAMERA_FACTORY_EYE"),
 ("RESEARCH_EYE","P2_CAMERA_RESEARCH_EYE"),
)
GROUPS=(
 "P2_CITY_MACRO_DIRECT_AUTHOR",
 "P2_INHABITED_SECTION_DIRECT_AUTHOR",
 "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
 "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
 "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
)
REJECTED=("M37L_","M37N_","M37O_","M37P1_","M37M_EDIT_")
ARCHIVED_NAMES={
 "M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART.blend",
 "R1_CIVIC_BRAID_AUTHORIAL_SECTION_ART_UNREVIEWED.blend",
 "R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART.blend",
}
ART_CONTRACT={
 "P2_ART":"HOLD",
 "P2_OFFICIAL_ADOPTIONS":0,
 "P2_FORMAL_331_993":"NOT_RUN",
 "P2_MINECRAFT":"FORBIDDEN",
}
SOURCE_SUBMISSION="DIRECT_ARTIST_SOURCE_REVIEW_ONLY_NOT_PASS"

def _bpy():
 import bpy
 return bpy

def file_hash(path):
 h=hashlib.sha256()
 with open(path,"rb") as stream:
  for block in iter(lambda:stream.read(1024*1024),b""):
   h.update(block)
 return h.hexdigest()

def source_issues(scene, require_art=False):
 """Only reject invalid source/provenance. Never call a success ART PASS."""
 bpy=_bpy()
 issues=[]
 path=Path(bpy.data.filepath)
 if not bpy.data.filepath or not path.is_file():
  issues.append("NEW_SAVED_NATIVE_BLEND_REQUIRED")
 if path.name in ARCHIVED_NAMES:
  issues.append("ARCHIVED_OR_REJECTED_ORIGINAL_CANNOT_BE_REWRITTEN")
 if path.suffix.lower()!=".blend":
  issues.append("NOT_BLENDER_NATIVE")
 for key,val in ART_CONTRACT.items():
  if scene.get(key)!=val:
   issues.append("FROZEN_CHARTER_MISMATCH:"+key)
 if scene.get("P2_PARENT_REJECTED_FORM_IMPORTED")!=0:
  issues.append("REJECTED_PARENT_IMPORT_PROHIBITED")
 for ob in scene.objects:
  if ob.type=="MESH" and ob.name.startswith(REJECTED):
   issues.append("REJECTED_FORM_MESH:"+ob.name)
 for eye,name in EYES:
  ob=bpy.data.objects.get(name)
  if not ob or ob.type!="CAMERA" or ob.name not in scene.objects:
   issues.append("MISSING_ACTUAL_CAMERA:"+eye)
  elif require_art and not ob.get("G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED",False):
   issues.append("CAMERA_NOT_DIRECTLY_REVIEWED:"+eye)
 if require_art:
  if scene.get("G4C7_R1_DIRECT_AUTHOR_BRIDGE_STATE")!=SOURCE_SUBMISSION:
   issues.append("AUTHOR_SUBMISSION_DECLARATION_REQUIRED")
  if not scene.get("G4C7_R1_CITY_AND_LIVED_SECTION_COAUTHORED",False):
   issues.append("COAUTHORED_MACRO_AND_LIVED_SECTION_UNCONFIRMED")
  for name in GROUPS:
   coll=bpy.data.collections.get(name)
   if not coll or not any(ob.type=="MESH" and
            len(ob.data.vertices)>0 and len(ob.data.polygons)>0
            for ob in coll.all_objects):
    issues.append("NO_ACTUAL_AUTHOR_MESH_IN:"+name)
  if not any(ob.type=="MESH" for ob in scene.objects):
   issues.append("EMPTY_AUTHOR_SOURCE_NOT_ART")
 return sorted(set(issues))

def new_cameras_only():
 """Only append two missing *cameras* to a NEW copy. No mesh creation."""
 bpy=_bpy()
 s=bpy.context.scene
 problems=source_issues(s,require_art=False)
 illegal=[x for x in problems if not x.startswith("MISSING_ACTUAL_CAMERA:")]
 if illegal: raise RuntimeError(";".join(illegal))
 coll=bpy.data.collections.get("P2_CAMERA_RIG_NOT_ART")
 if coll is None or coll.name not in s.collection.children:
  raise RuntimeError("EXISTING_DIRECT_AUTHOR_CAMERA_COLLECTION_REQUIRED")
 for eye,name in EYES:
  if bpy.data.objects.get(name) is not None: continue
  if eye in ("AERIAL","PUBLIC_EYE","HABITAT_EYE"):
   raise RuntimeError("ORIGINAL_THREE_DIRECT_AUTHOR_CAMERAS_MISSING")
  cam=bpy.data.cameras.new(name+"_NEW_DIRECT_AUTHOR_DATA")
  ob=bpy.data.objects.new(name,cam)
  coll.objects.link(ob)
  ob.location=(0,0,40)
  ob["G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED"]=False
  ob["G4C7_R1_PROVISIONAL_NO_GEOMETRY"]=True
 # Existing camera framing/attestations must NOT be reset on re-entry.
 # Newly created cameras already start unconfirmed.
 s["G4C7_R1_FIVE_EYE_NO_MESH_CREATED"]=True
 return [a for a,_ in EYES]

def _current_eye(context):
 return next(name for eye,name in EYES if eye==context.scene.g4c7_r1_eye)

def snap_view_to_eye(context):
 """Human moves viewport; transfers this exact framing to selected camera."""
 bpy=_bpy()
 if context.area.type!="VIEW_3D" or context.space_data.type!="VIEW_3D":
  raise RuntimeError("REQUIRE_ACTUAL_VIEW_3D")
 p=source_issues(context.scene,require_art=False)
 if any(not x.startswith("MISSING_ACTUAL_CAMERA") for x in p):
  raise RuntimeError(";".join(p))
 cam=bpy.data.objects.get(_current_eye(context))
 if cam is None:raise RuntimeError("RUN_PREPARE_FIVE_CAMERAS_FIRST")
 matrix=context.space_data.region_3d.view_matrix.inverted()
 cam.matrix_world=matrix
 cam["G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED"]=False
 cam["G4C7_R1_PROVISIONAL_NO_GEOMETRY"]=False
 context.scene.camera=cam
 return cam.name

def approve_eye(context):
 """Attestation of composition, NOT objective image-quality certification."""
 bpy=_bpy()
 cam=bpy.data.objects.get(_current_eye(context))
 if cam is None:raise RuntimeError("MISSING_CAMERA")
 if not context.scene.camera or context.scene.camera.name!=cam.name:
  raise RuntimeError("FIRST_VIEW_AND_SNAP_EXACT_EYE")
 cam["G4C7_R1_EYE_COMPOSITION_EDITOR_CONFIRMED"]=True
 return cam.name

def render_saved_native(output):
 """Runs in an INDEPENDENT Blender background process with saved source loaded.

 Creates ONLY new PNGs and JSON in a new output folder. Never saves .blend.
 """
 bpy=_bpy()
 if not bpy.app.background:
  raise RuntimeError("INDEPENDENT_BACKGROUND_BLENDER_REQUIRED")
 s=bpy.context.scene
 source=Path(bpy.data.filepath).resolve()
 # A newly reopened .blend may be reported dirty in some background builds.
 # Hash the on-disk native before and after instead; never save source here.
 problems=source_issues(s,require_art=True)
 if problems:raise RuntimeError("REVIEW_INPUT_BLOCKED:"+";".join(problems))
 out=Path(output).resolve()
 if out.exists():raise FileExistsError("REVIEW_OUTPUT_APPEND_ONLY")
 if out==source.parent or source.is_relative_to(out):
  raise ValueError("CANNOT_USE_OR_OVERWRITE_NATIVE_SOURCE_DIRECTORY")
 before=file_hash(source)
 out.mkdir(parents=True)
 rows=[]
 for eye,cam_name in EYES:
  s.camera=bpy.data.objects[cam_name]
  s.render.engine="CYCLES"
  s.cycles.samples=max(16,min(s.cycles.samples,64))
  s.render.resolution_x=960
  s.render.resolution_y=600
  s.render.resolution_percentage=100
  s.render.image_settings.file_format="PNG"
  dest=out/(eye+"_ACTUAL_SAVED_NATIVE.png")
  if dest.exists():raise FileExistsError("NO_RENDER_OVERWRITE")
  s.render.filepath=str(dest)
  bpy.ops.render.render(write_still=True)
  if not dest.is_file() or dest.stat().st_size<5000:
   raise RuntimeError("INDEPENDENT_VIEW_NOT_RECORDED:"+eye)
  rows.append({"eye":eye,"camera":cam_name,"file":dest.name,
               "sha256":file_hash(dest),"bytes":dest.stat().st_size,
               "camera_matrix_world":[list(row) for row in s.camera.matrix_world]})
 if file_hash(source)!=before:
  raise RuntimeError("NATIVE_SOURCE_WAS_CHANGED")
 report={
  "schema":"g4c7-r1-direct-artist-five-eye-saved-native-review-v1",
  "source_native":str(source),"source_sha256":before,
  "five_true_cycles_from_same_independent_blender":rows,
  "source_editor_declaration_not_proof":SOURCE_SUBMISSION,
  "automatic_art_pass":False,"art":"HOLD","official_adoptions":0,
  "quality_assessment":"HUMAN_REVIEW_STILL_REQUIRED",
  "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
  "makecode":"NOT_EVALUATED","minecraft":"FORBIDDEN","world_writes":0
 }
 dest=out/"R1_DIRECT_ARTIST_FIVE_VIEW_REVIEW_NOT_ART.json"
 dest.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
 return report

def register():
 bpy=_bpy()
 from bpy.props import EnumProperty,BoolProperty,StringProperty
 class R1_OT_PREPARE(bpy.types.Operator):
  bl_idname="g4c7.r1_prepare_five_eyes"
  bl_label="Prepare missing 2 eyes in NEW author source"
  def execute(self,context):
   try:new_cameras_only()
   except Exception as e:self.report({"ERROR"},str(e)[:240]);return {"CANCELLED"}
   self.report({"INFO"},"Now 5 provisional camera roles. NO geometry or ART.")
   return {"FINISHED"}
 class R1_OT_SNAP(bpy.types.Operator):
  bl_idname="g4c7.r1_snap_eye"
  bl_label="Use current GUI view to frame selected eye"
  def execute(self,context):
   try:name=snap_view_to_eye(context)
   except Exception as e:self.report({"ERROR"},str(e)[:240]);return {"CANCELLED"}
   self.report({"INFO"},"Editor framed "+name+"; human check still required")
   return {"FINISHED"}
 class R1_OT_CONFIRM(bpy.types.Operator):
  bl_idname="g4c7.r1_confirm_eye"
  bl_label="I visually checked selected camera framing"
  def execute(self,context):
   try:name=approve_eye(context)
   except Exception as e:self.report({"ERROR"},str(e)[:240]);return {"CANCELLED"}
   self.report({"INFO"},name+" author framing attested; NOT ART PASS")
   return {"FINISHED"}
 class R1_OT_DECL(bpy.types.Operator):
  bl_idname="g4c7.r1_submit_direct_artist_source"
  bl_label="Mark completed manual source for early review"
  def execute(self,context):
   scene=context.scene
   if not scene.g4c7_r1_coauthored:
    self.report({"ERROR"},"Author must model macro AND lived section")
    return {"CANCELLED"}
   old=scene.get("G4C7_R1_DIRECT_AUTHOR_BRIDGE_STATE")
   scene["G4C7_R1_DIRECT_AUTHOR_BRIDGE_STATE"]=SOURCE_SUBMISSION
   scene["G4C7_R1_CITY_AND_LIVED_SECTION_COAUTHORED"]=True
   errors=source_issues(scene,require_art=True)
   if errors:
    if old is None:del scene["G4C7_R1_DIRECT_AUTHOR_BRIDGE_STATE"]
    else:scene["G4C7_R1_DIRECT_AUTHOR_BRIDGE_STATE"]=old
    self.report({"ERROR"},";".join(errors)[:240])
    return {"CANCELLED"}
   self.report({"INFO"},"SAVE AS NEW .blend; render in independent Blender; ART HOLD")
   return {"FINISHED"}
 class R1_OT_RENDER_SAVED(bpy.types.Operator):
  bl_idname="g4c7.r1_review_render_saved_five"
  bl_label="Render saved 5-eye source in background"
  bl_description="Start independent Blender subprocess and monitor asynchronously; ART HOLD"
  _process=None
  _timer=None
  _log_file=None
  _target=None
  _original=None
  _source_hash=None
  _started=0

  @classmethod
  def poll(cls,context):
   return context.window_manager.g4c7_r1_render_status!="RUNNING"

  def _release(self,context):
   if self._timer:
    context.window_manager.event_timer_remove(self._timer)
    self._timer=None

  def invoke(self,context,event):
   import subprocess,tempfile,time
   bpy=_bpy()
   if bpy.data.is_dirty:
    self.report({"ERROR"},"SAVE NEW ARTIST .blend BEFORE FIVE-VIEW REVIEW")
    return {"CANCELLED"}
   faults=source_issues(context.scene,require_art=True)
   if faults:
    self.report({"ERROR"},";".join(faults)[:230])
    return {"CANCELLED"}
   script=Path(__file__).resolve() if "__file__" in globals() else None
   if not script or not script.is_file():
    self.report({"ERROR"},"INSTALL THIS .py AS FILE ADD-ON BEFORE ONE-CLICK REVIEW")
    return {"CANCELLED"}
   current=Path(bpy.data.filepath).resolve()
   target=current.parent/(current.stem+"_FIVE_EYE_DIRECT_ARTIST_REVIEW_NOT_ART")
   if target.exists():
    self.report({"ERROR"},"REVIEW FOLDER EXISTS: APPEND-ONLY; SAVE NEW .blend")
    return {"CANCELLED"}
   self._original=current
   self._source_hash=file_hash(current)
   self._target=target
   cmd=[bpy.app.binary_path,"-b",str(current),"--python",str(script),
        "--","--render",str(target)]
   log=tempfile.NamedTemporaryFile(mode="w+b",prefix="g4c7_r1_native_5eye_",suffix=".log",delete=False)
   self._log_file=Path(log.name)
   try:
    self._process=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,
                                  cwd=str(current.parent))
   except Exception as exc:
    context.window_manager.g4c7_r1_render_status="FAILED_TO_START"
    self.report({"ERROR"},"INDEPENDENT_BLENDER_ERROR:"+str(exc)[:170])
    return {"CANCELLED"}
   finally:log.close()
   self._started=time.monotonic()
   context.window_manager.g4c7_r1_render_status="RUNNING"
   self._timer=context.window_manager.event_timer_add(0.8,window=context.window)
   context.window_manager.modal_handler_add(self)
   self.report({"INFO"},"Background Blender rendering 5 TRUE views; GUI responsive, ART HOLD")
   return {"RUNNING_MODAL"}

  def modal(self,context,event):
   import time
   if event.type!="TIMER" or event.timer!=self._timer:
    return {"PASS_THROUGH"}
   status=self._process.poll()
   if status is None:
    if time.monotonic()-self._started>1200:
     self._process.kill()
     self._process.wait(timeout=15)
     status=124
    else:
     return {"RUNNING_MODAL"}
   self._release(context)
   if status!=0:
    tail=self._log_file.read_text(encoding="utf-8",errors="replace")[-350:]
    context.window_manager.g4c7_r1_render_status="FAILED"
    self.report({"ERROR"},"BLENDER "+str(status)+": "+tail[-195:])
    return {"CANCELLED"}
   try:
    manifest=self._target/"R1_DIRECT_ARTIST_FIVE_VIEW_REVIEW_NOT_ART.json"
    meta=json.loads(manifest.read_text(encoding="utf8"))
    if (meta.get("automatic_art_pass") is not False or meta.get("art")!="HOLD"
        or meta.get("official_adoptions")!=0 or meta.get("source_sha256")!=self._source_hash
        or file_hash(self._original)!=self._source_hash):
     raise ValueError("REVIEW_OR_SOURCE_CONTRACT_CHANGED")
    views=meta.get("five_true_cycles_from_same_independent_blender")
    if not isinstance(views,list) or len(views)!=5:
     raise ValueError("FIVE_ACTUAL_VIEWS_REQUIRED")
    for eye,item in zip((e for e,_ in EYES),views):
     p=self._target/(eye+"_ACTUAL_SAVED_NATIVE.png")
     if item.get("eye")!=eye or item.get("sha256")!=file_hash(p):
      raise ValueError("REVIEW_IMAGE_TAMPERED:"+eye)
   except Exception as exc:
    context.window_manager.g4c7_r1_render_status="FAILED_AUDIT"
    self.report({"ERROR"},"REVIEW EVIDENCE INCOMPLETE:"+str(exc)[:160])
    return {"CANCELLED"}
   context.window_manager.g4c7_r1_render_status="FIVE_TRUE_NATIVE_IMAGES_NOT_ART"
   self.report({"INFO"},"5 genuine saved-native views + hashes verified; HUMAN ART REVIEW REQUIRED")
   return {"FINISHED"}

  def cancel(self,context):
   if self._process and self._process.poll() is None:
    self._process.kill()
   self._release(context)
   context.window_manager.g4c7_r1_render_status="CANCELLED"
 class R1_PT_PANEL(bpy.types.Panel):
  bl_label="G4-C7 R1 5-Eye Direct Artist"
  bl_idname="G4C7_PT_R1_FIVE_EYE_ARTIST"
  bl_space_type="VIEW_3D"
  bl_region_type="UI"
  bl_category="G4-C7 Artist"
  def draw(self,context):
   col=self.layout.column(align=True)
   col.label(text="DIRECT 3D AUTHOR ONLY — NO CITY GENERATOR")
   col.label(text="ART HOLD • No Safety QA • No Minecraft")
   col.operator("g4c7.r1_prepare_five_eyes")
   col.prop(context.scene,"g4c7_r1_eye",text="Review eye")
   col.operator("g4c7.r1_snap_eye")
   col.operator("g4c7.r1_confirm_eye")
   col.prop(context.scene,"g4c7_r1_coauthored",text="I authored macro + lived section")
   col.operator("g4c7.r1_submit_direct_artist_source")
   col.label(text="Save a NEW native .blend after manual editing")
   col.operator("g4c7.r1_review_render_saved_five")
   col.label(text="5-view status: " + context.window_manager.g4c7_r1_render_status)
   col.label(text="Actual image quality is NEVER auto-approved")
 classes=(R1_OT_PREPARE,R1_OT_SNAP,R1_OT_CONFIRM,R1_OT_DECL,R1_OT_RENDER_SAVED,R1_PT_PANEL)
 for cls in classes:bpy.utils.register_class(cls)
 bpy.types.Scene.g4c7_r1_eye=EnumProperty(name="Eye",items=[(a,a,"") for a,_ in EYES])
 bpy.types.Scene.g4c7_r1_coauthored=BoolProperty(name="Actual coupled author meshes",default=False)
 bpy.types.WindowManager.g4c7_r1_render_status=StringProperty(default="NOT_STARTED")
 return classes

if __name__=="__main__":
 args=sys.argv
 if "--render" in args:
  idx=args.index("--render")
  if idx+1>=len(args):raise SystemExit("MISSING_OUTPUT_FOLDER")
  print("G4C7_R1_FIVE_ACTUAL_SAVED_NATIVE",render_saved_native(args[idx+1]))
 else:
  register()
