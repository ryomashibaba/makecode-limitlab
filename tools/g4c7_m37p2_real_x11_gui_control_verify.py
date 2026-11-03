#!/usr/bin/env python3
"""Independent Blender reload: GUI shortcuts created mesh and transform. Not art."""
import bpy
import hashlib
import json
import sys
from pathlib import Path

PIN="536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda:f.read(1<<20),b""):h.update(block)
    return h.hexdigest()

def main():
    if not bpy.app.background:raise RuntimeError("INDEPENDENT_BACKGROUND_PROCESS_REQUIRED")
    args=sys.argv[sys.argv.index("--")+1:]
    if len(args)!=2:raise RuntimeError("NEED_PARENT_AND_REPORT_PATH")
    parent,output=map(lambda x:Path(x).resolve(),args)
    native=Path(bpy.data.filepath).resolve()
    if not parent.is_file() or sha(parent)!=PIN:raise RuntimeError("PROTECTED_ORIGINAL_HASH_REJECT")
    if not native.is_file() or native==parent:raise RuntimeError("DISTINCT_REAL_SAVED_BLEND_REQUIRED")
    if output.exists():raise RuntimeError("APPEND_ONLY_OUTPUT_REJECT")
    scene=bpy.context.scene
    checks={"P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,"P2_MINECRAFT":"FORBIDDEN",
        "P2_FORMAL_331_993":"NOT_RUN","P2_MAKECODE_COST":"NOT_EVALUATED",
        "P2_STUDIO_STAGE":"EMPTY_NO_ART_CREATED"}
    for k,v in checks.items():
        if scene.get(k)!=v:raise RuntimeError("CHARTER_INVALID_"+k)
    objs=[x for x in scene.objects if x.type=="MESH"]
    if len(objs)!=1 or objs[0].name!="Suzanne":raise RuntimeError("GUI_ADD_MONKEY_NOT_PROVEN")
    o=objs[0]
    if len(o.data.vertices)<500 or len(o.data.polygons)<500:
        raise RuntimeError("REAL_MONKEY_MESH_NOT_PROVEN")
    if abs(o.location.x-8)>.02 or abs(o.scale.x-2)>.02:
        raise RuntimeError("GUI_MOVE_SCALE_NOT_PROVEN")
    result={"status":"TRUE_GUI_X11_SHORTCUT_AND_NATIVE_RELOAD_TECH_ONLY",
        "native_sha256":sha(native),"parent_sha256":sha(parent),
        "mesh_name":o.name,"vertices":len(o.data.vertices),
        "position":list(o.location),"scale":list(o.scale),
        "not_ai_art_author":True,"not_city_art":True,
        "art":"HOLD","official_adoptions":0,"safety":"NOT_RUN",
        "makecode":"NOT_EVALUATED","minecraft":"FORBIDDEN"}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(result["status"],flush=True)

if __name__=="__main__":main()
