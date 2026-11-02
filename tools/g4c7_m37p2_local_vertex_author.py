#!/usr/bin/env python3
"""M37-P2 local LLM authored explicit-vertex 3D trial; no primitive city generator.

Host Python: --mode propose --out PLAN.json [--model qwen3:14b]
Blender background: --python this-file -- --mode render --plan PLAN.json
                  --source PINNED_V3_COPY.blend --out DIRECTORY

The local model authors the VERTICES/FACES as data, never executable Python.
No code from an untrusted model is executed. No repeated cuboid generators,
O1/P1 meshes, external dependencies, Minecraft, or GitHub writes. Every
artifact is an UNAPPROVED early-art trial, never a formal direct GUI authoring
session or official art adoption.
"""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys
import urllib.request

EXPECTED_SHA = "536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
COLLECTIONS = [
    "P2_CITY_MACRO_DIRECT_AUTHOR",
    "P2_INHABITED_SECTION_DIRECT_AUTHOR",
    "P2_PUBLIC_FACTORY_BOUNDARY_DIRECT_AUTHOR",
    "P2_RESEARCH_CULTURE_DIRECT_AUTHOR",
    "P2_HABITAT_PRIVATE_DIRECT_AUTHOR",
]
ROLE_NAMES = ["city_macro", "inhabited", "factory_boundary", "research_culture", "habitat"]
CAMERAS = ["P2_CAMERA_AERIAL", "P2_CAMERA_PUBLIC_EYE", "P2_CAMERA_HABITAT_EYE"]
SCHEMA = {
    "type": "object",
    "required": ["title", "design_intent", "meshes"],
    "properties": {
        "title": {"type": "string"},
        "design_intent": {"type": "string"},
        "meshes": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "role", "why", "vertices", "faces"],
                "properties": {
                    "name": {"type": "string"},
                    "role": {"type": "string"},
                    "why": {"type": "string"},
                    "vertices": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "number"}},
                    },
                    "faces": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "integer"}},
                    },
                },
            },
        },
    },
}
BRIEF = """
You are a genuine 3D vertex-level artist (not an extrusion template generator).
For MakeCode LimitLab / G4-C7 M37-P2, author one richly interconnected
INHABITED SHIPBUILDING CITY, with city-wide density, real interior depth,
working shipyard tools and separate visitor gallery, shared daylit research /
culture and private home rooms, all at once in ONE coherent Blender scene.
This is a NEW absolute art direction. NEVER reuse rejected O1/P1 city shapes.
DO NOT assemble a city from boxes, walls, slabs, tube, road bands, bridges,
disconnected pavilions or repeated cubes. Form must have crafted folds,
recesses, courtyards, varied window reveals, sectional depths, asymmetric
human-scale fronts and curved or non-axis-aligned surfaces. Favor intelligent
crafted local surface topologies over many cheap isolated objects.

Output ONLY JSON data; no Python/code, no claims of safety or ART PASS.
Each mesh must contain explicit native vertices [[x,y,z],...] and faces as
0-based vertex index lists. Each vertex exactly 3 finite numeric coordinates,
each face 3-8 valid indices, consistent real non-zero surface area.
No cuboid primitives. Form a connected believable urban artwork, not
decorative icons or isolated geometry.
Five roles MUST be included: city_macro, inhabited, factory_boundary,
research_culture, habitat. At least 10 distinct meaningful meshes overall,
at least 3 non-axis-aligned sculpted meshes with >=16 vertices.
Describe visible machine activity, deeper interior room, and boundaries in
'why'. Keep coordinates within -150..150 (abstract art units, not meters).
This plan will be held as an UNAPPROVED experiment and judged by 3 real
Cycles viewpoints. If you cannot design strong and distinct forms, output
less and allow the validator to REJECT; never fabricate test success.
"""

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def _face_area(vertices, face):
    x,y,z = vertices[face[0]]
    sx=sy=sz=0.0
    for a,b in zip(face[1:-1],face[2:]):
        ax,ay,az=[vertices[a][k]-v for k,v in enumerate((x,y,z))]
        bx,by,bz=[vertices[b][k]-v for k,v in enumerate((x,y,z))]
        sx += ay*bz-az*by
        sy += az*bx-ax*bz
        sz += ax*by-ay*bx
    return (sx*sx+sy*sy+sz*sz)**0.5/2

