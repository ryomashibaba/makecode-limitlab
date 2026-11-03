#!/usr/bin/env python3
"""Evaluate *authentic* Blender GUI editor screenshots, without editing Blender.

Input must be the two real VIEW_3D PNGs plus SHA-bound native-scene JSON from
g4c7_m37p2_live_gui_context_capture.py. A model may be consulted using LOCAL
Ollama only when there is *real* geometry to review and the user explicitly
passes --vision-model. Empty studio is blocked BEFORE any AI call.

It never claims ART PASS or executes generated Python, and never calls
Minecraft, remote APIs, GitHub writes or Blender save operations.
"""
import argparse
import base64
import hashlib
import json
import math
from pathlib import Path
import urllib.request

NAMES=("MACRO_EDITOR","LIVED_EDITOR")
ROLES=(
    "P2_CITY_MACRO_DIRECT_AUTHOR",
    "P2_INHABITED_SECTION_DIRECT_AUTHOR",
    "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
    "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
    "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
)
PNG_SIGNATURE=bytes.fromhex("89504e470d0a1a0a")
MAX_PNG_BYTES=8_000_000

def sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as stream:
        for buf in iter(lambda:stream.read(1024*1024),b""):
            h.update(buf)
    return h.hexdigest()

def source_gate(manifest):
    """Perform cheap, deterministic, source-linked geometry gate FIRST."""
    folder=Path(manifest).resolve().parent
    if not Path(manifest).is_file():
        raise FileNotFoundError("REAL_GUI_MANIFEST_NOT_FOUND")
    data=json.loads(Path(manifest).read_text(encoding="utf-8"))
    if (data.get("schema")!="g4c7-m37p2-live-gui-visual-context-v1" or
        data.get("result")!="TRUE_GUI_VIEWPORTS_AND_NATIVE_SCENE_DATA_CAPTURED" or
        data.get("bpy_background") is not False or
        data.get("art")!="HOLD" or data.get("official_adoptions")!=0 or
        data.get("minecraft")!="FORBIDDEN" or
        data.get("formal_331_993")!="NOT_RUN" or
        data.get("no_model_calls") is not True):
        raise ValueError("REAL_NATIVE_GUI_SOURCE_AND_ART_CHARTER_NOT_VERIFIED")
    source=data.get("source_blend_sha256")
    if not isinstance(source,str) or len(source)!=64:
        raise ValueError("SOURCE_BLEND_SHA_MISSING")
    if set(data.get("views") or {})!=set(NAMES):
        raise ValueError("TWO_NATIVE_GUI_EDITORS_REQUIRED")
    images={}
    for key in NAMES:
        v=data["views"][key]
        name=v.get("file")
        if not isinstance(name,str) or name!=Path(name).name or not name.endswith(".png"):
            raise ValueError("UNSAFE_REAL_GUI_PNG_NAME_"+key)
        if v.get("source")!="ACTUAL_BLENDER_GUI_VIEW_3D_NOT_CYCLES_RENDER":
            raise ValueError("NOT_A_REAL_GUI_EDITOR_SCREENSHOT_"+key)
        fn=folder/name
        if not fn.is_file() or not 128<=fn.stat().st_size<=MAX_PNG_BYTES:
            raise ValueError("REAL_GUI_PNG_NOT_PRESENT_OR_TOO_LARGE_"+key)
        with fn.open("rb") as stream:
            if stream.read(8)!=PNG_SIGNATURE:
                raise ValueError("REAL_GUI_IMAGE_MAGIC_INVALID_"+key)
        if sha(fn)!=v.get("sha256"):
            raise ValueError("REAL_GUI_IMAGE_CHANGED_"+key)
        if not (isinstance(v.get("width_px"),int) and v["width_px"]>=100 and
                isinstance(v.get("height_px"),int) and v["height_px"]>=100):
            raise ValueError("REAL_GUI_SCREEN_DIMENSIONS_INVALID_"+key)
        images[key]=fn
    roles=data.get("mesh_collections")
    if not isinstance(roles,dict) or set(roles)!=set(ROLES):
        raise ValueError("FIVE_AUTHORED_NATIVE_COLLECTIONS_REQUIRED")
    counts={}
    for role in ROLES:
        value=roles[role]
        if not isinstance(value,dict) or type(value.get("count"))!=int:
            raise ValueError("REAL_COLLECTION_COUNT_BAD_"+role)
        if value["count"]<0 or value["count"]>2000:
            raise ValueError("UNSAFE_ROLE_COUNT_"+role)
        counts[role]=value["count"]
    if type(data.get("all_scene_mesh_count"))!=int or data["all_scene_mesh_count"]<0:
        raise ValueError("ALL_MESH_COUNT_NOT_TRUSTWORTHY")
    if sum(counts.values())>data["all_scene_mesh_count"]*5:
        raise ValueError("INCONSISTENT_NATIVE_ROLE_COUNTS")
    empty=data["all_scene_mesh_count"]==0
    if empty and any(counts.values()):
        raise ValueError("EMPTY_SCENE_HAS_NONZERO_AUTHORED_COLLECTIONS")
    missing=[x for x in ROLES if counts[x]==0]
    return data,images,{
        "scene_mesh_count":data["all_scene_mesh_count"],
        "collection_mesh_counts":counts,
        "missing_authored_collections":missing,
        "decision":"EMPTY_STUDIO_DIRECT_ART_REQUIRED" if empty
                   else ("FIVE_FUNCTIONAL_ZONES_STILL_MISSING" if missing else
                         "AUTHOR_VISUAL_REVIEW_REQUIRED"),
        "allow_model_image_review":not empty,
        "source_blend_sha256":source,
        "verified_gui_view_sha256":{k:sha(v) for k,v in images.items()},
    }

