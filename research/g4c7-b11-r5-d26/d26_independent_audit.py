"""D26 independent PLAN diagnostic. Reads author JSON, NEVER imports artist code.
Not true 3D, G0, S1/G1/G2/G3, structural validation or aesthetic certification.
"""
import copy, json, math
from pathlib import Path
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union
from xml.etree import ElementTree

ROOT=Path(__file__).resolve().parent
POLY_ROLES={'maker','research','culture','housing'}
STATUS={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1':'NOT_RUN','G1':'NOT_RUN','G2':'NOT_RUN','G3':'NOT_RUN',
        'construction':'FORBIDDEN','city_integration':'FORBIDDEN','pr53':'OPEN_DRAFT','main':'UNTOUCHED'}

def inspect(d):
    assert d['stage']=='B11-R5 D26' and d['protection']==STATUS
    assert d['scope']=='AUTHORED_PLAN_AND_SILHOUETTE_ONLY_NOT_TRUE_3D'
    assert len(d['variants'])==2 and [v['id'] for v in d['variants']]==['A','B']
    results=[]
    for v in d['variants']:
        assert set(v['polygons'])==POLY_ROLES
        polys={r:Polygon(p) for r,p in v['polygons'].items()}
        assert all(p.is_valid and p.area>100 for p in polys.values())
        assert all(len(p)>=4 for p in v['polygons'].values())
        assert all(k in v['targets'] for k in ['maker','research'])
        route=LineString(v['public_route'])
        eyes=v['eyes']
        assert len(eyes)==3 and len(route.coords)>=6
        # 2D path is CENTERLINE only. Checking an intended 0.65m half-width is a warning
        # not a human body continuous sweep (which needs saved 3D).
        route_hits={k:{'centerline_inside_polygon_m':round(float(route.intersection(p).length),3),
                       'halfwidth_0p65_buffer_touches':bool(route.buffer(.65).intersects(p))}
                    for k,p in polys.items() if route.buffer(.65).intersects(p)}
        mass=unary_union(list(polys.values()))
        components=len(mass.geoms) if hasattr(mass,'geoms') else 1
        ray_data={}
        angles=[]
        for eye in eyes:
            origin=Point(eye)
            maker=v['targets']['maker'];research=v['targets']['research']
            a=[maker[0]-eye[0],maker[1]-eye[1]]
            b=[research[0]-eye[0],research[1]-eye[1]]
            theta=math.degrees(math.acos(max(-1,min(1,(a[0]*b[0]+a[1]*b[1])/(math.hypot(*a)*math.hypot(*b))))))
            angles.append(round(theta,2))
            line_set={}
            for role,target in v['targets'].items():
                line=LineString([eye,target])
                # Only test *other* footprints. Target room should have a modeled door,
                # which does NOT exist in plan and must not be certified.
                block=[r for r,p in polys.items() if r!=role and line.intersects(p)]
                line_set[role]=block
            ray_data[f'{eye[0]}_{eye[1]}']=line_set
        sky=Polygon(v['open_sky_footprint'])
        assert sky.is_valid
        # Structural detail, upper transport, room portals and rain cover do not exist.
        svg=ROOT/f'd26_{v["id"].lower()}_author_plate.svg'
        png=ROOT/f'd26_{v["id"].lower()}_author_plate.png'
        assert svg.stat().st_size>5000 and png.stat().st_size>15000
        sr=ElementTree.parse(svg).getroot()
        assert sr.tag.endswith('svg')
        assert v['vertical_circulation']['evidence']=='NOT_MODELED'
        found={
          'id':v['id'],
          '2d_program_footprint_components':components,
          'public_route_buffer_0p65_intersections':route_hits,
          'maker_research_horizontal_angular_separation_deg':angles,
          'other_role_opaque_footprint_ray_blockers':ray_data,
          'human_eye_drawn':'yes, conceptual only',
          'shared_perspective_3d_visibility':'NOT_RUN',
          'upper_level_route':'NOT_MODELED',
          'interior_rooms':'NOT_MODELED',
          'daylight_3d_and_weather':'NOT_RUN',
          'formal_body_sweep_331_993':'NOT_RUN',
          'art':'PRE-3D ART REJECT',
          'reason':'A repeats four separated pavilion-like masses; B repeats oversized amphitheatre and separates activities. Neither a credible integrated megacity composition.',
        }
        results.append(found)
    return {'stage':'D26','scope':'INDEPENDENT_PLAN_DIAGNOSTIC_NOT_A_3D_AUDIT',
        'concepts':results,'not_aesthetic_score':True,'author_original_in_repo':True,
        'true_3d':'NOT_RUN','art':'BOTH_PRE_3D_ART_REJECT','adopted':0,'overall':'ART HOLD',
        'official_QA':'NOT_RUN','construction':'FORBIDDEN'}

def tests(d,res):
    assert res['art']=='BOTH_PRE_3D_ART_REJECT'
    assert res['adopted']==0
    forged=copy.deepcopy(d);forged['protection']['adopted']=1
    try:inspect(forged)
    except AssertionError: pass
    else:raise AssertionError('adoption forgery undetected')
    forged=copy.deepcopy(d);del forged['variants'][0]['targets']['research']
    try:inspect(forged)
    except AssertionError: pass
    else:raise AssertionError('research target deletion undetected')
    forged=copy.deepcopy(d);forged['variants'][0]['vertical_circulation']['evidence']='PASS'
    try:inspect(forged)
    except AssertionError: pass
    else:raise AssertionError('unverified vertical access promoted')
    assert len(res['concepts'])==2
    assert all(x['upper_level_route']=='NOT_MODELED' for x in res['concepts'])
    assert all(x['formal_body_sweep_331_993']=='NOT_RUN' for x in res['concepts'])
    # Actual findings are not invented; A route corridor passes this limited 2D test.
    a,b=res['concepts']
    assert not a['public_route_buffer_0p65_intersections'],'A unexpectedly has a corridor collision; review design'
    assert b['public_route_buffer_0p65_intersections']['culture']['centerline_inside_polygon_m']>0
    assert b['maker_research_horizontal_angular_separation_deg'][0]>150
    assert a['2d_program_footprint_components']>=3
    # Deliberately insert A's route through its maker workshop; must be caught.
    poisoned=copy.deepcopy(d)
    poisoned['variants'][0]['public_route'][4]=[-46,-20]
    assert inspect(poisoned)['concepts'][0]['public_route_buffer_0p65_intersections'].get('maker'), 'failed to detect corrupted route'
    print('Negative tests PASS: forged adoption, missing activity, forged access, and genuine plan problems detected.')

if __name__=='__main__':
    d=json.loads((ROOT/'d26_author_original.json').read_text(encoding='utf-8'))
    r=inspect(d); tests(d,r)
    (ROOT/'d26_independent_results.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False,indent=2))