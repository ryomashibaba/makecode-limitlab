#!/usr/bin/env python3
"""Fail-closed provenance and pixel binding for Blender X11 editor VIEW_3D regions.

This verifies externally captured Blender-window pixels, NOT bpy.screenshot_area,
interactive Blender authoring, original Cycles, model calls, or art approval.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

PIN="536e451c763c4326421b13285abf1056a3a11d755028f8ff20b54b99b08a0249"
BLEND="M37P2_DIRECT_AUTHOR_NATIVE_EDITOR_FIXED_REVIEW_V3_NOT_ART"
GEOMETRY="P2_GUI_NATIVE_REGION_GEOMETRY_DIAGNOSTIC_ONLY.json"
WINDOW="P2_X11_BLENDER_FULL_WINDOW_DIAGNOSTIC_ONLY.png"
SOURCE="P2_X11_BLENDER_WINDOW_DIAGNOSTIC.json"
CROP="P2_X11_NATIVE_REGION_CROP_DIAGNOSTIC_ONLY.json"
OUTPUT="P2_X11_TWO_REAL_EDITOR_PIXEL_CONTEXT_HOLD.json"
NAMES=("MACRO_EDITOR","LIVED_EDITOR")

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def bounded_json(path):
    if not path.is_file() or not 20<=path.stat().st_size<=65536:
        raise ValueError("METADATA_MISSING_OR_OVERSIZED_"+path.name)
    return json.loads(path.read_text(encoding="utf8"))

def rectangles(geo,size):
    if geo.get("schema")!="g4c7-p2-native-gui-window-regions-v1" or geo.get("source_blend_sha256")!=PIN:
        raise ValueError("NATIVE_SOURCE_NOT_PINNED")
    if geo.get("same_window") is not True or geo.get("window_dimensions")!=list(size):
        raise ValueError("NATIVE_X11_WINDOW_SIZE_OR_ID_MISMATCH")
    if geo.get("art")!="HOLD" or geo.get("official_adoptions")!=0 or geo.get("minecraft")!="FORBIDDEN":
        raise ValueError("ART_CHARTER_MISMATCH")
    regions=geo.get("regions")
    if not isinstance(regions,dict) or set(regions)!=set(NAMES):
        raise ValueError("EXACTLY_TWO_NATIVE_REGIONS_REQUIRED")
    w,h=size
    rect={}
    for name in NAMES:
        r=regions[name]
        if not isinstance(r,dict) or set(r)!={"x","y","width","height"}:
            raise ValueError("NATIVE_REGION_MALFORMED_"+name)
        x,y,dx,dy=(r[k] for k in ("x","y","width","height"))
        if any(type(v) is not int for v in (x,y,dx,dy)) or x<0 or y<0 or dx<100 or dy<100 or x+dx>w or y+dy>h:
            raise ValueError("NATIVE_REGION_OUTSIDE_WINDOW_"+name)
        rect[name]=(x,h-y-dy,x+dx,h-y)
    a,z=rect.values()
    if max(a[0],z[0])<min(a[2],z[2]) and max(a[1],z[1])<min(a[3],z[3]):
        raise ValueError("OVERLAPPING_NATIVE_VIEWPORTS")
    return rect

def verify(folder):
    folder=Path(folder)
    s=bounded_json(folder/SOURCE)
    g=bounded_json(folder/GEOMETRY)
    c=bounded_json(folder/CROP)
    raw=folder/WINDOW
    if not raw.is_file() or not 1000<=raw.stat().st_size<=8_000_000:
        raise ValueError("REAL_X11_WINDOW_MISSING")
    if s.get("schema")!="g4c7-m37p2-independent-x11-blender-window-diagnostic-v1" or s.get("status")!="X11_BLENDER_FULL_WINDOW_CAPTURED_NEEDS_PIXEL_INSPECTION":
        raise ValueError("X11_PROVENANCE_MISSING")
    if s.get("capture_tool")!="scrot --window <X11 id>" or s.get("matched_window_count")!=1 or s.get("tree_exit_code")!=0 or s.get("capture_exit_code")!=0:
        raise ValueError("NOT_ONE_NAMED_X11_BLENDER_WINDOW")
    titles=s.get("window_titles")
    if not isinstance(titles,list) or len(titles)!=1 or BLEND not in titles[0]:
        raise ValueError("X11_WINDOW_NOT_THE_PINNED_BLENDER")
    if s.get("capture_sha256")!=sha(raw) or s.get("capture_bytes")!=raw.stat().st_size:
        raise ValueError("TAMPERED_X11_WINDOW_IMAGE")
    if c.get("schema")!="g4c7-p2-x11-native-region-diagnostic-v1" or c.get("status")!="X11_CROPPED_TWO_REGIONS_DIAGNOSTIC_ONLY_NOT_EDITOR_CERTIFIED":
        raise ValueError("ORIGINAL_CROP_PROVENANCE_NOT_PRESENT")
    if c.get("accepted_as_art") is not False or c.get("x11_crop_is_verified_blender_editor") is not False or c.get("model_calls")!=0 or c.get("art")!="HOLD" or c.get("official_adoptions")!=0:
        raise ValueError("FALSE_NATIVE_ART_OR_EDITOR_CERTIFICATION")
    views=c.get("views")
    if not isinstance(views,dict) or set(views)!=set(NAMES):
        raise ValueError("TWO_CROPS_REQUIRED")
    with Image.open(raw) as win:
        win.load()
        if win.format!="PNG" or win.width*win.height>8_000_000:
            raise ValueError("X11_WINDOW_IMAGE_INVALID")
        rect=rectangles(g,win.size)
        rgb=win.convert("RGB")
        result={}
        for name in NAMES:
            item=views[name]
            filename="P2_X11_CROPPED_"+name+"_DIAGNOSTIC_ONLY.png"
            if item.get("filename")!=filename or item.get("crop_box_top_left")!=list(rect[name]):
                raise ValueError("X11_REGION_PROVENANCE_TAMPER_"+name)
            f=folder/filename
            if not f.is_file() or not 1000<=f.stat().st_size<=8_000_000 or item.get("sha256")!=sha(f):
                raise ValueError("X11_REGION_HASH_INVALID_"+name)
            with Image.open(f) as image:
                image.load()
                if image.format!="PNG" or item.get("pixel_dimensions")!=list(image.size):
                    raise ValueError("X11_REGION_DIMENSIONS_INVALID_"+name)
                actual=image.convert("RGB")
                expected=rgb.crop(rect[name])
                if actual.size!=expected.size or ImageChops.difference(actual,expected).getbbox() is not None:
                    raise ValueError("X11_REGION_NOT_EXACT_WINDOW_PIXELS_"+name)
                reduced=actual.resize((min(128,actual.width),min(128,actual.height)))
                pixels=list(reduced.get_flattened_data() if hasattr(reduced,"get_flattened_data") else reduced.getdata())
                bright=sum(max(p)>20 for p in pixels)/len(pixels)
                unique=len(set(pixels))
                if bright<0.035 or unique<32:
                    raise ValueError("X11_REGION_BLACK_OR_EMPTY_"+name)
                result[name]={
                    "file":filename,"sha256":sha(f),"dimensions":list(actual.size),
                    "source_rectangle_top_left":list(rect[name]),
                    "visible_fraction":round(bright,5),"sample_unique_colors":unique,
                    "source":"ACTUAL_X11_BLENDER_WINDOW_CROP_MATCHES_DECLARED_VIEW_3D_REGION"
                }
    return {
        "schema":"g4c7-p2-externally-captured-editor-pixels-v1",
        "result":"X11_TWO_LIVE_BLENDER_VIEW_3D_REGION_PIXELS_VERIFIED_READ_ONLY",
        "native_blend_source_sha256":PIN,
        "raw_named_blender_x11_window_sha256":sha(raw),
        "original_native_screenshot_area_proven_valid":False,
        "gui_auto_authoring_demonstrated":False,
        "read_only_viewing_possible":True,"views":result,
        "real_city_art":False,"art":"HOLD","official_adoptions":0,
        "formal_331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
        "MakeCode":"NOT_EVALUATED","minecraft":"FORBIDDEN",
        "model_calls":0,"work":"NOT_USED"
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--folder",required=True)
    args=p.parse_args()
    d=Path(args.folder).resolve()
    out=d/OUTPUT
    if out.exists():
        raise FileExistsError("APPEND_ONLY_X11_VISUAL_CONTEXT_EXISTS")
    report=verify(d)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(report["result"],flush=True)

if __name__=="__main__":
    main()
