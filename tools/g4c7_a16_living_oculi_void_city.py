"""G4-C7 A16: LIVING OCULI — real subtractive void-city architecture.

Generate two independent city-scale negative-space hypotheses by CARVING the
already hollow inhabited A15-B west/east cliffs in their spatial interiors.
No added roof/ribbon, no Minecraft, no art acceptance or structural certification.
Source: committed A13-C GLB, A12 GLB for comparison, reproducible A15 source.
"""
from pathlib import Path
import argparse
import json
import numpy as np
import trimesh
from PIL import Image,ImageDraw

import g4c7_a7_fourview as painter
from g4c7_a8_fullbody_clearance import route_sweep
from g4c7_a9_sculptural_route import route_a9
from g4c7_a15_split_tide_urban_shells import (
    WEST,EAST,build as a15_build,world_geometry,side_of,
    VISUAL_ONLY_OMISSIONS
)

SOURCE_NODES=616
RESEARCH_SCENE_NODES=610
CANDIDATES={
 "a":{
   "title":"INHABITED TIDAL OCULI",
   # Real vast carved voids positioned in the transformed cliffs, deliberately
   # NOT a repetition of small facade windows. Values relative to local
   # height, not Minecraft blocks.
   "cut_specs":{
      WEST:[(.48,(-2,0,-8),(43,20,29),-.24),
            (.73,( 4,0,11),(37,18,26), .30)],
      EAST:[(.43,( 1,0, 4),(42,22,28), .18),
            (.72,(-2,0,-9),(40,18,27),-.28)]
   }
 },
 "b":{
   "title":"OPEN CROWN ABYSS",
   "cut_specs":{
      WEST:[(.48,(10,0,-17),(45,23,32), .30),
            (.79,(12,0,16),(49,26,34),-.32)],
      EAST:[(.40,(-8,0, 16),(43,22,31),-.28),
            (.76,(-12,0,-17),(51,27,35), .38)]
   }
 }
}
# Every render column uses this same projection/target/scale (important: A15
# has almost twice the old height; we must not artificially enlarge A16).
FRAME_TARGET=np.array([0.,63.,0.])
FRAME_SCALE=410.

def ellipsoid(center,radii,tilt):
    solid=trimesh.creation.icosphere(subdivisions=3)
    solid.apply_scale(np.asarray(radii,dtype=float))
    solid.apply_transform(trimesh.transformations.rotation_matrix(
        float(tilt),(1.,0.,0.)))
    solid.apply_translation(np.asarray(center,float))
    solid.fix_normals()
    assert solid.is_volume and solid.is_watertight
    return solid

def cutter_origin(mesh,fraction,offset):
    """Select a real occupied y-slice of the *persisted* spatial cliff.

    Offset toward the urban canyon, and longitudinally, to make off-center
    NEGATIVE SPACES that expose the attached inherited multi-level city.
    """
    verts=mesh.vertices
    h0=float(mesh.bounds[0,1]);h1=float(mesh.bounds[1,1])
    y=h0+(h1-h0)*fraction
    sample=verts[np.abs(verts[:,1]-y)<13.0]
    assert len(sample)>20,("Not enough actual cliff shell vertices",y)
    center=np.median(sample[:,[0,2]],axis=0)
    return [float(center[0]+offset[0]),float(y+offset[1]),float(center[1]+offset[2])]

def carve_real_cliff(mesh,node,specs):
    """Actual manifold Boolean subtractions; reject failed/empty operations."""
    solid=mesh.copy()
    assert solid.is_volume and solid.is_watertight
    reports=[]
    for fraction,offset,radii,tilt in specs:
        pos=cutter_origin(mesh,fraction,offset)
        cutter=ellipsoid(pos,radii,tilt)
        before=float(solid.volume)
        carved=trimesh.boolean.difference([solid,cutter],engine="manifold")
        assert carved is not None and not carved.is_empty,(node,"empty carve",pos)
        carved.fix_normals()
        assert carved.is_watertight and carved.is_volume,(node,"broken manifold",pos)
        removed=before-float(carved.volume)
        assert removed>600.0,(node,"insufficient physical carving, not a monumental void",pos,removed)
        assert carved.volume>12000,(node,"destroyed inhabited cliff",pos)
        reports.append({
          "center":np.asarray(pos).round(3).tolist(),
          "radii":list(radii),"x_axis_tilt":tilt,
          "removed_real_volume":round(removed,2),
          "input_volume":round(before,2),
          "persisted_volume_candidate":round(float(carved.volume),2),
          "watertight_after_boolean":True,
          "human_access":"NOT VERIFIED",
          "interior_visible_through_opening":"VISUAL REVIEW REQUIRED",
          "new_opening_railing":"NOT TESTED"})
        solid=carved
    return solid,reports

