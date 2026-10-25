"""G4-C7 A17 honest architectural proximity audit (NO MINECRAFT).

Use this only after actual A17-A/B GLBs exist. Report how close the newly
generated megafold is to the 608 inherited city meshes. This is a
surface-VERTEX proximity diagnostic, NOT collision, attachment, structural
support, accessibility, nor a substitute for original 331/993 safety tests.
The old input model and all Minecraft worlds are read-only.
"""
from pathlib import Path
import argparse
import json

import numpy as np
import trimesh
from scipy.spatial import cKDTree

MONOLITH="A17_MONOLITHIC_TECTONIC_CIVIC_FOLD"
EXCLUDED_OLD={
    "A11_WEST_FAULT_ESCARPMENT_REAL_VOID",
    "A11_EAST_SKY_FOLD_REAL_VOID",
}
SAMPLE_COUNT=65000
SEED=20261025


def in_world(scene, node):
    matrix,geometry=scene.graph[node]
    m=scene.geometry[geometry].copy()
    m.apply_transform(matrix)
    return m


def city_reference_vertices(reference):
    assert len(reference.graph.nodes_geometry)==610
    assert EXCLUDED_OLD.issubset(reference.graph.nodes_geometry)
    nodes={n:in_world(reference,n).vertices
           for n in reference.graph.nodes_geometry
           if n not in EXCLUDED_OLD}
    assert len(nodes)==608
    assert all(len(verts)>0 for verts in nodes.values())
    return nodes


def measure_candidate(scene, original_nodes):
    assert len(scene.graph.nodes_geometry)==609
    assert MONOLITH in scene.graph.nodes_geometry
    assert EXCLUDED_OLD.isdisjoint(scene.graph.nodes_geometry)
    original_names=set(original_nodes)
    assert set(scene.graph.nodes_geometry)-{MONOLITH}==original_names
    sculpt=in_world(scene,MONOLITH)
    assert sculpt.is_watertight and sculpt.is_volume
    city=np.vstack(list(original_nodes.values()))
    nearest_city=cKDTree(city)
    samples,_=trimesh.sample.sample_surface(sculpt,SAMPLE_COUNT,seed=SEED)
    nearest_distance,_=nearest_city.query(samples,workers=-1)
    # On an orthographic painter the same building can appear 'attached' even
    # when it does not touch: record how much of the monumental skin is distant.
    quantiles={str(p):round(float(np.quantile(nearest_distance,p)),4)
               for p in [0,.001,.01,.05,.10,.50,.90,1.0]}
    nearest_macro=cKDTree(sculpt.vertices)
    per_node=[]
    for node,vertices in original_nodes.items():
        distance,_=nearest_macro.query(vertices,workers=-1)
        per_node.append({
            "node":node,
            "closest_vertex_distance":round(float(np.min(distance)),4),
            "median_vertex_distance":round(float(np.median(distance)),4),
            "count_vertices_within_3":int(np.count_nonzero(distance<=3.0)),
            "count_vertices_within_8":int(np.count_nonzero(distance<=8.0)),
        })
    per_node.sort(key=lambda item:item["closest_vertex_distance"])
    close=[node for node in per_node
           if node["closest_vertex_distance"]<3.0]
    return {
        "saved_real_GL B_and_vertex_position".replace(" ",""):"SOURCE MODEL ONLY",
        "city_node_count_excluding_two_replaced_cliffs":len(original_nodes),
        "city_vertex_count":len(city),
        "monolith_mesh_faces":len(sculpt.faces),
        "monolith_mesh_closed_positive_volume":True,
        "sampling_seed":SEED,
        "samples_on_macro_surface":SAMPLE_COUNT,
        "macro_samples_to_old_city_VERTEX_distance_quantiles":quantiles,
        "old_city_nodes_with_any_VERTEX_under_3_units":len(close),
        "old_city_nodes_with_any_VERTEX_under_8_units":sum(
            d["closest_vertex_distance"]<8.0 for d in per_node),
        "closest_old_city_nodes":per_node[:30],
        "old_city_named_civic_elements_proximity":[
            x for x in per_node if any(
                token in x["node"] for token in
                ("CIVIC_DECK","EXPOSED_CIVIC","INHABITED_FAULT","CROSS_ATRIUM"))
        ][:50],
        "vertex_sampling_caveat":"Nearest sampled surface points to OLD vertices, and OLD vertices to macro vertices, not exact triangle intersection; cannot prove loadbearing, real contact, movement, or engineering",
        "load_bearing":"NOT VERIFIED",
        "public_routes":"NOT VERIFIED",
        "surface_self_intersection":"NOT VERIFIED",
        "art_judgement":"HOLD",
        "Minecraft_Education_construction":"PROHIBITED",
        "city_integration":"PROHIBITED",
        "legacy_331_993_gate":"NOT RUN BY THIS AUDITOR; check canonical geometry QA separately"
    }


def run(a15,a17a,a17b,out):
    ref=trimesh.load(a15,force="scene")
    nodes=city_reference_vertices(ref)
    report={
        "audit":"A17 ARCHITECTURAL PROXIMITY ONLY",
        "source_reference":str(a15),
        "candidate_input_paths":{"a":str(a17a),"b":str(a17b)},
        "art_status":"HOLD",
        "Minecraft_construction":"PROHIBITED",
        "city_integration":"PROHIBITED",
        "variants":{
            "a":measure_candidate(trimesh.load(a17a,force="scene"),nodes),
            "b":measure_candidate(trimesh.load(a17b,force="scene"),nodes),
        },
    }
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return report


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--a15",type=Path,default=Path(
        "artifacts/g4c7-a15/a15_b_split_tide_urban_shells.glb"))
    parser.add_argument("--a17-a",type=Path,default=Path(
        "artifacts/g4c7-a17/a17_a_monolithic_rift_fold.glb"))
    parser.add_argument("--a17-b",type=Path,default=Path(
        "artifacts/g4c7-a17/a17_b_monolithic_rift_fold.glb"))
    parser.add_argument("--out",type=Path,default=Path(
        "build/g4c7_a17/a17_city_mass_proximity_audit.json"))
    args=parser.parse_args()
    a=run(args.a15,args.a17_a,args.a17_b,args.out)
    print(json.dumps({
        k:{"close_city_nodes":v["old_city_nodes_with_any_VERTEX_under_3_units"],
           "median_nearest_old_vertex":
             v["macro_samples_to_old_city_VERTEX_distance_quantiles"]["0.5"]}
        for k,v in a["variants"].items()},indent=2))
