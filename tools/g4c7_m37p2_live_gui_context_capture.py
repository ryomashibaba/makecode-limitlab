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
import shutil
import subprocess
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

def _prepare_two_viewports_for_pinned_ci_only():
    """Call the already-proven P2 GUI split operator from the pinned .blend.

    Only the --gui-ci-capture test path ever invokes this. It changes the
    transient visible Blender UI layout, not any meshes or saved original.
    Embedded script origin is a SHA-pinned protected native Blender v3.
    """
    source=Path(bpy.data.filepath)
    if not source.is_file() or sha(source)!=V3_SHA:
        raise RuntimeError("ONLY_PINNED_V3_MAY_BOOTSTRAP_CI_GUI_SPLIT")
    active=bpy.context.window or next(iter(bpy.context.window_manager.windows),None)
    if active is None:
        raise RuntimeError("REAL_NATIVE_WINDOW_REQUIRED_FOR_CI_SPLIT")
    areas=[a for a in active.screen.areas if a.type=="VIEW_3D"]
    if len(areas)>=2:
        return
    script=bpy.data.texts.get("M37P2_RUN_ONCE_PARALLEL_MACRO_LIVED_GUI.py")
    if script is None:
        raise RuntimeError("PINNED_V3_EMBEDDED_SPLIT_OPERATOR_MISSING")
    scope={
        "__name__":"g4c7_pinned_gui_split_ci",
        "__file__":"PINNED_V3_EMBEDDED_BLENDER_UI_SCRIPT",
    }
    exec(compile(script.as_string(),"PINNED_V3_GUI_SPLIT", "exec"),scope)
    scope["register"]()
    area=areas[0] if areas else None
    if area is None:
        raise RuntimeError("REAL_V3_VIEW_3D_EDITOR_MISSING")
    region=next((r for r in area.regions if r.type=="WINDOW"),None)
    if region is None:
        raise RuntimeError("REAL_V3_VIEW_WINDOW_REGION_MISSING")
    with bpy.context.temp_override(window=active,screen=active.screen,area=area,region=region):
        result=bpy.ops.g4c7.p2_parallel_split()
    if "FINISHED" not in result:
        raise RuntimeError("PINNED_V3_SPLIT_DID_NOT_EXECUTE")
    print("G4C7_CI_ONLY_NATIVE_GUI_SPLIT_REQUESTED",flush=True)


