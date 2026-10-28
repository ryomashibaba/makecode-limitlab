"""A83-B4: source-only multiscale design contract. No genuine 3D or safety pass."""
import copy
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"artifacts"/"g4c7-a83-b4-authorial-frontage"/"spatial_contract.json"

def load():
    return json.loads(PATH.read_text(encoding="utf8"))

def components(nodes,edges):
    adj={n:set() for n in nodes}
    for e in edges:
        a,b=e["a"],e["b"]
        if a not in adj or b not in adj:
            return []
        adj[a].add(b);adj[b].add(a)
    remaining=set(nodes);all_components=[]
    while remaining:
        start=next(iter(remaining));seen=set();todo=[start]
        while todo:
            node=todo.pop()
            if node in seen:continue
            seen.add(node);todo+=list(adj[node]-seen)
        remaining-=seen
        all_components.append(sorted(seen))
    return all_components

def frontage_profile_hash(frontage):
    """2D design dependency, emphatically not a material mesh or façade certificate."""
    x,z,span,depth=frontage["x"],frontage["z"],frontage["span"],frontage["depth"]
    pts=[(x-span/2,z-15),(x-.28*span,z+depth*.45),
         (x,z+depth),(x+span*.43,z+depth*.55),
         (x+span/2,z-10)]
    return hashlib.sha256(json.dumps(pts).encode()).hexdigest()

def audit(d):
    fail=[]
    expected={"art":"HOLD","construction":"FORBIDDEN","formal_art_adoptions":0,
              "real_3d_mesh":"NOT_RUN","true_interdistrict_walk":"NOT_TESTED",
              "s1_g1_g2_g3":"NOT_RUN"}
    s=d.get("evidence_status",{})
    if any(s.get(k)!=v for k,v in expected.items()):
        fail.append("FORBIDDEN_ART_OR_CONSTRUCTION_STATUS")
    districts=d.get("districts",[])
    if [e.get("id") for e in districts]!=["W","C","E"]:
        fail.append("DISTRICTS_NOT_REGISTERED")
    frontages=d.get("frontages",[])
    ids=[f.get("id") for f in frontages]
    if len(frontages)!=6 or len(set(ids))!=6:
        fail.append("INSUFFICIENT_DISTINCT_FRONTAGES")
    for district in ("W","C","E"):
        if sum(f.get("district")==district for f in frontages)!=2:
            fail.append("DISTRICT_FRONTAGES_MISSING:"+district)
    nodes=d.get("public_nodes",[])
    nodeids={n.get("id") for n in nodes}
    if len(nodes)!=6 or len(nodeids)!=6:
        fail.append("INVALID_PUBLIC_GRAPH_NODES")
    if len(components(nodeids,d.get("links",[])))!=1:
        fail.append("INTENDED_NETWORK_DISCONNECTED")
    if any(e.get("not_verified") is not True for e in d.get("links",[])):
        fail.append("CLAIMED_WALKABLE_WITHOUT_MESH")
    for f in frontages:
        if len(set(f.get("uses",[])))<3:
            fail.append("ONE_PROGRAM_ONE_FRONTAGE_RECURSION:"+str(f.get("id")))
        if f.get("span",0)<100 or f.get("depth",0)<35:
            fail.append("UNDERSIZED_VISUAL_FRONTAGE:"+str(f.get("id")))
        if len(f.get("access",[]))!=2 or not set(f["access"])<=nodeids:
            fail.append("ACCESS_WITNESSES_MISSING:"+str(f.get("id")))
        if len(f.get("levels",[]))!=2 or f["levels"][1]<=f["levels"][0]:
            fail.append("NO_VERTICAL_ACTIVITY_THICKNESS:"+str(f.get("id")))
        if not any(j["id"]==f["district"]+"G" for j in nodes if j["id"] in f["access"]):
            fail.append("MISSING_PUBLIC_ANCHOR:"+str(f.get("id")))
        if not any(j["id"]==f["district"]+"U" for j in nodes if j["id"] in f["access"]):
            fail.append("MISSING_UPPER_ANCHOR:"+str(f.get("id")))
    if len(d.get("voids",[]))!=3 or not all(v.get("real_void_not_proven") for v in d.get("voids",[])):
        fail.append("FALSE_COURTYARD_EVIDENCE")
    return {"stage":"A83-B4_SOURCE_PRE3D", "source_consistent":not fail,
            "rejected_reasons":fail, "public_graph_components":len(components(nodeids,d.get("links",[]))),
            "2d_frontage_hashes":{f["id"]:frontage_profile_hash(f) for f in frontages},
            "macro_art":"NOT_ADOPTED_UNREVIEWED_TRUE_3D",
            "real_3d":"NOT_RUN","s1_g1_g2_g3":"NOT_RUN","construction":"FORBIDDEN"}

if __name__=="__main__":
    print(json.dumps(audit(load()),ensure_ascii=False,indent=2))
