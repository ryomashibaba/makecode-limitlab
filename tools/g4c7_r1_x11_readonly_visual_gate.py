#!/usr/bin/env python3
"""Independent RGB pixel and provenance gate for real X11 on rejected native R1.

Deliberately a diagnostic, not a visual ART or GUI authoring certification.
No Blender bpy, geometry mutations, LLM, AI image creation or Minecraft access.
"""
import argparse, hashlib, json, statistics
from pathlib import Path
from PIL import Image, ImageChops, ImageStat

PIN="cadf0678f7a57636dbebe7432e95d4aae98a2a0cc57215652177d9cbd6ef0e06"
NAMES=("BEFORE_ROOT","AFTER_ROOT","BEFORE_WINDOW","AFTER_WINDOW")

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def pixel_info(path):
    with Image.open(path) as p:
        p.load()
        if p.format!="PNG" or p.width<700 or p.height<500 or p.width*p.height>4_000_000:
            raise ValueError("INVALID_PIXELS_SIZE_OR_FORMAT:"+path.name)
        im=p.convert("RGB")
        extrema=im.getextrema()
        sample=im.resize((160,90))
        pixels=list(sample.getdata())
        colors=len(set(pixels))
        sig=ImageStat.Stat(sample)
        std=max(sig.stddev)
        return {
            "file":path.name,"sha256":sha(path),
            "size":[im.width,im.height],"minmax":[list(x) for x in extrema],
            "sample_unique_colors":colors,
            "sample_max_channel_stdev":round(float(std),4),
            "is_flat":colors==1,
            "plausibly_visible":colors>=32 and std>=4.0,
        }

def significant_changes(left,right):
    with Image.open(left) as aa,Image.open(right) as bb:
        a=aa.convert("RGB");b=bb.convert("RGB")
        if a.size!=b.size:return -1
        diff=ImageChops.difference(a,b)
        # Downsample difference: cursor flicker cannot stand in for a view change.
        counts=0
        for rgb in diff.resize((160,90)).getdata():
            if max(rgb)>=18:counts+=1
        return counts

def audit(folder,source):
    folder=Path(folder).resolve();source=Path(source).resolve()
    if not source.is_file() or sha(source)!=PIN:
        raise ValueError("PROTECTED_REJECTED_R1_SOURCE_MISMATCH")
    if "R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART.blend"!=source.name:
        raise ValueError("WRONG_REJECTED_SCENE_NAME")
    window=(folder/"REAL_X11_WINDOW_TITLE.txt").read_text()
    if "R1_CIVIC_ESTUARY_GUI_DIRECT_EDIT_NOT_ART" not in window:
        raise ValueError("X11_WINDOW_ID_NOT_PINNED_SOURCE")
    images={}
    for n in NAMES:
        label="X11_REJECTED_R1_"+n+".png"
        image=folder/label
        if not image.exists():raise FileNotFoundError(label)
        images[n]=pixel_info(image)
    window_delta=significant_changes(folder/"X11_REJECTED_R1_BEFORE_WINDOW.png",folder/"X11_REJECTED_R1_AFTER_WINDOW.png")
    root_delta=significant_changes(folder/"X11_REJECTED_R1_BEFORE_ROOT.png",folder/"X11_REJECTED_R1_AFTER_ROOT.png")
    good_w=images["BEFORE_WINDOW"]["plausibly_visible"] and images["AFTER_WINDOW"]["plausibly_visible"] and window_delta>=250
    good_r=images["BEFORE_ROOT"]["plausibly_visible"] and images["AFTER_ROOT"]["plausibly_visible"] and root_delta>=250
    status=(
        "WINDOW_AND_ROOT_VISIBLE_CANDIDATE_NEEDS_MANUAL_NATIVE_VIEW_INSPECTION" if good_w and good_r else
        "WINDOW_VISIBLE_CANDIDATE_NEEDS_MANUAL_NATIVE_VIEW_INSPECTION" if good_w else
        "ROOT_ONLY_VISIBLE_CANDIDATE_NOT_NATIVE_WINDOW_PROOF" if good_r else
        "X11_VIEWPORT_VISUAL_FEEDBACK_NOT_ESTABLISHED"
    )
    report={
        "schema":"g4c7-r1-rejected-saved-native-x11-readonly-v1",
        "result":status,
        "previous_r1_civic_estuary_art":"EARLY_ART_REJECT",
        "new_r1_artwork_generated":False,
        "new_blender_meshes_generated":False,
        "read_only_source_sha256":sha(source),
        "x11_window_title":window.strip()[:450],
        "images":images,
        "window_significant_changed_samples":window_delta,
        "root_significant_changed_samples":root_delta,
        "x11_potentially_readable":bool(good_w or good_r),
        "independent_human_or_model_visual_inspection_done":False,
        "art":"HOLD","official_adoptions":0,
        "formal_331_993":"NOT_RUN","gates_G0_S1_G1_G2_G3":"NOT_RUN",
        "minecraft":"FORBIDDEN","world_writes":0,
        "work":"NOT_USED","sol":"NOT_USED",
        "observation_only":"This cannot prove autonomous artist GUI editing or ART eligibility."
    }
    out=folder/"R1_X11_REJECTED_NATIVE_VISUAL_FEEDBACK_AUDIT.json"
    if out.exists():raise FileExistsError("APPEND_ONLY_DIAGNOSTIC")
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    return report

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--folder",required=True)
    parser.add_argument("--source",required=True)
    p=parser.parse_args()
    r=audit(p.folder,p.source)
    print(r["result"],flush=True)
    if not r["x11_potentially_readable"]:
        raise SystemExit(9)

if __name__=="__main__":
    main()
