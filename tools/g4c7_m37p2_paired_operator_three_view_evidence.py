#!/usr/bin/env python3
"""Render an existing, saved M37-P2 two-role native-operator trial.

VISUAL TECH REVIEW ONLY. It neither generates geometry nor changes source .blend.
Renders AERIAL, PUBLIC_EYE, HABITAT_EYE from the SAME stored file as distinct
Cycles images; framing is automatic and NOT author-approved art photography.

Usage (with bpy):
  python g4c7_m37p2_paired_operator_three_view_evidence.py \
    --source /path/to/P2_NATIVE_EDITOR_PAIRED_STUDY_UNAPPROVED.blend \
    --out /new/path/three_view
"""
import argparse
import hashlib
import html
import json
from pathlib import Path
import sys

CAMERAS = (
    ("AERIAL", "P2_CAMERA_AERIAL", "都市全景／仮フレーミング"),
    ("PUBLIC_EYE", "P2_CAMERA_PUBLIC_EYE", "公共側目線／仮フレーミング"),
    ("HABITAT_EYE", "P2_CAMERA_HABITAT_EYE", "住居側目線／仮フレーミング"),
)

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(source, out):
    import bpy
    from mathutils import Vector
    source = Path(source).resolve()
    target = Path(out).resolve()
    if not source.is_file():
        raise FileNotFoundError("PAIRED_NATIVE_STUDY_BLEND_MISSING")
    if target.exists():
        raise FileExistsError("APPEND_ONLY_PREVIEW_FOLDER_EXISTS")
    source_sha = sha(source)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    sc = bpy.context.scene
    if (sc.get("P2_SOURCE_KIND") != "LOCAL_LLM_NATIVE_EDIT_OPERATOR_TRIAL_NOT_GUI_HUMAN" or
        sc.get("P2_ART") != "HOLD" or
        sc.get("P2_OFFICIAL_ADOPTIONS") != 0 or
        sc.get("P2_MINECRAFT") != "FORBIDDEN" or
        sc.get("P2_CAMERA_VIEWS_AUTHOR_APPROVED") is not False):
        raise RuntimeError("UNAPPROVED_SAVED_NATIVE_STUDY_PROVENANCE_REQUIRED")
    from g4c7_m37p2_native_operator_author import ROLES
    meshes={}
    for role, name in ROLES.items():
        col=bpy.data.collections.get(name)
        if col is None:
            raise RuntimeError("MISSING_P2_COLLECTION_"+name)
        objects=[o for o in col.objects if o.type == "MESH"]
        if len(objects) != 1 or len(objects[0].data.polygons)<2:
            raise RuntimeError("EXPECTED_ONE_ACTUALLY_EDITED_NATIVE_MESH_"+role)
        meshes[role]=objects[0]

    # Compute actual WORLD bounds of these two role-specific native meshes.
    corners=[]
    for obj in meshes.values():
        corners.extend(obj.matrix_world @ v.co for v in obj.data.vertices)
    if not corners:
        raise RuntimeError("NO_REAL_NATIVE_VERTICES")
    low=Vector([min(v[k] for v in corners) for k in range(3)])
    high=Vector([max(v[k] for v in corners) for k in range(3)])
    center=(low+high)/2
    size=max(high[k]-low[k] for k in range(3))
    size=max(size,4.0)

    positions={
        "AERIAL":(center+Vector((size*1.35,-size*1.45,size*1.6)),center),
        "PUBLIC_EYE":(center+Vector((0,-size*1.6,size*.18)),center+Vector((0,0,size*.13))),
        "HABITAT_EYE":(center+Vector((size*1.4,size*.38,size*.14)),meshes["habitat"].matrix_world.translation+Vector((0,0,size*.1))),
    }
    target.mkdir(parents=True,exist_ok=False)
    # A neutral light and world are added in-memory only, for test visibility.
    # They are NEVER saved back into the original .blend.
    world=bpy.data.worlds.new("P2_EVIDENCE_IN_MEMORY_WORLD")
    world.use_nodes=True
    bg=world.node_tree.nodes.get("Background")
    if bg is not None:
        bg.inputs["Color"].default_value=(.55,.60,.69,1)
        bg.inputs["Strength"].default_value=.9
    sc.world=world
    sun=bpy.data.lights.new("P2_EVIDENCE_IN_MEMORY_SUN","SUN")
    sun.energy=2.5
    sun_obj=bpy.data.objects.new("P2_EVIDENCE_IN_MEMORY_SUN",sun)
    sc.collection.objects.link(sun_obj)
    sun_obj.rotation_euler=(.25,-.45,-.65)

    sc.render.engine="CYCLES"
    sc.cycles.samples=12
    sc.render.resolution_x=900
    sc.render.resolution_y=560
    sc.render.resolution_percentage=100
    sc.render.image_settings.file_format="PNG"
    photos={}
    for key,camera_name,label in CAMERAS:
        camera=bpy.data.objects.get(camera_name)
        if camera is None or camera.type!="CAMERA":
            raise RuntimeError("P2_ACTUAL_CAMERA_NOT_FOUND_"+camera_name)
        eye,at=positions[key]
        camera.location=eye
        camera.rotation_euler=(at-eye).to_track_quat("-Z","Y").to_euler()
        camera.data.lens=38
        sc.camera=camera
        path=target/("P2_PAIRED_NATIVE_"+key+"_NO_ART.png")
        sc.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
            raise RuntimeError("NOT_GENUINE_BLENDER_PNG_"+key)
        photos[key]={"filename":path.name,"sha256":sha(path),
                     "camera":camera_name,"frame":"AUTOMATIC_NOT_ARTIST_APPROVED"}
    if sha(source)!=source_sha:
        raise RuntimeError("ORIGINAL_NATIVE_STUDY_CHANGED_DURING_RENDER")
    evidence={
        "schema":"g4c7-m37p2-paired-native-three-view-tech-only-v1",
        "result":"NATIVE_CYCLES_RENDERED_NON_ART_TECH_EVIDENCE",
        "original_stored_blend_sha256":source_sha,
        "roles":{role:{"object":obj.name,
                       "vertices":len(obj.data.vertices),
                       "faces":len(obj.data.polygons)} for role,obj in meshes.items()},
        "views":photos,
        "art":"HOLD","official_adoptions":0,
        "human_gui_authorship":"NOT_PERFORMED",
        "camera_positions_author_approved":False,
        "true_city":False,"factory_boundary":"NOT_AUTHORED",
        "research_culture":"NOT_AUTHORED",
        "habitat_living_interior":"NOT_AUTHORED",
        "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN",
        "makecode":"NOT_EVALUATED",
    }
    (target/"P2_NATIVE_PAIRED_THREE_VIEW_REPORT.json").write_text(
        json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    sections="".join(
        "<section><h2>"+html.escape(label)+"</h2><img src='"+
        html.escape(photos[key]["filename"])+"' alt='Actual Blender technical evidence'></section>"
        for key,_,label in CAMERAS
    )
    page=(
        "<!doctype html><html lang='ja'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        "<title>P2 Blender 3視点技術検証／ARTではない</title>"
        "<style>body{background:#151a22;color:#f1f1f4;font-family:system-ui;"
        "max-width:1080px;margin:auto;padding:20px}section{background:#222b39;"
        "border-radius:12px;padding:12px;margin:20px 0}img{width:100%;"
        "height:auto;display:block}</style></head><body>"
        "<h1>M37-P2／本物のBlender 3視点（技術テスト）</h1>"
        "<p><strong>ART HOLD／正式採用0。</strong> モデル自体は"
        "2つの操作検証用試験形状であり、街並み・室内・工場・文化空間を"
        "実際に造形したものではありません。正式美術の合格証拠ではありません。</p>"
        +sections+
        "<p>同一の保存済みBLENDを読み取り、メモリ上で仮カメラを配置した"
        "Cycles撮影結果です。正式331人体・993足元／Minecraft施工未実施。</p>"
        "</body></html>"
    )
    (target/"OPEN_REAL_THREE_VIEW_NON_ART.html").write_text(page,encoding="utf-8")
    print("P2_NATIVE_OPERATOR_3_REAL_CYCLES_TECH_ONLY_ART_HOLD",json.dumps(evidence),flush=True)
    return evidence

def main():
    argv=sys.argv
    argv=argv[argv.index("--")+1:] if "--" in argv else argv[1:]
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True)
    parser.add_argument("--out",required=True)
    args=parser.parse_args(argv)
    run(args.source,args.out)
    return 0

if __name__=="__main__":
    sys.exit(main())
