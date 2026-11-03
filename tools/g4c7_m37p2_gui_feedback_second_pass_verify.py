#!/usr/bin/env python3
"""Fresh Blender process verifies genuine screenshot-guided GUI delta. Not city art."""
import bpy,hashlib,json,math,sys
from pathlib import Path
OLD="3279d909da13e5b09660dc170e8bb79b51a733611e4d1d1c02ea97f4f920ded8"
PIN="536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    if not bpy.app.background:raise RuntimeError("INDEPENDENT_BLENDER_PROCESS_REQUIRED")
    args=sys.argv[sys.argv.index("--")+1:]
    if len(args)!=3:raise RuntimeError("NEED_SEED_PARENT_REPORT")
    seed,parent,output=[Path(s).resolve() for s in args]
    actual=Path(bpy.data.filepath).resolve()
    if not all(p.is_file() for p in (seed,parent,actual)):raise RuntimeError("NATIVE_FILES_MISSING")
    if len(set((actual,seed,parent)))!=3 or sha(seed)!=OLD or sha(parent)!=PIN:
        raise RuntimeError("PINNED_SOURCE_VIOLATION")
    if output.exists():raise FileExistsError("APPEND_ONLY_REPORT_REQUIRED")
    scene=bpy.context.scene
    fixed={"P2_ART":"HOLD","P2_OFFICIAL_ADOPTIONS":0,
           "P2_MINECRAFT":"FORBIDDEN","P2_FORMAL_331_993":"NOT_RUN",
           "P2_MAKECODE_COST":"NOT_EVALUATED","P2_STUDIO_STAGE":"EMPTY_NO_ART_CREATED"}
    for name,value in fixed.items():
        if scene.get(name)!=value:raise RuntimeError("CHARTER_CHANGED_"+name)
    objects=[o for o in scene.objects if o.type=="MESH"]
    if len(objects)!=1 or objects[0].name!="Suzanne":
        raise RuntimeError("SAME_NATIVE_TECH_PROBE_MESH_MISSING")
    ob=objects[0]
    if len(ob.data.vertices)!=507 or len(ob.data.polygons)<500:
        raise RuntimeError("TOPOLOGY_CHANGED_OUTSIDE_GUI_PLAN")
    if any((abs(ob.location.x-8)>.02,abs(ob.location.y-5)>.02,
            abs(ob.scale.x-1.3)>.02,abs(ob.scale.y-1.3)>.02,
            abs(ob.rotation_euler.z-math.radians(30))>.02)):
        raise RuntimeError("SECOND_GUI_SHORTCUT_TRANSFORMS_NOT_SAVED")
    result={"status":"SECOND_REAL_GUI_SAME_NATIVE_EDIT_FRESH_RELOAD_TECH_PASS",
      "previous_blend_sha256":OLD,"new_blend_sha256":sha(actual),
      "parent_blend_sha256":PIN,
      "previous_reviewed_gui_image_sha256":"f1b9d8edcf5fbc385f0cc9bf220fd999ba5be7c6308b307bc81397c3916ef71d",
      "object":"Suzanne","vertices":len(ob.data.vertices),
      "location":[float(v) for v in ob.location],
      "scale":[float(v) for v in ob.scale],
      "rotation_degrees_z":math.degrees(ob.rotation_euler.z),
      "geometry_created_this_pass":False,"not_city_art":True,
      "not_autonomous_visual_ai":True,"art":"HOLD","official_adoptions":0,
      "safety":"NOT_RUN","makecode":"NOT_EVALUATED","minecraft":"FORBIDDEN"}
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(result["status"],result["new_blend_sha256"],flush=True)
if __name__=="__main__":main()
