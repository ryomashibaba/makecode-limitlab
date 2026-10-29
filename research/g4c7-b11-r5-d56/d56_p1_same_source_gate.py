"""D56 P1: validate that four editorial crops reuse one original SVG section.
This is an XML/source identity gate, NOT artistic approval or physical feasibility.
Standard-library only. Deliberate broken variants must be rejected.
"""
import copy
import hashlib
import json
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SVG=ROOT/"D56_P1_FOUR_MOMENTS_ONE_MASTER.svg"
CONTRACT=ROOT/"D56_P1_VIEW_CONTRACT.json"
NS="{http://www.w3.org/2000/svg}"
XLINK="{http://www.w3.org/1999/xlink}href"
PANELS=("panel_far","panel_civic","panel_research","panel_living")

def by_id(root,identifier):
    return [n for n in root.iter() if n.get("id")==identifier]

def validate(root, contract):
    assert root.tag==NS+"svg"
    master=contract["master_id"]
    assert len(by_id(root,master))==1, ("missing or duplicate original master",master)
    assert len(by_id(root,contract["one_outer_material_outline_id"]))==1
    for n in contract["subtractions"]+contract["occupancies"]:
        assert len(by_id(root,n))==1, ("missing shared carved section element",n)
    assert len(contract["four_panels"])==4
    for name,record in zip(PANELS,contract["four_panels"]):
        assert record["id"]==name
        panels=by_id(root,name)
        assert len(panels)==1
        native=[n for n in panels[0] if n.tag==NS+"svg"]
        assert len(native)==1,("no dedicated SVG crop",name)
        v=native[0]
        assert [float(x) for x in v.get("viewBox").split()] ==record["viewBox"],(name,"viewBox mismatch")
        uses=[n for n in v.iter() if n.tag==NS+"use"]
        assert len(uses)==1,("must use original scene once and not redraw",name)
        u=uses[0]
        assert u.get("href")==f"#{master}",("wrong SVG2 source",name)
        assert u.get(XLINK)==f"#{master}",("wrong fallback source",name)
        assert record["reused_master"]==master
    uses=list(root.iter(NS+"use"))
    assert len(uses)==4,("unexpected scene duplication",len(uses))
    external=[n for n in root.iter() if n.tag in (NS+"image",NS+"foreignObject")]
    assert not external,"no external or hidden reference images permitted"
    return {"master_id":master,"view_count":4,"one_material_outline":True,
            "named_carved_regions":len(contract["subtractions"]),
            "activity_elements":len(contract["occupancies"])}

def should_reject(faulty,contract,label):
    try:validate(faulty,contract)
    except AssertionError:return True
    raise AssertionError("negative identity control escaped: "+label)

def main():
    src=SVG.read_bytes()
    meta=json.loads(CONTRACT.read_text(encoding="utf-8"))
    original=ET.fromstring(src)
    result=validate(original,meta)
    bad=copy.deepcopy(original)
    panel=by_id(bad,PANELS[0])[0]
    nested=next(n for n in panel if n.tag==NS+"svg")
    nested.remove(next(n for n in nested if n.tag==NS+"use"))
    should_reject(bad,meta,"one scene detached")
    bad=copy.deepcopy(original)
    panel=by_id(bad,PANELS[2])[0]
    nested=next(n for n in panel if n.tag==NS+"svg")
    nested.find(NS+"use").set("href","#invented-independent-scene")
    should_reject(bad,meta,"research redraw instead of reuse")
    bad=copy.deepcopy(original)
    master=by_id(bad,meta["master_id"])[0]
    outer=by_id(bad,meta["one_outer_material_outline_id"])[0]
    master.remove(outer)
    should_reject(bad,meta,"structural original removed")
    bad=copy.deepcopy(original)
    view=next(n for n in by_id(bad,PANELS[3])[0] if n.tag==NS+"svg")
    view.set("viewBox","760 180 250 200")
    should_reject(bad,meta,"living viewBox mismatch")
    out={"gate":"D56 P1 master-source SAME 2D SECTION ONLY",
         "source_sha256":hashlib.sha256(src).hexdigest(),
         **result,
         "negative_controls_passed":["scene detached","invented research original",
                                     "original material missing","independent living framing"],
         "actual_3d":"NOT RUN",
         "actual_eye_level_cameras":"NOT RUN",
         "closed_watertight_living_room":"NOT RUN",
         "sunlight_body_sweep_support":"NOT RUN",
         "official_331_993":"NOT RUN",
         "formal_G0_S1_G1_G2_G3":"NOT RUN",
         "art":"HOLD - author review; no evidence of aesthetic acceptance",
         "Minecraft":"CONSTRUCTION FORBIDDEN"}
    png=ROOT/"D56_P1_FOUR_MOMENTS_PREVIEW.png"
    if png.exists():
        raw=png.read_bytes()
        assert raw[:8]==b"\x89PNG\r\n\x1a\n" and len(raw)>30000
        width,height=struct.unpack(">II",raw[16:24])
        assert (width,height)==(1740,1260), (width,height)
        out["rendered_preview_png_bytes"]=len(raw)
        out["rendered_preview_png_sha256"]=hashlib.sha256(raw).hexdigest()
    (ROOT/"D56_P1_SOURCE_IDENTITY_AUDIT.json").write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
