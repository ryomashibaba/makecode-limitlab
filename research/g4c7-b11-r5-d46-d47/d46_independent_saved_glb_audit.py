"""D46 independently reopens saved GLBs (no import of artist generator). Rejects false adoption;
checks retained D42 hollow room, stair landing, role-dependent structural pieces.
This deliberately is NOT a building, human movement, accessibility or ART certification.
"""
import argparse,copy,json,hashlib
from pathlib import Path
import numpy as np
import trimesh

PROT={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN','city_integration':'FORBIDDEN','PR53':'DRAFT_OPEN','main':'UNTOUCHED'}
CASES=('d46_a_baseline','d46_b_baseline','d46_b_no_maker','d46_b_no_research')

def saved_meshes(path):
    s=trimesh.load(path,force='scene',process=False);m={}
    for node in s.graph.nodes_geometry:
        T,key=s.graph[node];mesh=s.geometry[key].copy();mesh.apply_transform(T)
        assert len(mesh.vertices)>=4 and len(mesh.faces)>=4
        m[str(node)]=mesh
    return m

def zmax(m):return float(m.bounds[1,2])
def overlaps(a,b):
    (lo,hi),(a0,a1)=a.bounds,b.bounds
    return bool(min(hi[0],a1[0])-max(lo[0],a0[0])>.03 and min(hi[1],a1[1])-max(lo[1],a0[1])>.03 and abs(hi[2]-a1[2])<.03)

def inside_any(m,point,prefix):
    return [n for n,x in m.items() if n.startswith(prefix) and all(x.bounds[0,i]+.02<point[i]<x.bounds[1,i]-.02 for i in range(3))]

def verify(scenes,doc):
    assert doc['stage']=='D46' and doc['protection']==PROT
    assert doc['scope']=='HUMAN_EYE_FIRST_TRUE3D_SCENE_FIRST_LOCAL_RESEARCH'
    assert doc['visual_decision']=='UNAPPROVED_PENDING_INDEPENDENT_REVIEW'
    assert set(scenes)==set(CASES)
    for case,m in scenes.items():
        assert len(m)==doc['cases'][case]['nodes']
        mandatory=['shared__hall_floor','shared__upper_gallery','room__upper_real_floor',
            'room__west_front_wall','room__west_back_wall','room__west_door_header',
            'room__east_actual_window','shared__middle_landing',
            'shared__stair_upper_landing','shared__upper_transition']
        assert all(n in m for n in mandatory),(case,'missing stable room or stair')
        for prefix in ('shared__stair_out_','shared__stair_return_'):
            stairs=[zmax(m[f'{prefix}{i}']) for i in range(18)]
            assert all(abs(stairs[i+1]-stairs[i]-.18)<.0001 for i in range(17))
        assert abs(zmax(m['shared__stair_out_17'])-4.0)<.02
        assert abs(zmax(m['shared__stair_return_17'])-7.24)<.02
        for name,top in [('shared__middle_landing',4),('shared__stair_upper_landing',7.24),
                         ('shared__upper_transition',7.24),('shared__upper_gallery',7.24),
                         ('room__upper_real_floor',7.24)]:assert abs(zmax(m[name])-top)<.02,(name,top)
        for a,b in [('shared__stair_upper_landing','shared__upper_transition'),
                    ('shared__upper_transition','shared__upper_gallery'),
                    ('shared__upper_gallery','room__upper_real_floor')]:assert overlaps(m[a],m[b]),(case,a,b)
        front=m['room__west_front_wall'].bounds[1,1]
        back=m['room__west_back_wall'].bounds[0,1]
        aperture=float(m['room__west_door_header'].bounds[0,2]-7.24)
        assert 4.5<back-front<5.5 and aperture>3.5
        for p in [(12.2,15.9,9.2),(13.2,18,10.1),(15.5,20,10.5),(11.5,29,9.4)]:
            assert not inside_any(m,p,'room__'),(case,p)
        assert not inside_any(m,(8.3,15.9,9.3),'room__'),(case,'blocked doorway')
    base=scenes['d46_b_baseline'];no_m=scenes['d46_b_no_maker'];no_r=scenes['d46_b_no_research']
    for role,removed,other,specific in [('maker',no_m,'research','maker__inhabited_splayed_service_wall'),
                                        ('research',no_r,'maker','research__inhabited_sensor_fold')]:
        own={n for n in base if n.startswith(role+'__')}
        assert len(own)>10 and specific in base
        assert not any(n.startswith(role+'__') for n in removed)
        assert len(base)-len(removed)==len(own)
        assert all(n in removed for n in base if n.startswith(other+'__'))
    assert 'shared__a_view_screen' in scenes['d46_a_baseline']
    assert 'shared__b_winding_observation_ledge' in base
    # Case-specific occupied-extents x change, deliberately omit uninhabited site terrain.
    def xbound(m):
        mm=[v.bounds for n,v in m.items() if not n.startswith('site__')]
        return round(float(min(v[0,0] for v in mm)),2),round(float(max(v[1,0] for v in mm)),2)
    ext={k:xbound(v) for k,v in scenes.items()}
    assert ext['d46_b_baseline'][0]<ext['d46_b_no_maker'][0]
    # Do NOT pretend that research deletion changes the overall outer envelope.
    # It does not: room balcony occupies x=31 farther than research fold.
    # This is an explicit art/form-causality FAILURE recorded in the result.
    # Actual room still inherited from D42. This is not proof of waterproof, accessibility or structural loads.
    return {'nodes':{c:len(m) for c,m in scenes.items()},
      'role_specific_removed':{'maker':len(base)-len(no_m),'research':len(base)-len(no_r)},
      'architectural_x_bounds':ext,
      'maker_removal_changes_xmin':ext['d46_b_baseline'][0]<ext['d46_b_no_maker'][0],
      'research_removal_changes_xmax':ext['d46_b_baseline'][1]>ext['d46_b_no_research'][1],
      'upper_landing_top':7.24,'stair_steps':36,
      'room_door_nominal_width':round(back-front,2),'room_door_nominal_height':round(aperture,2),
      'upper_room_void_witnesses':4,'physical_floor_connections_checked':3,
      'formal_human_3D_body_sweep':'NOT_RUN','structure_safety':'NOT_CERTIFIED',
      'climate_enclosure':'NOT_CERTIFIED','art':'ART HOLD'}

def negative_tests(scenes,doc):
    tests=['forged_adoption','forged_official_G0','missing_actual_room_floor','door_filled',
           'broken_upper_stair','disconnected_gallery','maker_not_removed',
           'missing_maker_envelope','missing_research_envelope']
    for t in tests:
        c={k:dict(v) for k,v in scenes.items()};d=copy.deepcopy(doc)
        if t=='forged_adoption':d['protection']['adopted']=1
        elif t=='forged_official_G0':d['protection']['G0']='PASS'
        elif t=='missing_actual_room_floor':del c['d46_b_baseline']['room__upper_real_floor']
        elif t=='door_filled':
            m=trimesh.creation.box(extents=(.8,5,3.1));m.apply_translation((8.3,15.9,9.1))
            c['d46_b_baseline']['room__fake_door_solid']=m;d['cases']['d46_b_baseline']['nodes']+=1
        elif t=='broken_upper_stair':del c['d46_b_baseline']['shared__stair_return_17']
        elif t=='disconnected_gallery':
            m=c['d46_b_baseline']['shared__upper_gallery'].copy();m.apply_translation((0,30,0))
            c['d46_b_baseline']['shared__upper_gallery']=m
        elif t=='maker_not_removed':c['d46_b_no_maker']['maker__floor']=c['d46_b_baseline']['maker__floor'];d['cases']['d46_b_no_maker']['nodes']+=1
        elif t=='missing_maker_envelope':del c['d46_b_baseline']['maker__inhabited_splayed_service_wall']
        elif t=='missing_research_envelope':del c['d46_b_baseline']['research__inhabited_sensor_fold']
        try:verify(c,d)
        except (AssertionError,KeyError):continue
        raise AssertionError(f'mutation not detected: {t}')
    return tests

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d46_build');a=p.parse_args();out=Path(a.out)
    doc=json.loads((out/'manifest.json').read_text(encoding='utf-8'))
    scenes={k:saved_meshes(out/(k+'.glb')) for k in CASES}
    for k in CASES:assert hashlib.sha256((out/(k+'.glb')).read_bytes()).hexdigest()==doc['cases'][k]['sha256']
    result=verify(scenes,doc);neg=negative_tests(scenes,doc)
    data={'stage':'D46','scope':'INDEPENDENT_RELOADED_GLB_GEOMETRY_AND_NEGATIVE_TESTS',
          'result':result,'detected_negative_tests':neg,'count':len(neg),
          'decision':'ART HOLD, UNAPPROVED','approved':False,'construction':'FORBIDDEN'}
    (out/'d46_independent_result.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'D46 independent geometry PASS, {len(neg)}/{len(neg)} mutations detected. ART HOLD')
if __name__=='__main__':main()
