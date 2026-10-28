"""D9 REVIEW SNAPSHOT gate; DOES NOT rebuild or inspect any 3D geometry."""
import json
from pathlib import Path
p=Path(__file__).with_name("D9_REVIEW_INDEX.json")
d=json.loads(p.read_text(encoding="utf8"))
assert d["art"]=="G0 ART REJECT"
assert d["next_sketch"]=="PRE-3D HOLD"
assert d["official_art_adopted"]==0
assert d["formal_qa"]=="NOT_RUN" and d["minecraft"]=="FORBIDDEN"
a,b=d["variants"]
assert a["name"]=="inhabited" and b["name"]=="research_removed"
assert a["faces"]>b["faces"]
assert a["research_view_blocked"] and not b["research_view_blocked"]
for row in (a,b):
    assert row["floor_witnesses"]==row["floor_samples"]==135
    assert row["overhead_hits"]==0 and row["maker_view_blocked"]
    assert len(row["obj_sha256"])==64 and len(row["glb_sha256"])==64
assert all(len(s)==64 for s in d["local_source_sha256"].values())
print("D9 REVIEW INDEX PASS. ART REJECT / formal QA NOT RUN / NO CONSTRUCTION")
print("This is NOT a saved-PLY or real-3D CI run.")
