"""G4-C7 B11-R5 D3 compact independent pre-3D design-contract audit.
Python stdlib only. No constructed geometry, path certification or Minecraft build.
The richer 2D matplotlib drawing source and raw diagrams are in the separately
delivered conversation evidence ZIP; this file does not claim to recreate them.
"""
import json
from collections import deque, defaultdict

RESEARCH_Z=132
RESIDENTIAL_Z=220
# Intended program nodes; not surveyed/buildable locations.
NODES={
"WEST_ARRIVAL":(-420,12,"public"),
"EAST_ARRIVAL":(420,12,"public"),
"CIVIC_ENTRY":(-265,18,"public"),
"FAB_PUBLIC_LOW":(-145,26,"public"),
"FAB_VIEW":(-150,None,"public"),
"RESEARCH_COMMON":(205,132,"public"),
"CULTURE_HALL":(318,132,"public"),
"SKY_COMMON":(236,220,"public"),
"RES_THRESHOLD":(344,220,"controlled"),
"SERVICE_ENTRY":(420,12,"service"),
"FAB_WORKFLOOR":(10,18,"service"),
}
WALKS=[
("WEST_ARRIVAL","CIVIC_ENTRY"),
("EAST_ARRIVAL","CIVIC_ENTRY"),
("CIVIC_ENTRY","FAB_PUBLIC_LOW"),
("FAB_PUBLIC_LOW","FAB_VIEW"),
("RESEARCH_COMMON","CULTURE_HALL"),
("RESEARCH_COMMON","SKY_COMMON"),
]
CORES={
"E1":("CIVIC_ENTRY","FAB_VIEW","RESEARCH_COMMON","SKY_COMMON"),
"E2":("CIVIC_ENTRY","FAB_VIEW","RESEARCH_COMMON","SKY_COMMON"),
}
SERVICE=[("SERVICE_ENTRY","FAB_WORKFLOOR")]

def reachable(start, enabled, cores=CORES):
    adj=defaultdict(set)
    for a,b in WALKS:
        adj[a].add(b);adj[b].add(a)
    for name,stops in cores.items():
        if name not in enabled:continue
        for a,b in zip(stops,stops[1:]):
            adj[a].add(b);adj[b].add(a)
    out={start};queue=deque([start])
    while queue:
        for b in adj[queue.popleft()]:
            if b not in out:out.add(b);queue.append(b)
    return out

def make(clearance):
    if clearance not in (70,90):
        raise ValueError("Only controlled study inputs 70 or 90 m")
    floor=18
    roof_soffit=floor+clearance
    roof_top=roof_soffit+16
    view_z=roof_soffit-12
    nodes={k:(x, view_z if k=="FAB_VIEW" else z, access)
           for k,(x,z,access) in NODES.items()}
    public={k for k,(_,_,access) in nodes.items() if access=="public"}
    checks={}
    for enabled in (("E1","E2"),("E1",),("E2",)):
        label="+".join(enabled)
        checks["public_topological_reachability_"+label]=all(
            public.issubset(reachable(entry,set(enabled)))
            for entry in ("WEST_ARRIVAL","EAST_ARRIVAL"))
    checks["no_vertical_cores_does_not_reach_upper"]=not public.issubset(
        reachable("WEST_ARRIVAL",set()))
    sabotage=dict(CORES);sabotage["E2"]=("CIVIC_ENTRY",)
    checks["sabotage_detected"]=not public.issubset(
        reachable("WEST_ARRIVAL",{"E2"},sabotage))
    unresolved=[(a,b,abs(nodes[a][1]-nodes[b][1])) for a,b in WALKS
                if abs(nodes[a][1]-nodes[b][1])>1]
    checks["service_separated_in_abstract_graph"]=all(
        nodes[a][2]=="service" and nodes[b][2]=="service" for a,b in SERVICE)
    checks["workshop_view_beyond_work_footprint"]=(nodes["FAB_VIEW"][0]<-120)
    buffer=RESEARCH_Z-roof_top
    result={
      "clearance_target_m":clearance,
      "fabrication_floor_z_m":floor,
      "roof_soffit_target_z_m":roof_soffit,
      "roof_superstructure_top_target_z_m":roof_top,
      "public_observation_target_z_m":view_z,
      "research_z_m_fixed":RESEARCH_Z,
      "residential_z_m_fixed":RESIDENTIAL_Z,
      "research_to_roof_buffer_z_m":buffer,
      "author_target_buffer_12m_met":buffer>=12,
      "unresolved_vertical_walk_edges":unresolved,
      "checks":checks,
      "limitations":["Only schematic intended adjacency, NOT actual human path",
                     "E1 and E2 not modeled as physical lift shafts or safe exits",
                     "Building form, structural span, and daylight not designed",
                     "roof-soffit HEIGHT IS TARGET not actual PLY measured"],
      "status":{"pre_3d":"HOLD","G0_art":"NOT_RUN","ART":"HOLD",
                "adopted_art_count":0,"S1_G1_G2_G3":"NOT_RUN",
                "formal_331_993":"NOT_RUN","minecraft":"FORBIDDEN"},
    }
    assert all(checks.values()),checks
    assert len(unresolved)==5
    return result

def run():
    a,b=make(70),make(90)
    assert (a["roof_soffit_target_z_m"],b["roof_soffit_target_z_m"])==(88,108)
    assert (a["public_observation_target_z_m"],b["public_observation_target_z_m"])==(76,96)
    assert a["research_z_m_fixed"]==b["research_z_m_fixed"]==132
    assert a["residential_z_m_fixed"]==b["residential_z_m_fixed"]==220
    assert a["author_target_buffer_12m_met"] and not b["author_target_buffer_12m_met"]
    print(json.dumps({"stage":"B11-R5 D3","kind":"PRE_3D_CONTRACT_ONLY",
       "cases":{"70":a,"90":b},"result":"DESIGN_HOLD_NOT_ART_PASS"},
       ensure_ascii=False,indent=2))
if __name__=="__main__":
    run()
