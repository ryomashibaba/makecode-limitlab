#!/usr/bin/env python3
"""M37-E: READ ONLY native M37-D inspection. Floor contact is NOT safe walking."""
import argparse, csv, hashlib, json, math
from pathlib import Path
from collections import Counter,defaultdict
ROOT=Path("artifacts/g4c7-m37d-verified-native-urban-fabric-art-hold")
OUT=Path("artifacts/g4c7-m37e-independent-contact-audit")
NAME="M37D_NEW_NATIVE_URBAN_FABRIC_ART_HOLD.blend"
SCENE="M37D_AUTHOR_OCCUPIED_CITY_ART_HOLD"
GATE="M37D_PUBLIC_GATE_REAL_FLOOR"
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for block in iter(lambda:f.read(1<<20),b""): h.update(block)
    return h.hexdigest()
def isfloor(name):
    return any(t in name for t in ("_REAL_FLOOR","_OCCUPIED_FLOOR",
        "_SHARED_WALK_","_BALCONY","_TREAD_","_CITY_UPPER_OBSERVATION",
        "_ACTUAL_GARDEN_COURT_","_ASSEMBLY_OPERATIONS_SPUR","_ACTUAL_WORK_FLOOR_"))
def group(name):
    if any(k in name for k in ("_HAB1_","_HAB2_","_HAB3_")):return "HABITAT"
    if any(k in name for k in ("_RES1_","_RES2_")):return "RESEARCH"
    if any(k in name for k in ("_FAB1_","_FAB2_","_ACTUAL_WORK_FLOOR_",
                               "_OPEN_SPACE_VEHICLE_","_ASSEMBLY_OPERATIONS")):return "FABRICATION"
    if any(k in name for k in ("_CULT1_","_CULT2_","_CIVIC_L")):return "CULTURE"
    if any(k in name for k in ("_TREAD_","_CITY_UPPER_OBSERVATION")):return "VERTICAL"
    return "PUBLIC"
def graph_of(floors):
    import networkx as nx
    graph=nx.Graph()
    for a in floors:graph.add_node(a["name"])
    overlapping=0;near=0
    for i,a in enumerate(floors):
        pa=a["poly"];xa,ya,ua,va=pa.bounds
        for b in floors[i+1:]:
            if abs(a["z"]-b["z"])>.36:continue
            pb=b["poly"];xb,yb,ub,vb=pb.bounds
            if ua<xb-.04 or ub<xa-.04 or va<yb-.04 or vb<ya-.04:continue
            area=pa.intersection(pb).area
            if area>=.20:
                graph.add_edge(a["name"],b["name"])
                overlapping+=1
            elif pa.distance(pb)<=.04:near+=1
    return graph,overlapping,near
def self_test():
    from shapely.geometry import Polygon
    def p(n,coords,z):return {"name":n,"poly":Polygon(coords),"z":z}
    a=p("A",[(0,0),(4,0),(4,4),(0,4)],0)
    b=p("B",[(3,1),(6,1),(6,3),(3,3)],0)
    c=p("C",[(6,1),(10,1),(10,3),(6,3)],0)
    d=p("D",[(0,0),(4,0),(4,4),(0,4)],3)
    e=p("E",[(2,2),(3,2),(3,3),(2,3)],.5)
    g,o,n=graph_of([a,b,c,d,e])
    assert g.has_edge("A","B") and not g.has_edge("B","C")
    assert not g.has_edge("A","D") and not g.has_edge("A","E")
    assert o==1 and n>=1,(o,n)
    assert isfloor("M37D_HAB1_L1_B3_OCCUPIED_FLOOR")
    assert not isfloor("M37D_HAB1_L1_B3_DOOR_LINTEL")
    print("M37E_NEGATIVE_CONTROL_TESTS_PASS")