def _prove_actual_visible_pixels(image_file):
    """Native Blender image decoder checks content; PNG magic alone is not art.

    Earlier CI #41559389596 returned SUCCESS but both 657x783 editor images
    were 100% black. Such fake-positive captures are NOT useful for vision.
    This raises before the saved source and screenshots can be called valid.
    """
    im=bpy.data.images.load(str(image_file),check_existing=False)
    try:
        count=im.size[0]*im.size[1]
        if count<10000:
            raise ValueError("REAL_GUI_IMAGE_TOO_SMALL")
        pixels=im.pixels
        stride=max(1,count//4096)
        bright=0
        total=0
        for i in range(0,count,stride):
            k=4*i
            r,g,b=float(pixels[k]),float(pixels[k+1]),float(pixels[k+2])
            if max(r,g,b)>0.08:
                bright+=1
            total+=1
        ratio=bright/max(total,1)
        # A real empty Blender viewport is dark gray with visible grid,
        # headings and controls. A 100%-black Xvfb texture is not.
        if ratio<0.035:
            raise RuntimeError("REAL_GUI_SCREENSHOT_BLACK_OR_UNDRAWN_REJECT")
        return round(ratio,6)
    finally:
        bpy.data.images.remove(im)


def capture_gui_context(directory):
    scene,source=_verify_scene()
    views=_viewport_areas()
    dest=Path(directory).expanduser().resolve()
    if dest.exists():
        raise FileExistsError("APPEND_ONLY_GUI_CONTEXT_EXPORT_FOLDER_EXISTS")
    # Local export is outside the user's original .blend and source git tree.
    if dest==source.parent or source.parent in dest.parents:
        raise ValueError("OUTPUT_MUST_NOT_BE_INSIDE_PROTECTED_BLEND_SOURCE_LOCATION")
    before=sha(source)
    mesh_before={o.name:(len(o.data.vertices),len(o.data.polygons))
                 for o in scene.objects if o.type=="MESH"}
    groups=_actual_meshes()
    dest.mkdir(parents=True,exist_ok=False)
    # Record Blender's native window-relative region coordinates BEFORE the
    # screenshot API can fail with a valid-but-completely-black PNG.
    # This is geometry provenance for an independent X11 pixel diagnostic,
    # not a model screenshot, ART evidence or source .blend mutation.
    main_window=views[0][0]
    geometry={
        "schema":"g4c7-p2-native-gui-window-regions-v1",
        "same_window":views[0][0] is views[1][0],
        "window_dimensions":[int(main_window.width),int(main_window.height)],
        "source_blend_sha256":before,
        "art":"HOLD","official_adoptions":0,"minecraft":"FORBIDDEN",
        "regions":{
            name:{
                "x":int(region.x),"y":int(region.y),
                "width":int(region.width),"height":int(region.height)}
            for name,(_,area,region) in zip(
                ("MACRO_EDITOR","LIVED_EDITOR"),views)
        },
        "x11_region_crop_is_art":False,
    }
    (dest/"P2_GUI_NATIVE_REGION_GEOMETRY_DIAGNOSTIC_ONLY.json").write_text(
        json.dumps(geometry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    imgs={}
    for idx,(win,area,region) in enumerate(views):
        name=("MACRO_EDITOR","LIVED_EDITOR")[idx]
        screenshot=dest/("P2_ACTUAL_GUI_"+name+".png")
        area.tag_redraw()
        with bpy.context.temp_override(window=win,screen=win.screen,area=area,region=region):
            # Force a full displayed-window draw and actual framebuffer swap.
            # The previous timer capture returned valid but entirely BLACK PNG.
            bpy.ops.wm.redraw_timer(type="DRAW_WIN_SWAP",iterations=4)
            rv=bpy.ops.screen.screenshot_area(
                filepath=str(screenshot),check_existing=False)
        if "FINISHED" not in rv or not screenshot.is_file():
            raise RuntimeError("REAL_GUI_SCREENSHOT_NOT_CREATED_"+name)
        if not 1000<=screenshot.stat().st_size<=MAX_OUTPUT_BYTES:
            raise ValueError("REAL_VIEW_SCREENSHOT_FILE_SIZE_INVALID_"+name)
        if screenshot.open("rb").read(8)!=PNG_MAGIC:
            raise RuntimeError("REAL_VIEW_PNG_SIGNATURE_MISSING_"+name)
        visible_ratio=_prove_actual_visible_pixels(screenshot)
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
            "visible_bright_pixel_ratio":visible_ratio,
            "content_not_blank_black":True,
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

def _ci_x11_root_diagnostic(path):
    """Capture the X11 framebuffer separately from Blender's screenshot API.

    CI ONLY.  This is *diagnostic*, never substituted for Blender's native
    viewport screenshots or counted as a visually valid city/art capture.
    A root capture helps isolate a bad bpy screenshot from an undrawn Xvfb
    window.  It may contain the whole display rather than either 3D editor.
    """
    output=Path(path).resolve()
    output.mkdir(parents=True,exist_ok=True)
    report={
        "status":"NOT_AVAILABLE",
        "mode":"X11_ROOT_DIAGNOSTIC_ONLY_NOT_ART_NOT_EDITOR_SCREENSHOT",
        "original_blend_not_saved":True,
    }
    tool=shutil.which("import")
    if os.environ.get("DISPLAY") and tool:
        image=output/"P2_X11_ROOT_DIAGNOSTIC_ONLY.png"
        try:
            proc=subprocess.run([tool,"-window","root",str(image)],
                  stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                  timeout=20,check=False)
            report["exit_code"]=proc.returncode
            report["stderr"]=proc.stderr.decode("utf-8","replace")[:1200]
            if proc.returncode==0 and image.is_file():
                report["status"]="CAPTURED_NEEDS_INDEPENDENT_PIXEL_INSPECTION"
                report["bytes"]=image.stat().st_size
                report["sha256"]=sha(image)
            else:
                report["status"]="X11_CAPTURE_COMMAND_FAILED"
        except Exception as exc:
            report["status"]="X11_DIAGNOSTIC_ERROR"
            report["error"]=str(exc)[:250]
    (output/"P2_X11_ROOT_DIAGNOSTIC_STATUS.json").write_text(
        json.dumps(report,ensure_ascii=False,indent=2)+"\n",
        encoding="utf-8")
    print("P2_CI_X11_ROOT_DIAGNOSTIC",report["status"],flush=True)


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
        _prepare_two_viewports_for_pinned_ci_only()
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
            # An independent X11 root snapshot, strictly diagnostic and NEVER
            # accepted as a substitute for valid native VIEW_3D screenshots.
            _ci_x11_root_diagnostic(ns.gui_ci_capture)
            # Independent X11 full-window diagnostic. This is NEVER a VIEW_3D
            # screenshot or city ART, and cannot make a black native capture PASS.
            try:
                script = Path(__file__).with_name("g4c7_m37p2_x11_window_probe.py")
                if script.is_file():
                    diag = subprocess.run(
                        ["python3", str(script), "--out", ns.gui_ci_capture],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                        timeout=30, check=False)
                    print("P2_INDEPENDENT_X11_BLENDER_WINDOW",
                          diag.returncode, diag.stdout.decode("utf-8", "replace")[:500],
                          diag.stderr.decode("utf-8", "replace")[:300], flush=True)
                else:
                    print("P2_X11_BLENDER_PROBE_SCRIPT_MISSING", flush=True)
            except Exception as exc:
                print("P2_X11_WINDOW_PROBE_DIAGNOSTIC_ERROR", repr(exc)[:300], flush=True)
            # Blender will exit its native GUI event loop; do not touch .blend.
            marker=Path(ns.gui_ci_capture).parent/"G4C7_GUI_SMOKE_STATUS.txt"
            marker.write_text(str(code),encoding="utf-8")
            # CI-only: stop without making any Blender session-recovery .blend
            # or prompting to save the unchanged original editor scene.
            os._exit(code)
            return None
        bpy.app.timers.register(once,first_interval=3.0)

if __name__=="__main__":
    _start()
