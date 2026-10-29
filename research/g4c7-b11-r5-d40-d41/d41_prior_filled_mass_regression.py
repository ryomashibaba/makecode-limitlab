"""D41 cross-generation check: D38 named 'inhabited' solids vs D40 genuine room pieces.
Reads two independent saved GLBs and D40 independent audit. Never auto-promotes art.
"""
import argparse,copy,json
from pathlib import Path
import trimesh

def nodes(p):
    sc=trimesh.load(p,force='scene',process=False); out={}
    for name in sc.graph.nodes_geometry:
        T,g=sc.graph[name];m=sc.geometry[g].copy();m.apply_transform(T);out[str(name)]=m
    return out

def evaluate(old,new,d40):
    r=d40['result']
    assert r['stage']=='D40' and r['art']=='ART HOLD' and r['adopted']==0
    assert r['full_triangle_body_sweep']=='NOT_RUN' and r['room_weather_integrity']=='NOT_CERTIFIED'
    previous=[m for k,m in old.items() if k.startswith('shared__inhabited_earthfold_')]
    assert len(previous)==6 and all(m.is_watertight for m in previous)
    assert not any(n.startswith('room__') for n in old)
    # A useful check of source evidence, NOT a magic test for habitability.
    room_nodes=[k for k in new if k.startswith('room__')]
    for k in ('room__ground_floor','room__front_left_wall','room__front_right_wall',
              'room__front_door_header','room__single_roof','room__window_actual_glass',
              'room__west_upper_joint','room__east_upper_joint','room__rear_upper_joint'):
        assert k in new
    assert len(room_nodes)>=20 and r['entry_real_aperture']['width']>=2.8
    assert r['public_to_room_approx_aabb_clearance_samples']>=100
    assert len(r['interior_empty_witness_points'])>=4
    return {
        'stage':'D41','scope':'CROSS_GENERATION_SAVED_GLB_ROOM_EVIDENCE_ONLY',
        'D38':{'false_inhabited_solid_mesh_count':6,
               'explicit_room_nodes':0,'massing_review':'PRE-G0 ART REJECT'},
        'D40':{'modelled_room_component_nodes':len(room_nodes),
               'nominal_entry_clear_width':r['entry_real_aperture']['width'],
               'nominal_entry_clear_height':r['entry_real_aperture']['height'],
               'sampled_clearance_points':r['public_to_room_approx_aabb_clearance_samples'],
               'interior_free_witnesses':len(r['interior_empty_witness_points']),
               'local_room_geometry_progress':'REAL_BUT_UNCERTIFIED',
               'vertical_city_access':'NOT_MODELED','art':'PRE-G0 ART REJECT'},
        'false_claim_preventions':['D38 filled solids are not dwellings',
               'D40 room geometry does not certify a weather-rated dwelling',
               'D40 AABB corridor samples do not prove human walkability',
               'D40 art still rejected'],
        'adopted':0,'overall_art':'ART HOLD','formal_QA':'NOT_RUN',
        'minecraft_construction':'FORBIDDEN'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prior',required=True)
    ap.add_argument('--d40',required=True);ap.add_argument('--out',required=True)
    a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    old=nodes(a.prior);new=nodes(Path(a.d40)/'d40_baseline.glb')
    report=json.loads((Path(a.d40)/'d40_independent_result.json').read_text(encoding='utf-8'))
    j=evaluate(old,new,report)
    for variant in ('false_approval','fake_room_absent','old_filled_masses_absent','misreported_weather'):
        o=old.copy();n=new.copy();r=copy.deepcopy(report)
        if variant=='false_approval':r['result']['adopted']=1
        elif variant=='fake_room_absent':del n['room__ground_floor']
        elif variant=='old_filled_masses_absent':del o['shared__inhabited_earthfold_0']
        else:r['result']['room_weather_integrity']='CERTIFIED'
        try:evaluate(o,n,r)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('Mutation not detected: '+variant)
    j['negative_controls']=4
    (out/'d41_prior_to_room_evidence.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D41 prior-to-room geometry comparison PASS; false certification still blocked')
if __name__=='__main__':main()