def validate(plan):
    problems=[]
    if not isinstance(plan,dict) or not isinstance(plan.get("meshes"),list):
        return ["MISSING_MESH_LIST"]
    if not isinstance(plan.get("design_intent"),str) or len(plan["design_intent"].strip())<24:
        problems.append("MISSING_CONCRETE_AUTHOR_DESIGN_INTENT")
    meshes=plan["meshes"]
    if len(meshes)<10 or len(meshes)>65:
        problems.append("OBJECT_COUNT_OUTSIDE_10_TO_65")
    present=Counter()
    names=set()
    complex_count=0
    cuboid=0
    all_vertices=[]
    total=0
    for i,m in enumerate(meshes[:70]):
        if not isinstance(m,dict):
            problems.append(f"MESH_{i}_MALFORMED");continue
        name=m.get("name","")
        role=m.get("role","")
        verts=m.get("vertices",[])
        faces=m.get("faces",[])
        if (not isinstance(name,str) or not name.strip() or name in names or
                len(name)>75 or any(ord(char)<32 for char in name)):
            problems.append(f"MESH_{i}_BAD_NAME")
        else: names.add(name)
        if role not in ROLE_NAMES: problems.append(f"MESH_{i}_BAD_ROLE")
        else: present[role]+=1
        if not isinstance(m.get("why"),str) or len(m["why"].strip())<12:
            problems.append(f"MESH_{i}_MISSING_LIVED_INTENT")
        if not isinstance(verts,list) or not 4<=len(verts)<=1600 or not isinstance(faces,list) or not 2<=len(faces)<=3000:
            problems.append(f"MESH_{i}_BAD_TOPOLOGY_SIZE");continue
        vout=[]
        for j,v in enumerate(verts):
            if (not isinstance(v,list) or len(v)!=3 or
                    any(type(n) not in (float,int) or not math.isfinite(n) or abs(n)>150 for n in v)):
                problems.append(f"MESH_{i}_INVALID_VERTEX_{j}");break
            vout.append(tuple(float(n) for n in v))
        if len(vout)!=len(verts):continue
        total+=len(verts)
        all_vertices.extend(vout)
        valid_faces=0
        for j,f in enumerate(faces):
            if (not isinstance(f,list) or not 3<=len(f)<=8 or
                    any(type(k)!=int or k<0 or k>=len(verts) for k in f) or
                    len(set(f))!=len(f)):
                problems.append(f"MESH_{i}_INVALID_FACE_{j}");continue
            if _face_area(vout,f)<0.001:
                problems.append(f"MESH_{i}_ZERO_AREA_FACE_{j}");continue
            valid_faces+=1
        if len(verts)>=16 and valid_faces>=8:complex_count+=1
        if len(verts)==8 and len(faces)==6:cuboid+=1
    for role in ROLE_NAMES:
        if not present[role]: problems.append("MISSING_ROLE_"+role)
    if total<150:problems.append("INSUFFICIENT_NATIVE_VERTEX_AUTHORSHIP")
    if complex_count<3:problems.append("MISSING_SCULPTED_COMPLEXITY")
    if cuboid>max(1,len(meshes)//5):problems.append("CUBOID_DOMINANT_REJECT")
    if all_vertices:
        for ax in range(3):
            if max(v[ax] for v in all_vertices)-min(v[ax] for v in all_vertices)<10:
                problems.append("SCENE_HAS_NO_REAL_SPATIAL_DEPTH_AXIS_"+str(ax))
    return sorted(set(problems))

def atomic_json(path,data):
    p=Path(path)
    if p.exists():raise FileExistsError("APPEND_ONLY_OUTPUT_EXISTS: "+str(p))
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def propose(args):
    if args.model is None:raise ValueError("LOCAL_MODEL_REQUIRED")
    body={
        "model":args.model, "prompt":BRIEF, "format":SCHEMA,
        # Ollama's documented structured-output field and non-thinking mode.
        # Disable thinking to reserve the entire output budget for explicit
        # vertices instead of hidden reasoning; do not use generated code.
        "stream":False, "think":False,
        "options":{"temperature":0.6,"num_predict":14500}
    }
    request=urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},
        method="POST")
    try:
        with urllib.request.urlopen(request,timeout=1200) as resp:
            # The local model is untrusted: cap bytes to avoid memory spikes.
            raw=resp.read(3_000_001)
        if len(raw)>3_000_000:
            raise ValueError("LOCAL_MODEL_RESPONSE_TOO_LARGE")
        output=json.loads(raw.decode("utf-8"))
        if output.get("done") is not True or output.get("done_reason") in ("length", "error"):
            raise ValueError("OLLAMA_INCOMPLETE_OR_FAILED_GENERATION")
        if len(output.get("response",""))>2_600_000:
            raise ValueError("MODEL_JSON_CONTENT_TOO_LARGE")
        plan=json.loads(output["response"])
    except Exception as ex:
        atomic_json(args.out+".FAIL.json",{
            "schema":"p2-local-llm-native-vertex-attempt-v1",
            "outcome":"MODEL_UNAVAILABLE_OR_INVALID_HOLD","detail":str(ex),
            "art":"HOLD","adoption":0,"minecraft":"FORBIDDEN"})
        raise
    problems=validate(plan)
    report={
        "schema":"p2-local-llm-native-vertex-attempt-v1",
        "outcome":"PLAN_REJECTED_HOLD" if problems else "PLAN_VALID_FOR_NATIVE_RENDER_NOT_ART",
        "model":args.model,"errors":problems,
        "objects":len(plan.get("meshes",[])) if isinstance(plan,dict) and isinstance(plan.get("meshes"),list) else 0,
        "art":"HOLD","official_adoptions":0,"formal_331_993":"NOT_RUN",
        "minecraft":"FORBIDDEN","method":"LLM_AUTHORED_EXPLICIT_VERTICES_NOT_DIRECT_GUI_AUTHOR"
    }
    atomic_json(args.out+".validation.json",report)
    if problems:
        # Preserve bounded model data for diagnosis, explicitly never as ART
        # or as a Blender input. This allows a single failed local attempt
        # to be reviewed without generating further rejected primitive cities.
        if len(json.dumps(plan,ensure_ascii=False))<=2_600_000:
            atomic_json(args.out+".REJECTED_NEVER_ART.json",plan)
        print("P2_AUTHOR_ART_FIRST_PLAN_REJECT",problems,flush=True)
        return 2
    atomic_json(args.out,plan)
    print("P2_EXPLICIT_NATIVE_VERTEX_PLAN_ACCEPTED_FOR_REVIEW_ONLY",flush=True)
    return 0

