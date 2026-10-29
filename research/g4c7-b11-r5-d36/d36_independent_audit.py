"""D36 independent inspection of SAVED GLB files. No generator import, no art or safety certification."""
import argparse,json,copy,math
from pathlib import Path
import numpy as np
import trimesh

def inspect(path):
    sc=trimesh.load(path,force='scene',process=False)
    result={}
    for node in sc.graph.nodes_geometry:
        T,k=sc.graph[node];mesh=sc.geometry[k].copy();mesh.apply_transform(T)
        assert len(mesh.vertices)>=4 and len(mesh.faces)>=4
        result[str(node)]=mesh
    return result

def extent(mesh):
    lo,hi=mesh.bounds
    return [list(map(float,lo)),list(map(float,hi))]

def footprint_intersects(a,b,eps=1e-8):
    al,au=a.bounds;bl,bu=b.bounds
    return (min(au[0],bu[0])-max(al[0],bl[0])>eps and
            min(au[1],bu[1])-max(al[1],bl[1])>eps and
            abs(au[2]-bu[2])<0.03)

def verify(states,manifest):
    saved=states['baseline'];no_m=states['no_maker'];no_r=states['no_research']
    p=manifest['protection']
    assert p=={'art':'ART HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
      'construction':'FORBIDDEN','city_integration':'FORBIDDEN','PR53':'DRAFT_OPEN','main':'UNTOUCHED'}
    assert manifest['stage']=='D36' and manifest['scope']=='LOCAL_TRUE_3D_RESEARCH_ONLY'
    assert all(len(states[k])==manifest['case_details'][k]['geometry_nodes'] for k in states)
    assert all('shared__ground' in d and 'shared__upper_living_gallery' in d for d in states.values())
    for role,absent in [('maker',no_m),('research',no_r)]:
        original={k for k in saved if k.startswith(role+'__')}
        assert len(original)>=15
        assert not any(k.startswith(role+'__') for k in absent)
        other={k for k in saved if k.startswith(('research' if role=='maker' else 'maker')+'__')}
        assert other.issubset(absent)
        for suffix in ('actual_work_floor','upper_mezzanine','inhabited_fold_0'):
            assert f'{role}__{suffix}' in saved
        assert len(saved)-len(absent)==len(original)
    st=manifest['stair'];assert st=={'rise':.18,'run':.62,'flights':2,'steps_each':18,'mid_top':3.86,'upper_top':7.1}
    h1=[];h2=[]
    for k in range(18):
        for prefix,lst in [('shared__stair_out_',h1),('shared__stair_return_',h2)]:
            name=prefix+str(k);assert name in saved
            m=saved[name];bounds=extent(m)
            assert math.isclose(bounds[1][2]-bounds[0][2],.18,abs_tol=.0001)
            assert math.isclose(bounds[1][1]-bounds[0][1],.62,abs_tol=.0001)
            lst.append(bounds[1][2])
    assert all(math.isclose(lst[i+1]-lst[i],.18,abs_tol=.0001) for lst in [h1,h2] for i in range(17))
    assert math.isclose(h1[-1],3.86,abs_tol=.0001)
    assert math.isclose(h2[-1],7.10,abs_tol=.0001)
    for key,top in [('shared__middle_landing',3.86),('shared__upper_landing',7.10),
                    ('shared__upper_return',7.10),('shared__upper_living_gallery',7.10),
                    ('maker__upper_mezzanine',7.10),('research__upper_mezzanine',7.10)]:
        assert math.isclose(saved[key].bounds[1][2],top,abs_tol=.0001),(key,top)
    adjacency={
        'stair_landing_to_return':bool(footprint_intersects(saved['shared__upper_landing'],saved['shared__upper_return'])),
        'return_to_gallery':bool(footprint_intersects(saved['shared__upper_return'],saved['shared__upper_living_gallery'])),
        'gallery_to_maker_mezzanine':bool(footprint_intersects(saved['shared__upper_living_gallery'],saved['maker__upper_mezzanine'])),
        'gallery_to_research_mezzanine':bool(footprint_intersects(saved['shared__upper_living_gallery'],saved['research__upper_mezzanine']))}
    assert all(adjacency.values())
    assert len([x for x in saved if x.startswith('maker__inhabited_fold_')])==4
    assert len([x for x in saved if x.startswith('research__inhabited_fold_')])==4
    assert sum(len(saved[k].faces) for k in saved if '__inhabited_fold_' in k)>150
    # Additional actual room voids are not measured by this test. No illusion of engineering approval.
    return {'saved_geometry_counts':{k:len(x) for k,x in states.items()},
            'maker_specific_removed':len(saved)-len(no_m),
            'research_specific_removed':len(saved)-len(no_r),
            'stair':{'steps':36,'rise':.18,'run':.62,'mid_top':h1[-1],'upper_top':h2[-1]},
            'upper_level_floor_footprint_overlaps':adjacency,
            'upper_level_3d_body_sweep':'NOT_RUN','public_3d_body_sweep':'NOT_RUN',
            'roof/weatherproofing':'NOT_RUN','structure_loads':'NOT_RUN','art':'ART HOLD'}

def mutation_trials(states,manifest):
    baseline=verify(states,manifest)
    scenarios=['forged_adoption','maker_left_in_removed','missing_upper_return',
               'bad_mid_landing','broken_housing_contact','missing_maker_fold','forged_formal_qa']
    for typ in scenarios:
        d={k:v.copy() for k,v in states.items()};p=copy.deepcopy(manifest)
        if typ=='forged_adoption':p['protection']['adopted']=1
        elif typ=='maker_left_in_removed':d['no_maker']['maker__actual_work_floor']=d['baseline']['maker__actual_work_floor']
        elif typ=='missing_upper_return':del d['baseline']['shared__upper_return']
        elif typ=='bad_mid_landing':
            m=d['baseline']['shared__middle_landing'].copy();m.apply_translation((0,0,1));d['baseline']['shared__middle_landing']=m
        elif typ=='broken_housing_contact':
            m=d['baseline']['shared__upper_living_gallery'].copy();m.apply_translation((0,20,0));d['baseline']['shared__upper_living_gallery']=m
        elif typ=='missing_maker_fold':del d['baseline']['maker__inhabited_fold_0']
        else:p['protection']['G0']='PASS'
        try:verify(d,p)
        except (AssertionError,KeyError):continue
        raise AssertionError('Mutation not caught: '+typ)
    return baseline,len(scenarios)

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',default='d36_build');x=Path(a.parse_args().out)
    manifest=json.loads((x/'manifest.json').read_text(encoding='utf-8'))
    states={c:inspect(x/f'd36_{c}.glb') for c in ('baseline','no_maker','no_research')}
    baseline,n=mutation_trials(states,manifest)
    result={'stage':'D36','scope':'INDEPENDENT_SAVED_GLB_GEOMETRY_ONLY',
       'results':baseline,'detected_mutations':n,
       'artist_visual_review':'REJECT_REPETITIVE_PAIRED_ARCHES',
       'does_not_certify':['human movement','building safety','usable stairs','weatherproofing','beautiful architecture'],
       'overall':'ART HOLD','adopted':0,'formal_G0_S1_G1_G2_G3':'NOT_RUN','construction':'FORBIDDEN'}
    (x/'d36_independent_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D36 SAVED-GLB audit OK, 7/7 negative mutations caught. ART REJECT, no safety certificate.')
if __name__=='__main__':main()