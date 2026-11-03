#!/usr/bin/env python3
"""Negative-only observability gate for real saved-native Blender R1 Cycles views.

Never produces ART PASS; absence of a fatal pixel fault is not art quality.
"""
import argparse,hashlib,json
from pathlib import Path
from PIL import Image

EYES={"AERIAL","PUBLIC_EYE","HABITAT_EYE","FACTORY_EYE","RESEARCH_EYE"}
INTERIOR={"PUBLIC_EYE","HABITAT_EYE","FACTORY_EYE","RESEARCH_EYE"}
DARK_THRESHOLD=34
FATAL_DARK_RATIO=.93

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def metrics(path):
    p=Path(path)
    if not p.is_file() or not 1000<=p.stat().st_size<=12000000:
        raise ValueError("SOURCE_PNG_MISSING_OR_OUT_OF_BOUNDS")
    with Image.open(p) as image:
        image.load()
        if image.format!="PNG" or image.width<500 or image.height<300:
            raise ValueError("NOT_ACTUAL_RENDER_SIZE_OR_FORMAT")
        rgb=image.convert("RGB")
        small=rgb.resize((160,100))
        data=list(small.get_flattened_data() if hasattr(small,"get_flattened_data") else small.getdata())
        central=rgb.crop((rgb.width//5,rgb.height//5,rgb.width*4//5,rgb.height*4//5)).resize((120,80))
        center=list(central.get_flattened_data() if hasattr(central,"get_flattened_data") else central.getdata())
        return {
          "file":p.name,"sha256":sha(p),"dimensions":[rgb.width,rgb.height],
          "sample_distinct_colors":len(set(data)),
          "frame_dark_ratio":round(sum(max(v)<=DARK_THRESHOLD for v in data)/len(data),6),
          "center_dark_ratio":round(sum(max(v)<=DARK_THRESHOLD for v in center)/len(center),6)
        }

def audit(directory):
    base=Path(directory).resolve()
    manifestfile=base/"INDEPENDENT_SAME_NATIVE_FIVE_TRUE_CYCLES_AUDIT.json"
    if not manifestfile.is_file() or manifestfile.is_symlink():
        raise ValueError("INDEPENDENT_BLENDER_MANIFEST_REQUIRED")
    meta=json.loads(manifestfile.read_text(encoding="utf8"))
    allowed={"g4c7-r1-civic-braid-single-native-reopen-art-review-v1",
             "g4c7-r1-same-native-vision-provenance-v1"}
    if meta.get("schema") not in allowed:raise ValueError("UNSUPPORTED_NATIVE_MANIFEST_SCHEMA")
    if (meta.get("art")!="HOLD" or meta.get("official_art_adoptions")!=0
        or meta.get("minecraft")!="FORBIDDEN" or meta.get("formal_331_body_993_foot")!="NOT_RUN"
        or meta.get("G0_S1_G1_G2_G3")!="NOT_RUN"):
        raise ValueError("CHARTER_OR_FORMAL_QA_MISREPRESENTATION")
    name=meta.get("native_file")
    if not isinstance(name,str) or "/" in name or "\\" in name or not name.endswith(".blend"):
        raise ValueError("INVALID_NATIVE_FILENAME")
    blend=base/name
    if not blend.is_file() or sha(blend)!=meta.get("native_sha256"):
        raise ValueError("NATIVE_SOURCE_HASH_MISMATCH")
    with blend.open("rb") as f:
        magic=f.read(96)
    # Blender's compressed .blend may begin with a Zstandard frame; independent
    # genuine Blender re-open is attested in the pinned source manifest.
    if not (magic.startswith(b"BLENDER") or
            (magic.startswith(bytes.fromhex("28b52ffd")) and b"BLENDER" in magic)):
        raise ValueError("NOT_A_RECOGNIZABLE_NATIVE_BLENDER_FILE")
    views={}
    rows=meta.get("five_true_cycles_from_one_native")
    if not isinstance(rows,list) or len(rows)!=5:
        raise ValueError("FIVE_SAVED_NATIVE_VIEWS_REQUIRED")
    for item in rows:
        if not isinstance(item,dict):raise ValueError("INVALID_VIEW_RECORD")
        view=item.get("view");file=item.get("file")
        if view not in EYES or view in views:raise ValueError("DUPLICATE_OR_UNKNOWN_EYE")
        if (not isinstance(file,str) or "/" in file or "\\" in file
            or not file.endswith("_CYCLES_TRUE_NATIVE.png")):
            raise ValueError("INVALID_RENDER_PATH")
        p=base/file
        m=metrics(p)
        if item.get("sha256")!=m["sha256"] or item.get("size_bytes")!=p.stat().st_size:
            raise ValueError("IMAGE_TAMPERED_OR_NOT_SAME_NATIVE")
        views[view]=m
    if set(views)!=EYES:raise ValueError("MISSING_SAME_NATIVE_EYE")
    flags=[]
    for name,m in views.items():
        if name in INTERIOR and m["center_dark_ratio"]>=FATAL_DARK_RATIO:
            flags.append({"view":name,"reason":"FATAL_INTERIOR_VISUAL_INACCESSIBILITY",
                          "center_dark_ratio":m["center_dark_ratio"],
                          "threshold":FATAL_DARK_RATIO})
        if m["sample_distinct_colors"]<48:
            flags.append({"view":name,"reason":"PRACTICALLY_UNIFORM_RENDER"})
    return {
      "schema":"g4c7-r1-negative-only-same-native-visibility-v1",
      "result":"BLOCK_VISUAL_OBSERVABILITY" if flags else "NO_FATAL_FLAG_ART_STILL_HOLD",
      "source_native_sha256":sha(blend),"manifest_sha256":sha(manifestfile),
      "views":views,"blocking_evidence":flags,
      "art":"HOLD","official_adoptions":0,
      "never_proves_visual_art_acceptance":True,
      "human_quality_judgment":"REQUIRED_FOR_ANY_ART_DECISION",
      "deliberately_dark_art_warning":"a dark design may be flagged; gate cannot judge intentionality",
      "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
      "minecraft":"FORBIDDEN","world_writes":0,"work":"NOT_USED","sol":"NOT_USED"
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--folder",required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--expect-blocked",action="store_true")
    a=p.parse_args()
    destination=Path(a.out)
    if destination.exists():raise FileExistsError("APPEND_ONLY_OUTPUT_ALREADY_EXISTS")
    r=audit(a.folder)
    destination.write_text(json.dumps(r,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(r["result"],r["blocking_evidence"],flush=True)
    if a.expect_blocked and r["result"]!="BLOCK_VISUAL_OBSERVABILITY":
        raise SystemExit("HISTORIC_BAD_ART_NOT_BLOCKED")

if __name__=="__main__":main()