def render(args):
    import bpy
    from mathutils import Vector
    source=Path(args.source).resolve()
    if not source.is_file() or sha(source)!=EXPECTED_SHA:
        raise RuntimeError("PINNED_V3_EMPTY_AUTHOR_SOURCE_SHA_MISMATCH")
    target=Path(args.out).resolve()
    if target.exists():raise RuntimeError("APPEND_ONLY_TRIAL_FOLDER_ALREADY_EXISTS")
    plan=json.loads(Path(args.plan).read_text(encoding="utf-8"))
    problems=validate(plan)
    if problems:raise RuntimeError("PLAN_VALIDATION_REFUSED:"+str(problems))
    target.mkdir(parents=True)
    bpy.ops.wm.open_mainfile(filepath=str(source))
    sc=bpy.context.scene
    if (sc.get("P2_ART")!="HOLD" or sc.get("P2_OFFICIAL_ADOPTIONS")!=0 or
        sc.get("P2_MINECRAFT")!="FORBIDDEN" or
        any(o.type=="MESH" for o in sc.objects)):
        raise RuntimeError("ORIGINAL_STUDIO_NOT_EMPTY_OR_CHARTER_BROKEN")
    roles=dict(zip(ROLE_NAMES,COLLECTIONS))
    all_vertices=[]
    for m in plan["meshes"]:
        mesh=bpy.data.meshes.new("P2_LOCAL_AI_UNAPPROVED_"+m["name"]+"_data")
        mesh.from_pydata(m["vertices"],[],m["faces"])
        mesh.update(calc_edges=True)
        obj=bpy.data.objects.new("P2_LOCAL_AI_UNAPPROVED_"+m["name"],mesh)
        bpy.data.collections[roles[m["role"]]].objects.link(obj)
        obj["AUTHORSHIP"]="LOCAL_AI_EXPLICIT_NATIVE_VERTICES_NO_HUMAN_GUI_EDIT"
        obj["LOCAL_AI_REASON"]=m["why"]
        all_vertices.extend(tuple(v) for v in m["vertices"])
    sc["P2_STUDIO_STAGE"]="LOCAL_AI_ART_FIRST_EARLY_TRIAL_UNAPPROVED"
    sc["P2_SOURCE_KIND"]="LOCAL_LLM_EXPLICIT_VERTICES_NOT_GUI_DIRECT_AUTHOR"
    sc["P2_ART"]="HOLD"
    sc["P2_OFFICIAL_ADOPTIONS"]=0
    sc["P2_CAMERA_VIEWS_AUTHOR_APPROVED"]=False
    mins=[min(v[k] for v in all_vertices) for k in range(3)]
    maxs=[max(v[k] for v in all_vertices) for k in range(3)]
    center=Vector([(a+b)/2 for a,b in zip(mins,maxs)])
    size=max(maxs[k]-mins[k] for k in range(3))
    z0=mins[2]
    # Genuine render-camera placements, not formal artist-approved view positions.
    poses={
        CAMERAS[0]:(center+Vector((size*1.55,-size*1.5,size*1.25)),center),
        CAMERAS[1]:(Vector((mins[0]-size*.28,mins[1]-size*.30,z0+max(2,size*.07))),center+Vector((0,0,max(4,size*.16)))),
        CAMERAS[2]:(Vector((maxs[0]+size*.13,maxs[1]+size*.10,z0+max(3,size*.10))),center+Vector((0,0,max(4,size*.16)))),
    }
    for name,(eye,look) in poses.items():
        obj=bpy.data.objects[name]
        obj.location=eye
        obj.rotation_euler=(look-eye).to_track_quat("-Z","Y").to_euler()
        obj.data.lens=35
        obj["P2_CAMERA_STATUS"]="LOCAL_AI_AUTO_FRAMED_ART_NOT_APPROVED"
        try:obj.hide_set(True)
        except Exception:pass
    if sc.world is None:sc.world=bpy.data.worlds.new("P2_AI_TRIAL_WORLD")
    sc.world.use_nodes=True
    bg=sc.world.node_tree.nodes.get("Background")
    if bg is not None:
        bg.inputs["Color"].default_value=(0.37,0.43,0.56,1)
        bg.inputs["Strength"].default_value=0.8
    lightdata=bpy.data.lights.new("P2_AI_TRIAL_SUN","SUN")
    lightdata.energy=2.2
    light=bpy.data.objects.new("P2_AI_TRIAL_SUN",lightdata)
    sc.collection.objects.link(light)
    light.rotation_euler=(0.34,-0.55,-0.43)
    sc.render.engine="CYCLES"
    sc.cycles.samples=12
    sc.render.resolution_x=1000
    sc.render.resolution_y=620
    sc.render.resolution_percentage=100
    sc.render.image_settings.file_format="PNG"
    native=target/"P2_LOCAL_AI_VERTEX_ART_FIRST_UNAPPROVED.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(native),compress=False)
    scene_sha=sha(native)
    photos={}
    for view,name in (("AERIAL",CAMERAS[0]),("PUBLIC_EYE",CAMERAS[1]),("HABITAT_EYE",CAMERAS[2])):
        sc.camera=bpy.data.objects[name]
        path=target/("P2_LOCAL_AI_"+view+"_UNAPPROVED.png")
        sc.render.filepath=str(path)
        bpy.ops.render.render(write_still=True)
        if path.read_bytes()[:8]!=b"\x89PNG\r\n\x1a\n":
            raise RuntimeError("GENUINE_PNG_SIGNATURE_REQUIRED:"+view)
        photos[view]={"file":path.name,"sha256":sha(path)}
    output={
        "schema":"g4c7-m37p2-llm-explicit-vertex-native-trial-v1",
        "outcome":"NATIVE_TRIAL_RENDERED_ART_UNREVIEWED",
        "art":"HOLD","official_adoptions":0,
        "model_authorship":"LOCAL_LLM_VERTEX_DATA_NOT_DIRECT_GUI",
        "native_sha256":scene_sha,"original_v3_sha256":sha(source),
        "object_count":len(plan["meshes"]),"camera_review":photos,
        "formal_331_993":"NOT_RUN","Minecraft":"FORBIDDEN",
        "makecode_cost":"NOT_EVALUATED","art_gates":"NOT_PASSED",
    }
    atomic_json(target/"P2_LOCAL_AI_NATIVE_ART_HOLD_REPORT.json",output)

    # ART-FIRST: present the THREE *actual native Blender render files* on one
    # offline, read-only inspection page. Never represent this as a final city.
    # No remote service, image generator, or user tracking is involved.
    review=target/"OPEN_THREE_REAL_BLENDER_VIEWS_ART_HOLD.html"
    if review.exists():
        raise FileExistsError("APPEND_ONLY_REVIEW_ALREADY_EXISTS")
    views=(("AERIAL","都市全景"),("PUBLIC_EYE","公共・製造の人間視点"),
           ("HABITAT_EYE","居住の人間視点"))
    cards="\\n".join(
        '<section><h2>'+title+'</h2><img src="'+photos[key]["file"]+
        '" alt="'+title+'：実Blender出力・未採用"><p><code>'+photos[key]["sha256"]+
        '</code></p></section>' for key,title in views
    )
    review.write_text(
        '<!doctype html><html lang="ja"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<title>G4C7 P2 真正Blender 3視点・絶対美術審査 未採用</title>'
        '<style>body{font-family:system-ui,sans-serif;background:#151a22;'
        'color:#e9edf2;margin:2rem auto;max-width:1550px;padding:0 1rem}'
        'h1{font-size:1.6rem}p{line-height:1.7}section{margin:2rem 0;'
        'padding:1rem;background:#222935;border-radius:12px}'
        'img{display:block;width:100%;height:auto;border-radius:8px}'
        'code{font-size:.74rem;overflow-wrap:anywhere;color:#aebcd0}'
        '</style></head><body><h1>G4-C7 M37-P2 / 真正Blender 3視点</h1>'
        '<p><strong>ART HOLD／正式採用0件／未審査のローカルAI試作。</strong>'
        'この3枚は同じ保存済み3Dからの実レンダ画像であり、'
        '美術的な合格や安全認証を意味しません。</p>'
        '<p>全景が巨大な板・箱・空白なら即不採用。公共視点で'
        '工場見学と職員境界・研究文化の活動が分からなければ不採用。'
        '住居視点で玄関・奥行・窓・街並みが分からなければ不採用。</p>'
        +cards+
        '<p>331人体／993足元 NOT RUN・Minecraft施工禁止・'
        'MakeCode未評価・main未変更。正式ART採用は本人だけが決定します。</p>'
        '</body></html>',encoding="utf-8"
    )
    print("P2_LOCAL_AI_EXPLICIT_VERTEX_NATIVE_RENDER_SUCCESS_ART_HOLD",json.dumps(output),flush=True)
    return 0

def main():
    argsv=sys.argv
    if "--" in argsv:argsv=argsv[argsv.index("--")+1:]
    else:argsv=argsv[1:]
    p=argparse.ArgumentParser()
    p.add_argument("--mode",choices=["propose","render","validate"],required=True)
    p.add_argument("--plan")
    p.add_argument("--model",default="qwen3:14b")
    p.add_argument("--out",required=True)
    p.add_argument("--source")
    args=p.parse_args(argsv)
    if args.mode=="propose":return propose(args)
    if args.mode=="render":return render(args)
    probs=validate(json.loads(Path(args.plan).read_text(encoding="utf-8")))
    print("P2_NATIVE_VERTEX_VALIDATION",json.dumps(probs),flush=True)
    return 2 if probs else 0

if __name__=="__main__":sys.exit(main())
