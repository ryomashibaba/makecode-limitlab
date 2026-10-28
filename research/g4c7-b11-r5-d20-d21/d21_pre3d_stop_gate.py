"""D21 evidence-based early rejection, not aesthetic score or safety certification.
Reads D20's independent saved-GLB audit. Must NOT import the D20 generator.
"""
import argparse,json
from pathlib import Path

RULES={'construction':'FORBIDDEN','formal_QA':{'G0':'NOT_RUN','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN'}}

def evaluate(artifact):
    assert artifact['stage']=='D20' and artifact['scope']=='SAVED_GLB_3D_REJECTION_AUDIT'
    assert artifact['actual_saved_glbs_loaded']==3
    assert artifact['adopted']==0 and artifact['construction']==RULES['construction']
    assert artifact['formal_QA']==RULES['formal_QA']
    # 1:12 (8.33%) used ONLY as a provisional routing design benchmark, not a legal code claim.
    max_grade=max(x['max_rise_per_horizontal'] for x in artifact['inhabited_deck_grade_diagnostics'].values())
    roles=artifact['exposed_counterfactual_defects']
    failures={
      'public_culture_form_is_aerial_bridge':artifact['art']=='PRE-G0 ART REJECT',
      'upper_public_route_3d_not_proved':not artifact['verified_3D_walkable_upper_path'],
      'grade_exceeds_provisional_1_to_12':max_grade>1/12,
      'maker_counterfactual_retains_floor_or_deck':roles['no_maker_has_floor'] or roles['no_maker_has_demo_deck'],
      'research_counterfactual_retains_floor_or_deck':roles['no_research_has_floor'] or roles['no_research_has_demo_deck'],
      'formal_safety_not_certified':artifact['three_dimensional_body_sweep']=='NOT_RUN'
    }
    assert all(failures.values()), 'D20 evidence changed: reevaluate, do not reuse rejection blindly'
    return {'stage':'D21 pre-3D methodological gate', 'evaluated_stage':'D20',
      'all_rejection_signals':failures, 'max_measured_deck_grade_ratio':max_grade,
      'benchmark':'1:12 preliminary design heuristic only, NOT certification',
      'counterfactual_scope':'In the baseline geometry, original role floors/decks survive the removed-role scenario',
      'next_candidate_spec':{
       'narrative':'One shared civic scene linking fabrication, public learning, research and residence must be spatially modelled before sculpting a megashell.',
       'forbid':'freestanding bridges/ribbons, mirrored pavilions, giant boxes, decorative slit/arch-only tweaks',
       'mechanism':'human-scale walkable public rooms + real thresholds and inhabited vertical mass create the silhouette together',
       'pre3d_required_evidence':['one human-eye drawing showing maker AND research as a real experience',
         'one macro drawing created from the SAME architectural original',
         'site-to-upper continuous travel concept; no implausible free ramps or isolated cores',
         'honest removal scenarios with all activity-specific rooms/floors removed',
         'structural path hypothesis and direct open-air daylight path',
         'no artistic approval by CI or arbitrary numerical beauty score']},
      'artist':'BOTH D20 AND D19 NOT ADOPTED', 'promote_to_real3d':False,
      'official_QA':'NOT_RUN','art':'HOLD / NO ADOPTION','construction':'FORBIDDEN'}

def run(out):
    baseline=json.loads((out/'d20_independent_result.json').read_text(encoding='utf-8'))
    result=evaluate(baseline)
    assert len(result['all_rejection_signals'])==6
    # Mutation: falsely mark no-research as cleaned. Explicitly must not trigger hidden acceptance.
    modified=json.loads(json.dumps(baseline))
    modified['exposed_counterfactual_defects']['no_research_has_floor']=False
    modified['exposed_counterfactual_defects']['no_research_has_demo_deck']=False
    try:evaluate(modified)
    except AssertionError:pass
    else:raise AssertionError('Must detect evidence mismatch')
    # Mutation: forged ART PASS has to invalidate D20 preflight contract.
    forged=json.loads(json.dumps(baseline));forged['art']='ART PASS'
    try:evaluate(forged)
    except AssertionError:pass
    else:raise AssertionError('Must detect forged art promotion')
    (out/'d21_pre3d_stop_gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D21 preflight GATE: VALIDATED REJECT. No artwork promoted / no construction.')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',default='d20_build');run(Path(p.parse_args().out))
