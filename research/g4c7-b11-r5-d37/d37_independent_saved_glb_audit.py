"""D37 independent saved-GLB audit. Deliberately never imports the author's generator.
No human sweep, safety / weatherproofing / ART certification performed.
"""
import argparse, copy, json, math
from pathlib import Path
import numpy as np
import trimesh

def load_scene(path):
    sc=trimesh.load(path,force='scene',process=False)
    out={}
    for node in sc.graph.nodes_geometry:
        T,key=sc.graph[node];m=sc.geometry[key].copy();m.apply_transform(T)
        out[str(node)]=m
    return out

def bb(m):return np.asarray(m.bounds,float)
def top(m):return float(m.bounds[1,2])
def overlap(a,b):
    A=bb(a);B=bb(b)
    return (min(A[1,0],B[1,0])-max(A[0,0],B[0,0])>0.10 and
            min(A[1,1],B[1,1])-max(A[0,1],B[0,1])>0.10 and
            abs(top(a)-top(b))<.025)

def overlap_stair_rise(landing,step,rise):
    A=bb(landing);B=bb(step)
    return (min(A[1,0],B[1,0])-max(A[0,0],B[0,0])>.1 and
            min(A[1,1],B[1,1])-max(A[0,1],B[0,1])>.1 and
            abs(top(step)-top(landing)-rise)<.02)

def segment_hits(p,q,m):
    # Bidirectional two-sided segment/triangle hit, independently of trimesh.ray/rtree
    tri=np.asarray(m.triangles,float)
    if not len(tri):return False
    p=np.asarray(p,float);q=np.asarray(q,float);d=q-p
    a,b,c=tri[:,0],tri[:,1],tri[:,2]
    e=b-a;f=c-a;h=np.cross(np.broadcast_to(d,f.shape),f)
    det=np.einsum('ij,ij->i',e,h)
    valid=np.abs(det)>1e-9;inverse=np.zeros_like(det);inverse[valid]=1/det[valid]
    tvec=p-a
    u=inverse*np.einsum('ij,ij->i',tvec,h)
    qvec=np.cross(tvec,e)
    v=inverse*np.einsum('ij,j->i',qvec,d)
    t=inverse*np.einsum('ij,ij->i',f,qvec)
    return bool(np.any(valid&(u>=-1e-7)&(v>=-1e-7)&(u+v<=1+1e-7)&(t>1e-4)&(t<1-1e-4)))

