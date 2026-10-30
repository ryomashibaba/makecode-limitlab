"""D3S9 SOURCE GUARD: prevent false artistic and TRUE3D promotion. No beauty algorithm."""
import json,copy
from pathlib import Path
p=Path(__file__).resolve().parent
d=json.loads((p/"D3S9_ART_GATE_STATE.json").read_text(encoding="utf-8"))
def check(x):
    assert x["art_criterion_is_manual"] is True, "art is human judgment"
    assert x["art_adoptions"]==0 and x["approved_true3d_models"]==0,"false art/GLB adoption"
    assert all(v["author_art"]=="REJECT" for v in x["candidates"].values()),"art promotion"
    assert all(len(v["scenes"])==5 and v["full_glb"]=="NOT_BUILT" for v in x["candidates"].values()),"fake 3D camera"
    assert x["actual_model_reimport"]=="NOT_RUN","fake GLB verification"
    assert x["actual_roof_floor_shared"]=="NOT_BUILT","fake shared triangles"
    assert x["actual_internal_public_axes"]=="NOT_BUILT" and x["actual_vertical_transfer"]=="NOT_BUILT","fake public rooms"
    assert x["human_body_331_foot_993"]=="NOT_RUN" and x["formal_G0_S1_G1_G2_G3"]=="NOT_RUN","fake QA"
    assert not any((x["minecraft_world_changes"],x["city_integration"],x["main_branch_changes"])),"unsafe change"
    assert x["PR53_must_be_draft"],"unsafe PR state"
check(d)
changes={
 "false art adoption":lambda x:x.update(art_adoptions=1),
 "false GLB adoption":lambda x:x.update(approved_true3d_models=1),
 "fake GLB import":lambda x:x.update(actual_model_reimport="PASS"),
 "fake shared structure":lambda x:x.update(actual_roof_floor_shared="PASS"),
 "fake public rooms":lambda x:x.update(actual_internal_public_axes="PASS"),
 "fake formal humans":lambda x:x.update(human_body_331_foot_993="PASS"),
 "unauthorized main change":lambda x:x.update(main_branch_changes=True),
 "computer-certified art":lambda x:x.update(art_criterion_is_manual=False)}
results=[]
for name,mutation in changes.items():
    altered=copy.deepcopy(d);mutation(altered)
    try:check(altered);ok=False
    except AssertionError:ok=True
    results.append({"mutation":name,"detected":ok})
assert all(x["detected"] for x in results),"SOURCE GUARD FAILED"
print(json.dumps({"kind":"D3S9 SOURCE ONLY; NOT ART OR TRUE3D","detected":len(results),"total":len(results),"checks":results},ensure_ascii=False,indent=2))