def sculpt_variant(a15scene,mark):
    assert mark in CANDIDATES
    output=trimesh.Scene()
    changes={}
    for name in a15scene.graph.nodes_geometry:
        mesh=world_geometry(a15scene,name)
        if name in (WEST,EAST):
            before=float(mesh.volume)
            mesh,cuts=carve_real_cliff(mesh,name,CANDIDATES[mark]["cut_specs"][name])
            changes[name]={
                "original_real_volume":round(before,2),
                "after_boolean_volume":round(float(mesh.volume),2),
                "total_excavated":round(before-float(mesh.volume),2),
                "excavated_fraction":round((before-float(mesh.volume))/before,5),
                "apertures":cuts,
                "original_cavities":"Inherited from A11/A12 original hollow cliff",
                "structural_loads":"NOT VERIFIED"}
        output.add_geometry(mesh,geom_name=name,node_name=name)
    assert len(output.graph.nodes_geometry)==RESEARCH_SCENE_NODES
    assert len(changes)==2
    return output,changes

def compare_four(a13,a15,variants,out):
    out.mkdir(parents=True,exist_ok=True)
    old_cameras=dict(painter.CAMERAS)
    old_target=painter.TARGET.copy()
    old_scale=painter.SCALE
    painter.CAMERAS={
       name:tuple(np.asarray(eye,dtype=float)+np.array([0.,39.,0.]))
       for name,eye in old_cameras.items()}
    painter.TARGET=FRAME_TARGET.copy()
    painter.SCALE=FRAME_SCALE
    metadata={}
    try:
        for name,eye in painter.CAMERAS.items():
            images=[];counts=[]
            for scene in (a13,a15,variants["a"],variants["b"]):
                img,n=painter.render(scene,name)
                images.append(img);counts.append(n)
            w=painter.WIDTH;h=painter.HEIGHT
            canvas=Image.new("RGB",(w*4,h+42),(241,244,246))
            draw=ImageDraw.Draw(canvas)
            labels=("A13-C / PRE-SCULPT","A15-B / BLOOMING CLIFFS",
                    "A16-A / GIANT TIDAL OCULI","A16-B / BROKEN CROWN ABYSS")
            for i,(img,label) in enumerate(zip(images,labels)):
                canvas.paste(img,(w*i,42))
                draw.text((w*i+13,14),label,fill=(30,35,40))
            canvas.save(out/(name+"_a13c_a15b_a16a_a16b.png"),optimize=True)
            metadata[name]={"camera":list(eye),"scale":FRAME_SCALE,
                            "target":FRAME_TARGET.tolist(),"triangles":counts}
    finally:
        painter.CAMERAS=old_cameras
        painter.TARGET=old_target
        painter.SCALE=old_scale
    (out/"provenance.json").write_text(json.dumps({
      "real_binary_source":"Actual A13-C GLB and GLB-reimported A15-B/A16-A/A16-B",
      "render_engine":"Inherited Pillow triangle painter, not Blender/Minecraft",
      "identical_camera_target_projection_scale_in_all_columns":True,
      "scope":"Architectural shape review ONLY; no human route approval",
      "views":metadata},indent=2)+"\n")

