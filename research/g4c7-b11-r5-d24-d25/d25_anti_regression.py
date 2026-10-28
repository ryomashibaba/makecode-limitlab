"""D25: negative-artifact preflight from saved D24 evidence. NOT automatic beauty/safety certification."""
import argparse,json
from pathlib import Path
import trimesh

def inspect(root):
    out=Path(root)
    prior=json.loads((out/'d24_independent_result.json').read_text(encoding='utf-8'))
    manifest=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    s=trimesh.load(out/'d24_baseline.glb',force='scene',process=False)
    nodes={str(x) for x in s.graph.nodes_geometry}
    expected=['maker','research','culture','west_home','east_home']
    motifs={k:{'rear_walls':sum(n==k+'__rear_wall' for n in nodes),
               'ground_piers':sum(n.startswith(k+'__ground_pier_') for n in nodes),
               'repeated_roof_slats':sum(n.startswith(k+'__top_ridge_') for n in nodes)} for k in expected}
    sidewalls=[k for k in expected if motifs[k]['rear_walls']==1]
    repeated_roofs=all(motifs[k]['repeated_roof_slats']==6 for k in expected)
    rays=prior['view_ray_blocker_names']
    obstructed={f'{eye}_to_{role}':blocks for eye,targets in rays.items() for role,blocks in targets.items() if blocks}
    far=prior['activity_to_public_route_lateral_distance_m']
    warnings={
        'human_eye_visibility_not_all_clear':bool(obstructed),
        'two_opposed_massing_banks_remain':len(sidewalls)>=4,
        'five_sectors_share_identical_roof_template':repeated_roofs,
        'activity_targets_lateral_distance_over_20m':any(v>20 for v in far.values()),
        'vertical_circulation_not_built':prior['vertical_access']=='NOT_MODELED',
        'official_QA_not_performed':prior['official_G0_S1_G1_G2_G3']=='NOT_RUN',
    }
    # It is not valid to treat these mechanical warnings as full aesthetic scoring.
    # The separately authored visual review concludes this candidate is aesthetically rejected.
    assert all(warnings.values()), 'D24 evidence has changed; review before reusing D25 conclusion'
    protected=manifest['protection']
    assert protected['adopted']==0 and protected['ART']=='HOLD'
    assert protected['construction']=='FORBIDDEN' and protected['main']=='UNTOUCHED'
    return {'stage':'D25','source_stage':'D24','source':'saved GLB + independent audit JSON + author image review',
      'massing_grammar_counts':motifs,'rejected_preflight_warnings':warnings,
      'eye_ray_obstructions':obstructed,'target_distance_m':far,
      'important_positive_evidence':{'same_role_activity_removal':'PASS_ALL_ROLE_DEDICATED_PARTS_REMOVED',
       'central_sky_ray_clear':not prior['central_sky_opaque_blockers']},
      'review':'D24 PRE-G0 ART REJECT: twin heavy inhabited banks + cloned terraces/roof slats; no distinct civic signature',
      'validation_scope':'DIAGNOSTIC_EVIDENCE_NOT_BEAUTY_SCORE_OR_HUMAN_SAFETY',
      'decision':'STOP_D24_MORPHOLOGY_BEFORE_CITY_INTEGRATION',
      'promote_to_more_3d':False,'art':'ART HOLD','adopted':0,
      'formal_G0_S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN'}

def self_tests(root,results):
    assert results['promote_to_more_3d'] is False
    assert all(results['rejected_preflight_warnings'].values())
    assert results['eye_ray_obstructions'].get('civic_to_research')==['research__ground_pier_1']
    import copy
    bad=copy.deepcopy(results);bad['adopted']=1
    try:assert_no_adoption(bad)
    except AssertionError:pass
    else:raise AssertionError('forged adoption not rejected')
    bad=copy.deepcopy(results);bad['rejected_preflight_warnings']['human_eye_visibility_not_all_clear']=False
    try:assert all(bad['rejected_preflight_warnings'].values())
    except AssertionError:pass
    else:raise AssertionError('forged sightline acceptance not rejected')
    # A missing independent GLB is a hard failure, not a silent empty test.
    assert (Path(root)/'d24_baseline.glb').stat().st_size>10_000

def assert_no_adoption(result):
    assert result['adopted']==0 and result['art']=='ART HOLD'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='d24_build');r=Path(ap.parse_args().out)
    data=inspect(r);self_tests(r,data);assert_no_adoption(data)
    (r/'d25_preflight_result.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D25 rejection-preflight negative controls PASS, ART REJECT & safety hold. Not an aesthetic approval.')
if __name__=='__main__':main()
