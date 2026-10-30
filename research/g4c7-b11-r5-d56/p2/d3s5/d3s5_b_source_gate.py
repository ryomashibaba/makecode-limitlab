"""D56-P2-D3S5 B: source reservation only. Never claims mesh, life safety or art pass."""
import json, copy, math, hashlib
from pathlib import Path
P=Path(__file__).resolve().parent
SRC=P/"D3S5_B_SPATIAL_RESERVATION.json"
d=json.loads(SRC.read_text(encoding="utf-8"))

def require(cond,message):
    if not cond: raise ValueError(message)

def crossing(a,b):
    p,q=a["from"],a["to"];s,t=b["from"],b["to"]
    u=[q[i]-p[i] for i in range(2)]
    v=[t[i]-s[i] for i in range(2)]
    determinant=u[0]*v[1]-u[1]*v[0]
    require(abs(determinant)>1e-6,"parallel public axes")
    offset=[s[i]-p[i] for i in range(2)]
    f=(offset[0]*v[1]-offset[1]*v[0])/determinant
    g=(offset[0]*u[1]-offset[1]*u[0])/determinant
    require(0<f<1 and 0<g<1,"axes do not intersect in their segments")
    delta=abs((p[2]+f*(q[2]-p[2]))-(s[2]+g*(t[2]-s[2])))
    angle=math.degrees(math.acos(min(1.,max(-1.,abs(u[0]*v[0]+u[1]*v[1])/(math.hypot(*u)*math.hypot(*v))))))
    require(angle>25 and delta>8,"not meaningful 3D axis separation")
    return {"x":round(p[0]+f*u[0],3),"y":round(p[1]+f*u[1],3),
            "z_gap":round(delta,3),"smaller_angle_deg":round(angle,3)}

def check(s):
    require(s["status"]=="PRE3D RESERVATION ONLY; NOT ACTUAL GLB; NOT ART PASS","false true3d claim")
    require(s["actual_roof_floor_triangles"]=="NOT BUILT" and s["actual_public_room_meshes"]=="NOT BUILT","false physical pass")
    require(s["formal_331_body_993_foot"]=="NOT RUN" and s["formal_G0_S1_G1_G2_G3"]=="NOT RUN","false formal pass")
    require(not s["minecraft_world_write"] and not s["city_integration"],"world boundary violated")
    districts=s["districts"]
    for key in ("M","R","L"):
        lower,upper=districts[key]["bounds"]; eye=districts[key]["eye"]
        require(all(lower[i]<eye[i]<upper[i] for i in range(3)),"eye outside "+key)
    overlaps=[]
    for pair in (["M","R"],["R","L"]):
        require(pair in [s1["pair"] for s1 in s["unbuilt_shared_thickness_reservations"]],"shared pair missing")
        left,right=[districts[key]["bounds"] for key in pair]
        dims=[round(min(left[1][i],right[1][i])-max(left[0][i],right[0][i]),3) for i in range(3)]
        require(min(dims)>1,"shared XYZ reservation collapsed")
        overlaps.append({"pair":"/".join(pair),"reserved_overlap":dims,"physical_triangle_support":"NOT BUILT"})
    require(len(s["civic_axes"])==2,"not two axes")
    cross=crossing(*s["civic_axes"])
    edges=s["public_route_edges_undirected"];adj={}
    for a,b in edges:adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a)
    def reachable(a,b):
        seen={a};queue=[a]
        while queue:
            node=queue.pop()
            if node==b:return True
            for nbr in adj.get(node,()):
                if nbr not in seen:seen.add(nbr);queue.append(nbr)
        return False
    for a,b in [("A_WEST","A_EAST"),("B_NORTH","B_SOUTH"),("A_WEST","B_SOUTH"),("LIVING_LOBBY","LIVING_PRIVATE")]:
        require(reachable(a,b),"disconnected "+a+"/"+b)
    for a,b in edges:
        require(not ((a in s["public_nodes"] and b in s["private_nodes"]) or
                     (b in s["public_nodes"] and a in s["private_nodes"])),"privacy bypass")
    vt=s["vertical_transfer"]["node"]
    require(set(adj.get(vt,()))>={"INTERCHANGE_UPPER","INTERCHANGE_LOWER"},"no reserved vertical interchange")
    require(s["vertical_transfer"]["unverified"] is True,"fake vertical transfer build")
    return {"overlap_reservations":overlaps,"intersecting_axes_not_mesh":cross,"graph_nodes":len(adj),"graph_edges":len(edges)}

def main():
    success=check(d)
    actions={
      "parallel axes":lambda v:v["civic_axes"].__setitem__(1,dict(v["civic_axes"][1],to=[v["civic_axes"][1]["from"][0]+290,v["civic_axes"][1]["from"][1]+200,24])),
      "remove shared thickness":lambda v:(v["districts"]["R"].__setitem__("bounds",[[-25,8,140],[105,82,182]]),v["districts"]["R"].__setitem__("eye",[15,45,150])),
      "break vertical interchange":lambda v:v.__setitem__("public_route_edges_undirected",[e for e in v["public_route_edges_undirected"] if "VERTICAL_TRANSFER" not in e]),
      "public directly opens into private":lambda v:v["public_route_edges_undirected"].append(["A_WEST","LIVING_PRIVATE"]),
      "false actual public-room mesh":lambda v:v.__setitem__("actual_public_room_meshes","PASS"),
      "eye outside living room":lambda v:v["districts"]["L"].__setitem__("eye",[400,108,76]),
      "false formal human QA":lambda v:v.__setitem__("formal_331_body_993_foot","PASS")}
    controls=[]
    for name,mutator in actions.items():
        corrupted=copy.deepcopy(d);mutator(corrupted)
        try:check(corrupted);controls.append({"mutation":name,"detected":False})
        except ValueError as exc:controls.append({"mutation":name,"detected":True,"reason":str(exc)})
    require(all(v["detected"] for v in controls),"one or more adversarial controls escaped")
    result={"study":d["study"],"classification":"SOURCE PREFLIGHT ONLY; NOT ACTUAL MESH OR ART PASS",
            "source_sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
            **success,"detected":len(controls),"total_negative_controls":len(controls),
            "negative_controls":controls,"formal_331_993":"NOT RUN","formal_G0_S1_G1_G2_G3":"NOT RUN"}
    (P/"D3S5_B_PRE3D_AUDIT.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
