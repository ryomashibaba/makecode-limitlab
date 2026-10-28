"""D28 independent topology/interaction diagnosis of SAVED D27 author geometry.
No import from the author; no 3D, structural, accessibility or artistic approval.
"""
import argparse
import copy
import json
from pathlib import Path
from itertools import combinations
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union

REQUIRED = ['maker', 'research', 'shared', 'housing']

def evaluate(source, counterfactuals, independent):
    p = source['protection']
    assert source['stage'] == 'B11-R5 D27'
    assert source['study'] == 'SCENE_FIRST_AUTHOR_2D_ONLY'
    assert p['art'] == 'ART HOLD' and p['adopted'] == 0
    assert p['true_3d'] == 'NOT_RUN' and p['upper_level_continuous_path'] == 'NOT_MODELED'
    assert p['formal_G0'] == p['formal_S1_G1_G2_G3'] == 'NOT_RUN'
    assert p['minecraft_construction'] == p['city_integration'] == 'FORBIDDEN'
    assert len(source['scenes']) == 5
    assert independent['scope'] == '2D_SAVED_AUTHOR_GEOMETRY_ONLY'
    assert len(independent['candidates']) == 2
    answer = []
    for c in source['candidates']:
        roles = {r['role']: Polygon(r['outline']) for r in c['program']}
        assert set(roles) == set(REQUIRED)
        assert all(poly.is_valid and poly.area > 1 for poly in roles.values())
        groups = unary_union(list(roles.values()))
        comp = len(groups.geoms) if hasattr(groups, 'geoms') else 1
        gaps = {}
        overlaps = {}
        for a, b in combinations(REQUIRED, 2):
            gaps[f'{a}|{b}'] = round(float(roles[a].distance(roles[b])), 3)
            overlaps[f'{a}|{b}'] = round(float(roles[a].intersection(roles[b]).area), 3)
        route = LineString(c['route'])
        eye = Point(c['view_eye'])
        targets = {k: Point(c[k + '_target']) for k in ('maker','research')}
        d_eye = {k: round(float(eye.distance(v)), 3) for k,v in targets.items()}
        d_route = {k: round(float(route.distance(v)), 3) for k,v in targets.items()}
        to_housing = round(float(route.distance(roles['housing'])), 3)
        prior = next(x for x in independent['candidates'] if x['id'] == c['id'])
        assert prior['art'] == 'NOT_ADOPTED'
        assert prior['upper_level_continuous_3d_route'] == 'NOT_MODELED'
        assert counterfactuals[c['id']]['baseline'] == list(counterfactuals[c['id']]['all_roles'])
        evidence = {
            'candidate': c['id'],
            'program_footprint_2d_connected_components': comp,
            'program_pair_distances_author_units': gaps,
            'program_pair_overlap_areas_author_units_squared': overlaps,
            'eye_to_activity_author_units': d_eye,
            'abstract_path_to_activity_target_author_units': d_route,
            'abstract_path_to_housing_footprint_author_units': to_housing,
            'independently_reported_2d_angle_degrees': prior['2d_view_angle_degrees'],
            'source_2d_wall_blockers': prior['2d_other_role_wall_blockers'],
            'interior_rooms': 'NOT_MODELED',
            'working_vertical_access': 'NOT_MODELED',
            '3d_eye_level_sightlines': 'NOT_RUN',
            '3d_body_sweep': 'NOT_RUN',
            'visible_craft_at_human_scale': 'NOT_DEMONSTRATED',
        }
        if c['id'] == 'A':
            assert comp >= 2, 'A no longer disjoint: review author sketch'
            assert to_housing > 0, 'A housing/route distance changed: review again'
            assert all(not lst for lst in prior['2d_other_role_wall_blockers'].values())
            evidence['pre3d_stop_reasons'] = [
                'Separated program footprints despite promised single spatial organism',
                'Housing has no shown 3D upper route or true public threshold',
                'Macro silhouette does not emerge from built rooms: author sketch is generic hills'
            ]
        else:
            assert comp == 1, 'B footprint union changed: review again'
            assert sum(v > 100 for v in overlaps.values()) >= 2
            assert any(prior['2d_other_role_wall_blockers'].values())
            evidence['pre3d_stop_reasons'] = [
                'Large program overlaps are not designed portals or inhabitable rooms',
                'Central 2D wall obstructs the public eye-to-activity lines',
                'Macro silhouette dominated by a single mound/rotunda primitive'
            ]
        answer.append(evidence)
    return {'stage': 'B11-R5 D28',
            'source': 'D27 saved author JSON and independent audit; no generator import',
            'technical_preflight': 'STOP_BOTH_CURRENT_2D_MORPHOLOGIES',
            'separate_author_image_review': 'BOTH_PRE3D_ART_REJECT',
            'candidates': answer, 'new_3d_created': False,
            'formal_QA': 'NOT_RUN', 'overall': 'ART HOLD', 'adopted': 0,
            'minecraft_construction': 'FORBIDDEN',
            'not_a_beauty_score': True}

def main():
    a=argparse.ArgumentParser()
    a.add_argument('--from-d27',default='d27_build')
    a.add_argument('--out',default='d28_build')
    o=a.parse_args()
    root=Path(o.from_d27);out=Path(o.out);out.mkdir(parents=True,exist_ok=True)
    doc=json.loads((root/'d27_author_original.json').read_text(encoding='utf-8'))
    cnt=json.loads((root/'d27_role_counterfactuals.json').read_text(encoding='utf-8'))
    prior=json.loads((root/'d27_independent_2d_result.json').read_text(encoding='utf-8'))
    data=evaluate(doc,cnt,prior)
    for case in ('forged_adoption','deleted_program','forged_upper_route','missing_prior_audit'):
        s=copy.deepcopy(doc); p=copy.deepcopy(prior)
        if case=='forged_adoption':s['protection']['adopted']=1
        elif case=='deleted_program':s['candidates'][0]['program'].pop()
        elif case=='forged_upper_route':s['protection']['upper_level_continuous_path']='PASS'
        else:p['candidates']=[]
        try:evaluate(s,cnt,p)
        except (AssertionError,KeyError,StopIteration):pass
        else:raise AssertionError(f'negative mutation not detected: {case}')
    data['negative_controls_passed']=4
    (out/'d28_spatial_failure_report.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D28 preflight STOP both; 4/4 mutations detected; no ART / true 3D / safety certified.')
if __name__=='__main__':main()
