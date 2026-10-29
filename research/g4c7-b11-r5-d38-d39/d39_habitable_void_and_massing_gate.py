"""D39 anti-regression: tests SAVED D38 GLBs + independent audit, NOT beauty scoring.
Critical question: do supposedly 'inhabited' shapes actually define accessible rooms?
Positive closed-solid wedge volume is not a room; a sealed solid is NOT an internal void.
"""
import argparse,json,copy
from pathlib import Path
import trimesh
import numpy as np

def scene(path):
    s=trimesh.load(path,force='scene',process=False);ret={}
    for node in s.graph.nodes_geometry:
        T,k=s.graph[node];m=s.geometry[k].copy();m.apply_transform(T);ret[str(node)]=m
    return ret

def evaluate(s,independent):
    assert independent['stage']=='D38' and independent['adopted']==0
    assert independent['art']=='HOLD' and independent['construction']=='FORBIDDEN'
    d=independent['geometry_evidence'];assert d['broad_massing_stays_after_role_removed'] is True
    for c in ('no_maker','no_research'):
        assert d['non_site_3d_bounds'][c]==d['non_site_3d_bounds']['baseline']
    mass={n:m for n,m in s.items() if n.startswith('shared__inhabited_earthfold_')}
    assert len(mass)==6
    properties={n:{'faces':len(m.faces),'watertight':bool(m.is_watertight),
        'abs_enclosed_volume_model_units_cubed':round(abs(float(m.volume)),2),
        'internal_rooms_explicitly_modelled':0,
        'enclosed_solid_not_room':True} for n,m in sorted(mass.items())}
    assert all(x['faces']==12 and x['watertight'] and x['abs_enclosed_volume_model_units_cubed']>10
        for x in properties.values()),'geometry changed; re-review, do not reuse D39 STOP'
    assert not any(n.startswith('shared__habitable_room_') or n.startswith('shared__door_opening_') for n in s)
    return {'scope':'SAVED_GLB_ARCHITECTURAL_VOID_PREFLIGHT_NOT_FORMAL_QA',
        'stage':'D39','examined_source':'D38',
        'solid_inhabited_named_mass':properties,
        'claimed_habitable_room_nodes':0,
        'truth':'Six named inhabited earthfold objects are closed solid wedges with no modelled doors or accessible room voids',
        'massing_dependency_failure':True,
        'role_counterfactual_global_bounds_identical':True,
        'preflight_decision':'STOP_D38_BEFORE_MEGACITY_AND_DETAILING',
        'no_aesthetic_certification':True,
        'aesthetic_author_judgment':'PRE-G0 ART REJECT',
        'formal_QA':'NOT_RUN','adopted':0,'ART':'HOLD','construction':'FORBIDDEN'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--d38',default='d38_build');ap.add_argument('--out',default='d39_build')
    a=ap.parse_args();root=Path(a.d38);dst=Path(a.out);dst.mkdir(parents=True,exist_ok=True)
    s=scene(root/'d38_baseline.glb')
    data=json.loads((root/'d38_independent_result.json').read_text(encoding='utf-8'))
    result=evaluate(s,data)
    for kind in ('false_approval','fake_usable_room','remove_wedge','falsify_bounds'):
        t={k:v.copy() for k,v in s.items()};d=copy.deepcopy(data)
        if kind=='false_approval':d['adopted']=1
        elif kind=='fake_usable_room':t['shared__habitable_room_0']=t['shared__inhabited_earthfold_0']
        elif kind=='remove_wedge':del t['shared__inhabited_earthfold_0']
        else:d['geometry_evidence']['broad_massing_stays_after_role_removed']=False
        try:evaluate(t,d)
        except AssertionError:pass
        else:raise AssertionError('negative control not detected: '+kind)
    result['negative_controls_detected']=4
    (dst/'d39_void_and_massing_gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D39 PASS = caught 6 non-habitable solid wedges + 4/4 mutation falsifications. Reject artwork.')
if __name__=='__main__':main()
