#!/usr/bin/env python3
"""Conservative independent pixel gate for architecturally targeted X11 Blender GUI edits.

The command --before MUST succeed before any G/X/2 keyboard edit occurs.
--pair independently proves real content and a changed displayed region,
not artistic acceptability or semantic understanding.
"""
import argparse,json,hashlib
from pathlib import Path
from PIL import Image,ImageStat,ImageChops

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def inspect(p):
    with Image.open(p) as raw:
        raw.load()
        if raw.format!="PNG" or raw.size!=(1600,900):
            raise ValueError("UNEXPECTED_BLENDER_X11_FRAME")
        im=raw.convert("RGB")
        # Sample middle of Blender's 3D editor, not the menus or outliner.
        center=im.crop((80,90,1110,800))
        small=center.resize((160,110))
        colors=len(set(small.getdata()))
        variation=max(ImageStat.Stat(small).stddev)
        # Real Blender object selection is a hairline orange contour over a
        # flat gray edit viewport. A broad 5-point variance gate incorrectly
        # rejects actual visible geometry; use pixel-level selected topology
        # instead, while still failing closed on blank/black/root-only images.
        selected_outline_pixels=sum(
            1 for r,g,b in center.getdata()
            if r >= g*1.30 and r >= b*1.55 and r>85 and g>45
        )
        if colors<100 or variation<2.5 or selected_outline_pixels<200:
            raise ValueError("BLENDER_VIEWPORT_NO_VISIBLE_SELECTED_MESH")
        return {"filename":p.name,"sha256":sha(p),
                "unique_viewport_colors":colors,
                "max_viewport_stdev":round(float(variation),3),
                "selected_orange_contour_pixels":selected_outline_pixels,
                "dimensions":list(im.size)}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--folder",required=True)
    parser.add_argument("--mode",choices=["before","pair"],required=True)
    args=parser.parse_args()
    d=Path(args.folder)
    a=d/"ACTUAL_R1_GUI_BEFORE_ARCHITECTURE_INPUT.png"
    info=inspect(a)
    result={"before":info,"art":"HOLD","official_adoptions":0,
            "source_rejected":"EARLY_ART_REJECT","method_only":True}
    if args.mode=="pair":
        b=d/"ACTUAL_R1_GUI_AFTER_ARCHITECTURE_INPUT.png"
        result["after"]=inspect(b)
        with Image.open(a) as i,Image.open(b) as j:
            left=i.convert("RGB").crop((80,90,1110,800)).resize((160,110))
            right=j.convert("RGB").crop((80,90,1110,800)).resize((160,110))
            diff=ImageChops.difference(left,right)
            changed=sum(1 for p in diff.getdata() if max(p)>=16)
            if changed<80:
                raise ValueError("GUI_EDIT_NOT_VISUALLY_DEMONSTRABLE")
        result["changed_pixel_samples"]=changed
        result["status"]="REAL_VIEWPORT_VISUALLY_DIFFERENT_AFTER_GUI_KEY_EDIT_NOT_ART"
    else:
        result["status"]="REAL_BLENDER_VIEWPORT_VISIBLE_BEFORE_ANY_GUI_EDIT"
    dest=d/("X11_VIEW_VISIBLE_PRE_EDIT.json" if args.mode=="before" else "X11_VIEW_CHANGED_POST_EDIT.json")
    if dest.exists():raise FileExistsError("APPEND_ONLY_VISUAL_GATE")
    dest.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(result["status"],flush=True)

if __name__=="__main__":
    main()