ART_BRIEF="""You are evaluating authentic Blender VIEW_3D editing screenshots
from one real saved project source, NOT polished concept art. The native object
counts attached as text are evidence; do not hallucinate components from names.
The established original direction is an inhabited dense, contiguous
spacecraft-building city. Five linked functions must really exist:
(1) city-scale inhabited macro fabric; (2) coherent street-to-door-to-
vestibule-to-interior-to-view window; (3) staff manufacturing and actual
hoists, assembly stands, tools; (4) thick physical public/staff separation;
(5) research/culture spaces with usable access. Avoid repeated generic
boxes, floating plates, cylindrical towers, anonymous skybridges. 
Describe only what is actually visible. Write short JSON:
{"visible_macro":"...", "visible_lived":"...", "missing":["..."],
"next_authoring_focus":"...", "uncertainty":"..."}.
Never output Python, Blender code, import steps, mesh arrays, ART PASS, 
Minecraft instructions, or claims about invisible interiors. If not sure say so.
"""

def local_ollama_vision(images,counts,model,timeout=480):
    attachments=[base64.b64encode(images[k].read_bytes()).decode("ascii") for k in NAMES]
    request_data={
        "model":model,"stream":False,"think":False,"format":"json",
        "messages":[{
            "role":"user",
            "content":ART_BRIEF+"\nNative scene mesh counts: "+json.dumps(counts,ensure_ascii=False),
            "images":attachments
        }],
        "options":{"temperature":0.1,"num_predict":1300},
    }
    req=urllib.request.Request("http://127.0.0.1:11434/api/chat",
        data=json.dumps(request_data).encode("utf-8"),
        headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=timeout) as response:
        raw=response.read(80001)
    if len(raw)>80000:
        raise ValueError("LOCAL_VISION_RESPONSE_TOO_LARGE")
    reply=json.loads(raw.decode("utf-8"))
    if reply.get("done") is not True or reply.get("done_reason") in ("length","error"):
        raise ValueError("LOCAL_VISION_RESPONSE_NOT_COMPLETE")
    obj=json.loads((reply.get("message") or {}).get("content") or "null")
    if not isinstance(obj,dict) or not all(isinstance(obj.get(k),str) for k in
          ("visible_macro","visible_lived","next_authoring_focus","uncertainty")):
        raise ValueError("VISION_STRUCTURED_RESPONSE_REQUIRED")
    missing=obj.get("missing")
    if not isinstance(missing,list) or any(not isinstance(s,str) for s in missing):
        raise ValueError("VISION_MISSING_LIST_NOT_VALID")
    return {
        "status":"ADVISORY_ONLY_NEVER_ART_PASS",
        "model":model,
        "visible_macro":obj["visible_macro"][:1000],
        "visible_lived":obj["visible_lived"][:1000],
        "missing":[x[:170] for x in missing[:12]],
        "next_authoring_focus":obj["next_authoring_focus"][:650],
        "uncertainty":obj["uncertainty"][:650],
    }

def evaluate(manifest,out_file,vision_model=None):
    data,imgs,gate=source_gate(manifest)
    output=Path(out_file).resolve()
    if output.exists():
        raise FileExistsError("APPEND_ONLY_VISION_REPORT")
    # Don't waste a full Gemma4 query on the verified 0-mesh studio.
    if not gate["allow_model_image_review"]:
        note={"status":"SKIPPED_EMPTY_STUDIO_NO_IMAGE_MODEL_CALL"}
    elif vision_model:
        try:
            note=local_ollama_vision(imgs,gate["collection_mesh_counts"],vision_model)
        except Exception as exc:
            note={"status":"MODEL_UNAVAILABLE_OR_INVALID_STAY_ART_HOLD",
                  "model":vision_model,"reason":str(exc)[:360]}
    else:
        note={"status":"NOT_REQUESTED"}
    result={
        "schema":"g4c7-m37p2-local-gui-vision-advisory-v1",
        **gate,
        "vision_review":note,
        "image_model_sent_outside_localhost":False,
        "new_geometry_produced":False,
        "native_blend_modified":False,
        "model_code_executed":False,
        "art":"HOLD","official_adoptions":0,
        "formal_331_993":"NOT_RUN",
        "makecode":"NOT_EVALUATED","minecraft":"FORBIDDEN",
        "work":"NOT_USED",
    }
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("P2_REAL_GUI_TO_LOCAL_VISION_GATE",result["decision"],note["status"],flush=True)
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--manifest",required=True)
    ap.add_argument("--out",required=True)
    ap.add_argument("--vision-model",default=None)
    args=ap.parse_args()
    evaluate(args.manifest,args.out,args.vision_model)

if __name__=="__main__":
    main()
