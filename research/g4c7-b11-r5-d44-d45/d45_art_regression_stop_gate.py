"""D45: Evidence-limited stop gate. Reads independent D44 GLB audit ONLY.
This is not an AI art score; the human visual rejection is separately recorded.
"""
import argparse,copy,json
from pathlib import Path

def evaluate(e):
    r=e['audit']
    assert r['stage']=='D44' and r['scope']=='INDEPENDENT_SAVED_GLB_GEOMETRY_NOT_SAFETY_OR_ART'
    assert r['adopted']==0 and r['art']=='ART HOLD' and r['official_QA']=='NOT_RUN'
    assert r['human_body_sweep']=='NOT_RUN' and r['construction']=='FORBIDDEN'
    assert len(e['negative_controls_detected'])==10
    assert r['nodes']=={'a_baseline':107,'b_baseline':119,'b_no_maker':102,'b_no_research':105}
    assert r['role_specific_removed']=={'maker':17,'research':14}
    stats=r['architectural_box_bounds']
    a=stats['A'];b=stats['B'];bm=stats['B_no_maker'];br=stats['B_no_research']
    # Not an aesthetic metric: representative non-site axis extents from the genuine GLB.
    max_z_same=(b['max'][2]==bm['max'][2]==br['max'][2])
    x_max_same=(b['max'][0]==bm['max'][0]==br['max'][0])
    y_max_same=(b['max'][1]==bm['max'][1]==br['max'][1])
    assert all([max_z_same,x_max_same,y_max_same])
    assert a['max'][2]>b['max'][2]
    assert 'shared__a_broad_veil' in a['signature_element_names']
    assert 'shared__a_broad_veil' not in b['signature_element_names']
    assert all(not blockers for kind in ('A','B')
       for eyes in r['view_rays_blocker_nodes'][kind].values()
       for blockers in eyes.values())
    assert all(not blockers for kind in ('A','B')
       for blockers in r['vertical_sky_rays_blocker_nodes'][kind].values())
    return {
      'stage':'D45','source':'D44 saved-GLB independent audit + separately authored image critique',
      'diagnostic_positive':{
        'same_functional_upper_room_and_36_step_stair_in_all_saved_models':True,
        'two_public_eyes_each_looking_at_both_activities_have_no_triangle_ray_blockers':True,
        'three_representative_vertical_sky_rays_unobstructed':True,
        'maker_or_research_role_specific_structures_removed':True},
      'rejection_signals_not_automatic_aesthetic_score':{
        'A_broad_veil_extends_above_B_and_dominates_macro_view':True,
        'B_silhouette_non_site_max_x_max_y_max_z_unchanged_in_role_removals':max_z_same and x_max_same and y_max_same,
        'B_actual_roof_garden_support_undemonstrated':True,
        'true_meteorological_or_thermal_room_comfort_unverified':True,
        'full_human_volume_sweep_unperformed':True,
        'hero_human_scene_and_futuristic_urban_identity_weak_in_6_view_author_critique':True},
      'measured_baseline_height_model_units':{'A':a['max'][2],'B':b['max'][2]},
      'role_removal_B_max_height_model_units':{'baseline':b['max'][2], 'without_maker':bm['max'][2], 'without_research':br['max'][2]},
      'author_art_decision':'BOTH A AND B PRE-G0 ART REJECT',
      'next_stage':['Do not enlarge either D44 massing into a city.',
         'Preserve working D42–D44 real room/door/stair evidence as technical baseline only.',
         'Hand-author one interior hero experience with genuine daylight and spatial choreography before further geometry.',
         'Ensure room furniture, cultural work, public view, and skyline are one necessity rather than ornaments.'],
      'CI_means':'reproducible measurements and detection of falsified evidence, not beauty or architectural safety',
      'adopted':0,'ART':'HOLD','official_G0_S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d44_build');o=Path(p.parse_args().out)
    source=json.loads((o/'d44_independent_result.json').read_text(encoding='utf-8'))
    outcome=evaluate(source)
    for kind in ['fake_adoption','fake_sightline','fake_role_silhouette','missing_negative_controls']:
        s=copy.deepcopy(source)
        if kind=='fake_adoption':s['audit']['adopted']=1
        elif kind=='fake_sightline':s['audit']['view_rays_blocker_nodes']['B']['arrival']['maker']=['forged_pier']
        elif kind=='fake_role_silhouette':s['audit']['architectural_box_bounds']['B_no_maker']['max'][2]+=2
        else:s['negative_controls_detected'].pop()
        try:evaluate(s)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('D45 did not catch manipulation '+kind)
    outcome['negative_controls_detected']=['fake_adoption','fake_sightline','fake_role_silhouette','missing_negative_controls']
    (o/'d45_stop_gate.json').write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D45 pre-promotion gate rejects A/B with separate visual review, 4 negative controls detected.')
if __name__=='__main__':main()
