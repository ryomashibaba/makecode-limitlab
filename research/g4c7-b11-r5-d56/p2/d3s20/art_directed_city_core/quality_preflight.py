"""D3S20 ART-FIRST nonconstruction quality preflight.
Checks evidence provenance and detects missing interlocks; never grants ART PASS.
Run from the same directory as the D3S20 research audit JSONs.
"""
import json, hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def evaluate(root=HERE):
    root=Path(root)
    m=json.loads((root/'GLB_AUDIT.json').read_text())
    t=json.loads((root/'INDEPENDENT_SAVED_TRIANGLE_AUDIT.json').read_text())
    c=json.loads((root/'COUNTERFACTUAL_AND_VOXEL_AUDIT.json').read_text())
    s=json.loads((root/'AUTHOR_SEMANTIC.json').read_text())
    b=t['ART_DIRECTED_CITY_CORE.glb']; n1=t['NEGATIVE_BODY_BLOCK.glb']; n2=t['NEGATIVE_MISSING_TREAD.glb']
    checks={
       'saved_glb_sha_matches':hashlib.sha256((root/'ART_DIRECTED_CITY_CORE.glb').read_bytes()).hexdigest()==m['sha256'],
       'local_stair_has_actual_treads':b['supported_treads']==20 and b['collision_sample_count']==0,
       'negative_body_block_detected':n1['local_gate']=='LOCAL_SAMPLE_FAIL' and n1['test_intentional_body_block_hit'],
       'negative_tread_removal_detected':n2['local_gate']=='LOCAL_SAMPLE_FAIL' and n2['supported_treads']==19,
       'public_width_changes_inhabited_rooms':c['civic_public_width_plus20']['diff']['change_in_cultural_market_room_parts']>0,
       'research_shift_changes_public_street':c['move_research_sail_x24']['diff']['change_in_ground_public_street_parts']>0,
       'high_destination_access_verified':all(p.get('upper_access')!='NOT_BUILT' for p in s['programmes'] if p['space'] in ('RESEARCH','HOUSING')),
    }
    # Aesthetics must be reviewed by a human from genuine views; never auto-approve.
    can_enter_art_review=all(checks.values())
    return {'checks':checks,'all_technical_preflight_conditions_met':can_enter_art_review,
            'art_pass_from_automated_gate':'NEVER','status':'BLOCKED_FOR_REDESIGN' if not can_enter_art_review else 'ELIGIBLE_FOR_HUMAN_ART_REVIEW_ONLY',
            'formal_331_993_qa':'NOT_RUN','education_construction':'PROHIBITED',
            'note':'Local stair success alone cannot satisfy city-scale living and exterior coupling.'}
if __name__=='__main__':
    result=evaluate()
    (HERE/'PREFLIGHT_RESULT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
