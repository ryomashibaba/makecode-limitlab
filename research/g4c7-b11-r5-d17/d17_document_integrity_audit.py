"""D17 independent *document-integrity* checks, NOT geometry, G0, visual quality or safety certification."""
import copy
import json
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT=Path(__file__).resolve().parent
SVG_NS="{http://www.w3.org/2000/svg}"
REQUIRED={"urban-silhouette","inhabited-mass","daylight","public-eye",
          "maker-bay","research-bay","upper-home","civic-route",
          "weather-shelter","vertical-core-e1","vertical-core-e2","ground"}

def inspect_svg(data):
    root=ET.fromstring(data)
    assert root.tag==SVG_NS+"svg"
    ids=[node.attrib["id"] for node in root.iter() if "id" in node.attrib]
    assert len(ids)==len(set(ids)), "duplicate SVG ids"
    assert REQUIRED.issubset(set(ids)), "missing diagram roles"
    for node in root.iter():
        if node.attrib.get("id")=="urban-silhouette":
            assert len(node.attrib.get("d",""))>80, "insufficient silhouette"
            return node.attrib["d"]
    raise AssertionError("silhouette not found")

def inspect_record(record,svg_texts):
    assert record["stage"]=="G4-C7 B11-R5 D17"
    s=record["state"]
    assert s["overall"]=="ART HOLD" and s["adopted_art_count"]==0
    assert s["true_3D"]=="NOT_RUN" and s["official_G0"]=="NOT_RUN"
    assert all(s["official_"+gate]=="NOT_RUN" for gate in ("S1","G1","G2","G3"))
    assert s["minecraft_education_construction"]=="FORBIDDEN"
    assert s["city_integration"]=="FORBIDDEN"
    assert s["pr53"]=="KEEP_DRAFT_OPEN" and s["main"]=="DO_NOT_EDIT"
    candidates=record["candidates"]
    assert [c["id"] for c in candidates]==["C1","C2"]
    assert "HOLD" in candidates[0]["pre3d_status"]
    assert "REJECT" in candidates[1]["pre3d_status"]
    silhouettes=[inspect_svg(svg_texts[c["id"]]) for c in candidates]
    assert silhouettes[0]!=silhouettes[1], "same silhouette reused"
    for c in candidates:
        assert len(c["risks"])>=3
        assert len(c["activity_counterfactual"])>=40
        assert c["structural_hypothesis"].endswith("NOT engineered") or "NOT engineered" in c["structural_hypothesis"]
        assert "NOT modeled" in c["vertical_access"]
    return {"source_svg_roles":"PASS", "two_distinct_2D_silhouettes":"PASS",
            "scope_honesty":"PASS", "independent_negative_controls":"PASS",
            "art":"NOT_ADOPTED","true_3D":"NOT_RUN", "official_G0_S1_G1_G2_G3":"NOT_RUN",
            "construction":"FORBIDDEN"}

def main():
    record=json.loads((ROOT/"d17_author_study.json").read_text(encoding="utf-8"))
    svg={name:(ROOT/f"d17_{name.lower()}_author_plate.svg").read_text(encoding="utf-8")
         for name in ("C1","C2")}
    result=inspect_record(record,svg)
    bad=copy.deepcopy(record);bad["state"]["adopted_art_count"]=1
    try: inspect_record(bad,svg)
    except AssertionError: pass
    else: raise AssertionError("must reject fabricated adoption")
    bad_svg=svg.copy();bad_svg["C1"]=svg["C1"].replace('id="research-bay"','id="missing-research-bay"')
    try: inspect_record(record,bad_svg)
    except AssertionError: pass
    else: raise AssertionError("must detect missing research")
    identical=svg.copy();identical["C2"]=svg["C1"]
    try: inspect_record(record,identical)
    except AssertionError: pass
    else: raise AssertionError("must detect copied silhouette")
    (ROOT/"d17_document_integrity_results.json").write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("D17 document/source integrity PASS; 2D DESIGN ONLY; NO art approval, NO 3D/QA/Minecraft")
if __name__=="__main__": main()
