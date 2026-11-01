#!/usr/bin/env python3
"""M37-P0 activity-to-form SOURCE/INTENT contract, never a visual ART PASS.

Reject the M37-O1 failure of isolated program footprints + route slabs at the
*input* stage. This only validates the authored commitments, not their
physical realization or visual quality. No bpy, Blender scene, MakeCode,
network, or Minecraft world writes.
"""
import copy
import json
from collections import deque
from pathlib import Path

DOC = Path("research/g4c7-b11-r5-d56/p2/d3s26/M37P0_SHARED_AUTHOR_DECISION_SOURCE_OF_FORM_V1.json")
REQUIRED = {"arrival","commons","maker_view","maker_staff_gate","maker_work",
            "research","habitat_gate","habitat_private","culture","upper"}
PUBLIC_REACH = {"commons","maker_view","research","habitat_gate","culture","upper"}
REQUIRED_BANS = {
    "program_footprint_extrusion","independent_pavilions_then_links",
    "long_urban_tube","road_band","stacked_shelf","primitive_first_city"
}
REQUIRED_COUPLINGS = [
    {"maker_work","maker_view","research"},
    {"commons","habitat_gate","habitat_private"},
    {"research","culture","maker_view"},
    {"commons","culture","upper"}
]

def validate(d):
    assert d["schema"]=="g4c7-m37p0-artist-owned-source-of-form-contract-v1"
    assert d["status"]=="AUTHOR_INPUT_ONLY_NOT_ART"
    assert d["formal_art_adoptions"]==0
    assert d["formal_331_993"]=="NOT_RUN"
    assert d["formal_S1_G1_G2_G3"]=="NOT_RUN"
    assert d["minecraft"]=="FORBIDDEN"
    assert d["route_status"]=="INTENT_ONLY_NOT_WALKABLE"
    assert d["proposed_geometry"]=="NONE_NOT_GENERATED"
    assert d["no_proxy_passing"]=="GRAPH_CONTRACT_PASS_NEVER_IMPLIES_ART_OR_ROUTE_OR_SAFETY_PASS"
    assert REQUIRED_BANS<=set(d["banned_dominant_generators"])
    nodes=d["nodes"]
    by_id={n["id"]:n for n in nodes}
    assert len(by_id)==len(nodes)
    assert set(by_id)==REQUIRED
    assert by_id["maker_work"]["realm"]=="staff"
    assert by_id["maker_staff_gate"]["realm"]=="staff"
    assert by_id["habitat_private"]["realm"]=="private"
    for key in REQUIRED - {"maker_work","maker_staff_gate","habitat_private"}:
        assert by_id[key]["realm"]=="public"
    assert all(len(n["experience"])>=20 for n in nodes)
    edges=d["route_edges"]
    assert len(edges)==9
    assert all(e["from"] in by_id and e["to"] in by_id and e["from"]!=e["to"] for e in edges)
    assert all(e["access"] in {"public","private_controlled","staff_controlled"} for e in edges)
    public_graph={key:set() for key in by_id}
    for e in edges:
        if e["access"]=="public":
            public_graph[e["from"]].add(e["to"])
            public_graph[e["to"]].add(e["from"])
        else:
            assert e["access"]!="private_controlled" or (
                "habitat_private" in {e["from"],e["to"]})
            assert e["access"]!="staff_controlled" or (
                "maker_staff_gate" in {e["from"],e["to"]} or
                "maker_work" in {e["from"],e["to"]})
    queue=deque(["arrival"])
    reachable={"arrival"}
    while queue:
        for nxt in public_graph[queue.popleft()]:
            if nxt not in reachable:
                reachable.add(nxt)
                queue.append(nxt)
    # Every key PUBLIC experience must be reachable without walking through
    # the spacecraft factory or private home. Still intent, NOT actual walking.
    assert PUBLIC_REACH<=reachable
    assert not reachable & {"maker_work","maker_staff_gate","habitat_private"}
    assert any(e["access"]=="private_controlled" and
               set((e["from"],e["to"]))=={"habitat_gate","habitat_private"}
               for e in edges)
    assert any(e["access"]=="staff_controlled" and
               set((e["from"],e["to"]))=={"maker_staff_gate","maker_work"}
               for e in edges)
    decisions=d["shared_author_decisions"]
    assert len(decisions)>=4
    assert len({x["id"] for x in decisions})==len(decisions)
    sets=[]
    impact_universe=set()
    for x in decisions:
        affected=set(x["affected"])
        impact=set(x["impacts"])
        assert len(affected)>=3 and affected<=REQUIRED
        assert len(affected)==len(x["affected"])
        assert {"urban_form","occupied_space"}<=impact
        assert len(impact)>=3
        assert len(x["author_why"])>=45
        sets.append(affected)
        impact_universe |= impact
    for core in REQUIRED_COUPLINGS:
        assert any(core<=s for s in sets),core
    assert {"staff_separation","privacy","daylight","vertical_access"}<=impact_universe
    assert len(d["critical_next_proof"])>=4
    assert all(len(x)>=30 for x in d["critical_next_proof"])
    return {
        "result":"SOURCE_OF_FORM_INPUT_CONTRACT_COHERENT_ONLY",
        "geometry_generated":False,
        "art_pass":False,
        "formal_art_adoptions":0,
        "formal_331_993":"NOT_RUN",
        "minecraft":"FORBIDDEN",
        "shared_author_decisions":len(decisions),
        "public_route_intent_connected":True,
        "physical_walkability":"NOT_TESTED",
        "real_shared_mesh":"NOT_TESTED",
        "meaning":"SOURCE INTENT ONLY; visual/art and native geometry must be proved separately"
    }

def negative_controls(original):
    rejected=[]
    def reject(name,change):
        candidate=copy.deepcopy(original)
        change(candidate)
        try:
            validate(candidate)
        except (AssertionError,KeyError,TypeError):
            rejected.append(name)
            return
        raise AssertionError("NEGATIVE_NOT_DETECTED:"+name)
    reject("make_habitat_private_public",
           lambda x:next(e for e in x["route_edges"] if e["to"]=="habitat_private").update(access="public"))
    reject("make_factory_work_public",lambda x:[
        e.update(access="public") for e in x["route_edges"]
        if e["to"] in ("maker_staff_gate","maker_work")])
    reject("delete_manufacturing_shared_form_decision",
           lambda x:x["shared_author_decisions"].pop(0))
    reject("remove_actual_form_effect",
           lambda x:x["shared_author_decisions"][1]["impacts"].remove("urban_form"))
    reject("claim_blend_art_before_creating_it",
           lambda x:x.update(proposed_geometry="NATIVE_MODEL_COMPLETE"))
    reject("erase_banned_simple_generator",
           lambda x:x["banned_dominant_generators"].remove("program_footprint_extrusion"))
    assert len(rejected)==6
    return rejected

if __name__=="__main__":
    root=json.loads(DOC.read_text(encoding="utf-8"))
    report=validate(root)
    report["negative_controls_rejected"]=negative_controls(root)
    print(json.dumps(report,ensure_ascii=False,indent=2))