def assess(states,manifest):
    p=manifest['protection']
    assert p=={'ART':'HOLD','adopted':0,'G0':'NOT_RUN','S1_G1_G2_G3':'NOT_RUN',
      'Minecraft':'FORBIDDEN','integration':'FORBIDDEN','main':'UNTOUCHED','PR53':'DRAFT_OPEN'}
    assert manifest['stage']=='D37' and manifest['scope']=='LOCAL_TRUE_3D_RESEARCH_ONLY'
    assert set(states)=={'baseline','no_maker','no_research'}
    for case,meshes in states.items():
        assert len(meshes)==manifest['states'][case]['nodes']
        assert 'shared__single_atrium_floor' in meshes
        assert 'shared__upper_gallery' in meshes
        assert all(len(m.faces)>3 for m in meshes.values())
    b=states['baseline'];N=states['no_maker'];R=states['no_research']
    role_losses={}
    for role,minus in [('maker',N),('research',R)]:
        removed={k for k in b if k.startswith(role+'__')}
        assert len(removed)>=12
        assert not removed.intersection(minus)
        assert set(b)-set(minus)==removed
        other='research' if role=='maker' else 'maker'
        assert {k for k in b if k.startswith(other+'__')}.issubset(minus)
        assert f'{role}__work_island' in removed
        role_losses[role]=len(removed)
    assert all('shared__glazed_light_fault' in meshes for meshes in states.values())
    # A genuine glass mesh covers the designed roof light slot, though this is NOT weather certification.
    assert len(b['shared__glazed_light_fault'].faces)>=12
    steps=manifest['stair']
    assert steps=={'flights':2,'steps_per_flight':18,'rise':.19,'run':.44,
                  'ground_top':.44,'mid_top':3.86,'upper_top':7.28}
    flight_tops={}
    for prefix in ('shared__stair_out_','shared__stair_return_'):
        heights=[]
        for i in range(18):
            m=b[f'{prefix}{i}'];heights.append(top(m))
            assert abs(m.extents[1]-.44)<.01
            assert abs(m.extents[0]-3.0)<.01
        assert np.allclose(np.diff(heights),.19,atol=.001)
        flight_tops[prefix]=heights
    assert abs(flight_tops['shared__stair_out_'][-1]-3.86)<.01
    assert abs(flight_tops['shared__stair_return_'][-1]-7.28)<.01
    required={'shared__mid_landing':3.86,'shared__upper_landing':7.28,
              'shared__upper_bridge_floor':7.28,'shared__upper_gallery':7.28}
    for name,h in required.items(): assert abs(top(b[name])-h)<.015,(name,top(b[name]),h)
    connects={
      'first_flight_to_mid':overlap(b['shared__stair_out_17'],b['shared__mid_landing']),
      'mid_to_return_one_riser':overlap_stair_rise(b['shared__mid_landing'],b['shared__stair_return_0'],.19),
      'return_to_upper':overlap(b['shared__stair_return_17'],b['shared__upper_landing']),
      'upper_to_bridge':overlap(b['shared__upper_landing'],b['shared__upper_bridge_floor']),
      'bridge_to_gallery':overlap(b['shared__upper_bridge_floor'],b['shared__upper_gallery'])}
    assert all(connects.values()),connects
    assert len([k for k in b if k.startswith('shared__stair_out_stringer_')])==2
    assert len([k for k in b if k.startswith('shared__stair_return_stringer_')])==2
    # Check selected positions within common room for a short vertical HEAD segment.
    # Ignore intended floor, glazing and human-reference meshes. No whole-body sweep.
    head_points=[(-5,-23),(-2,-9),(0,2),(4,8)]
    hard={name:m for name,m in b.items() if not name.startswith('shared__person_')}
    head_clear={}
    for i,(x,y) in enumerate(head_points):
        p0=[x,y,2.3];p1=[x,y,3.9]
        hits=[name for name,m in hard.items() if segment_hits(p0,p1,m)]
        head_clear[f'sample_{i}']=hits
    # Do not assert all clear if evidence contradicts it: report truth.
    rays={}
    for eye,origin in manifest['eyes'].items():
        if eye not in ('entry','civic'):continue
        rays[eye]={}
        for role,target in manifest['targets'].items():
            architectural={name:m for name,m in b.items() if name.startswith('shared__') and
                          ('person' not in name and 'single_atrium_floor' not in name and 'upper_gallery' not in name)}
            hits=[name for name,m in architectural.items() if segment_hits(origin,target,m)]
            rays[eye][role]=hits
    roof_names=[k for k in b if k.startswith('shared__roof_')]
    assert len(roof_names)==3
    silhouette_bounds={case:np.vstack([m.bounds for m in states[case].values()]).reshape(-1,3)
      for case in states}
    macro={case:[np.min(v,axis=0).round(3).tolist(),np.max(v,axis=0).round(3).tolist()]
      for case,v in silhouette_bounds.items()}
    return {'geometry_nodes':{case:len(nodes) for case,nodes in states.items()},
      'activity_role_specific_removed_nodes':role_losses,
      'stair':{'steps':36,'rise':.19,'tread_run':.44,'mid_top':3.86,'upper_top':7.28,
               'contact_footprints_same_top':connects,'stringers_designed':4},
      'selected_short_head_clearance_intersections':head_clear,
      'limited_activity_sightline_architectural_intersections':rays,
      'macro_bounds_by_condition':macro,
      'shared_roof_is_not_role_dependent':all(set(roof_names).issubset(states[c]) for c in states),
      'one_shared_positive_floor':True,
      'human_3D_sweep':'NOT_RUN','functional_stair_certification':'NOT_RUN',
      'structure_and_weatherproofing':'NOT_RUN','art':'ART HOLD'}

def mutations(states,manifest):
    result=assess(states,manifest)
    cases=['forged_adoption','maker_residue','missing_floor','offset_upper_gallery',
      'offset_mid_landing','missing_roof','fake_G0','missing_stair_support']
    for case in cases:
        cloned={k:v.copy() for k,v in states.items()};doc=copy.deepcopy(manifest)
        if case=='forged_adoption':doc['protection']['adopted']=1
        elif case=='maker_residue':cloned['no_maker']['maker__work_island']=cloned['baseline']['maker__work_island']
        elif case=='missing_floor':del cloned['baseline']['shared__single_atrium_floor']
        elif case=='offset_upper_gallery':
            m=cloned['baseline']['shared__upper_gallery'].copy();m.apply_translation((0,0,-.4))
            cloned['baseline']['shared__upper_gallery']=m
        elif case=='offset_mid_landing':
            m=cloned['baseline']['shared__mid_landing'].copy();m.apply_translation((0,0,.3))
            cloned['baseline']['shared__mid_landing']=m
        elif case=='missing_roof':del cloned['baseline']['shared__roof_back']
        elif case=='fake_G0':doc['protection']['G0']='PASS'
        else:del cloned['baseline']['shared__stair_out_stringer_0']
        try:assess(cloned,doc)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('mutation not detected: '+case)
    return result,len(cases)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d37_build');d=Path(p.parse_args().out)
    m=json.loads((d/'manifest.json').read_text())
    states={key:load_scene(d/f'd37_{key}.glb') for key in ('baseline','no_maker','no_research')}
    data,n=mutations(states,m)
    out={'stage':'D37','scope':'INDEPENDENT_SAVED_GLBS','result':data,
         'mutation_controls_caught':n,'visual_review':'PRE_G0_ART_REJECT_BY_AUTHOR',
         'no_auto_beauty_score':True,'formal_G0_S1_G1_G2_G3':'NOT_RUN',
         'art':'ART HOLD','adopted':0,'construction':'FORBIDDEN'}
    (d/'independent_result.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D37 saved GLB: stair upper contacts verified; independent mutations:',n,
          'view blockers:',data['limited_activity_sightline_architectural_intersections'])
if __name__=='__main__':main()