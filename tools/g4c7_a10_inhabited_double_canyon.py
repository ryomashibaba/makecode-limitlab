"""G4-C7 A10 — inhabited asymmetrical shell-canyon, independent ART-FIRST study.

Construct two genuinely hollow, heavy, curved multi-level public bodies inside A9
rather than decorative roof fins or tinted boxes. Operates only on an A9 GLB;
never accesses Minecraft, any world, USED latch, or historical evidence.
Coordinate system: GLB Y-up, *conceptual units*, not Minecraft block proof.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import trimesh
from g4c7_a7_portal_route import add_deck, color, STONE, DARK
from g4c7_a8_fullbody_clearance import route_sweep, triangles_by_mesh
from g4c7_a9_sculptural_route import route_a9, approach_centerline
from g4c7_a7_fourview import render, CAMERAS, TARGET, WIDTH, HEIGHT, SCALE
from PIL import Image, ImageDraw

WEST = "A10_WEST_INHABITED_FAULT_SHELL"
EAST = "A10_EAST_INHABITED_TIDAL_SHELL"
BASE_EXPECTED = 590
INTERIOR_COLOR=(168,199,195,255)
LIGHT_SHELL=(218,229,218,255)
BLUE_GLASS=(67,159,177,255)
BRONZE=(182,126,76,255)
BODY_WIDTH_HALF=0.65
FLOOR_STEP_COUNT=3

def add(scene,mesh,name,rgba=None):
    if rgba is not None:
        mesh=color(mesh,rgba)
    if not mesh.is_watertight or not mesh.is_volume:
        raise AssertionError("A10 volume is not a valid closed solid: "+name)
    scene.add_geometry(mesh,geom_name=name,node_name=name)
    return mesh

def gallery_path(which,n=96):
    pts=[]
    for i in range(n+1):
        u=i/n
        if which=="W":
            # Dramatic, elevated thick inhabited fault bank rising toward arch crown.
            x=-28+6.7*math.sin(2*math.pi*u+0.35)
            z=-39+78*u
            y=31+7*u+10.5*math.sin(math.pi*u)**2
            width=18+5*math.sin(math.pi*u)**2
            depth=13+2*math.sin(math.pi*u)**2
        else:
            # Opposing taller inner-city escarpment; nonrepeating curvature and ascent.
            x=25.5+7.0*math.sin(2*math.pi*u+2.0)
            z=-34+70*u
            y=35+5*u+9.0*math.sin(math.pi*u)**2
            width=16.8+5.5*math.sin(math.pi*u)**2
            depth=13.5+2*math.sin(math.pi*u)**2
        pts.append((x,y,z,width,depth))
    return pts

def swept_prism(rows, inset_width=0., inset_roof=0., inset_floor=0.,
                extend_ends=0.):
    """Swept CLOSED solid prism with horizontal cross section, true side walls."""
    verts=[]
    for i,(x,top,z,w,d) in enumerate(rows):
        prev=np.array(rows[max(0,i-1)][:3],float)
        nxt=np.array(rows[min(len(rows)-1,i+1)][:3],float)
        tangent=nxt-prev
        horizontal=np.array([-tangent[2],0.,tangent[0]])
        horizontal/=np.linalg.norm(horizontal)
        center=np.array([x,top,z],float)
        if i==0 and extend_ends:
            c=rows[1]
            p=np.array(rows[0][:3],float)-np.array(c[:3],float)
            center+=p/max(np.linalg.norm(p),1e-9)*extend_ends
        elif i==len(rows)-1 and extend_ends:
            p=np.array(rows[-1][:3],float)-np.array(rows[-2][:3],float)
            center+=p/max(np.linalg.norm(p),1e-9)*extend_ends
        half=(w-inset_width)/2
        roof=top-inset_roof
        floor=top-d+inset_floor
        if half<3.5 or roof-floor<2.5:
            raise AssertionError("Degenerate or non-usable gallery void profile")
        for horizontal_side,yy in ((-half,roof),(half,roof),
                                   (half,floor),(-half,floor)):
            p=center+horizontal_side*horizontal+np.array([0,yy-top,0])
            verts.append(p)
    faces=[]
    for i in range(len(rows)-1):
        a=i*4
        b=(i+1)*4
        for j in range(4):
            k=(j+1)%4
            faces.extend(((a+j,b+j,b+k),(a+j,b+k,a+k)))
    faces.extend(((0,2,1),(0,3,2)))
    e=4*(len(rows)-1)
    faces.extend(((e,e+1,e+2),(e,e+2,e+3)))
    m=trimesh.Trimesh(vertices=np.asarray(verts),faces=np.asarray(faces),process=True)
    m.fix_normals()
    assert m.is_volume and m.is_watertight
    return m

def real_hollow_gallery(rows,label,window_side):
    outer=swept_prism(rows)
    bore=swept_prism(rows,inset_width=4.4,inset_roof=2.1,
                     inset_floor=2.0,extend_ends=2.7)
    shell=trimesh.boolean.difference([outer,bore],engine="manifold")
    if shell is None or not shell.is_watertight or not shell.is_volume:
        raise AssertionError("Unable to create real traversable conceptual hollow: "+label)
    removed_void=float(outer.volume-shell.volume)
    if removed_void/outer.volume<.23:
        raise AssertionError("Shell mostly filled, missing true inhabitable void")
    windows=[]
    # Two actual side apertures for daylight/visibility in each long occupied band.
    for index,u in enumerate((.29,.72)):
        i=round(u*(len(rows)-1))
        x,y,z,w,depth=rows[i]
        before=np.array(rows[i-1][:3],float)
        after=np.array(rows[i+1][:3],float)
        tangent=after-before
        normal=np.array([-tangent[2],0,tangent[0]],float)
        normal/=np.linalg.norm(normal)
        center=np.array([x,y-depth*.53,z],float)+normal*window_side*(w/2-.45)
        cutter=trimesh.creation.box(extents=(6.4,3.6,9.0))
        cutter.apply_translation(center)
        intersection=trimesh.boolean.intersection([shell,cutter],engine="manifold")
        volume=float(intersection.volume) if intersection is not None else 0.0
        if volume<1.0:
            raise AssertionError("Real side-window cutter missed shell: "+label)
        candidate=trimesh.boolean.difference([shell,cutter],engine="manifold")
        if candidate is None or not candidate.is_watertight or not candidate.is_volume:
            raise AssertionError("Window punch invalid; no fake black painted glass")
        shell=candidate
        windows.append({"station":u,"removed_volume":round(volume,2),
                        "center":[round(float(v),2) for v in center]})
    shell.fix_normals()
    return shell,{"outer_volume":round(float(outer.volume),2),
                  "hollow_volume":round(float(shell.volume),2),
                  "void_fraction_before_window":round(removed_void/outer.volume,4),
                  "opening_ends":"Real loft boolean channels open at both ends",
                  "cut_windows":windows,
                  "occupied_space":"GEOMETRIC CAVITY ONLY; NOT ROUTE TESTED"}

def tapered_ground_support(start,end,bottom_r=2.5,top_r=1.35,sides=12):
    a=np.array(start,float);b=np.array(end,float)
    direction=b-a
    direction/=np.linalg.norm(direction)
    tangent=np.array([1.,0.,0.])
    if abs(direction@tangent)>.9:tangent=np.array([0.,0.,1.])
    side=np.cross(direction,tangent);side/=np.linalg.norm(side)
    tangent=np.cross(side,direction);tangent/=np.linalg.norm(tangent)
    verts=[]
    for p,r in ((a,bottom_r),(b,top_r)):
        for k in range(sides):
            theta=2*math.pi*k/sides
            verts.append(p+r*(math.cos(theta)*side+math.sin(theta)*tangent))
    faces=[]
    for k in range(sides):
        n=(k+1)%sides
        faces.extend(((k,n,sides+k),(n,sides+n,sides+k)))
    for k in range(1,sides-1):
        faces.append((0,k+1,k))
        faces.append((sides,sides+k,sides+k+1))
    m=trimesh.Trimesh(vertices=verts,faces=faces,process=True)
    m.fix_normals()
    return m

def add_occupied_shell(scene,which,label):
    rows=gallery_path(which)
    # For a northbound X/Z path, cross normal points approximately WEST.
    # Facing the central canyon: EAST of the west bank, WEST of east bank.
    window_side=-1 if which=="W" else 1
    shell,facts=real_hollow_gallery(rows,label,window_side)
    add(scene,shell,label,LIGHT_SHELL if which=="W" else INTERIOR_COLOR)
    # A thin inset interior floor is actually geometry, but is NOT a proof
    # of reaching it from ground or of step-free egress.
    floor=[]
    for x,top,z,w,depth in rows:
        floor.append((x,top-depth+2.8,z))
    deck=add_deck(scene,label+"_INSET_OCCUPIED_FLOOR",floor,
                  width=rows[len(rows)//2][3]-6.0,depth=.95,rgba=STONE)
    if not deck.is_volume or not deck.is_watertight:
        raise AssertionError("Interior floor broken")
    # Three thick raking ground supports per shell, not unsupported levitation.
    supports=[]
    for k,u in enumerate((.12,.49,.87)):
        idx=round(u*(len(rows)-1))
        x,y,z,w,depth=rows[idx]
        floor_y=y-depth
        p=[x, floor_y+.45,z]
        ground=[x+(-4 if which=="W" else 4),.1,z+2.0*(-1 if k%2 else 1)]
        member=tapered_ground_support(ground,p,2.9,1.6)
        add(scene,member,label+"_GROUNDED_FAN_PIER_"+str(k),DARK)
        supports.append({"ground":ground,"upper":p})
    facts["supports"]=supports
    facts["approximate_interior_floor_area"] = round(
        sum(np.linalg.norm(np.asarray(rows[i][:3])-np.asarray(rows[i-1][:3]))
            for i in range(1,len(rows)))*(rows[len(rows)//2][3]-6),1)
    facts["cross_section_depth_range"]=[min(x[4] for x in rows),max(x[4] for x in rows)]
    facts["bounds"]=np.asarray(shell.bounds).round(3).tolist()
    return facts

def cross_void_decks(scene):
    summary=[]
    # Two interlocked diagonal, broad, deep sky-bridges in one spatial system.
    # Ends lie by the banks; no claim of actually walkable attachment.
    for name,z0,y0,shift in (
      ("A10_LOW_CANYON_DIAGONAL",-15.,28.5,-5.0),
      ("A10_UPPER_CANYON_DIAGONAL",18.,36.0,5.0)):
        pts=[]
        for i in range(57):
            u=i/56
            x=-23+46*u
            z=z0+shift*math.sin(math.pi*u)+2.5*math.sin(2*math.pi*u)
            y=y0+3.2*math.sin(math.pi*u)**2+1.4*u
            pts.append((x,y,z))
        mesh=add_deck(scene,name,pts,width=10.5,depth=4.0,rgba=BRONZE)
        if not mesh.is_volume:raise AssertionError("No real occupied bridge volume")
        summary.append({"name":name,"deck_mesh_volume":round(mesh.volume,1),
                        "physical_form":"Thick curved inhabited bridging volume",
                        "ends_reach_shell":"NOT VERIFIED"})
    return summary

def preserve_and_build(original):
    result=trimesh.Scene()
    # Rebuild the inherited civic approach with a physically overlapping last
    # landing. The original GLB truncates at the ramp endpoint (78,1,70);
    # after float32 GLB round-trip one *edge* support ray missed it. This is
    # real added walkable-width floor geometry, not a QA tolerance change.
    for name in original.graph.nodes_geometry:
        if name=="A7_APPROACH_CURVED_DECK":
            continue
        transform,key=original.graph[name]
        result.add_geometry(original.geometry[key].copy(),
                            geom_name=name,node_name=name,transform=np.asarray(transform))
    approach=approach_centerline()
    approach.extend([(78.,1.,70.8),(78.,1.,72.2)])
    landing=add_deck(result,"A7_APPROACH_CURVED_DECK",approach,
                     width=10.0,depth=1.12,rgba=STONE)
    assert landing.is_watertight and landing.is_volume
    facts={"civic_approach_endpoint_repaired":True,
           "new_end_z":72.2,
           "original_end_z":70.0,
           "qa_tolerances_unchanged":True}
    facts["west"]=add_occupied_shell(result,"W",WEST)
    facts["east"]=add_occupied_shell(result,"E",EAST)
    facts["cross_void_decks"]=cross_void_decks(result)
    return result,facts

def four_view(old,new,out):
    out.mkdir(parents=True,exist_ok=True)
    records={}
    for name,eye in CAMERAS.items():
        before,ta=render(old,name)
        after,tb=render(new,name)
        panel=Image.new("RGB",(2*WIDTH,HEIGHT+38),(242,246,246))
        panel.paste(before,(0,38));panel.paste(after,(WIDTH,38))
        pen=ImageDraw.Draw(panel)
        pen.text((18,10),"A9 INPUT — ART HOLD",fill=(20,24,27))
        pen.text((WIDTH+18,10),"A10 INHABITED DOUBLE CANYON — ART HOLD",fill=(20,24,27))
        panel.save(out/(name+"_a9_a10.png"),optimize=True)
        records[name]={"camera":list(eye),"scale":SCALE,
                       "a9_triangles":ta,"a10_triangles":tb}
    (out/"view_provenance.json").write_text(json.dumps({
      "origin":"Same actual GLB meshes, not ImageGen",
      "renderer":"Pillow polygon rasterizer, not Blender EEVEE or Minecraft",
      "fixed_target":TARGET.tolist(),"cameras":records},indent=2)+"\n")

def generate(source,out):
    out.mkdir(parents=True,exist_ok=True)
    baseline=trimesh.load(source,force="scene")
    assert len(baseline.graph.nodes_geometry)==BASE_EXPECTED,"Wrong A9 exact baseline"
    result,shapes=preserve_and_build(baseline)
    actual=out/"a10_inhabited_double_shell_canyon.glb"
    actual.write_bytes(result.export(file_type="glb"))
    (out/"a10_inhabited_double_shell_canyon.obj").write_text(
        result.export(file_type="obj"),encoding="utf8")
    fresh=trimesh.load(actual,force="scene")
    assert len(fresh.graph.nodes_geometry)==len(result.graph.nodes_geometry)
    assert np.allclose(fresh.bounds,baseline.bounds,atol=.1),"Changed district external envelope"
    for label in (WEST,EAST):
        if label not in fresh.graph.nodes_geometry:raise AssertionError("No inhabited shell")
    route=route_a9()
    before=route_sweep(baseline,route)
    after=route_sweep(fresh,route)
    # Do not weaken body envelope, foot widths or sampling to manufacture PASS.
    assert before["body_envelope"]==after["body_envelope"]
    assert before["route_samples"]==after["route_samples"]==331
    assert before["foot_support_samples"]==after["foot_support_samples"]==993
    assert before["negative_intentional_blocker_detected"]
    assert after["negative_intentional_blocker_detected"]
    four_view(baseline,fresh,out/"fourview")
    resultqa={
        "source_a9_meshes":len(baseline.graph.nodes_geometry),
        "a10_result_meshes":len(fresh.graph.nodes_geometry),
        "new_form":shapes,
        "quantified_canyon_change":{
          "hollow_shells":2,"real_side_openings":4,
          "ground_tied_supports":6,"thick_cross_canyon_volumes":2,
          "role":"CULTURE DISTRICT ARCHITECTURAL STUDY; NOT MINECRAFT PROGRAM"},
        "a9_clearance":{
          "sample_count":before["route_samples"],
          "surface_collision_locations":before["body_surface_intersection_sample_count"],
          "unsupported_foot_samples":before["unsupported_foot_samples"]},
        "a10_clearance":after,
        "collision_change":after["body_surface_intersection_sample_count"]-
          before["body_surface_intersection_sample_count"],
        "support_change":after["unsupported_foot_samples"]-
          before["unsupported_foot_samples"],
        "full_interior_paths":"NOT VERIFIED",
        "cross_bridge_access":"NOT VERIFIED",
        "structural_loads":"NOT VERIFIED",
        "art_status":"HOLD","construction":"PROHIBITED",
        "city_integration":"PROHIBITED","minecraft_walk":"NOT TESTED",
        "private_evidence":"UNTOUCHED"}
    (out/"a10_art_function_qa.json").write_text(
      json.dumps(resultqa,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    return resultqa

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
        "artifacts/g4c7-a9/a9_orbital_commons_sculpted_route_study.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a10"))
    a=p.parse_args()
    q=generate(a.input,a.out)
    print(json.dumps({
      "input_meshes":q["source_a9_meshes"],"output_meshes":q["a10_result_meshes"],
      "a9_collisions":q["a9_clearance"]["surface_collision_locations"],
      "a10_collisions":q["a10_clearance"]["body_surface_intersection_sample_count"],
      "a10_unsupported":q["a10_clearance"]["unsupported_foot_samples"],
      "hollow_shells":2,"interior_gallery_area_approx":(
        q["new_form"]["west"]["approximate_interior_floor_area"]+
        q["new_form"]["east"]["approximate_interior_floor_area"]),
      "art":"HOLD"},indent=2))
