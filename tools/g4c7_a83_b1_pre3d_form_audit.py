"""A83-B1 authored 2D contract: pre-3D art rejection, NOT safety or true 3D."""
import json
import math
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "artifacts/g4c7-a83-b1-pre3d-review/source_contract.json"

def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

def is_inside_silhouette(points, x, z):
    if z < 0:
        return False
    for (x1,z1),(x2,z2) in zip(points,points[1:]):
        if x1 <= x <= x2 and x1 < x2:
            return z <= z1 + (z2-z1)*(x-x1)/(x2-x1) + 1e-7
    return False

def connected_components(ids, links):
    adj={p:set() for p in ids}
    for a,b in links:
        if a not in adj or b not in adj:
            return None
        adj[a].add(b)
        adj[b].add(a)
    remaining=set(ids)
    components=[]
    while remaining:
        seen=set()
        stack=[next(iter(remaining))]
        while stack:
            node=stack.pop()
            if node in seen:
                continue
            seen.add(node)
            stack.extend(adj[node]-seen)
        components.append(sorted(seen))
        remaining-=seen
    return sorted(components)

def b0_components():
    from g4c7_a83_b0_support_growth_g0 import sample_model
    model=sample_model()
    return connected_components([x["id"] for x in model["zones"]],
                                [(r["from"],r["to"]) for r in model["routes"]])

def audit(data):
    errors=[]
    if len(data.get("schemes",[]))!=3 or any(s.get("decision")!="PRE_3D_REJECT" for s in data["schemes"]):
        errors.append("NO_REJECTED_FORM_REVIEW")
    c=next((s for s in data.get("schemes",[]) if s.get("id")=="C"),None)
    if c is None:
        return {"source_review_consistent":False,"errors":errors+["NO_C_SILHOUETTE"],"art":"HOLD"}
    ps=data.get("programs",[])
    ids=[p.get("id") for p in ps]
    if len(ids)!=6 or len(set(ids))!=6:
        errors.append("SIX_DISTINCT_PROGRAM_WITNESSES_REQUIRED")
    if any(sum(p.get("district")==d for p in ps)!=2 for d in ("W","C","E")):
        errors.append("DISTRICT_PROGRAM_BALANCE")
    for p in ps:
        if not is_inside_silhouette(c["points"],p["x"],p["z"]):
            errors.append("PROGRAM_OUTSIDE_AUTHOR_SILHOUETTE:"+p["id"])
    roots=data.get("roots",[])
    if len(roots)!=6:
        errors.append("ROOT_COUNT")
    for x,z,u,v in roots:
        if abs(z)>1e-6 or not is_inside_silhouette(c["points"],u,v):
            errors.append("UNROOTED_SUPPORT_INTENTION")
        if not any(math.dist((p["x"],p["z"]),(u,v))<1e-6 for p in ps):
            errors.append("SUPPORT_INTENTION_NOT_REGISTERED_TO_PROGRAM")
    for p in ps:
        if not any(math.dist((p["x"],p["z"]),(r[2],r[3]))<1e-6 for r in roots):
            errors.append("ACTIVITY_NO_SUPPORT_WITNESS:"+p["id"])
    components=connected_components(ids,data.get("links",[]))
    if components is None or len(components)!=1:
        errors.append("DISCONNECTED_ABSTRACT_CITY")
    return {
      "source_review_consistent":not errors,
      "errors":errors,
      "2d_silhouettes":"ALL_PRE_3D_REJECT",
      "abstract_links":"GRAPH_ONLY_NOT_WALKABLE",
      "real_enclosed_rooms":"NOT_TESTED",
      "real_openings":"NOT_TESTED",
      "real_floor_support":"NOT_TESTED",
      "structural_load":"NOT_TESTED",
      "331_humans_993_feet":"NOT_RUN",
      "true_3d_render":"NOT_RUN",
      "art":"HOLD",
      "formal_s1_g1_g2_g3":"NOT_RUN",
      "minecraft_construction":"FORBIDDEN",
      "city_integration":"FORBIDDEN"
    }

if __name__=="__main__":
    print(json.dumps(audit(load()),indent=2))
