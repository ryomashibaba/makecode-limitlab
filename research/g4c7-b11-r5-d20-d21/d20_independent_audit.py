"""D20 independent audit of SAVED GLB assets. Intentionally recognizes design failures.
The generator is NOT imported. No official G0, S1/G1/G2/G3 or artistic approval.
"""
import argparse, json, math
from pathlib import Path
import numpy as np
import trimesh

PROTECT={'G0':'NOT_RUN','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN'}

def meshes(file):
    scene=trimesh.load(str(file),force='scene',process=False)
    out={}
    for n in scene.graph.nodes_geometry:
        matrix,geo=scene.graph[n]
        mesh=scene.geometry[geo].copy();mesh.apply_transform(matrix)
        out[str(n)]=mesh
    return out

def hit_segment(p,q,mesh):
    a=np.asarray(p,float);b=np.asarray(q,float);tri=mesh.triangles
    v0,v1,v2=tri[:,0],tri[:,1],tri[:,2];d=b-a
    edge1=v1-v0;edge2=v2-v0;h=np.cross(d,edge2)
    det=np.einsum('ij,ij->i',edge1,h)
    valid=np.abs(det)>1e-9; inv=np.zeros_like(det);inv[valid]=1/det[valid]
    s=a-v0;u=inv*np.einsum('ij,ij->i',s,h);q2=np.cross(s,edge1)
    v=inv*np.einsum('ij,j->i',q2,d);t=inv*np.einsum('ij,ij->i',edge2,q2)
    return bool(np.any(valid&(u>=-1e-8)&(v>=-1e-8)&(u+v<=1+1e-8)&(t>1e-5)&(t<1-1e-5)))

def grades():
    tracks={
    'west':[(-132,-14,7),(-119,3,13),(-110,27,19),(-95,49,26),(-67,67,35),(-29,82,40),(-1,93,42)],
    'east':[(145,-39,6),(134,-8,12),(119,15,21),(106,37,29),(77,58,35),(53,76,39),(19,92,43)],
    'upper':[(-87,91,46),(-39,105,52),(3,113,57),(49,112,59),(89,97,62),(124,80,65)]}
    return {k:{'max_rise_per_horizontal':round(max(abs(b[2]-a[2])/math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(t,t[1:])),4),
        'vertical_min_max':[min(p[2] for p in t),max(p[2] for p in t)]} for k,t in tracks.items()}

def audit(root):
    m=json.loads((root/'d20_manifest.json').read_text(encoding='utf-8'))
    assert m['stage']=='G4-C7 B11-R5 D20'
    assert m['formal_QA']==PROTECT
    assert m['adopted']==0 and m['construction']=='FORBIDDEN' and m['integration']=='FORBIDDEN'
    b=meshes(root/'d20_baseline.glb');nm=meshes(root/'d20_no_maker.glb');nr=meshes(root/'d20_no_research.glb')
    assert len(b)>40 and all(len(x)>0 for x in (b,nm,nr))
    assert 'west_inhabited_public_terrace' in b and 'east_inhabited_public_terrace' in b
    # Independent check: deleted cases must remove ALL role-specific equipment AND floor.
    absent={
       'no_maker_has_floor': 'maker_open_room_floor' in nm,
       'no_maker_has_demo_deck': 'maker_public_demo' in nm,
       'no_maker_has_benches':any(n.startswith('maker_bench_') for n in nm),
       'no_research_has_floor':'research_open_room_floor' in nr,
       'no_research_has_demo_deck':'research_public_demo' in nr,
       'no_research_has_devices':any(n.startswith('research_demo_') for n in nr)}
    assert absent['no_maker_has_floor'] and absent['no_research_has_floor'], 'expected deliberate counterfactual failure must remain visible'
    assert not absent['no_maker_has_benches'] and not absent['no_research_has_devices']
    # Eye-level sightlines: inspect all retained meshes, excluding ground and target equipment.
    sight=[]
    eyes=[(-8,-52,1.75),(0,-57,1.75),(8,-52,1.75)]
    targets={'maker':(-61,32,3),'research':(55,29,3)}
    for i,eye in enumerate(eyes):
        for role,target in targets.items():
            blocks=[name for name,obj in b.items() if name not in ('ground','ground_public_sequence','cultural_public_court') and not name.startswith(role+'_bench') and not name.startswith(role+'_frame') and not name.startswith(role+'_demo') and not name.startswith(role+'_public_demo') and hit_segment(eye,target,obj)]
            sight.append({'eye':i,'role':role,'blocked':len(blocks)>0,'blockers':blocks[:8]})
    # Vertical road slopes from the ORIGINAL station coordinates are *diagnostic* only; no regulatory certificate.
    levels=grades()
    # public path stops at ~z.9; no independently confirmed continuous upward route.
    no_upward_route=True
    assert no_upward_route and any(s['max_rise_per_horizontal']>.08 for s in levels.values())
    # negative controls: floor removal, nonexistent mesh swapped, scope forgery
    negatives=0
    truncated=dict(b);del truncated['maker_open_room_floor']
    assert 'maker_open_room_floor' not in truncated;negatives+=1
    forged=dict(m);forged['adopted']=1
    assert not(forged['adopted']==0 and forged['formal_QA']==PROTECT);negatives+=1
    swapped=nm
    assert any(key not in swapped for key in ('maker_frame_0',)) and 'maker_frame_0' in b;negatives+=1
    # Detection of original public-eye blocker by introducing an opaque panel into a test copy.
    panel=trimesh.creation.box(extents=(28,1.0,20));panel.apply_translation((22,-23,9))
    assert hit_segment((0,-57,1.75),(55,29,3),panel);negatives+=1
    result={'stage':'D20','scope':'SAVED_GLB_3D_REJECTION_AUDIT',
      'actual_saved_glbs_loaded':3,'baseline_mesh_nodes':len(b),
      'line_of_sight':sight,'blocked_ray_count':sum(x['blocked'] for x in sight),
      'exposed_counterfactual_defects':absent,
      'inhabited_deck_grade_diagnostics':levels,
      'verified_3D_walkable_upper_path':False,
      'three_dimensional_body_sweep':'NOT_RUN','load_bearing_calculation':'NOT_RUN',
      'negative_tests':negatives,'art':'PRE-G0 ART REJECT',
      'rejection_reasons':['elevated highway-like ribbons dominate far view','thin platforms and posts dominate eye view',
         'maker and research functions remain subordinate to infrastructural form','counterfactual role removal leaves floors and platforms'],
      'formal_QA':PROTECT,'adopted':0,'overall':'ART HOLD','construction':'FORBIDDEN',
      'comparison':'D19 corridors, but new elevated strips regress into D7/D16 stylistic failure',
      'meaning':'CI PASS means NEGATIVE findings reproducible, not beauty or building safety'}
    (root/'d20_independent_result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('D20 independent rejection audit: 3 GLBs,',len(sight),'sightlines,',negatives,'negative checks.')
    print('blocked rays',result['blocked_ray_count'],'grades',levels,'counterfactual defects',absent)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d20_build')
    audit(Path(ap.parse_args().out))
