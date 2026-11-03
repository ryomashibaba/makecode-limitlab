#!/usr/bin/env python3
"""G4-C7 M37-P2: genuine DISPLAY-BACKED Blender GUI authoring context.

This addresses the gap between offline Cycles renders and the AUTHOR'S ACTUAL
two-panel 3D editing workspace. From Blender's real GUI, save native viewport
PNG screenshots + object/collection geometry evidence, *never* change meshes,
save the .blend, execute model code, or issue Minecraft writes.

This is a CAMERA / VIEWPORT CAPTURE capability, NOT autonomous city authoring.
No model API request is made; no images are sent outside the user's computer.

Blender 4.5+ GUI:
  blender <a vetted COPY of P2 v3 .blend> --python this_script.py

UI: 3D View -> side panel -> "P2 Live AI Context" -> "Capture Real 3D Views"
Smoke with display/Xvfb:
  blender path/to/pinned-v3.blend --python this_script.py -- \
      --gui-ci-capture /tmp/NEW_OUTPUT_FOLDER
"""
bl_info={
    "name":"G4C7 P2 Direct Author GUI Context — No Art",
    "author":"G4C7 research only",
    "version":(0,1,0),
    "blender":(4,5,0),
    "location":"3D View > Sidebar > P2 Live AI Context",
    "category":"3D View",
    "description":"Capture authentic editor views and mesh topology evidence; no geometry edits or ART PASS",
}
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import uuid

import bpy

V3_SHA="536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
COLLECTIONS=(
    "P2_CITY_MACRO_DIRECT_AUTHOR",
    "P2_INHABITED_SECTION_DIRECT_AUTHOR",
    "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
    "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
    "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
)
PNG_MAGIC=bytes.fromhex("89504e470d0a1a0a")
MAX_OBJECTS_PER_COLLECTION=180
MAX_OUTPUT_BYTES=8_000_000

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for part in iter(lambda:stream.read(1024*1024),b""):
            h.update(part)
    return h.hexdigest()

def _verify_scene():
    sc=bpy.context.scene
    if bpy.app.background:
        raise RuntimeError("REAL_BLENDER_GUI_REQUIRED_NOT_BACKGROUND")
    if (sc.get("P2_ART")!="HOLD" or sc.get("P2_OFFICIAL_ADOPTIONS")!=0
        or sc.get("P2_MINECRAFT")!="FORBIDDEN"
        or sc.get("P2_FORMAL_331_993")!="NOT_RUN"):
        raise RuntimeError("PROTECTED_P2_CHARTER_NOT_CONFIRMED")
    source=Path(bpy.data.filepath)
    if not bpy.data.filepath or not source.is_file():
        raise RuntimeError("SAVED_SOURCE_BLEND_REQUIRED")
    for name in COLLECTIONS:
        if bpy.data.collections.get(name) is None:
            raise RuntimeError("P2_AUTHORED_COLLECTION_MISSING_"+name)
    return sc,source

def _actual_meshes():
    result={}
    for name in COLLECTIONS:
        co=bpy.data.collections[name]
        meshes=[o for o in co.all_objects if o.type=="MESH"]
        result[name]={
            "count":len(meshes),
            "objects":[{
                "name":o.name[:120],
                "vertices":len(o.data.vertices),
                "faces":len(o.data.polygons),
                "scale":[round(float(x),4) for x in o.scale],
                "location":[round(float(x),4) for x in o.location],
                "bounds_local":[
                    [round(min(float(v.co[k]) for v in o.data.vertices),4) for k in range(3)],
                    [round(max(float(v.co[k]) for v in o.data.vertices),4) for k in range(3)]
                ] if o.data.vertices else None
            } for o in meshes[:MAX_OBJECTS_PER_COLLECTION]]
        }
    return result

def _viewport_areas():
    result=[]
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type!="VIEW_3D":continue
            region=next((r for r in area.regions if r.type=="WINDOW"),None)
            if region is not None and region.width>=100 and region.height>=100:
                result.append((win,area,region))
    # Do not pretend 2 camera renders are 2 native Blender viewports.
    if len(result)<2:
        raise RuntimeError("TWO_REAL_VIEW_3D_GUI_AREAS_REQUIRED")
    return result[:2]

