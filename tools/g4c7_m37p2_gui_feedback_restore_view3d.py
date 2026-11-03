#!/usr/bin/env python3
"""Restore real VIEW_3D after loading a native .blend last saved in Console.
No mesh mutation, no save, no Minecraft, ART HOLD.
"""
import bpy,hashlib,json,os
from pathlib import Path
PIN="3279d909da13e5b09660dc170e8bb79b51a733611e4d1d1c02ea97f4f920ded8"
def fix():
    if bpy.app.background:raise RuntimeError("REAL_GUI_REQUIRED")
    p=Path(bpy.data.filepath)
    if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=PIN:
        raise RuntimeError("PREVIOUS_SAVED_GUI_SOURCE_HASH_MISMATCH")
    s=bpy.context.scene
    if s.get("P2_ART")!="HOLD" or s.get("P2_OFFICIAL_ADOPTIONS")!=0:
        raise RuntimeError("CHARTER_BROKEN")
    ob=bpy.data.objects.get("Suzanne")
    if not ob or ob.type!="MESH" or len(ob.data.vertices)!=507:
        raise RuntimeError("EXACT_SAVED_GUI_MESH_NOT_PRESENT")
    windows=list(bpy.context.window_manager.windows)
    if len(windows)!=1:return 0.3
    areas=sorted((a for a in windows[0].screen.areas if a.type in ("CONSOLE","VIEW_3D")),
                 key=lambda a:a.width*a.height,reverse=True)
    if not areas:return 0.3
    area=areas[0]; old=area.type
    if old=="CONSOLE":area.type="VIEW_3D"
    if area.type!="VIEW_3D":raise RuntimeError("GUI_VIEW3D_NOT_RESTORED")
    ob.select_set(True)
    bpy.context.view_layer.objects.active=ob
    rv=area.spaces.active.region_3d
    rv.view_location=ob.location.copy()
    rv.view_distance=11
    area.tag_redraw()
    marker=Path(os.environ["G4C7_GUI_READY_MARKER"])
    if marker.exists():raise FileExistsError("APPEND_ONLY_GUI_READY_MARKER")
    marker.write_text(json.dumps({"status":"REAL_VIEW3D_RESTORED_NOT_ART",
        "before":old,"after":area.type,"source_sha256":PIN,
        "selected":ob.select_get(),"art":"HOLD","official_adoptions":0},indent=2)+"\n")
    print("REAL_GUI_VIEW3D_RESTORED_NOT_ART",flush=True)
    return None
bpy.app.timers.register(fix,first_interval=1.0)