def analyze():
    import bpy,networkx as nx
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    from shapely.geometry import Polygon
    pin=json.loads((ROOT/"M37D_MANIFEST.json").read_text(encoding="utf8"))
    source=ROOT/NAME
    assert sha(source)==pin["saved_blend"]["sha256"],"Saved BLEND pin mismatch"
    assert pin["art"]=="HOLD_UNREVIEWED"
    assert pin["formal_331_993"]=="NOT_RUN" and pin["minecraft"]=="FORBIDDEN"
    bpy.ops.wm.open_mainfile(filepath=str(source.resolve()))
    scene=bpy.data.scenes[SCENE]
    assert scene.get("M37D_ART_STATUS")=="UNREVIEWED_HOLD"
    assert scene.get("M37D_MINECRAFT")=="FORBIDDEN"
    meshes=[o for o in scene.objects if o.type=="MESH"]
    assert len(meshes)==1163
    floors=[];invalid=[]
    for o in meshes:
        if not isfloor(o.name):continue
        coords=[o.matrix_world @ v.co for v in o.data.vertices]
        top=max(float(p.z) for p in coords)
        ring=list(dict.fromkeys((round(float(p.x),6),round(float(p.y),6))
                  for p in coords if abs(float(p.z)-top)<.001))
        if len(ring)<3:
            invalid.append((o.name,"top vertices <3"));continue
        poly=Polygon(ring)
        if not poly.is_valid or poly.area<=.01:
            invalid.append((o.name,"invalid polygon"));continue
        floors.append({"name":o.name,"poly":poly,"z":top,"group":group(o.name)})
    # Do not silently omit defective floor shapes and then certify them.
    assert not invalid,invalid[:10]
    assert len(floors)>120,len(floors)
    graph,edges,near=graph_of(floors)
    assert GATE in graph
    reachable=nx.node_connected_component(graph,GATE)
    components=sorted(nx.connected_components(graph),key=len,reverse=True)
    counts=Counter(x["group"] for x in floors)
    bygroup={g:{"floor_proxies":n,"gate_strict_overlap_connected":sum(
             x["group"]==g and x["name"] in reachable for x in floors)}
             for g,n in sorted(counts.items())}
    doors=[o for o in meshes if "_DOOR_LINTEL" in o.name]
    assert len(doors)==pin["spatial_components"]["named_door_openings"]
    door_proofs=[]
    for ob in doors:
        target=ob.name.replace("_DOOR_LINTEL","_OCCUPIED_FLOOR")
        assert target in graph,ob.name
        door_proofs.append({"door_lintel":ob.name,"floor":target,
                            "in_gate_strict_floor_component":target in reachable})
    no_gate_door=[d for d in door_proofs if not d["in_gate_strict_floor_component"]]
    # Single center ray per fixed native camera, real polygon raycast.
    # Not a full FOV or human clearance assessment.
    bvh=[]
    for ob in meshes:
        verts=[tuple(ob.matrix_world@v.co) for v in ob.data.vertices]
        polys=[tuple(p.vertices) for p in ob.data.polygons]
        tree=BVHTree.FromPolygons(verts,polys,all_triangles=False)
        bvh.append((ob.name,tree))
    cams=sorted([o for o in scene.objects if o.type=="CAMERA"
                 and o.name.startswith("M37D_CAM_")],key=lambda o:o.name)
    assert len(cams)==9
    # In non-active scenes matrix_world may be unevaluated identity.
    # These authored cameras are unparented: use actual saved transforms.
    assert all(c.parent is None for c in cams)
    origins={tuple(round(float(v),3) for v in c.location) for c in cams}
    assert len(origins)==9,("collapsed camera origins",origins)
    rays=[]
    for cam in cams:
        pos=cam.location.copy()
        direction=cam.rotation_euler.to_quaternion()@Vector((0,0,-1))
        direction.normalize()
        assert pos.length>10,("unexpected camera origin",cam.name,tuple(pos))
        best=None
        for name,tree in bvh:
            hit,normal,index,distance=tree.ray_cast(pos,direction,120)
            if hit is None or distance is None or distance<1e-5:continue
            if best is None or distance<best[1]:best=(name,float(distance))
        rays.append({"camera":cam.name,
                     "first_hit_polygon":best[0] if best else None,
                     "distance_research_units":round(best[1],3) if best else None})
    # Different elevations can have zero 2D overlap and still be possible
    # with a suitable stair; this is conservative evidence of missing proof.
    report={
      "test":"M37E_INDEPENDENT_NATIVE_FLOOR_OVERLAP_AND_9_CAMERA_CENTER_RAYS",
      "status":"METHOD_AUDIT_ONLY_NO_ART_OR_SAFETY_PASS",
      "source_blend_sha256":sha(source),
      "new_scene_meshes":len(meshes),
      "floor_proxy":{"count":len(floors),
          "strict_xy_overlap_edges_height_delta_le_0_36":edges,
          "excluded_boundary_near_edges":near,
          "connected_components":len(components),
          "largest_component_floors":len(components[0]),
          "gate_anchor":GATE,
          "gate_strict_component_floors":len(reachable),
          "group_counts":bygroup},
      "nominal_door_lintels":{"count":len(doors),
          "door_floor_on_gate_contact_component":len(door_proofs)-len(no_gate_door),
          "door_floors_not_on_gate_contact_component":len(no_gate_door),
          "not_on_gate_component_examples":no_gate_door[:12]},
      "camera_center_rays":rays,
      "method_scope":"Only positive-area top-floor footprint overlap at z difference <=0.36; line-touch excluded. Stricter than possible true connection; no exhaustive walking claim.",
      "safety_limits":{"331_993":"NOT_RUN","G0_S1_G1_G2_G3":"NOT_RUN",
         "headroom":"NOT_RUN","swept_body":"NOT_RUN","stairs":"NOT_RUN",
         "structures":"NOT_CERTIFIED"},
      "city_art":"M37D_ART_REJECT_UNCHANGED","formal_adoption":0,
      "Minecraft_writes":0,"Minecraft_construction":"FORBIDDEN",
      "next_work":"Author one genuinely contiguous cross-district section in Blender directly; retain citywide bulk, no repeated row generation."
    }
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"M37E_NATIVE_FLOOR_CONTACT_AND_EYE_AUDIT.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False),encoding="utf8")
    with (OUT/"M37E_GROUP_FLOOR_CONTACT.csv").open("w",newline="",encoding="utf8") as f:
        w=csv.writer(f);w.writerow(["group","floor_proxies","gate_strict_overlap_connected"])
        for g,d in sorted(bygroup.items()):
            w.writerow([g,d["floor_proxies"],d["gate_strict_overlap_connected"]])
    print("M37E_NATIVE_AUDIT_RESULT",json.dumps({
       "floors":len(floors),"gate_floors":len(reachable),
       "components":len(components),"nominal_doors":len(doors),
       "gate_component_door_floors":len(door_proofs)-len(no_gate_door),
       "camera_rays":rays},ensure_ascii=False),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--self-test",action="store_true")
    p.add_argument("--analyze",action="store_true");a=p.parse_args()
    assert a.self_test or a.analyze
    if a.self_test:self_test()
    if a.analyze:analyze()