def capture_gui_context(directory):
    scene,source=_verify_scene()
    views=_viewport_areas()
    dest=Path(directory).expanduser().resolve()
    if dest.exists():
        raise FileExistsError("APPEND_ONLY_GUI_CONTEXT_EXPORT_FOLDER_EXISTS")
    # Local export is outside the user's original .blend and source git tree.
    if str(dest)==str(source.parent) or dest==source or source in dest.parents:
        raise ValueError("OUTPUT_MUST_NOT_BE_INSIDE_PROTECTED_BLEND_SOURCE_LOCATION")
    before=sha(source)
    mesh_before={o.name:(len(o.data.vertices),len(o.data.polygons))
                 for o in scene.objects if o.type=="MESH"}
    groups=_actual_meshes()
    dest.mkdir(parents=True,exist_ok=False)
    imgs={}
    for idx,(win,area,region) in enumerate(views):
        name=("MACRO_EDITOR","LIVED_EDITOR")[idx]
        screenshot=dest/("P2_ACTUAL_GUI_"+name+".png")
        with bpy.context.temp_override(window=win,screen=win.screen,area=area,region=region):
            rv=bpy.ops.screen.screenshot_area(
                filepath=str(screenshot),check_existing=False)
        if "FINISHED" not in rv or not screenshot.is_file():
            raise RuntimeError("REAL_GUI_SCREENSHOT_NOT_CREATED_"+name)
        if not 1000<=screenshot.stat().st_size<=MAX_OUTPUT_BYTES:
            raise ValueError("REAL_VIEW_SCREENSHOT_FILE_SIZE_INVALID_"+name)
        if screenshot.open("rb").read(8)!=PNG_MAGIC:
            raise RuntimeError("REAL_VIEW_PNG_SIGNATURE_MISSING_"+name)
        view3d=area.spaces.active
        region3d=view3d.region_3d
        imgs[name]={
            "file":screenshot.name,
            "sha256":sha(screenshot),
            "width_px":region.width,"height_px":region.height,
            "projection":str(region3d.view_perspective),
            "look_at":[round(float(v),4) for v in region3d.view_location],
            "view_distance":round(float(region3d.view_distance),4),
            "source":"ACTUAL_BLENDER_GUI_VIEW_3D_NOT_CYCLES_RENDER",
        }
    if sha(source)!=before:
        raise RuntimeError("OPEN_SOURCE_BLEND_BYTES_CHANGED_DURING_GUI_CAPTURE")
    if mesh_before!={o.name:(len(o.data.vertices),len(o.data.polygons))
                    for o in scene.objects if o.type=="MESH"}:
        raise RuntimeError("MESH_TOPOLOGY_CHANGED_DURING_READ_ONLY_CAPTURE")
    report={
        "schema":"g4c7-m37p2-live-gui-visual-context-v1",
        "result":"TRUE_GUI_VIEWPORTS_AND_NATIVE_SCENE_DATA_CAPTURED",
        "blender_version":bpy.app.version_string,
        "bpy_background":bool(bpy.app.background),
        "source_basename":source.name,
        "source_blend_sha256":before,
        "source_is_protected_empty_v3":before==V3_SHA,
        "mesh_collections":groups,
        "all_scene_mesh_count":len(mesh_before),
        "views":imgs,
        "real_city_made":False if len(mesh_before)==0 else "NOT_ESTABLISHED",
        "human_art_quality":"NOT_JUDGED",
        "no_model_calls":True,
        "human_gui_edited_by_this_script":False,
        "art":"HOLD",
        "official_adoptions":0,
        "formal_331_993":"NOT_RUN",
        "makecode":"NOT_EVALUATED",
        "minecraft":"FORBIDDEN",
        "work":"NOT_USED",
    }
    (dest/"P2_ACTUAL_GUI_CONTEXT_HOLD.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return report

class G4C7_OT_p2_export_live_gui_context(bpy.types.Operator):
    bl_idname="g4c7.p2_export_live_gui_context"
    bl_label="Capture ACTUAL 3D Editors (No Art)"
    bl_description="Save read-only PNGs from both real Blender 3D editors and P2 scene data"

    def execute(self,context):
        root=(Path.home()/"Documents"/"G4C7"/"P2_Author_Sessions"/"LIVE_GUI_CONTEXT")
        root.mkdir(parents=True,exist_ok=True)
        dest=root/("P2_GUI_"+uuid.uuid4().hex[:12])
        try:
            result=capture_gui_context(dest)
        except Exception as exc:
            self.report({"ERROR"},str(exc)[:240])
            return {"CANCELLED"}
        self.report({"INFO"},("Real GUI captured: "+str(dest))[:230])
        print("P2_TRUE_GUI_CONTEXT_CAPTURE_HOLD",str(dest),result["all_scene_mesh_count"],flush=True)
        return {"FINISHED"}

class G4C7_PT_p2_live_gui_context(bpy.types.Panel):
    bl_label="P2 Live AI Context"
    bl_idname="G4C7_PT_P2_LIVE_GUI_CONTEXT"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="P2 Live AI Context"
    def draw(self,context):
        layout=self.layout
        layout.label(text="ACTUAL EDITOR 3D CONTEXT",icon="VIEW3D")
        layout.label(text="No models called. No geometry changed.")
        layout.operator("g4c7.p2_export_live_gui_context")
        layout.label(text="ART HOLD - 0 official adoptions",icon="ERROR")

CLASSES=(G4C7_OT_p2_export_live_gui_context,G4C7_PT_p2_live_gui_context)

def register():
    for cls in CLASSES:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

def unregister():
    for cls in reversed(CLASSES):
        try:
            bpy.utils.unregister_class(cls)
        except (ValueError,RuntimeError):
            pass

def _start():
    if "--" in sys.argv:
        args=sys.argv[sys.argv.index("--")+1:]
    else:
        args=[]
    p=argparse.ArgumentParser()
    p.add_argument("--gui-ci-capture",default=None)
    ns=p.parse_args(args)
    register()
    if ns.gui_ci_capture:
        # Give the GUI real frames to present both live editors before taking
        # a real screenshot. No fake Cycles still renders are substituted.
        def once():
            try:
                r=capture_gui_context(ns.gui_ci_capture)
                if len(r["views"])!=2:
                    raise RuntimeError("TWO_ACTUAL_GUI_VIEWPORTS_NOT_CAPTURED")
                print("PASS_GENUINE_P2_TWO_LIVE_GUI_VIEWPORTS_ART_HOLD",flush=True)
                code=0
            except Exception as exc:
                print("FAIL_GENUINE_GUI_SCREENSHOT",repr(exc),flush=True)
                code=8
            # Blender will exit its native GUI event loop; do not touch .blend.
            marker=Path(ns.gui_ci_capture).parent/"G4C7_GUI_SMOKE_STATUS.txt"
            marker.write_text(str(code),encoding="utf-8")
            bpy.ops.wm.quit_blender()
            return None
        bpy.app.timers.register(once,first_interval=3.0)

if __name__=="__main__":
    _start()
