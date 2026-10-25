"""G4-C7 A13: two honest architectural integration hypotheses, actual GLB.

A = preserve inherited monumental outer arch and add continuous folded civic span.
B = reinterpret the historic outer arch as subordinate (do not copy two outer
shells) and add four *conceptual* raking links. Both derived independently from
exact committed A12 GLB; neither overwrites it or touches Minecraft.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
import trimesh
from PIL import Image,ImageDraw
from g4c7_a7_fourview import CAMERAS,TARGET,SCALE,WIDTH,HEIGHT,render
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9

INPUT_COUNT=619
REMOVED_OUTER={
    "NORTH outer load shell",
    "SOUTH outer load shell_A7_PORTAL_A9_FLARED",
}
REMOVED_INNER={
    "NORTH inner load shell",
    "SOUTH inner load shell_A7_PORTAL"
}
BRACE_COLOR=(191,196,181,255)
FOLD_COLOR=(225,224,203,255)

def valid(mesh,label):
    mesh.fix_normals()
    assert mesh.is_watertight and mesh.is_volume and mesh.volume>100,(label,mesh.volume)
    return mesh

def paint(mesh,rgba):
    mesh.visual=trimesh.visual.ColorVisuals(
        mesh,vertex_colors=np.tile(np.asarray(rgba,dtype=np.uint8),
                                  (len(mesh.vertices),1)))
    return mesh

def continuous_megafold():
    """One watertight elevated transverse fold with nonrepetitive wave + mass."""
    n=151
    verts=[]
    for i in range(n):
        u=i/(n-1)
        x=-56+112*u
        z=-22+12*np.sin(np.pi*u)**2+10*np.sin(2*np.pi*u+.3)
        top=77+27*np.sin(np.pi*u)**1.4+8*u+2*np.sin(3*np.pi*u)
        width=13+9*np.sin(np.pi*u)**1.4
        for zoffset,y in ((-width,top),(width,top),
                          (width,top-9),(-width,top-9)):
            verts.append((x,y,z+zoffset))
    faces=[]
    for i in range(n-1):
        a=4*i; b=4*(i+1)
        for k in range(4):
            j=(k+1)%4
            faces.extend(((a+k,b+k,b+j),(a+k,b+j,a+j)))
    last=4*(n-1)
    faces.extend(((0,1,2),(0,2,3)))
    faces.extend(((last,last+2,last+1),(last,last+3,last+2)))
    g=valid(trimesh.Trimesh(vertices=verts,faces=faces,process=True),
            "A13 continuous megafold")
    return paint(g,FOLD_COLOR)

def raking_arch_link(index):
    """Real closed cylinder-shaped spatial link; structural proof is absent."""
    side,front=[(-1,True),(1,True),(-1,False),(1,False)][index]
    start=np.array([side*39.,49. if front else 39.,25. if front else -23.])
    finish=np.array([side*51.,82.,-10. if front else -27.])
    delta=finish-start
    height=float(np.linalg.norm(delta))
    mesh=trimesh.creation.cylinder(radius=3.3,height=height,sections=14)
    mat=trimesh.geometry.align_vectors([0,0,1],delta)
    mesh.apply_transform(mat)
    mesh.apply_translation((start+finish)/2)
    return paint(valid(mesh,"A13 raking link "+str(index)),BRACE_COLOR),{
        "from":start.tolist(),"to":finish.tolist(),
        "closed_volume":round(float(mesh.volume),2),
        "intersection_to_old_cliff":"NOT PROVEN",
        "structural_loads":"NOT PROVEN"
    }

def build(source,mode):
    assert mode in ("a","b","c")
    if mode=="a":
        omitted=set()
    elif mode=="b":
        omitted=REMOVED_OUTER
    else:
        # A13-C is a *new independent visual composition*: de-emphasize both
        # inner and outer historical arch shells without altering the A12 GLB.
        omitted=REMOVED_OUTER|REMOVED_INNER
    result=trimesh.Scene()
    if not omitted.issubset(source.graph.nodes_geometry):
        raise AssertionError("Missing precisely named historical arch shells")
    for name in source.graph.nodes_geometry:
        if name in omitted:continue
        matrix,key=source.graph[name]
        result.add_geometry(source.geometry[key].copy(),geom_name=name,
                            node_name=name,transform=np.asarray(matrix))
    roof=continuous_megafold()
    braces=[]
    if mode=="c":
        # Unlike A/B, *no floating upper roof*: the same continuous mass is
        # transformed down into the mid-canyon public space. This reshapes
        # the architectural hierarchy instead of stacking another sky slab.
        roof.vertices[:,1]=0.55*(roof.vertices[:,1]-68)+31
        roof=valid(roof,"A13-C middle occupied urban fold")
        mass_name="A13_MIDDLE_INHABITED_CIVIC_FOLD"
    else:
        mass_name="A13_UNIFIED_FOLDED_CIVIC_SKY"
    result.add_geometry(roof,geom_name=mass_name,node_name=mass_name)
    if mode!="c":
        for i in range(4):
            member,detail=raking_arch_link(i)
            name=f"A13_RAKING_HISTORIC_LINK_{i}"
            result.add_geometry(member,geom_name=name,node_name=name)
            braces.append({"name":name,**detail})
    facts={
      "strategy":{
          "a":"PRESERVE_OUTER_ARCH_WITH_SKY_ROOF",
          "b":"OMIT_TWO_OUTER_ARCH_SHELLS_WITH_SKY_ROOF",
          "c":"OMIT_FOUR_HISTORIC_ARCH_SHELLS_WITH_MID_CANYON_FOLD"
      }[mode],
      "old_outer_shells_omitted":sorted(omitted),
      "omitted_not_destroyed":"A12 original GLB preserved byte-for-byte",
      "new_mass_name":mass_name,
      "new_mass":"One physically closed 3D folded continuous public body",
      "new_mass_volume":round(float(roof.volume),2),
      "new_mass_bounds":np.asarray(roof.bounds).round(3).tolist(),
      "raking_members":braces,
      "interior_walkability":"NOT VERIFIED",
      "historical_shell_removal":"ART EXPERIMENT ONLY; NO ENGINEERING DEMOLITION PASS"
    }
    return result,facts

def compare_all(base,A,B,C,out):
    out.mkdir(parents=True,exist_ok=True)
    camera_evidence={}
    for view,cam in CAMERAS.items():
        ims=[]
        counts=[]
        for candidate in (base,A,B,C):
            im,n=render(candidate,view)
            ims.append(im);counts.append(n)
        panel=Image.new("RGB",(4*WIDTH,HEIGHT+43),(244,248,249))
        for index,im in enumerate(ims):
            panel.paste(im,(WIDTH*index,43))
        d=ImageDraw.Draw(panel)
        for i,label in enumerate((
            "A12 SOURCE / ART HOLD",
            "A13-A SKY ROOF + ORIGINAL ARCH / REJECT CANDIDATE",
            "A13-B SKY ROOF + OUTER ARCH OMIT / REJECT CANDIDATE",
            "A13-C OPEN CLIFFS + MID-CANYON CITY FOLD / HOLD"
        )):
            d.text((WIDTH*i+16,13),label,fill=(25,32,35))
        panel.save(out/(view+"_a12_a13a_a13b_a13c.png"),optimize=True)
        camera_evidence[view]={"fixed_eye":list(cam),"fixed_scale":SCALE,
                               "triangles":counts}
    (out/"provenance.json").write_text(json.dumps({
        "source":"Actual A12 input and exported A13-A/B/C GLB geometry",
        "renderer":"GLB-derived Pillow painter; NOT EEVEE, Blender or Minecraft",
        "comparison":"Same camera, same target, same projection, same scale",
        "cameras":camera_evidence},indent=2)+"\n")

def run(input_glb,out):
    out.mkdir(parents=True,exist_ok=True)
    source=trimesh.load(input_glb,force="scene")
    assert len(source.graph.nodes_geometry)==INPUT_COUNT
    source_qa=route_sweep(source,route_a9())
    assert source_qa["route_samples"]==331
    assert source_qa["body_surface_intersection_sample_count"]==45
    assert source_qa["unsupported_foot_samples"]==0
    inputs={"input_a12_meshes":INPUT_COUNT,
            "source_a12_bounds":np.asarray(source.bounds).round(3).tolist(),
            "source_route":{
                "body_collision_samples":source_qa["body_surface_intersection_sample_count"],
                "unsupported_foot_samples":source_qa["unsupported_foot_samples"]}}
    variants={}
    loaded={}
    for mark in ("a","b","c"):
        scene,facts=build(source,mark)
        filename="a13_%s_unified_megafold.glb"%mark
        path=out/filename
        path.write_bytes(scene.export(file_type="glb"))
        (out/("a13_%s_unified_megafold.obj"%mark)).write_text(
            scene.export(file_type="obj"),encoding="utf8")
        new=trimesh.load(path,force="scene")
        assert len(new.graph.nodes_geometry)==len(scene.graph.nodes_geometry)
        assert facts["new_mass_name"] in new.graph.nodes_geometry
        assert np.allclose(source.bounds[:,[0,2]],new.bounds[:,[0,2]],atol=0.1)
        q=route_sweep(new,route_a9())
        assert q["body_envelope"]==source_qa["body_envelope"]
        assert q["route_samples"]==331 and q["foot_support_samples"]==993
        assert q["negative_intentional_blocker_detected"]
        variants[mark]={
            "meshes":len(new.graph.nodes_geometry),
            "art_form":facts,
            "real_output_bounds":np.asarray(new.bounds).round(3).tolist(),
            "original_legacy_path":q,
            "path_collision_delta":q["body_surface_intersection_sample_count"]-
                source_qa["body_surface_intersection_sample_count"],
            "path_support_delta":q["unsupported_foot_samples"]-
                source_qa["unsupported_foot_samples"],
            "geometric_walk_gate":"HOLD: current legacy route has 45 collisions",
            "aesthetic_approval":"HOLD"
        }
        loaded[mark]=new
    compare_all(source,loaded["a"],loaded["b"],loaded["c"],out/"fourview")
    answer={**inputs,"variants":variants,
            "art_status":"HOLD","construction":"PROHIBITED",
            "city_integration":"PROHIBITED","minecraft_walk":"NOT TESTED",
            "old_arch_shell_omission":"A13-B/C art studies ONLY; not structural demolition signoff",
            "interior_crossing_paths":"NOT VERIFIED",
            "source_a12_unchanged":True,
            "all_private_worlds_used_csv_zip":"UNTOUCHED"}
    (out/"a13_comparative_geometry_qa.json").write_text(
        json.dumps(answer,indent=2,ensure_ascii=False)+"\n")
    return answer

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
        "artifacts/g4c7-a12/a12_exposed_atrium_canyon.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a13"))
    args=p.parse_args()
    q=run(args.input,args.out)
    print(json.dumps({
      "source":q["input_a12_meshes"],
      "variants":{k:{
          "meshes":v["meshes"],
          "top":v["real_output_bounds"][1][1],
          "collisions":v["original_legacy_path"]["body_surface_intersection_sample_count"],
          "unsupported":v["original_legacy_path"]["unsupported_foot_samples"],
          "omitted_old_outer":v["art_form"]["old_outer_shells_omitted"]
      } for k,v in q["variants"].items()},
      "ART":"HOLD"},indent=2))
