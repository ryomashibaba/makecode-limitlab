"""D43 separate saved D42 GLB topology & representative 3D clearance witnesses.
No generator import. Limited AABB samples, NOT formal 3D body sweep or safe egress.
"""
import argparse,copy,json,math
from pathlib import Path
import numpy as np,trimesh

def load(path):
    scene=trimesh.load(path,force='scene',process=False)
    result={}
    for n in scene.graph.nodes_geometry:
        T,g=scene.graph[n];m=scene.geometry[g].copy();m.apply_transform(T);result[str(n)]=m
    return result

def overlap(a,b):
    x,y=a.bounds;b1,b2=b.bounds
    return all(min(y[i],b2[i])-max(x[i],b1[i])>.02 for i in (0,1)) and abs(y[2]-b2[2])<.015

def clear_prism_nodes(nodes,x,y,z1,z2,halfwidth=.48):
    lo=np.array([x-halfwidth,y-halfwidth,z1]);hi=np.array([x+halfwidth,y+halfwidth,z2]);hits=[]
    for n,m in nodes.items():
        if n.startswith('site__') or n.endswith('_floor') or 'upper_connector' in n or n in (
            'shared__upper_gallery','shared__stair_upper_landing','shared__upper_transition',
            'room__upper_real_floor','shared__hall_floor','shared__approach_floor','shared__civic_run'):
            continue
        a,b=m.bounds
        if np.all(np.minimum(hi,b)-np.maximum(lo,a)>1.e-3):hits.append(n)
    return hits

def check(cases,manifest):
    assert manifest['stage']=='D42' and manifest['protection']['adopted']==0
    assert manifest['protection']['G0']=='NOT_RUN' and manifest['protection']['construction']=='FORBIDDEN'
    baseline=cases['baseline'];no_m=cases['no_maker'];no_r=cases['no_research']
    segments=[('shared__stair_upper_landing','shared__upper_transition'),
      ('shared__upper_transition','shared__upper_gallery'),
      ('shared__upper_gallery','room__upper_real_floor'),
      ('shared__upper_gallery','maker__short_upper_connector'),
      ('maker__short_upper_connector','maker__public_viewing_floor'),
      ('shared__upper_gallery','research__short_upper_connector'),
      ('research__short_upper_connector','research__public_viewing_floor')]
    continuity={}
    for a,b in segments:
        assert a in baseline and b in baseline
        continuity[a+' -> '+b]=bool(overlap(baseline[a],baseline[b]))
    assert all(continuity.values()),continuity
    # case deletion must preserve shared landing and actual room but delete role-specific connector.
    assert 'maker__short_upper_connector' not in no_m and 'research__short_upper_connector' not in no_r
    assert all(n in no_m and n in no_r for n in ('room__upper_real_floor','shared__upper_gallery','shared__stair_upper_landing'))
    # AABBs, not triangles: detect apparent clearance clashes at selected gallery->room travel points.
    points=[[x,15.9,8.0,10.15] for x in np.arange(3.5,14.1,.5)]
    blockers={str(round(x,1)):clear_prism_nodes(baseline,x,y,z1,z2) for x,y,z1,z2 in points}
    # Any blocker is evidence to revise; this is intentionally honest, not automatic art pass.
    return {'stage':'D43','scope':'INDEPENDENT_SAVED_GLB_UPPER_PRELIMINARY_ACCESS',
      '7_floor_overlap_edges':continuity,'upper_room_entry_corridor_approx_sample_count':len(points),
      'upper_room_entry_corridor_aabb_blockers':{k:v for k,v in blockers.items() if v},
      'body_sweep_certified':False,'structure_certified':False,'weatherproofing_certified':False,
      'no_adoption':True,'preliminary_art':'HOLD'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='d42_build');o=Path(p.parse_args().out)
    manifest=json.loads((o/'manifest.json').read_text(encoding='utf-8'))
    cases={k:load(o/f'd42_{k}.glb') for k in ('baseline','no_maker','no_research')}
    r=check(cases,manifest)
    negatives=['fake_adoption','missing_maker_connector','missing_research_connector','gallery_shift',
      'living_room_shift','stair_landing_shift','false_qa']
    for test in negatives:
        c={k:v.copy() for k,v in cases.items()};m=copy.deepcopy(manifest)
        if test=='fake_adoption':m['protection']['adopted']=1
        elif test=='missing_maker_connector':del c['baseline']['maker__short_upper_connector']
        elif test=='missing_research_connector':del c['baseline']['research__short_upper_connector']
        elif test=='gallery_shift':
            mesh=c['baseline']['shared__upper_gallery'].copy();mesh.apply_translation((0,60,0));c['baseline']['shared__upper_gallery']=mesh
        elif test=='living_room_shift':
            mesh=c['baseline']['room__upper_real_floor'].copy();mesh.apply_translation((50,0,0));c['baseline']['room__upper_real_floor']=mesh
        elif test=='stair_landing_shift':
            mesh=c['baseline']['shared__stair_upper_landing'].copy();mesh.apply_translation((0,0,.7));c['baseline']['shared__stair_upper_landing']=mesh
        elif test=='false_qa':m['protection']['G0']='PASS'
        try:check(c,m)
        except (AssertionError,KeyError):pass
        else:raise AssertionError('undetected '+test)
    r['negative_controls_detected']=negatives
    (o/'d43_upper_access_result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('D43 upper same-height overlap checks',len(r['7_floor_overlap_edges']),'and negative controls',len(negatives),'PASS; corridor AABB blockers:',r['upper_room_entry_corridor_aabb_blockers'])
if __name__=='__main__':main()