def run(input_glb,out):
    out.mkdir(parents=True,exist_ok=True)
    original=trimesh.load(input_glb,force="scene")
    assert len(original.graph.nodes_geometry)==SOURCE_NODES
    assert VISUAL_ONLY_OMISSIONS.issubset(original.graph.nodes_geometry)
    legacy=route_sweep(original,route_a9())
    assert legacy["route_samples"]==331
    assert legacy["foot_support_samples"]==993
    assert legacy["body_surface_intersection_sample_count"]==45
    assert legacy["unsupported_foot_samples"]==0
    assert legacy["negative_intentional_blocker_detected"]
    intermediate,changed=a15_build(original,"b")
    a15_file=out/"a16_reference_a15b_reconstructed.glb"
    a15_file.write_bytes(intermediate.export(file_type="glb"))
    a15=trimesh.load(a15_file,force="scene")
    assert len(a15.graph.nodes_geometry)==RESEARCH_SCENE_NODES
    verified_ref=route_sweep(a15,route_a9())
    assert verified_ref["route_samples"]==331
    assert verified_ref["foot_support_samples"]==993
    assert verified_ref["body_surface_intersection_sample_count"]<=45
    assert verified_ref["unsupported_foot_samples"]==0
    assert verified_ref["negative_intentional_blocker_detected"]
    results={}
    reloaded={}
    for mark in ("a","b"):
        candidate,cuts=sculpt_variant(a15,mark)
        file=out/("a16_"+mark+"_living_oculi_void_city.glb")
        file.write_bytes(candidate.export(file_type="glb"))
        (out/("a16_"+mark+"_living_oculi_void_city.obj")).write_text(
            candidate.export(file_type="obj"),encoding="utf8")
        check=trimesh.load(file,force="scene")
        assert len(check.graph.nodes_geometry)==RESEARCH_SCENE_NODES
        for name in (WEST,EAST):
            final=world_geometry(check,name)
            assert final.is_watertight and final.is_volume
            assert final.volume>12000
            assert len(cuts[name]["apertures"])==2
            assert cuts[name]["excavated_fraction"]>=0.035,(
                "Too little of inhabited cliff re-sculpted",name,mark,cuts[name])
            for cut in cuts[name]["apertures"]:
                assert cut["removed_real_volume"]>600
        qa=route_sweep(check,route_a9())
        assert qa["route_samples"]==verified_ref["route_samples"]==331
        assert qa["foot_support_samples"]==verified_ref["foot_support_samples"]==993
        assert qa["body_envelope"]==legacy["body_envelope"]
        assert qa["negative_intentional_blocker_detected"]
        assert qa["body_surface_intersection_sample_count"]<=45
        assert qa["unsupported_foot_samples"]==0
        results[mark]={
          "concept":CANDIDATES[mark]["title"],
          "scene_meshes":len(check.graph.nodes_geometry),
          "true_boolean_cliff_excavation":cuts,
          "genuine_carved_aperture_count":sum(len(i["apertures"]) for i in cuts.values()),
          "sum_cliff_excavated_fraction":round(sum(i["excavated_fraction"] for i in cuts.values()),5),
          "total_removed_real_volume":round(sum(i["total_excavated"] for i in cuts.values()),2),
          "full_output_bounds":np.asarray(check.bounds).round(3).tolist(),
          "unchanged_legacy_route_check":qa,
          "body_surface_collision_delta":qa["body_surface_intersection_sample_count"]-45,
          "unsupported_foot_delta":qa["unsupported_foot_samples"],
          "surface_self_intersections":"NOT VERIFIED",
          "fully_integrated_structural_transfers":"NOT VERIFIED",
          "upper_floor_free_walking":"NOT TESTED",
          "visual_judgement":"HOLD_REQUIRES_REAL_FOURVIEW"}
        reloaded[mark]=check
    compare_four(original,a15,reloaded,out/"fourview")
    report={
        "a13c_input_node_count":SOURCE_NODES,
        "a15b_reference_node_count":RESEARCH_SCENE_NODES,
        "a16_actual_mesh_count":RESEARCH_SCENE_NODES,
        "a15_b_sculpted_city_elements":len(changed),
        "concept":"Carve giant living voids directly into the two inhabited city cliffs; no floating ribbon or roof",
        "all_original_inputs":"READ ONLY",
        "prior_research_scene_omissions":sorted(VISUAL_ONLY_OMISSIONS),
        "historic_load_shell_omissions":"Inherited from A13-C visual study; NOT engineered removal",
        "historical_body_collision_samples":45,
        "historical_unsupported_samples":0,
        "variants":results,
        "art_status":"HOLD",
        "minecraft_construction":"PROHIBITED",
        "city_integration":"PROHIBITED",
        "real_minecraft_walk":"NOT TESTED",
        "A5_through_A15_and_world_used_csv_zip":"UNTOUCHED",
        "structural_loads_and_egress":"NOT VERIFIED"}
    (out/"a16_geometry_qa.json").write_text(
        json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    return report

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,default=Path(
      "artifacts/g4c7-a13/a13_c_unified_megafold.glb"))
    p.add_argument("--out",type=Path,default=Path("build/g4c7_a16"))
    args=p.parse_args()
    v=run(args.input,args.out)
    print(json.dumps({"counts":{k:{"real_removed":r["total_removed_real_volume"],
       "holes":r["genuine_carved_aperture_count"],
       "collisions":r["unchanged_legacy_route_check"]["body_surface_intersection_sample_count"]}
       for k,r in v["variants"].items()},"ART":v["art_status"]},indent=2))
