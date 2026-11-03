#!/usr/bin/env python3
"""Read-only extraction of Blender-declared VIEW_3D regions from an X11 window PNG.

This is an independent visibility diagnostic. X11 pixels are not a vetted
native Blender screenshot, not newly authored city art, and never reach a model.
Coordinate contract: Blender Region.x/y are WINDOW-relative with a bottom-left
origin. Pillow's top-left origin is inverted only after exact client-size match.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

NAMES = ('MACRO_EDITOR', 'LIVED_EDITOR')
GEOMETRY = 'P2_GUI_NATIVE_REGION_GEOMETRY_DIAGNOSTIC_ONLY.json'
WINDOW = 'P2_X11_BLENDER_FULL_WINDOW_DIAGNOSTIC_ONLY.png'
WINDOW_REPORT = 'P2_X11_BLENDER_WINDOW_DIAGNOSTIC.json'
RESULT = 'P2_X11_NATIVE_REGION_CROP_DIAGNOSTIC_ONLY.json'
MAX_PNG_BYTES = 8_000_000


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def bounded_json(path):
    if not path.is_file() or not 10 <= path.stat().st_size <= 120_000:
        return None
    return json.loads(path.read_text(encoding='utf-8'))


def rect_geometry(geometry, image_size):
    if not isinstance(geometry, dict) or geometry.get('schema') != 'g4c7-p2-native-gui-window-regions-v1':
        raise ValueError('BLENDER_REGION_METADATA_UNVERIFIED')
    if geometry.get('art') != 'HOLD' or geometry.get('official_adoptions') != 0:
        raise ValueError('BLENDER_REGION_ART_CHARTER_MISMATCH')
    if geometry.get('same_window') is not True:
        raise ValueError('MULTIPLE_BLENDER_WINDOWS_UNSUPPORTED')
    expected=geometry.get('window_dimensions')
    if (not isinstance(expected, list) or len(expected)!=2 or
        any(type(x)!=int or x<200 or x>8192 for x in expected)):
        raise ValueError('WINDOW_DIMENSIONS_UNVERIFIED')
    # Never guess decorations, DPI scales, border offsets, or resize images.
    if tuple(expected)!=tuple(image_size):
        raise ValueError('X11_WINDOW_SIZE_DIFFERS_FROM_BLENDER_CLIENT')
    regions=geometry.get('regions')
    if not isinstance(regions, dict) or set(regions)!=set(NAMES):
        raise ValueError('EXACT_TWO_BLENDER_REGIONS_REQUIRED')
    width,height=expected
    result={}
    for name in NAMES:
        region=regions[name]
        if not isinstance(region, dict) or set(region)!=set(('x','y','width','height')):
            raise ValueError('REGION_RECT_UNVERIFIED_'+name)
        x,y,w,h=(region[k] for k in ('x','y','width','height'))
        if any(type(n)!=int for n in (x,y,w,h)) or x<0 or y<0 or w<100 or h<100 or x+w>width or y+h>height:
            raise ValueError('REGION_OUTSIDE_CLIENT_'+name)
        result[name]=(x,height-y-h,x+w,height-y)
    a,b=(result[n] for n in NAMES)
    if max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3]):
        raise ValueError('BLENDER_VIEWPORT_REGIONS_OVERLAP')
    return result


def run(folder):
    folder=Path(folder).resolve()
    if not folder.is_dir():
        raise FileNotFoundError('CI_EXPORT_DIRECTORY_MISSING')
    dest=folder/RESULT
    if dest.exists():
        raise FileExistsError('APPEND_ONLY_NATIVE_REGION_DIAGNOSTIC_ALREADY_EXISTS')
    report={
        'schema':'g4c7-p2-x11-native-region-diagnostic-v1',
        'status':'NOT_AVAILABLE',
        'x11_crop_is_verified_blender_editor':False,
        'accepted_as_art':False,
        'model_calls':0,
        'art':'HOLD',
        'official_adoptions':0,
        'minecraft':'FORBIDDEN',
        'views':{}
    }
    def finish(status):
        report['status']=status
        dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        return report
    geometry=bounded_json(folder/GEOMETRY)
    source=bounded_json(folder/WINDOW_REPORT)
    raw=folder/WINDOW
    if geometry is None or source is None or not raw.is_file():
        return finish('DIAGNOSTIC_SOURCE_INCOMPLETE')
    if source.get('status')!='X11_BLENDER_FULL_WINDOW_CAPTURED_NEEDS_PIXEL_INSPECTION':
        return finish('X11_WINDOW_CAPTURE_NOT_CONFIRMED')
    if (raw.stat().st_size>MAX_PNG_BYTES or
        source.get('capture_sha256')!=digest(raw)):
        return finish('X11_WINDOW_IMAGE_TAMPER_OR_OVERSIZE')
    try:
        with Image.open(raw) as opened:
            opened.load()
            if opened.format!='PNG':
                raise ValueError('X11_WINDOW_NOT_PNG')
            rectangles=rect_geometry(geometry,opened.size)
            base=opened.convert('RGB')
            for name in NAMES:
                region=base.crop(rectangles[name])
                filename='P2_X11_CROPPED_'+name+'_DIAGNOSTIC_ONLY.png'
                file=folder/filename
                if file.exists():
                    raise FileExistsError('APPEND_ONLY_X11_REGION_IMAGE_ALREADY_EXISTS')
                preview=region.resize((min(region.width,256), min(region.height,256)))
                pixels=preview.get_flattened_data() if hasattr(preview, 'get_flattened_data') else preview.getdata()
                fraction=sum(max(px)>20 for px in pixels)/(preview.width*preview.height)
                region.save(file,format='PNG')
                report['views'][name]={
                    'filename':filename,'sha256':digest(file),
                    'crop_box_top_left':list(rectangles[name]),
                    'pixel_dimensions':[region.width,region.height],
                    'fraction_visible_nonblack':round(fraction,6),
                    'visible_hint_only':fraction>=0.035,
                    'not_art_and_not_certified':True
                }
    except (ValueError, OSError, Image.DecompressionBombError) as exc:
        report['error']=type(exc).__name__+': '+str(exc)[:150]
        return finish('X11_REGION_GEOMETRY_OR_PNG_REJECTED')
    return finish('X11_CROPPED_TWO_REGIONS_DIAGNOSTIC_ONLY_NOT_EDITOR_CERTIFIED')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--folder',required=True)
    args=ap.parse_args()
    result=run(args.folder)
    print('G4C7_X11_VIEWPORT_CROP',result['status'],flush=True)


if __name__=='__main__':
    main()
