"""G4-C7 A7: real mesh portal, supported pedestrian route, sky-slot roof.
Pure offline ART HOLD study. Coordinates are GLB Y-up. No Minecraft I/O.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import trimesh
from g4c7_a6_open_sky_study import generate as generate_a6, color, make_loft, gallery_rows, cylinder, STONE, DARK

PORTAL_CENTER_Z = 20.0
FLOOR_Y = 13.0 - 10.0 * 20.0 / 49.0
PORTAL_BOUNDS = ((36.0, 8.72, 16.6), (71.0, 13.55, 23.4))
CLEAR_BOUNDS = ((39.2, FLOOR_Y + 0.13, 18.55),
                (65.5, FLOOR_Y + 3.25, 21.45))
MAIN_PREFIX = "SOUTH "
ROUTE_MESH_NAMES = (
    "Public ground, continuous E-W axis",
    "Street to common ramp",
    "Continuous elliptical public promenade",
    "A7_APPROACH_",
    "A7_PORTAL_DECK",
)

def world_mesh(scene, name):
    transform, key = scene.graph[name]
    mesh = scene.geometry[key].copy()
    mesh.apply_transform(transform)
    return mesh

def box_bounds(bounds):
    low, high = np.asarray(bounds[0],float), np.asarray(bounds[1],float)
    mesh = trimesh.creation.box(extents=high-low)
    mesh.apply_translation((low+high)/2)
    return mesh

def touching_bounds(a, b, margin=1e-7):
    return bool(np.all(a[0] < b[1]-margin) and np.all(a[1] > b[0]+margin))

def boolean_volume(a, b):
    if not touching_bounds(a.bounds,b.bounds):
        return 0.0
    inter=trimesh.boolean.intersection([a,b],engine="manifold")
    return float(inter.volume) if inter is not None else 0.0

def cut_main_portal(original, output):
    """Test solid-solid overlap before cutting, then actual manifold closed-mesh cuts."""
    cutter = box_bounds(PORTAL_BOUNDS)
    corridor = box_bounds(CLEAR_BOUNDS)
    cut_names=[]
    measures=[]
    for name in original.graph.nodes_geometry:
        if not name.startswith(MAIN_PREFIX):
            continue
        old=world_mesh(original,name)
        if not touching_bounds(old.bounds,cutter.bounds):
            continue
        if not old.is_watertight:
            raise AssertionError("Solid boolean input is not watertight: "+name)
        old.fix_normals()
        removed=boolean_volume(old,cutter)
        if removed < 0.01:
            continue
        remaining=trimesh.boolean.difference([old,cutter],engine="manifold")
        if remaining is None or remaining.is_empty or not remaining.is_watertight:
            raise AssertionError("Portal cut did not leave a watertight mesh: "+name)
        before=boolean_volume(old,corridor)
        after=boolean_volume(remaining,corridor)
        measures.append({"name":name,"cut_volume":round(removed,4),
                         "corridor_intersection_before":round(before,5),
                         "corridor_intersection_after":round(after,5),
                         "mesh_watertight":bool(remaining.is_watertight)})
        cut_names.append(name)
    if not any("inner load shell" in n for n in cut_names):
        raise AssertionError("Main arch INNER shell was not physically cut")
    if not any("outer load shell" in n for n in cut_names):
        raise AssertionError("Main arch OUTER shell was not physically cut")
    cutset=set(cut_names)
    for name in original.graph.nodes_geometry:
        if name in cutset:
            old=world_mesh(original,name)
            remaining=trimesh.boolean.difference([old,cutter],engine="manifold")
            output.add_geometry(remaining, geom_name=name+"_A7_PORTAL",node_name=name+"_A7_PORTAL")
        else:
            mat,key=original.graph[name]
            output.add_geometry(original.geometry[key].copy(),
                                geom_name=name,node_name=name,transform=np.array(mat))
    assert any(m["corridor_intersection_before"] > 0.1 for m in measures), "No baseline route obstruction detected"
    assert all(m["corridor_intersection_after"] < 0.0001 for m in measures), "Residual shell blockage"
    return measures,cut_names

def add_loft_strip(scene,name,rows,left_edge=True):
    newrows=[]
    for z,c,left,right,bot,top in rows:
        if left_edge:
            a,b=left,left+2.9
        else:
            a,b=right-2.9,right
        newrows.append((z,c,a,b,bot,top))
    scene.add_geometry(make_loft(newrows,STONE),geom_name=name,node_name=name)

def add_deck(scene,name,points,width,depth=1.3,rgba=STONE):
    """Real 3D deck loft, horizontal cross sections normal to XZ path."""
    vertices=[]
    for i,(x,y,z) in enumerate(points):
        prev=np.array(points[max(0,i-1)],float)
        nex=np.array(points[min(len(points)-1,i+1)],float)
        d=nex-prev
        norm=np.array([-d[2],0,d[0]],float)
        norm=norm/np.linalg.norm(norm)*(width/2)
        p=np.array([x,y,z],float)
        # Perimeter order: left-low, right-low, right-high, left-high.
        for side,h in ((-1,-depth),(1,-depth),(1,0),(-1,0)):
            vertices.append((p+norm*side+np.array([0,h,0])).tolist())
    faces=[]
    for i in range(len(points)-1):
        a,b=4*i,4*(i+1)
        for j in range(4):
            u,v=a+j,a+(j+1)%4
            U,V=b+j,b+(j+1)%4
            faces.extend(((u,U,v),(v,U,V)))
    faces.extend(((0,2,1),(0,3,2)))
    q=4*(len(points)-1)
    faces.extend(((q,q+1,q+2),(q,q+2,q+3)))
    mesh=trimesh.Trimesh(vertices=vertices,faces=faces,process=True)
    mesh.fix_normals()
    scene.add_geometry(color(mesh,rgba),geom_name=name,node_name=name)
    return mesh

def modified_scene(a6):
    """A7 output built from A6 unchanged except cut shells and two replaced roofs."""
    output=trimesh.Scene()
    measures,cut_names=cut_main_portal(a6,output)
    # Remove only the two outdated roof meshes via a node-preserving rebuild.
    roofs={n for n in output.graph.nodes_geometry
           if n.startswith("A6_CURVED_SKY_") and n.endswith("_ROOF")}
    assert len(roofs)==2
    trimmed=trimesh.Scene()
    for n in output.graph.nodes_geometry:
        if n in roofs: continue
        mat,key=output.graph[n]
        trimmed.add_geometry(output.geometry[key].copy(),geom_name=n,node_name=n,
                             transform=np.array(mat))
    for sign,label in ((-1,"WEST"),(1,"EAST")):
        rows=gallery_rows(sign,"ROOF")
        add_loft_strip(trimmed,"A7_SKY_SLOT_"+label+"_LEFT",rows,True)
        add_loft_strip(trimmed,"A7_SKY_SLOT_"+label+"_RIGHT",rows,False)
    # At-grade link from the existing E-W public axis to the pre-existing rising ramp.
    # Winding walkway, not another large rectilinear urban building.
    approach=[(78.0-math.sin(math.pi*i/48)*1.8,1.0,70*i/48)
              for i in range(49)]
    add_deck(trimmed,"A7_APPROACH_CURVED_DECK",approach,10.0,1.12)
    # Existing promenade center at (63.956..., FLOOR_Y, +20).
    bridge=[(x,FLOOR_Y,PORTAL_CENTER_Z) for x in np.linspace(38,67,30)]
    add_deck(trimmed,"A7_PORTAL_DECK",bridge,5.0,1.3)
    # Four real ground-anchored columns at the two ends, outside center passage.
    for i,x in enumerate((39.5,66.5)):
        for j,z in enumerate((17.75,22.25)):
            trimmed.add_geometry(cylinder([x,0.2,z],[x,FLOOR_Y-1.05,z],.52,DARK),
                geom_name="A7_DECK_COLUMN_%s_%s"%(i,j),
                node_name="A7_DECK_COLUMN_%s_%s"%(i,j))
    return trimmed,measures,sorted(roofs)

def triangulated_support(scene):
    triangles=[]
    for name in scene.graph.nodes_geometry:
        if not any(name.startswith(prefix) for prefix in ROUTE_MESH_NAMES):
            continue
        mesh=world_mesh(scene,name)
        tri=mesh.triangles
        # Only upward-facing triangles can support feet.
        norms=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
        ok=norms[:,1] > 0.005
        triangles.extend(tri[ok])
    if not triangles:
        raise AssertionError("No mesh geometry for route support")
    return np.asarray(triangles)

def support_gap(triangles,p):
    """Vertical ray/triangle barycentric check, no cached analytic-floor shortcut."""
    x,y,z=p
    xx=triangles[:,:,0]
    zz=triangles[:,:,2]
    # Barycentric coordinates on horizontal XZ projection.
    ax,bx,cx=xx[:,0],xx[:,1],xx[:,2]
    az,bz,cz=zz[:,0],zz[:,1],zz[:,2]
    den=(bz-cz)*(ax-cx)+(cx-bx)*(az-cz)
    good=np.abs(den)>1e-9
    s=np.zeros(len(triangles));t=np.zeros(len(triangles))
    s[good]=((bz[good]-cz[good])*(x-cx[good])+(cx[good]-bx[good])*(z-cz[good]))/den[good]
    t[good]=((cz[good]-az[good])*(x-cx[good])+(ax[good]-cx[good])*(z-cz[good]))/den[good]
    inside=good&(s>=-1e-7)&(t>=-1e-7)&((s+t)<=1.0000001)
    if not np.any(inside):
        return None
    height=(s*triangles[:,0,1]+t*triangles[:,1,1]+
            (1-s-t)*triangles[:,2,1])
    below=height[inside]
    below=below[below<=y+0.09]
    if len(below)==0: return None
    return float(y-np.max(below))

def sample_route():
    route=[]
    route.extend(("GROUND_APPROACH",(78.0-math.sin(math.pi*u)*1.8,1.0,70*u))
                 for u in np.linspace(0,1,81))
    route.extend(("EXISTING_RAMP",(78-26*u,1+6.1*u,70-40*u))
                 for u in np.linspace(0,1,81))
    # End of ramp is inside width-9 walkway and width-8 ellipse.
    t0=math.asin(-30/49)
    t1=math.asin(-20/49)
    route.extend(("ELLIPTICAL_LOOP",(70*math.cos(t),13+10*math.sin(t),-49*math.sin(t)))
                 for t in np.linspace(t0,t1,45))
    route.extend(("A7_PORTAL",(x,FLOOR_Y,20.0))
                 for x in np.linspace(64,39,101))
    return route

def verify_route(scene):
    tris=triangulated_support(scene)
    route=sample_route()
    worst={}
    unsupported=[]
    for kind,pt in route:
        gap=support_gap(tris,pt)
        if gap is None or gap < -0.09 or gap > 0.31:
            unsupported.append([kind,[round(float(v),3) for v in pt],gap])
        elif kind not in worst or gap>worst[kind]:
            worst[kind]=gap
    # Specifically demand a negative control: removing the A7 bridge loses support
    # at the interior exit; do not allow shell surface to count as pedestrian deck.
    # Build a real mesh-derived support set excluding A7.
    bridge_sources=trimesh.Scene()
    for name in scene.graph.nodes_geometry:
        if name.startswith("A7_PORTAL_DECK"):continue
        if any(name.startswith(prefix) for prefix in ROUTE_MESH_NAMES):
            m,k=scene.graph[name]
            bridge_sources.add_geometry(scene.geometry[k].copy(),
               geom_name=name,node_name=name,transform=np.array(m))
    absent=support_gap(triangulated_support(bridge_sources),(39.5,FLOOR_Y,20))
    assert absent is None or absent>0.31, "Negative control: portal bridge removal did not break support"
    return {"sample_count":len(route),"unsupported_count":len(unsupported),
            "unsupported_examples":unsupported[:12],"worst_supported_gap":worst,
            "positive_supported_route":len(unsupported)==0,
            "negative_missing_bridge_fails":True,
            "two_way_geometric_samples":True}

def generate(input_glb,out):
    out.mkdir(parents=True,exist_ok=True)
    a6out=out/"source_a6"
    generate_a6(input_glb,a6out)
    a6=trimesh.load(a6out/"a6_orbital_commons_study.glb",force="scene")
    result, cuts, roofs=modified_scene(a6)
    # A5/A6 never overwritten.
    glb=out/"a7_orbital_commons_portal_study.glb"
    glb.write_bytes(result.export(file_type="glb"))
    (out/"a7_orbital_commons_portal_study.obj").write_text(
        result.export(file_type="obj"),encoding="utf8")
    route=verify_route(result)
    opened=bool(cuts and route["positive_supported_route"])
    qa={"a6_meshes":len(a6.graph.nodes_geometry),
        "a7_meshes":len(result.graph.nodes_geometry),
        "portal_cut":cuts,"removed_full_sky_roofs":roofs,
        "opening_clearance_xyz":{"width_z":6.8,"height_y":13.55-8.72,
                                 "corridor_width_z":2.9,
                                 "corridor_height_y":3.12},
        "walkway_route":route,
        "main_arch_opening_confirmed":opened,
        "art_status":"HOLD","construction":"PROHIBITED",
        "in_game_walking":"NOT TESTED",
        "world_modified":False}
    (out/"a7_geometry_route_qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n")
    assert opened, "A7 route or physical penetration is not verified"
    reread=trimesh.load(glb,force="scene")
    assert len(reread.graph.nodes_geometry)==len(result.graph.nodes_geometry)
    assert np.allclose(reread.bounds,a6.bounds,atol=.15),(reread.bounds,a6.bounds)
    return qa

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path("artifacts/g4c7-a5/a5_orbital_commons.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a7"))
    args=p.parse_args()
    print(json.dumps(generate(args.input,args.out),ensure_ascii=False,indent=2))
